import pytest
import sys
import os
from dotenv import load_dotenv
from comai import cli, config

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def test_installation_flow(monkeypatch):
    config.delete_api_key()
   
    monkeypatch.setattr(cli.getch, 'getch', lambda: '\n')

    monkeypatch.setattr('builtins.input', lambda _: api_key )
    sys.argv = ['comai', 'show', 'files']
    cli.main()
    monkeypatch.setattr('builtins.input', lambda _: None)
    cli.main()

def test_translation():
    c1 = cli.translate_to_command("show files", api_key)
    assert c1 == 'ls'
