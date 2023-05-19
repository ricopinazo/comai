import openai

def translate_to_command(nl_description, openai_api_key): 
    openai.api_key = openai_api_key
    prompt = (f"Convert the following natural language instruction to a Unix command:\n"
                f"{nl_description}\n"
                f"UNIX command:")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.2,
    )
    return response.choices[0].text.strip()