import openai
from typing import Iterator, List
from . import context
from .interactions import Interaction, Query, Command

def adapt_interaction(interaction: Interaction):
    match interaction:
        case Query(content):
            return {'role': 'user', 'content': content}
        case Command(content):
            return {'role': 'assistant', 'content': content}

def translate_to_command(nl_description: str, openai_api_key: str, prev_interactions: List[Interaction], context: context.Context) -> Iterator[str]: 
    openai.api_key = openai_api_key
    system = f'You are a bot translating natural language instructions into commands for {context.shell} in {context.system}. Your output is just an executable command, with no explanation'
    system_message = {'role': 'system', 'content': system}
    new_user_message = {'role': 'user', 'content': nl_description}
    # TODO: maybe nl_description might come embedded in prev_messages
    prev_messages = [adapt_interaction(interaction) for interaction in prev_interactions]
    messages = [system_message, *prev_messages, new_user_message]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.2,
        stream=True,
        messages=messages
    )

    for chunk in response:
        if 'content' in chunk.choices[0].delta:
            yield chunk.choices[0].delta.content

    # TODO: set the new state for messages record here

def validate_api_key(openai_api_key) -> bool:
    try:
        openai.Model.list(api_key=openai_api_key)
        return True
    except Exception:
        return False
