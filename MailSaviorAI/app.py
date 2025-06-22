from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib

app = FastAPI()

# Charger le modèle
model = joblib.load("model/phishing_model.pkl")

class EmailRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_email(req: EmailRequest):
    proba = model.predict_proba([req.text])[0][1]
    is_phishing = int(proba >= 0.5)
    return {
        "prediction": is_phishing,
        "probability": round(proba * 100, 2)
    }


# === Ancien code utilisant un modèle Hugging Face, désactivé ===
# from transformers import pipeline
# classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")
# def analyze_email(request: EmailRequest):
#     result = classifier(request.text)
#     return {"label": result[0]["label"], "score": result[0]["score"]}
