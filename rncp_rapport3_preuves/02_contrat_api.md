# 02 - Contrat API (C9)

API : FastAPI · Base URL locale : `http://127.0.0.1:8000` · OpenAPI : `exports/openapi.json` · Swagger : `/docs`

| Route | Méthode | Entrée | Sortie | Accès |
|-------|---------|--------|--------|-------|
| `/health` | GET | — | `status, model_loaded, model_version, uptime_seconds, timestamp` | Public |
| `/analyze_email` | POST | `{ "text": str }` (1..10000 car.) | `{ label, suspicion_score, model_version }` | Public ou clé API |
| `/feedback` | POST | `{ suspicion_score, feedback, predicted_label?, text_length? }` | `{ message, request_id }` | Public ou clé API |
| `/feedbacks` | GET | — | liste agrégée (sans corps d'e-mail) | Public |

## Réponse type `/analyze_email`

```json
{ "label": "phishing", "suspicion_score": 0.7768, "model_version": "1.0.0" }
```
(preuve réelle : `logs/api_responses.log`)

## Cas d'erreur prouvés

| Cas | Code | Preuve |
|-----|------|--------|
| Texte vide / blanc | 422 | logs/api_responses.log |
| Champ manquant | 422 | tests/test_api.py::test_analyze_missing_field_returns_422 |
| Non authentifié (clé API active) | 401 | logs/api_auth_401.log |
| Modèle non chargé | 503 | logs/api_503_model_absent.log |
| Erreur interne | 500 masqué | handler générique `app.py` (message « Erreur interne du serveur. ») |

## Contrat WPF ↔ API

Le WPF consomme **exactement** `label`, `suspicion_score`, `model_version`. Un test verrouille
ce contrat : `tests/test_api.py::test_analyze_returns_contract_fields`
(`set(body.keys()) == {"label","suspicion_score","model_version"}`).
