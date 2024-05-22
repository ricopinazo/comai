import itertools
import logging
import re
import os
import textwrap
import uuid
from dataclasses import dataclass
from typing import Iterable, Iterator, List
from pydantic import BaseModel, SecretStr

from langchain.globals import set_debug, set_verbose
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableGenerator
from langchain_core.runnables.base import Runnable
from langchain_core.runnables.history import (
    MessagesOrDictWithMessages,
    RunnableWithMessageHistory,
)
from langchain_core.runnables.utils import ConfigurableFieldSpec
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from comai.context import Context
from comai.history import load_history
from comai.settings import Settings

logging.getLogger().setLevel(logging.CRITICAL)


def create_prompt(context: Context):
    system_message = f"""
    You are a CLI tool called comai  with access to a {context.shell} shell on {context.system}. Your goal is to translate the instruction from the user into a command.

    ALWAYS use the following format, with no additional comments, explanation, or notes before or after AT ALL:

    COMMAND <the command> END

    Example:

    User:
    show files

    Your answer:
    COMMAND ls END
    """

    return ChatPromptTemplate.from_messages(
        [
            ("system", textwrap.dedent(system_message).strip()),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )


def parse_command(tokens: Iterable[AIMessageChunk]) -> Iterator[str]:
    input = ""
    output: str = ""
    for token in tokens:
        if type(token.content) == str:
            input += token.content
            pattern = r"COMMAND(.*?)(END|$)"
            match = re.search(pattern, input)
            if match:
                updated_output = match.group(1).strip()
                if len(updated_output) > len(output):
                    yield updated_output[len(output) :]
                    output = updated_output


parse_command_generator = RunnableGenerator(parse_command)


def attatch_history(
    runnable: Runnable[
        MessagesOrDictWithMessages,
        str | BaseMessage | MessagesOrDictWithMessages,
    ]
):
    return RunnableWithMessageHistory(
        runnable,
        lambda session_id: load_history(session_id),
        input_messages_key="question",
        history_messages_key="history",
    )


class OpenaiSecrets(BaseModel):
    default_key: SecretStr | None
    comai_key: SecretStr | None


def extract_secret(key: str | None):
    if key is None:
        return None
    else:
        return SecretStr(key)


def create_chain_stream(settings: Settings, context: Context):
    prompt = create_prompt(context)
    if settings.provider == "ollama":
        model = ChatOllama(model=settings.model, temperature=0)
    elif settings.provider == "openai":
        default_key = extract_secret(os.environ.get("OPENAI_API_KEY"))
        comai_key = extract_secret(os.environ.get("COMAI_OPENAI_API_KEY"))
        api_key = comai_key if comai_key is not None else default_key
        model = ChatOpenAI(model=settings.model, temperature=0, api_key=api_key)  # type: ignore
    base_chain = prompt | model

    if context.session_id is not None:
        session_id = context.session_id
    else:
        session_id = str(uuid.uuid4())  # FIXME: should just not use history at all

    chain_with_history = attatch_history(base_chain)
    runnable = chain_with_history | parse_command_generator

    def stream(input: dict[str, str]):
        return runnable.stream(
            input=input, config={"configurable": {"session_id": session_id}}
        )

    return stream


# TODO: move this to different file
@dataclass
class StreamStart:
    pass


@dataclass
class Token:
    content: str


@dataclass
class FinalCommand:
    command: str


def query_command(
    query: str, settings: Settings, context: Context
) -> Iterator[StreamStart | Token | FinalCommand]:
    stream = create_chain_stream(settings, context)
    output = stream({"question": query})

    started = False
    buffer = ""
    for token in output:
        if not started:
            started = True
            yield StreamStart()
        yield Token(token)
        buffer += token
    yield FinalCommand(buffer)
