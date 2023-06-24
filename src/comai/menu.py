import click
from enum import Enum
from .animations import show_cursor
from rich import print
from rich.markup import escape


class MenuOption(str, Enum):
    run = "r"
    cancel = "c"


DEFAULT_OPTION = escape("[r]")
MENU_PROMPT = f"[bright_black] ➜ [underline bold]r[/underline bold]un | [underline bold]c[/underline bold]ancel {DEFAULT_OPTION}:[/bright_black]"


def get_option_from_menu() -> MenuOption:
    print(MENU_PROMPT, end="", flush=True)
    show_cursor()
    option = click.prompt(
        "",
        prompt_suffix="",
        type=MenuOption,
        default=MenuOption.run,
        show_default=False,
        show_choices=False,
    )
    return option
