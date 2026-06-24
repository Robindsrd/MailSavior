# 05 - Sécurité, confidentialité et OWASP API

| Risque | Mesure en place | Preuve |
|--------|-----------------|--------|
| Accès non autorisé | Auth optionnelle par clé (`MAILSAVIOR_API_KEY`) → 401 | logs/api_auth_401.log |
| Texte trop long / vide | Validation Pydantic `min_length=1, max_length=10000` → 422 | logs/api_responses.log |
| CORS trop large | Origines restreintes à `http://localhost` / `127.0.0.1` | app.py (CORSMiddleware) |
| Secret dans le dépôt | `.env` ignoré ; clé API via variable d'environnement | .gitignore |
| Exception exposée | Handler 500 générique (« Erreur interne du serveur. ») | app.py |
| Logs / stockage sensibles | Ni feedback ni monitoring ne stockent le corps d'e-mail (seulement `text_length`) | exports/monitoring_sample.csv, app.py |
| Feedback sensible | Schéma minimisé, aucun texte brut | 06_monitoring.md |
| Artefact modèle | Chargé depuis un chemin contrôlé (`MAILSAVIOR_MODEL_PATH`), pas d'entrée arbitraire | app.py `load_model()` |

## Donnée personnelle traitée (P0)

Le fichier `MailSaviorAI/feedback_log.json` était commité **avec de vrais noms** (prénoms et
noms de personnes). Actions réalisées :

1. Contenu remplacé par des exemples **synthétiques** au schéma minimisé (sans texte d'e-mail).
2. Fichier **retiré du suivi git** (`git rm --cached`) et ajouté au `.gitignore`.
3. **Purge de l'historique git** (voir section suivante) car les anciens commits contiennent
   encore les noms réels.

## Purge de l'historique git — procédure

> ⚠ Réécrit l'historique : nécessite un `git push --force` et impacte les branches `hugo`/`bastou`.

```bash
# Option recommandée (git-filter-repo) :
pip install git-filter-repo
git filter-repo --path MailSaviorAI/feedback_log.json --invert-paths --force

# Puis re-pousser toutes les branches concernées :
git push origin --force --all
```
Prévenir les autres contributeurs (rebase de leurs branches nécessaire).
