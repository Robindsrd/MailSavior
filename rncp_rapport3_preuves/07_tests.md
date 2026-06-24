# 07 - Tests automatisés (C12)

Framework : pytest + FastAPI TestClient. Résultat : **13 tests passés**, couverture **app.py = 89 %**.
Preuves : `logs/pytest_output.txt`, `logs/coverage_output.txt`.

## Couverture fonctionnelle

| Niveau | Test | Fichier |
|--------|------|---------|
| Artefact modèle | charge + expose `predict_proba` | test_model.py::test_artefact_exists_and_loads |
| Dataset | lisible, colonnes, labels valides | test_model.py::test_dataset_readable_and_valid |
| Prédiction | label valide + proba dans [0,1] | test_model.py::test_prediction_returns_valid_label_and_score |
| API health | 200 + model_loaded | test_api.py::test_health_returns_200_and_model_loaded |
| API analyse | contrat label/score/version | test_api.py::test_analyze_returns_contract_fields |
| Cohérence | phishing vs safe | test_api.py::test_analyze_phishing_vs_safe |
| Validation | texte vide/blanc → 422 | test_api.py::test_analyze_empty_text_returns_422 |
| Validation | champ manquant → 422 | test_api.py::test_analyze_missing_field_returns_422 |
| Modèle absent | 503 | test_api.py::test_analyze_returns_503_when_model_absent |
| Modèle absent | /health degraded | test_api.py::test_health_degraded_when_model_absent |
| Feedback | persistance + minimisation (`text` absent) | test_api.py::test_feedback_valid_is_persisted |
| Feedback | rejet d'un feedback invalide → 422 | test_api.py::test_feedback_invalid_is_rejected |
| Monitoring | écriture CSV sur analyse | test_api.py::test_monitoring_csv_written_on_analyze |

## Lancer

```bash
cd MailSaviorAI
pip install -r requirements-dev.txt
pytest -v
pytest --cov=app --cov-report=term-missing
```

## Incohérence évitée par un test

`test_analyze_returns_contract_fields` verrouille le contrat WPF↔API : si un développeur ajoutait
ou renommait un champ de réponse (régression de l'ancien `{suspicion_score}` seul), le test
échouerait immédiatement, évitant de casser le client WPF.
