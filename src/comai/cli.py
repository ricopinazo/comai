import os
import typer
from termcolor import colored
import getch
from typing import List, Tuple, Optional
from typing_extensions import Annotated
from time import sleep
from threading import Thread, Lock

from . import config, translation, __version__

LEFT = '\033[D'

num_dots = 0
initial_prompt = '🧠≫ '
answer_prompt = '💡≫ '


app = typer.Typer()

def print_wait_dots(print_mutex):
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
    print_mutex = Lock()
    t = Thread(target = print_wait_dots, args=(print_mutex,))
    t.daemon = True
    t.start()
    return print_mutex

def print_answer(command: str, print_mutex):
    print_mutex.acquire()
    characters_to_remove = len(initial_prompt) + num_dots
    print(LEFT * characters_to_remove, end='') 
    print(LEFT, end='') 
    print(' ' * characters_to_remove, end='')
    print(LEFT * characters_to_remove, end='')

    print(colored(answer_prompt, 'green'), end='', flush=True)
    print_words_sequentially(command)

def version_callback(value: bool):
    if value:
        print(f"comai version: {__version__}")
        raise typer.Exit()

@app.command()
def main(
    instructions: List[str],
    version: Annotated[Optional[bool], typer.Option("--version", callback=version_callback)] = None
):
    input_text = ' '.join(instructions[1:])

    api_key = config.load_api_key()
    if not api_key:
        api_key = typer.prompt("Input OpenAI API key")
        assert len(api_key) > 0
        config.save_api_key(api_key)

    print_mutex = start_wait_prompt()
    command = translation.translate_to_command(input_text, api_key)
    print_answer(command, print_mutex)

    char = getch.getch()
    print()
    if char == "\n":
        os.system(command)
