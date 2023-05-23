import openai

def translate_to_command(nl_description, openai_api_key, prev_messages): 
    openai.api_key = openai_api_key
    system = 'You are a bot translating natural language instructions into UNIX commands. Your output is just an executable command'
    system_message = {'role': 'system', 'content': system}
    new_user_message = {'role': 'user', 'content': nl_description}
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
