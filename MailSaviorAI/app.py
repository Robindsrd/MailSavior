"""API FastAPI de MailSavior - exposition sécurisée du modèle de détection de phishing.

Routes :
    GET  /health          -> état du service et du modèle
    POST /analyze_email   -> {label, suspicion_score, model_version}
    POST /feedback        -> enregistrement minimisé d'un retour utilisateur
    GET  /feedbacks       -> agrégat des feedbacks (sans corps des e-mails)

Sécurité / confidentialité :
    - Le modèle est chargé depuis un artefact contrôlé (model/phishing_model.pkl).
    - Aucune route ne stocke le corps complet des e-mails (seule la longueur est conservée).
    - Authentification optionnelle par clé API (variable d'environnement MAILSAVIOR_API_KEY).
    - CORS restreint aux origines locales du client WPF.
"""
import csv
import json
import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import joblib
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).parent
MODEL_PATH = Path(os.getenv("MAILSAVIOR_MODEL_PATH", BASE_DIR / "model" / "phishing_model.pkl"))
FEEDBACK_PATH = BASE_DIR / "feedback_log.json"
MONITORING_PATH = BASE_DIR / "monitoring.csv"

# Clé API optionnelle : si définie, /analyze_email et /feedback exigent l'en-tête X-API-Key.
API_KEY = os.getenv("MAILSAVIOR_API_KEY")

MAX_TEXT_LENGTH = 10000
MONITORING_COLUMNS = [
    "created_at", "request_id", "model_version", "predicted_label",
    "suspicion_score", "latency_ms", "http_status", "text_length", "feedback_correct",
]

# État du modèle (rempli au démarrage).
MODEL = {"pipeline": None, "model_version": None, "phishing_index": None}
START_TIME = time.monotonic()


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_model() -> None:
    """Charge l'artefact joblib depuis un chemin contrôlé. En cas d'absence, le
    service reste opérationnel mais /analyze_email renverra 503."""
    if not MODEL_PATH.exists():
        MODEL["pipeline"] = None
        return
    artifact = joblib.load(MODEL_PATH)
    pipeline = artifact["pipeline"]
    classes = list(pipeline.classes_)
    MODEL["pipeline"] = pipeline
    MODEL["model_version"] = artifact.get("model_version", "unknown")
    MODEL["phishing_index"] = classes.index("phishing") if "phishing" in classes else 1


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield


app = FastAPI(title="MailSavior IA API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    """Dépendance d'authentification, active uniquement si MAILSAVIOR_API_KEY est définie."""
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Clé API manquante ou invalide.")


# --- Schémas ----------------------------------------------------------------
class EmailRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TEXT_LENGTH)

    @field_validator("text")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Le texte ne peut pas être vide.")
        return v


class AnalyzeResponse(BaseModel):
    label: str
    suspicion_score: float
    model_version: str


class FeedbackRequest(BaseModel):
    suspicion_score: float = Field(..., ge=0.0, le=1.0)
    feedback: str = Field(..., min_length=1)
    predicted_label: Optional[str] = None
    text_length: Optional[int] = Field(default=None, ge=0)


# --- Monitoring -------------------------------------------------------------
def append_monitoring(row: dict) -> None:
    is_new = not MONITORING_PATH.exists()
    with MONITORING_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MONITORING_COLUMNS)
        if is_new:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in MONITORING_COLUMNS})


@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    if request.url.path == "/analyze_email":
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        data = getattr(request.state, "monitoring", None)
        if data is not None:
            append_monitoring({
                "created_at": _utcnow(),
                "request_id": data["request_id"],
                "model_version": data["model_version"],
                "predicted_label": data["predicted_label"],
                "suspicion_score": data["suspicion_score"],
                "latency_ms": latency_ms,
                "http_status": response.status_code,
                "text_length": data["text_length"],
            })
    return response


# --- Routes -----------------------------------------------------------------
@app.get("/health")
async def health():
    loaded = MODEL["pipeline"] is not None
    return {
        "status": "ok" if loaded else "degraded",
        "model_loaded": loaded,
        "model_version": MODEL["model_version"],
        "uptime_seconds": round(time.monotonic() - START_TIME, 1),
        "timestamp": _utcnow(),
    }


@app.post("/analyze_email", response_model=AnalyzeResponse)
async def analyze_email(email: EmailRequest, request: Request, _=Depends(require_api_key)):
    if MODEL["pipeline"] is None:
        raise HTTPException(status_code=503, detail="Modèle indisponible.")

    proba = MODEL["pipeline"].predict_proba([email.text])[0]
    score = round(float(proba[MODEL["phishing_index"]]), 4)
    label = "phishing" if score >= 0.5 else "safe"

    # Métadonnées de monitoring (jamais le corps de l'e-mail).
    request.state.monitoring = {
        "request_id": f"req-{uuid.uuid4().hex[:8]}",
        "model_version": MODEL["model_version"],
        "predicted_label": label,
        "suspicion_score": score,
        "text_length": len(email.text),
    }
    return {"label": label, "suspicion_score": score, "model_version": MODEL["model_version"]}


@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest, _=Depends(require_api_key)):
    # Minimisation : on ne stocke jamais le texte de l'e-mail, seulement sa longueur.
    feedback_correct = (
        feedback.predicted_label is not None
        and feedback.predicted_label == feedback.feedback
    )
    entry = {
        "created_at": _utcnow(),
        "request_id": f"req-{uuid.uuid4().hex[:8]}",
        "model_version": MODEL["model_version"],
        "predicted_label": feedback.predicted_label,
        "suspicion_score": feedback.suspicion_score,
        "feedback_label": feedback.feedback,
        "feedback_correct": feedback_correct,
        "text_length": feedback.text_length,
    }

    if FEEDBACK_PATH.exists():
        try:
            data = json.loads(FEEDBACK_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    FEEDBACK_PATH.write_text(
        json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8"
    )
    return {"message": "Feedback enregistré", "request_id": entry["request_id"]}


@app.get("/feedbacks")
async def get_feedbacks():
    if not FEEDBACK_PATH.exists():
        return []
    try:
        return json.loads(FEEDBACK_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Message générique côté utilisateur ; le détail reste dans les logs serveur.
    return JSONResponse(status_code=500, content={"detail": "Erreur interne du serveur."})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
