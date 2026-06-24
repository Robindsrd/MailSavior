# 01 - Audit du dépôt

## Inventaire

```
MailSaviorAI/            # service IA Python (FastAPI)
  app.py                 # API : /health, /analyze_email, /feedback, /feedbacks
  make_dataset.py        # génération du dataset synthétique
  train_model.py         # entraînement TF-IDF + LogisticRegression
  emails_dataset.csv     # dataset synthétique (88 lignes)
  model/phishing_model.pkl   # artefact joblib (généré)
  model/classification_report.txt
  requirements.txt / requirements-dev.txt
  tests/                 # test_model.py, test_api.py, conftest.py
MailSaviorApp/           # application desktop WPF (.NET 8)
  MainWindow.*           # authentification LDAP/AD
  UserDashboard.*        # analyse + feedback
  FeedbackWindow.*       # historique feedbacks
  ApiConfig.cs           # URL API centralisée + timeout
.github/workflows/rapport3-ci.yml   # CI
```

Branches distantes : `origin/main`, `origin/hugo`, `origin/bastou`.

## État INITIAL constaté (avant corrections de cette session)

| Point | Constat initial | Risque |
|-------|-----------------|--------|
| Modèle | `score = random.uniform(0.4, 0.99)` dans app.py | **Faux modèle / P0** |
| Artefact | `model/` ne contenait qu'un `.gitkeep` | Aucun modèle livrable |
| Dépendances ML | absentes de requirements.txt | Non reproductible |
| README | annonçait un modèle **RoBERTa/HuggingFace** inexistant | Documentation fausse |
| `/analyze_email` | renvoyait `{suspicion_score}` seul | Pas de `label`/`model_version` |
| `/health` | **absente** | Pas de supervision |
| Tests | **absents** | C12 non prouvable |
| CI | **absente** | C13 non prouvable |
| Monitoring | **absent** | C11 non prouvable |
| `feedback_log.json` | commité **avec de vrais noms de personnes** | **Fuite de données / P0** |
| CORS | `allow_origins=["*"]` | Trop permissif |
| Ports | docker-compose `5000` vs app/WPF `8000` | Incohérence |

## Corrections appliquées dans cette session

- Remplacement du score aléatoire par un **vrai pipeline scikit-learn** chargé via joblib.
- Ajout `make_dataset.py`, `train_model.py`, `emails_dataset.csv`, artefact `.pkl`.
- Refonte `app.py` : `/health`, `/analyze_email` (label/score/version), validation 422,
  503 si modèle absent, 401 optionnel, monitoring CSV, CORS restreint, 500 masqué.
- Alignement WPF : lecture label+version, URL centralisée, timeout, erreurs propres,
  verdict textuel (accessibilité), feedback minimisé.
- Tests pytest (13) + CI GitHub Actions + README corrigé.
- **Confidentialité** : `feedback_log.json` anonymisé + ignoré par git + retiré du suivi ;
  purge de l'historique git planifiée (voir 05_securite_api.md).

## Reste à produire manuellement

- Build WPF + captures d'écran (pas de SDK .NET dans l'environnement d'audit).
- Push GitHub + capture du workflow vert.
