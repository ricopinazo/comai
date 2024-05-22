import sys
from threading import Event, Thread
from contextlib import contextmanager
from typing import Generator, Iterator
from rich import print
import prompt_toolkit
from prompt_toolkit.styles import Style

from comai.prompt import prompt_str

LEFT = "\033[D"
CLEAR_LINE = "\033[K"
INITIAL_PROMPT = "🧠≫ "
LOADED_PROMPT = "✔"
ANSWER_PROMPT = "❯ "
ANSWER_PROMPT_COLOR = "magenta"
CONTACT_PROMPT = "fetching command"
FRAME_PERIOD = 0.1
LOADING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
COMMAND_COLOR = "cyan"

stdout_is_tty = sys.stdout.isatty()


def print_query_animation(finish: Event):
    next_frame = 0
    while not finish.wait(0):
        sys.stdout.write(f"\r{CLEAR_LINE}")
        frame = f"[cyan]{LOADING_FRAMES[next_frame]}[/cyan] {CONTACT_PROMPT}"
        print(frame, end="", flush=True)
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


def start_printing_command():
    print(f"[{ANSWER_PROMPT_COLOR}]{ANSWER_PROMPT}", end="", flush=True)


def print_command_token(chunk: str):
    print(f"[{COMMAND_COLOR}]{chunk}", end="", flush=True)


def print_command_prompt(command: str):
    sys.stdout.write(f"\r{CLEAR_LINE}")
    style = Style.from_dict(
        {
            # User input (default text)
            "": "ansicyan",
            "mark": "ansimagenta",
        }
    )
    message = [
        ("class:mark", ANSWER_PROMPT),
    ]
    return prompt_toolkit.prompt(message, default="%s" % command, style=style)  # type: ignore


def hide_cursor() -> None:
    if stdout_is_tty:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


def show_cursor() -> None:
    if stdout_is_tty:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
