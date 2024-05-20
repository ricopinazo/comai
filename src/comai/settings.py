import os
import sys
from typing import Literal
import typer
from pydantic import BaseModel

APP_NAME = "comai"
config_dir = typer.get_app_dir(APP_NAME, force_posix=True)
settings_path = os.path.join(config_dir, "settings.json")


class Settings(BaseModel):
    provider: Literal["ollama", "openai"]
    model: str = "llama3"


DEFAULT_SETTINGS: Settings = Settings(provider="ollama")


class InvalidSettingsFileException(BaseException):
    def __init__(self, settings_path: str):
        self.settings_path = settings_path
        super().__init__()


def load_settings() -> Settings:
    try:
        with open(settings_path, "r") as file:
            content = file.read()
            return Settings.model_validate_json(content)
    except FileNotFoundError:
        return DEFAULT_SETTINGS
    except Exception:
        raise InvalidSettingsFileException(settings_path=settings_path)


def write_settings(settings: Settings):
    json = settings.model_dump_json(indent=2)
    with open(settings_path, "w") as file:
        file.write(json + "\n")
