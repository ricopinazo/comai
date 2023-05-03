import pytest
import sys
import os
from dotenv import load_dotenv
from comai_ricopinazo import cli, config

def test_installation_flow(monkeypatch):
    load_dotenv()
    config.delete_api_key()
   
    monkeypatch.setattr(cli.getch, 'getch', lambda: '\n')

    monkeypatch.setattr('builtins.input', lambda _: os.getenv('OPENAI_API_KEY') )
    sys.argv = ['comai', 'show', 'files']
    cli.main()
    monkeypatch.setattr('builtins.input', lambda _: None)
    cli.main()
