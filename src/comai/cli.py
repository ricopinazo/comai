import os
import sys
import typer
import click
import itertools
from typing import List, Optional, Iterator
from typing_extensions import Annotated
from langchain_community.llms.ollama import OllamaEndpointNotFoundError

from comai import __version__
from comai.chain import StreamStart, Token, FinalCommand, query_command
from comai.ollama import get_ollama_model_names
from comai.settings import load_settings, write_settings, Settings
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


def show_settings_callback(value: bool):
    if value:
        settings = load_settings()
        print("Current settings:")
        print(settings.model_dump_json(indent=2))
        raise typer.Exit()


def settings_callback(value: bool):
    if value:
        settings = load_settings()
        ollama_models = get_ollama_model_names()
        if settings.model in ollama_models:
            default_model = settings.model
        elif "llama3" in ollama_models:
            default_model = "llama3"
        elif len(ollama_models) > 0:
            default_model = ollama_models[0]
        else:
            default_model = "llama3"
        model = click.prompt(
            "Ollama model",
            type=click.Choice(ollama_models),
            default=default_model,
            show_default=True,
            show_choices=True,
        )
        verbose = click.prompt(
            "Verbose mode",
            type=click.BOOL,
            default="yes" if settings.verbose else "no",
            show_default=True,
            show_choices=True,
        )
        settings.provider = "ollama"
        settings.model = model
        settings.verbose = verbose
        write_settings(settings)
        raise typer.Exit()


def main_normal_flow(instructions: List[str], settings: Settings):
    final_command: str | None = None
    input_text = " ".join(instructions)

    hide_cursor()

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

    match get_option_from_menu(settings):
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
    config: Annotated[
        Optional[bool], typer.Option("--config", callback=settings_callback)
    ] = None,
    show_config: Annotated[
        Optional[bool], typer.Option("--show-config", callback=show_settings_callback)
    ] = None,
):
    settings = load_settings()

    try:
        main_normal_flow(instructions, settings)
    except OllamaEndpointNotFoundError as e:
        sys.stderr.write(
            f"Model '{settings.model}' not found in the ollama service. Please download it with 'ollama pull {settings.model}' or select a different model with 'comai --config'"
        )
        typer.Exit(1)
    except Exception as e:
        raise e
    finally:
        show_cursor()
