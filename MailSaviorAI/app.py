from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib

app = FastAPI()


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

class Feedback(BaseModel):
    text: str
    score: float
    feedback: str


feedback_storage: List[Feedback] = []


@app.post("/feedback")
def receive_feedback(fb: Feedback):
    feedback_storage.append(fb)
    return {"status": "success"}

@app.get("/feedbacks")
def get_all_feedbacks():
    return feedback_storage