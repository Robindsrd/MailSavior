from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")

class EmailRequest(BaseModel):
    text: str

@app.post("/analyze_email")
def analyze_email(request: EmailRequest):
    try:
        result = classifier(request.text)
        return {"label": result[0]["label"], "score": result[0]["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
