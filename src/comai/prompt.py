from typing import Literal
from simple_term_menu import TerminalMenu
from rich import print
import prompt_toolkit
from prompt_toolkit.styles import Style


def prompt_str(question: str, default: str) -> str:
    style = Style.from_dict(
        {
            # User input (default text)
            "": "ansicyan",
            "mark": "ansicyan",
            "question": "ansiwhite",
        }
    )
    message = [
        ("class:mark", "? "),
        ("class:question", f"{question.strip()} "),
    ]
    return prompt_toolkit.prompt(message, default="%s" % default, style=style)  # type: ignore


def prompt_options(question: str, options: list[str], default: str) -> str:
    terminal_menu = TerminalMenu(
        options,
        title=f"? {question}",
        menu_cursor="• ",
        menu_cursor_style=("bg_black", "fg_green"),
        menu_highlight_style=("bg_black", "fg_green"),
    )
    index = terminal_menu.show()
    answer = options[index]
    print(f"[cyan]?[/cyan] {question} [cyan]{answer}[/cyan]")
    return answer


def prompt_bool(question: str, default: bool) -> bool:
    default_option = "Yes" if default == True else "No"
    answer = prompt_options(question, ["Yes", "No"], default_option)
    if answer == "Yes":
        return True
    elif answer == "No":
        return False
    else:
        raise Exception(f"unexpected input {answer}")
