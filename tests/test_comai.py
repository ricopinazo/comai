import prompt_toolkit
from typing import Any
from typer.testing import CliRunner

from langchain_core.messages import AIMessageChunk
from langchain_community.chat_models import ChatOllama

from comai import cli, __version__

runner = CliRunner()


def test_normal_flow(monkeypatch):
    def mock_stream(*args, **kwargs):
        for token in ["COMMAND", " ls", " END"]:
            yield AIMessageChunk(content=token)

    def mock_prompt(message: str, default: str, style: Any = None):
        return default

    monkeypatch.setattr(ChatOllama, "stream", mock_stream)
    monkeypatch.setattr(prompt_toolkit, "prompt", mock_prompt)

    result = runner.invoke(cli.app, ["show", "files"])
    assert result.exit_code == 0
    assert "ls" in result.stdout


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"comai version: {__version__}" in result.stdout


def test_missing_instruction():
    result = runner.invoke(cli.app, [])
    assert result.exit_code != 0
