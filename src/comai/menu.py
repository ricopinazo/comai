import click
import typer
from enum import Enum
from termcolor import colored
from .animations import show_cursor


class MenuOption(str, Enum):
    run = "r"
    cancel = "c"


def get_option_from_menu() -> MenuOption:
    color = "dark_grey"
    click_choice = click.Choice(MenuOption)
    execute = colored("r", color, attrs=["underline", "bold"])
    cancel = colored("c", color, attrs=["underline", "bold"])
    prompt = (
        colored(" ➜ ", color)
        + execute
        + colored("un | ", color)
        + cancel
        + colored("ancel [r]:", color)
    )
    show_cursor()
    option = typer.prompt(
        prompt,
        prompt_suffix="",
        default=MenuOption.run,
        type=click_choice,
        show_choices=False,
        show_default=False,
    )
    return option
