import pytest
import sys
import os
from typer.testing import CliRunner
from dotenv import load_dotenv
from comai import cli, config, translation, context, __version__

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

runner = CliRunner()


def test_invalid_api_key(monkeypatch):
    config.delete_api_key()

    monkeypatch.setattr(cli.getch, "getch", lambda: "\n")
    monkeypatch.setattr(cli.typer, "prompt", lambda _: "bad-api-key")

    result = runner.invoke(cli.app, ["show", "files"])
    assert result.exit_code != 0
    assert "API key not valid" in result.stdout


def test_installation_flow(monkeypatch):
    config.delete_api_key()

    monkeypatch.setattr(cli.getch, "getch", lambda: "\n")
    monkeypatch.setattr(cli.typer, "prompt", lambda _: api_key)

    result = runner.invoke(cli.app, ["show", "files"])
    assert result.exit_code == 0
    # assert "Input OpenAI API key: " not in result.stdout # FIXME: this should work
    assert "ls" in result.stdout

    result = runner.invoke(cli.app, ["show", "files"])
    assert result.exit_code == 0
    assert "Input OpenAI API key: " not in result.stdout
    assert "ls" in result.stdout


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert "comai version: {__version__}" not in result.stdout


def test_missing_instruction():
    result = runner.invoke(cli.app, [])
    assert result.exit_code != 0


def test_translation():
    ctx = context.get_context()
    command = translation.translate_to_command("show files", api_key, [], ctx)
    assert "".join(command) == "ls"
