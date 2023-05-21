import openai

def translate_to_command(nl_description, openai_api_key): 
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.2,
        stream=True,
        messages=[
            {'role': 'system', 'content': 'You are a bot translating natural language instructions into UNIX commands. Your output is just an executable command'},
            {'role': 'user', 'content': 'generate random UUID'},
            {'role': 'assistant', 'content': 'uuidgen'},
            {'role': 'user', 'content': nl_description},
        ]
    )

    for chunk in response:
        if 'content' in chunk.choices[0].delta:
            yield chunk.choices[0].delta.content
