"""Tests du modèle et du dataset (C12)."""
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "phishing_model.pkl"
DATASET_PATH = BASE_DIR / "emails_dataset.csv"

VALID_LABELS = {"phishing", "safe"}


def test_artefact_exists_and_loads():
    assert MODEL_PATH.exists(), "L'artefact modèle doit exister (lancez train_model.py)."
    artifact = joblib.load(MODEL_PATH)
    assert "pipeline" in artifact and "model_version" in artifact
    assert hasattr(artifact["pipeline"], "predict_proba")


def test_dataset_readable_and_valid():
    df = pd.read_csv(DATASET_PATH)
    assert {"text", "label"}.issubset(df.columns)
    assert len(df) > 0
    assert set(df["label"].unique()).issubset(VALID_LABELS)


def test_prediction_returns_valid_label_and_score():
    pipeline = joblib.load(MODEL_PATH)["pipeline"]
    proba = pipeline.predict_proba(["Cliquez ici pour vérifier votre compte suspendu"])[0]
    assert all(0.0 <= p <= 1.0 for p in proba)
    pred = pipeline.predict(["Bonjour, la réunion est confirmée à 10h"])[0]
    assert pred in VALID_LABELS
