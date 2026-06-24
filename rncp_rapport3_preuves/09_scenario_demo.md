# 09 - Scénario de démonstration (20 min)

| Temps | Action | Preuve |
|-------|--------|--------|
| 0-3 | Contexte MailSavior + architecture | schéma + 01_audit_depot.md |
| 3-6 | `/health` + Swagger `/docs` | api_swagger.png + logs/api_responses.log |
| 6-11 | Analyser 2 e-mails synthétiques dans le WPF | wpf_result_phishing.png + wpf_result_safe.png |
| 11-14 | Envoyer un feedback + montrer le monitoring | monitoring_dashboard_ou_csv.png + monitoring_sample.csv |
| 14-17 | Lancer `pytest` + montrer la CI | pytest_result.png + github_actions_green.png |
| 17-20 | Conclusion : résultats, limites, livraison | README + tag + checklist |

## Pré-lancement (avant la soutenance)

```bash
cd MailSaviorAI
python make_dataset.py && python train_model.py
python app.py          # laisser tourner
# puis lancer le WPF depuis Visual Studio
```

## Plan B (si la démo live plante)

- Vidéo locale 3-5 min de bout en bout.
- Toutes les captures dans `captures/`.
- Backend déjà lancé avant la soutenance.
- E-mails synthétiques prêts dans `demo_inputs.txt`.
- Aucun contenu réel ou sensible.
