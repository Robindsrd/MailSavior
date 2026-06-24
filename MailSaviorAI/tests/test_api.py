"""Tests du contrat API et des cas d'erreur (C9 / C12)."""
import app as app_module

PHISHING_TEXT = "Votre compte a été suspendu, cliquez ici pour vérifier vos informations"
SAFE_TEXT = "Bonjour, la réunion de demain est confirmée à 10h en salle A12"


def test_health_returns_200_and_model_loaded(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["model_loaded"] is True
    assert body["status"] == "ok"
    assert body["model_version"] == "1.0.0"


def test_analyze_returns_contract_fields(client):
    r = client.post("/analyze_email", json={"text": PHISHING_TEXT})
    assert r.status_code == 200
    body = r.json()
    # Contrat consommé par le WPF : exactement ces 3 propriétés.
    assert set(body.keys()) == {"label", "suspicion_score", "model_version"}
    assert body["label"] in {"phishing", "safe"}
    assert 0.0 <= body["suspicion_score"] <= 1.0
    assert body["model_version"] == "1.0.0"


def test_analyze_phishing_vs_safe(client):
    phishing = client.post("/analyze_email", json={"text": PHISHING_TEXT}).json()
    safe = client.post("/analyze_email", json={"text": SAFE_TEXT}).json()
    assert phishing["label"] == "phishing"
    assert safe["label"] == "safe"


def test_analyze_empty_text_returns_422(client):
    assert client.post("/analyze_email", json={"text": ""}).status_code == 422
    assert client.post("/analyze_email", json={"text": "   "}).status_code == 422


def test_analyze_missing_field_returns_422(client):
    assert client.post("/analyze_email", json={}).status_code == 422


def test_analyze_returns_503_when_model_absent(client, monkeypatch):
    monkeypatch.setitem(app_module.MODEL, "pipeline", None)
    r = client.post("/analyze_email", json={"text": PHISHING_TEXT})
    assert r.status_code == 503


def test_health_degraded_when_model_absent(client, monkeypatch):
    monkeypatch.setitem(app_module.MODEL, "pipeline", None)
    body = client.get("/health").json()
    assert body["model_loaded"] is False
    assert body["status"] == "degraded"


def test_feedback_valid_is_persisted(client):
    payload = {
        "suspicion_score": 0.87,
        "feedback": "phishing",
        "predicted_label": "phishing",
        "text_length": 71,
    }
    r = client.post("/feedback", json=payload)
    assert r.status_code == 200
    assert "request_id" in r.json()

    feedbacks = client.get("/feedbacks").json()
    assert len(feedbacks) == 1
    saved = feedbacks[0]
    assert saved["feedback_correct"] is True
    # Minimisation : aucun champ de texte brut ne doit être stocké.
    assert "text" not in saved
    assert saved["text_length"] == 71


def test_feedback_invalid_is_rejected(client):
    # score hors [0,1] et feedback manquant -> 422
    assert client.post("/feedback", json={"suspicion_score": 2.0, "feedback": "x"}).status_code == 422
    assert client.post("/feedback", json={"feedback": "phishing"}).status_code == 422


def test_monitoring_csv_written_on_analyze(client):
    client.post("/analyze_email", json={"text": PHISHING_TEXT})
    assert app_module.MONITORING_PATH.exists()
    content = app_module.MONITORING_PATH.read_text(encoding="utf-8")
    assert "predicted_label" in content  # en-tête
    assert "phishing" in content
