import os
import sys
import typer
import click
import itertools
from typing import List, Optional, Iterator, Literal
from typing_extensions import Annotated
from langchain_community.llms.ollama import OllamaEndpointNotFoundError
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError

from comai import __version__
from comai.chain import StreamStart, Token, FinalCommand, query_command
from comai.ollama import get_ollama_model_names
from comai.openai import get_openai_model_names
from comai.prompt import prompt_bool, prompt_options
from comai.settings import (
    InvalidSettingsFileException,
    load_settings,
    write_settings,
    Settings,
)
from comai.context import get_context
from comai.animations import (
    print_command_token,
    query_animation,
    show_cursor,
    hide_cursor,
    start_printing_command,
    print_command_prompt,
)

# this is to avoid using rich for the help panel
typer.core.rich = None  # type: ignore

app = typer.Typer(pretty_exceptions_enable=False, add_completion=False)


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

        provider = prompt_options(
            "Which provider do you want to use?",
            ["ollama", "openai"],
            settings.provider,
        )
        if provider == "ollama":
            models = get_ollama_model_names()
        elif provider == "openai":
            models = get_openai_model_names()
        else:
            raise Exception(f"Got unknown provider option: {provider}")

        if settings.model in models:
            default_model = settings.model
        elif "llama3" in models:
            default_model = "llama3"
        elif "gpt-3.5-turbo" in models:
            default_model = "gpt-3.5-turbo"
        elif len(models) > 0:
            default_model = models[0]
        else:
            raise Exception("No models available for the selected provider")
        model = prompt_options("Which model do you want to use?", models, default_model)
        updated_settings = Settings.parse_obj({"provider": provider, "model": model})
        write_settings(updated_settings)
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

    user_command = print_command_prompt(final_command)
    os.system(user_command)


@app.command(help="Translates natural language instructions into commands")
def main(
    instructions: List[str],
    config: Annotated[
        Optional[bool],
        typer.Option(
            "--config",
            callback=settings_callback,
            help="Starts an interactive menu to select your configuration",  # assisted isntead?
        ),
    ] = None,
    show_config: Annotated[
        Optional[bool],
        typer.Option(
            "--show-config",
            callback=show_settings_callback,
            help="Show the current configuration",
        ),
    ] = None,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", callback=version_callback, help="Show the current version"
        ),
    ] = None,
):

    try:
        settings = load_settings()
    except InvalidSettingsFileException as e:
        message = f"Your settings file at {e.settings_path} is incorrect. Please fix it or start from scratch with comai --config"
        sys.stderr.write(message + "\n")
        exit(1)
    except Exception as e:
        raise e

    try:
        main_normal_flow(instructions, settings)
    except OllamaEndpointNotFoundError:
        message = f"Model '{settings.model}' not found in the ollama service. Please download it with 'ollama pull {settings.model}' or select a different model with 'comai --config'"
        sys.stderr.write(message + "\n")
        typer.Exit(2)
    except ConnectionError as e:
        if settings.provider == "ollama":
            message = f"Ollama service is not running. Please install it and run it (https://ollama.com/download) or select a different provider with 'comai --config'"
            sys.stderr.write(message + "\n")
            typer.Exit(3)
        else:
            raise e
    except Exception as e:
        raise e
    finally:
        show_cursor()
