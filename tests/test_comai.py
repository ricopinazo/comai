import os
from typer.testing import CliRunner
from dotenv import load_dotenv
from comai import cli, config, translation, context, __version__
from comai.history import History

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

runner = CliRunner()


def test_invalid_api_key():
    config.delete_api_key()

    result = runner.invoke(cli.app, ["show", "files"], input="bad-api-key\n")
    assert result.exit_code != 0
    assert "API key not valid" in result.stdout


def test_installation_flow():
    config.delete_api_key()

    result = runner.invoke(cli.app, ["show", "files"], input=f"{api_key}\n\n")
    assert result.exit_code == 0
    assert "Please enter your OpenAI API key:" in result.stdout
    assert "ls" in result.stdout

    result = runner.invoke(cli.app, ["show", "files"], input="\n")
    assert result.exit_code == 0
    assert "Please enter your OpenAI API key:" not in result.stdout
    assert "ls" in result.stdout


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"comai version: {__version__}" in result.stdout


def test_missing_instruction():
    result = runner.invoke(cli.app, [])
    assert result.exit_code != 0


def test_translation():
    ctx = context.get_context()
    history = History.create_local()
    history.append_user_message("show files")

    answer = translation.request_command(history, ctx, api_key)
    command = translation.filter_assistant_message(answer)
    assert "".join(command) == "ls"
