import os
import typer
import itertools
from typing import List, Optional, Iterator
from typing_extensions import Annotated

from . import config, context, translation, __version__
from .menu import get_option_from_menu, MenuOption
from .animations import (
    query_animation,
    print_answer,
    show_cursor,
    hide_cursor,
)

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"comai version: {__version__}")
        raise typer.Exit()


def save_command(command_chunks, command: list):
    for chunk in command_chunks:
        command.append(chunk)
        yield chunk


def wait_for_first_chunk(iterator: Iterator[str]):
    iter1, iter2 = itertools.tee(iterator)
    _ = next(iter1)
    return iter2


def main_normal_flow(instructions: List[str]):
    input_text = " ".join(instructions)

    api_key = config.load_api_key()
    if not api_key:
        api_key = typer.prompt("Please enter your OpenAI API key")
        assert len(api_key) > 0
        if not translation.validate_api_key(api_key):
            print("API key not valid")
            exit(1)
        config.save_api_key(api_key)

    hide_cursor()

    command_chunks = None
    command = []
    with query_animation():
        ctx = context.get_context()
        history_path = config.get_history_path()
        command_chunks = translation.translate_with_history(
            input_text, history_path, ctx, api_key
        )
        command_chunks = save_command(command_chunks, command)
        command_chunks = wait_for_first_chunk(command_chunks)

    print_answer(command_chunks)
    command = "".join(command)

    match get_option_from_menu():
        case MenuOption.run:
            os.system(command)
        case MenuOption.cancel:
            pass


@app.command()
def main(
    instructions: List[str],
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
):
    try:
        main_normal_flow(instructions)
    except Exception as e:
        raise e
    finally:
        show_cursor()
