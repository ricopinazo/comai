import pytest
import sys
import os
import keyring
from dotenv import load_dotenv
from comai_ricopinazo import cli

def test_installation_flow(monkeypatch):
    load_dotenv()
    try:
        keyring.delete_password("comai", "openai_api_key")
    except Exception:
        pass
    monkeypatch.setattr(cli.getch, 'getch', lambda: '\n')

    monkeypatch.setattr('builtins.input', lambda _: os.getenv('OPENAI_API_KEY') )
    sys.argv = ['comai', 'show', 'files']
    cli.main()
    monkeypatch.setattr('builtins.input', lambda _: None)
    cli.main()
