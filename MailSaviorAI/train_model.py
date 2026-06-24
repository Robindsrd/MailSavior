"""Entraîne le modèle de détection de phishing de MailSavior.

Pipeline scikit-learn : TfidfVectorizer + LogisticRegression.
- Lit emails_dataset.csv (colonnes text,label)
- Split train/test stratifié
- Entraîne, évalue (classification_report), sauvegarde l'artefact avec joblib

Usage :
    python train_model.py
Produit :
    model/phishing_model.pkl   (artefact versionné chargé par l'API)
    model/classification_report.txt
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "emails_dataset.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "phishing_model.pkl"
REPORT_PATH = MODEL_DIR / "classification_report.txt"

MODEL_VERSION = "1.0.0"
RANDOM_STATE = 42


def load_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"{DATASET_PATH} introuvable. Lancez d'abord : python make_dataset.py"
        )
    df = pd.read_csv(DATASET_PATH)
    missing = {"text", "label"} - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes dans le dataset : {missing}")
    return df


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ]
    )


def main():
    df = load_dataset()
    print(f"Dataset : {len(df)} lignes")
    print("Répartition des labels :")
    print(df["label"].value_counts().to_string())

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"],
        test_size=0.25, random_state=RANDOM_STATE, stratify=df["label"],
    )
    print(f"\nTrain={len(X_train)} | Test={len(X_test)}")

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred, digits=3)
    print("\n=== classification_report (jeu de test) ===")
    print(report)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    # On sauvegarde un dict pour transporter la version avec l'artefact.
    joblib.dump({"pipeline": pipeline, "model_version": MODEL_VERSION}, MODEL_PATH)
    REPORT_PATH.write_text(
        f"Modèle MailSavior v{MODEL_VERSION}\n"
        f"Algorithme : TfidfVectorizer + LogisticRegression\n"
        f"Dataset : {len(df)} lignes (train={len(X_train)}, test={len(X_test)})\n\n"
        f"{report}\n",
        encoding="utf-8",
    )
    print(f"\nArtefact sauvegardé : {MODEL_PATH}")
    print(f"Rapport sauvegardé : {REPORT_PATH}")


if __name__ == "__main__":
    main()
