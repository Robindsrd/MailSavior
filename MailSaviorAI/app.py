from fastapi import FastAPI
from pydantic import BaseModel
import os
from typing import List
import joblib

app = FastAPI()

# Chargement du modèle
model = joblib.load("model/phishing_model.pkl")

# Classe pour le corps de la requête
class EmailRequest(BaseModel):
    text: str

# Endpoint principal
@app.post("/analyze")
def analyze_email(req: EmailRequest):
    proba = model.predict_proba([req.text])[0][1]
    is_phishing = int(proba >= 0.5)
    return {
        "prediction": is_phishing,
        "probability": round(proba * 100, 2)
    }

class Feedback(BaseModel):
    text: str
    score: float
    feedback: str  # "phishing" ou "safe"

# Liste en mémoire des feedbacks (tu peux remplacer ça par un fichier ou une DB plus tard)
feedback_storage: List[Feedback] = []

# Endpoint POST pour recevoir un feedback
@app.post("/feedback")
def receive_feedback(fb: Feedback):
    feedback_storage.append(fb)
    return {"status": "success"}

# Endpoint GET pour les consulter (utile pour l'affichage dans l'app C#)
@app.get("/feedbacks")
def get_all_feedbacks():
    return feedback_storage