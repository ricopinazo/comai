import os
import typer
import itertools
from typing import List, Optional, Iterator
from typing_extensions import Annotated

from comai import __version__
from comai.chain import StreamStart, Token, FinalCommand, query_command
from comai.settings import load_settings
from comai.context import get_context
from comai.menu import get_option_from_menu, MenuOption
from comai.animations import (
    print_command_token,
    query_animation,
    show_cursor,
    hide_cursor,
    start_printing_command,
)

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"comai version: {__version__}")
        raise typer.Exit()


def main_normal_flow(instructions: List[str]):
    final_command: str | None = None
    input_text = " ".join(instructions)

    hide_cursor()

    settings = load_settings()
    context = get_context()
    output = query_command(input_text, settings, context)
    with query_animation():
        stream_start = next(output)
        assert type(stream_start) == StreamStart

    start_printing_command()
    for chunk in output:
        match chunk:
            case Token(token):
                print_command_token(token)
            case FinalCommand(command):
                final_command = command

    if final_command is None:
        raise Exception("failed to fetch command")

    match get_option_from_menu():
        case MenuOption.run:
            os.system(final_command)
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
