import os
import typer
import itertools
import getch
from typing import List, Optional, Iterator
from typing_extensions import Annotated

from . import config, context, translation, __version__
from .interactions import Command, Query
from .animations import query_animation, print_answer, show_cursor, hide_cursor

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
        api_key = typer.prompt("Input OpenAI API key")
        assert len(api_key) > 0
        if not translation.validate_api_key(api_key):
            print("API key not valid")
            typer.Exit(1)
        config.save_api_key(api_key)

    command_chunks = None
    command = []
    with query_animation():
        prev_interactions = config.get_prev_interactions()
        ctx = context.get_context()
        command_chunks = translation.translate_to_command(
            input_text, api_key, prev_interactions, ctx
        )
        command_chunks = save_command(command_chunks, command)
        command_chunks = wait_for_first_chunk(command_chunks)

    print_answer(command_chunks)
    command = "".join(command)

    config.save_interaction(Query(input_text))
    config.save_interaction(Command(command))

    char = getch.getch()
    print()
    if char == "\n":
        os.system(command)


@app.command()
def main(
    instructions: List[str],
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
):
    hide_cursor()
    try:
        main_normal_flow(instructions)
    except Exception as e:
        raise e
    finally:
        show_cursor()
