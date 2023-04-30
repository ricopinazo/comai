import pytest
import sys
import os
from dotenv import load_dotenv
from comai_ricopinazo import cli

class RawKeyring(cli.keyring.backend.KeyringBackend):
    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def get_password(self, servicename, username):
        return None

    def delete_password(self, servicename, username):
        pass

class CookedKeyring(cli.keyring.backend.KeyringBackend):
    priority = 1

    def set_password(self, servicename, username, password):
        pass

    def get_password(self, servicename, username):
        return os.getenv('OPENAI_API_KEY')

    def delete_password(self, servicename, username):
        pass

def test_cli_init(monkeypatch):
    load_dotenv()
    cli.keyring.set_keyring(RawKeyring())
    monkeypatch.setattr('builtins.input', lambda _: os.getenv('OPENAI_API_KEY'))
    monkeypatch.setattr(cli.getch, 'getch', lambda: '\n')
    sys.argv = ['comai', 'show', 'files']
    cli.main()

def test_cli_normal_operation(monkeypatch):
    load_dotenv()
    cli.keyring.set_keyring(CookedKeyring())
    monkeypatch.setattr(cli.getch, 'getch', lambda: '\n')
    sys.argv = ['comai', 'show', 'files']
    cli.main()
