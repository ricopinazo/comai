import os
from typing import Literal
import typer
from pydantic import BaseModel

APP_NAME = "comai"
config_dir = typer.get_app_dir(APP_NAME, force_posix=True)
settings_path = os.path.join(config_dir, "settings.json")


class Settings(BaseModel):
    provider: Literal["ollama", "openai"]
    model: str = (
        "llama3"  # TODO: improve this, should be typed per provider, although possible models can be queried at runtime
    )


DEFAULT_SETTINGS: Settings = Settings(provider="ollama", model="llama3")


def load_settings() -> Settings:
    try:
        return Settings.parse_file(settings_path)
    except:
        # TODO: if there is indeed a file but the file is incorrect, we should complain instead of returning the default
        return DEFAULT_SETTINGS
