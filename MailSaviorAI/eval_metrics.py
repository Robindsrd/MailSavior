"""Recalcule les métriques RÉELLES du modèle sur le jeu de test (preuve jury).

Reproduit exactement le split de train_model.py (random_state=42) et évalue
l'artefact sauvegardé : accuracy, precision, recall, F1, matrice de confusion.

Usage : python eval_metrics.py
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).parent
df = pd.read_csv(BASE_DIR / "emails_dataset.csv")
artifact = joblib.load(BASE_DIR / "model" / "phishing_model.pkl")
pipeline = artifact["pipeline"]

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
)
y_pred = pipeline.predict(X_test)

print(f"Modèle version : {artifact['model_version']}")
print(f"Dataset total : {len(df)} | train : {len(X_train)} | test : {len(X_test)}")
print(f"Classes : {list(pipeline.classes_)}")
print()
print(f"Accuracy  : {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision (phishing) : {precision_score(y_test, y_pred, pos_label='phishing'):.3f}")
print(f"Recall    (phishing) : {recall_score(y_test, y_pred, pos_label='phishing'):.3f}")
print(f"F1-score  (phishing) : {f1_score(y_test, y_pred, pos_label='phishing'):.3f}")
print()
labels = list(pipeline.classes_)
cm = confusion_matrix(y_test, y_pred, labels=labels)
print("Matrice de confusion (lignes = réel, colonnes = prédit)")
print("            " + "  ".join(f"{l:>9}" for l in labels))
for i, l in enumerate(labels):
    print(f"{l:>10}  " + "  ".join(f"{v:>9}" for v in cm[i]))
print()
print("=== classification_report ===")
print(classification_report(y_test, y_pred, digits=3))
