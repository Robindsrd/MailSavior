# 00 - Manifest des preuves (Rapport 3 - MailSavior - RNCP 37827)

Date de vérification : 2026-06-24
Branche : `main` — Commit de départ : `0b940a2`
Environnement : Windows 11, Python 3.14.2, scikit-learn 1.8.0, FastAPI 0.128.7

Légende statut : **OK** (preuve générée et vérifiée) · **À capturer** (capture écran à
réaliser par l'étudiant : GUI WPF ou GitHub) · **Absent** · **N/A**.

| ID | Comp. | Fichier | Description | Commande | Statut |
|----|-------|---------|-------------|----------|--------|
| R3-C9-API-001 | C9 | exports/openapi.json | Contrat OpenAPI complet (routes + schémas) | `curl /openapi.json` | OK |
| R3-C9-API-002 | C9 | logs/api_responses.log | /health 200 + modèle chargé | `curl -i /health` | OK |
| R3-C9-API-003 | C9 | logs/api_responses.log | /analyze_email 200 (label+score+version) | `curl -i POST /analyze_email` | OK |
| R3-C9-API-004 | C9/C12 | logs/api_responses.log | /analyze_email 422 (texte vide) | `curl -i POST /analyze_email -d '{"text":""}'` | OK |
| R3-C9-API-005 | C9 | logs/api_auth_401.log | 401 sans clé API / 200 avec clé | `MAILSAVIOR_API_KEY=... curl -i` | OK |
| R3-C9-API-006 | C9/C12 | logs/api_503_model_absent.log | 503 + /health degraded si modèle absent | `MAILSAVIOR_MODEL_PATH=/inexistant` | OK |
| R3-C9-SWAG-001 | C9 | captures/api_swagger.png | Swagger UI `/docs` | navigateur sur `/docs` | À capturer |
| R3-C9-MOD-001 | C9/C12 | exports/classification_report.txt | Métriques réelles du modèle | `python train_model.py` | OK |
| R3-C10-WPF-001 | C10 | captures/wpf_dashboard.png | Écran principal avant analyse | VS Run | À capturer |
| R3-C10-WPF-002 | C10 | captures/wpf_result_phishing.png | Résultat phishing (label+score+version) | VS Run | À capturer |
| R3-C10-WPF-003 | C10 | captures/wpf_result_safe.png | Résultat safe | VS Run | À capturer |
| R3-C10-WPF-004 | C10 | captures/wpf_error_api_unavailable.png | Message API arrêtée | VS Run (API stoppée) | À capturer |
| R3-C10-WPF-005 | C10 | captures/wpf_feedback_sent.png | Confirmation d'envoi feedback | VS Run | À capturer |
| R3-C11-MON-001 | C11 | exports/monitoring_sample.csv | Lignes de monitoring réelles | appels `/analyze_email` | OK |
| R3-C11-MON-002 | C11 | captures/monitoring_dashboard_ou_csv.png | Visualisation du monitoring | ouvrir le CSV | À capturer |
| R3-C12-TEST-001 | C12 | logs/pytest_output.txt | 13 tests verts | `pytest -v` | OK |
| R3-C12-TEST-002 | C12 | logs/coverage_output.txt | Couverture app.py = 89 % | `pytest --cov=app` | OK |
| R3-C12-TEST-003 | C12 | captures/pytest_result.png | Capture pytest vert | terminal | À capturer |
| R3-C13-CI-001 | C13 | ../.github/workflows/rapport3-ci.yml | Workflow CI (tests + artefact) | — | OK (fichier) |
| R3-C13-CI-002 | C13 | captures/github_actions_green.png | Exécution CI verte | GitHub Actions | À capturer (après push) |
| R3-C13-GIT-001 | C13 | exports/git_log_anonymise.txt | Traçabilité des commits | `git log` | OK |
| R3-SEC-001 | C9 | 05_securite_api.md | Synthèse sécurité / OWASP API | — | OK |

> Les preuves "À capturer" nécessitent l'IHM WPF (build Visual Studio) ou le compte GitHub :
> elles ne peuvent pas être générées dans l'environnement d'audit (pas de SDK .NET, pas de
> push). Le mode opératoire pour chacune est décrit dans `captures/README.md`.
