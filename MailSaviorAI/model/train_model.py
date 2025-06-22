import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# Crée le dossier s'il n'existe pas
os.makedirs("model", exist_ok=True)

# Chargement du dataset
df = pd.read_csv("emails_dataset.csv")

# Séparation des données
X_train, X_test, y_train, y_test = train_test_split(df['email'], df['label'], test_size=0.2, random_state=42)

# Pipeline avec vectorizer et modèle
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(max_iter=1000))
])

# Entraînement
model.fit(X_train, y_train)

# Évaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Sauvegarde du modèle complet (vectorizer + modèle)
joblib.dump(model, "model/phishing_model.pkl")

# Plus besoin de sauvegarder le vectorizer seul, car il est déjà dans le pipeline
