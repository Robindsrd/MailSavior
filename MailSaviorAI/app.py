#importation des bibliothèques nécessaires
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib

#api MailSaviorAI
app = FastAPI()

#chargement du modèle
model = joblib.load("model/phishing_model.pkl")

class EmailRequest(BaseModel): #Modèle pour la requête d'analyse d'email
    text: str

#endpoit pour analyser les emails
@app.post("/analyze")
def analyze_email(req: EmailRequest):
    proba = model.predict_proba([req.text])[0][1]
    is_phishing = int(proba >= 0.5)
    return {
        "prediction": is_phishing,
        "probability": round(proba * 100, 2)
    }

class Feedback(BaseModel): #Modele pour le feedback
    text: str
    score: float
    feedback: str

#stockage pour le feedback
feedback_storage: List[Feedback] = []

#endpoint pour recevoir le feedback
@app.post("/feedback")
def receive_feedback(fb: Feedback):
    feedback_storage.append(fb)
    return {"status": "success"}

#endpoint pour récupérer tous les feedbacks
@app.get("/feedbacks")
def get_all_feedbacks():
    return feedback_storage