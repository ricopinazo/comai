#!/Users/pedrorico/.pyenv/versions/comai/bin/python

import openai
import os
import sys
from termcolor import colored
# from dotenv import load_dotenv
import getch
from time import sleep
from threading import Thread, Lock
import keyring

LEFT = '\033[D'

print_mutex = Lock()
num_dots = 0
initial_prompt = '🧠≫ '
answer_prompt = '💡≫ '

def load_openai_api_key():
    api_key = keyring.get_password("comai", "openai_api_key")
    if api_key is None:
        api_key = input("Input OpenAI API key: ")
        keyring.set_password("comai", "openai_api_key", api_key)
    return api_key

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

def print_wait_dots():
    global num_dots
    while(True):
        print_mutex.acquire()
        try:
            if num_dots >= 3:
                print(LEFT * 3 + '   ' + LEFT * 3, end='', flush=True)
                num_dots = 0
            else:
                print('.', end='', flush=True) 
                num_dots += 1
        finally:
            print_mutex.release()
        sleep(0.2)

def print_words_sequentially(text):
    words = text.split(' ')
    for word in words:
        sleep(0.1)
        print(word + ' ', end='', flush=True)


def start_wait_prompt():
    print(colored(initial_prompt, 'cyan'), end='')
    t = Thread(target = print_wait_dots)
    t.daemon = True
    t.start()

def print_answer(command: str):
    print_mutex.acquire()
    characters_to_remove = len(initial_prompt) + num_dots
    print(LEFT * characters_to_remove, end='') 
    print(LEFT, end='') 
    print(' ' * characters_to_remove, end='')
    print(LEFT * characters_to_remove, end='')

    print(colored(answer_prompt, 'green'), end='', flush=True)
    print_words_sequentially(command)

def main():
    assert len(sys.argv) > 1
    input_text = ' '.join(sys.argv[1:])

    api_key = load_openai_api_key()
    start_wait_prompt()
    command = translate_to_command(input_text, api_key)
    print_answer(command)

    char = getch.getch()
    print()
    if char == "\n":
        os.system(command)
