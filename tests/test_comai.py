import pytest
import sys
from comai import cli


def test_comai(monkeypatch):
    monkeypatch.setattr(cli.getch, 'getch', lambda: '\n')
    sys.argv = ['comai', 'show', 'files']
    cli.main()
    