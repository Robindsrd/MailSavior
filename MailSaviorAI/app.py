from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import json
from datetime import datetime
from typing import List
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    text: str

@app.post("/analyze_email")
async def analyze_email(email: EmailRequest):
    score = round(random.uniform(0.4, 0.99), 2)
    return {"suspicion_score": score}



class FeedbackRequest(BaseModel):
    text: str
    score: float
    feedback: str  

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "text": feedback.text,
        "score": feedback.score,
        "feedback": feedback.feedback
    }

    file_path = "feedback_log.json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {"message": "Feedback enregistré"}




@app.get("/feedbacks")
async def get_feedbacks():
    file_path = "feedback_log.json"

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []

    return data
