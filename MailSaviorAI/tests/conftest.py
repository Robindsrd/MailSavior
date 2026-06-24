import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Permet d'importer app.py depuis MailSaviorAI/
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import app as app_module  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Isolation : feedback et monitoring écrits dans un dossier temporaire.
    monkeypatch.setattr(app_module, "FEEDBACK_PATH", tmp_path / "feedback_log.json")
    monkeypatch.setattr(app_module, "MONITORING_PATH", tmp_path / "monitoring.csv")
    with TestClient(app_module.app) as c:  # déclenche le lifespan (chargement du modèle)
        yield c
