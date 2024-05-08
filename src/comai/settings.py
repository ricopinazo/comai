import os
from typing import Literal
import typer
from pydantic import BaseModel

APP_NAME = "comai"
config_dir = typer.get_app_dir(APP_NAME, force_posix=True)
settings_path = os.path.join(config_dir, "settings.json")


class Settings(BaseModel):
    provider: Literal["ollama", "openai"]
    # TODO: improve this, should be typed per provider, although possible models can be queried at runtime
    model: str = "llama3"
    verbose: bool = True


DEFAULT_SETTINGS: Settings = Settings(provider="ollama")


def load_settings() -> Settings:
    try:
        return Settings.parse_file(settings_path)
    except:
        # TODO: if there is indeed a file but the file is incorrect, we should complain instead of returning the default
        return DEFAULT_SETTINGS


def write_settings(settings: Settings):
    json = settings.model_dump_json(indent=2)
    with open(settings_path, "w") as file:
        file.write(json + "\n")
