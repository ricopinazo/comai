import sys
from threading import Event, Thread
from contextlib import contextmanager
from typing import Generator
from termcolor import colored

LEFT = "\033[D"
CLEAR_LINE = "\033[K"
INITIAL_PROMPT = "🧠≫ "
LOADED_PROMPT = "✔"
ANSWER_PROMPT = "❯ "
CONTACT_PROMPT = "fetching command"
FRAME_PERIOD = 0.1
LOADING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

stdout_is_tty = sys.stdout.isatty()


def print_query_animation(finish: Event):
    next_frame = 0
    while not finish.wait(0):
        sys.stdout.write(f"\r{CLEAR_LINE}")
        sys.stdout.write(colored(LOADING_FRAMES[next_frame], "cyan"))
        sys.stdout.write(f" {CONTACT_PROMPT}")
        sys.stdout.flush()
        next_frame = (next_frame + 1) % len(LOADING_FRAMES)
        if finish.wait(FRAME_PERIOD):
            break
    sys.stdout.write(f"\r{CLEAR_LINE}")


@contextmanager
def query_animation() -> Generator[None, None, None]:
    finish = Event()
    t = Thread(target=print_query_animation, args=(finish,))
    t.start()
    try:
        yield
    finally:
        finish.set()
        t.join()


def print_answer(command_chunks: str):
    print(colored(ANSWER_PROMPT, "magenta"), end="", flush=True)
    color = "cyan"
    first_chunk = next(command_chunks)
    print(colored(first_chunk, color), end="", flush=True)
    for chunk in command_chunks:
        print(colored(chunk, color), end="", flush=True)


def print_menu() -> None:
    print("[↩] execute [x↩] cancel")


def hide_cursor() -> None:
    if stdout_is_tty:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


def show_cursor() -> None:
    if stdout_is_tty:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
