import os
from typer.testing import CliRunner

from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_community.chat_models import ChatOllama

# from dotenv import load_dotenv
from comai import cli, context, __version__

# from comai.history import History

# load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

runner = CliRunner()


def test_normal_flow(monkeypatch):
    def mock_stream(*args, **kwargs):
        for token in ["COMMAND", " ls", " END"]:
            yield AIMessageChunk(content=token)

    monkeypatch.setattr(ChatOllama, "stream", mock_stream)

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
