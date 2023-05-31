import openai
from typing import Iterator, List
from . import context
from .interactions import Interaction, Query, Command


def adapt_interaction(interaction: Interaction):
    match interaction:
        case Query(content):
            return {"role": "user", "content": f"INSTRUCTION: {content}\n COMMAND:"}
        case Command(content):
            return {"role": "assistant", "content": content}


def translate_to_command(
    nl_description: str,
    openai_api_key: str,
    prev_interactions: List[Interaction],
    context: context.Context,
) -> Iterator[str]:
    openai.api_key = openai_api_key
    system = f"""You are a bot with access to a {context.shell} shell
        on {context.system} on the user computer.
        User describes actions, and your output is directly run on the shell,
        so you just return shell code, with no explanation"""
    system_message = {"role": "system", "content": system}
    new_user_message = adapt_interaction(Query(nl_description))
    prev_messages = [
        adapt_interaction(interaction) for interaction in prev_interactions
    ]
    messages = [system_message, *prev_messages, new_user_message]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.2,
        stream=True,
        messages=messages,
    )

    for chunk in response:
        if "content" in chunk.choices[0].delta:
            yield chunk.choices[0].delta.content

    # TODO: set the new state for messages record here


def validate_api_key(openai_api_key) -> bool:
    try:
        openai.Model.list(api_key=openai_api_key)
        return True
    except Exception:
        return False
