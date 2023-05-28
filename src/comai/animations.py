import sys
from threading import Event, Thread
from contextlib import contextmanager
from typing import Generator
from termcolor import colored

LEFT = '\033[D'
INITIAL_PROMPT = '🧠≫ '
ANSWER_PROMPT = '💡≫ '
FRAME_PERIOD = 0.2
stdout_is_tty = sys.stdout.isatty()


def print_query_animation(finish: Event):
    num_dots = 0
    while not finish.wait(0):
        if num_dots >= 3:
            print(LEFT * 3 + '   ' + LEFT * 3, end='', flush=True)
            num_dots = 0
        else:
            print('.', end='', flush=True) 
            num_dots += 1
        if finish.wait(FRAME_PERIOD):
                break
    characters_to_remove = len(INITIAL_PROMPT) + num_dots
    print(LEFT * characters_to_remove, end='') 
    print(LEFT, end='') 
    print(' ' * characters_to_remove, end='')
    print(LEFT * characters_to_remove, end='')
    
@contextmanager
def query_animation() -> Generator[None, None, None]:
    print(colored(INITIAL_PROMPT, 'cyan'), end='')
    finish = Event()
    t = Thread(target = print_query_animation, args=(finish,))
    t.start()
    try:
        yield
    finally:
        finish.set()
        t.join()

def print_answer(command_chunks: str):
    print(colored(ANSWER_PROMPT, 'green'), end='', flush=True)
    first_chunk = next(command_chunks)
    print(first_chunk, end='', flush=True)
    for chunk in command_chunks:
        print(chunk, end='', flush=True)



def hide_cursor() -> None:
    if stdout_is_tty:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor() -> None:
    if stdout_is_tty:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
