import importlib
import os
import sys


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)


def test_database_module_handles_missing_password(monkeypatch):
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.delenv("DB_PORT", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    monkeypatch.delenv("DB_USER", raising=False)

    sys.modules.pop("database", None)
    sys.modules.pop("config", None)

    module = importlib.import_module("database")

    assert module.engine is not None
    assert module.DATABASE_URL.startswith("sqlite")
