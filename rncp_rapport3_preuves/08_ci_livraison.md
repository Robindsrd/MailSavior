# 08 - Intégration et livraison continues (C13)

Workflow : `.github/workflows/rapport3-ci.yml`.

## Étapes du job `backend-tests` (ubuntu-latest)

1. `checkout` du dépôt.
2. `setup-python` 3.11.
3. Installation `requirements-dev.txt`.
4. `make_dataset.py` + `train_model.py` (génère le modèle).
5. `pytest --cov=app` (tests + couverture).
6. `upload-artifact` : `phishing_model.pkl`.

Déclencheurs : `push` et `pull_request`. Aucun secret de production dans le workflow.

## Preuves

| Preuve | Statut |
|--------|--------|
| `rapport3-ci.yml` (fichier versionné) | OK |
| `captures/github_actions_green.png` | À capturer après `git push` |
| `exports/git_log_anonymise.txt` | OK |

## Procédure de livraison / tag

```bash
git add -A && git commit -m "Rapport 3 : vrai modèle, API sécurisée, tests, CI, monitoring"
git push origin main
git tag rncp-mailsavior-v1 && git push origin rncp-mailsavior-v1
```

## Rollback

Voir README (« Rollback du modèle ») : restaurer `model/phishing_model.pkl` depuis un commit
antérieur ou réentraîner. La version active est lisible via `/health` (`model_version`).
