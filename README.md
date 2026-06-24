# MailSavior

MailSavior est une application de détection de phishing : un service IA (FastAPI) expose
un modèle de classification, consommé par une application desktop WPF.

## Architecture réelle

- **Application desktop** : C# / .NET 8 / WPF (`MailSaviorApp/`)
- **Service IA** : Python / FastAPI (`MailSaviorAI/`)
- **Modèle** : pipeline scikit-learn **TfidfVectorizer + LogisticRegression**, sérialisé avec joblib
  (`MailSaviorAI/model/phishing_model.pkl`)
- **Authentification (desktop)** : LDAP / Active Directory
- **Monitoring** : `monitoring.csv` (latence, label, score, version, statut HTTP — sans corps d'e-mail)

> Note : aucun modèle RoBERTa/HuggingFace n'est utilisé. Le modèle livré est le pipeline
> scikit-learn ci-dessus.

## Contrat API

| Route            | Méthode | Entrée            | Sortie                                              |
|------------------|---------|-------------------|-----------------------------------------------------|
| `/health`        | GET     | —                 | `status, model_loaded, model_version, uptime_seconds, timestamp` |
| `/analyze_email` | POST    | `{ "text": str }` | `{ label, suspicion_score, model_version }`         |
| `/feedback`      | POST    | retour minimisé   | `{ message, request_id }`                           |
| `/feedbacks`     | GET     | —                 | liste agrégée (sans corps d'e-mail)                 |

Erreurs : `422` (texte vide/invalide), `503` (modèle non chargé), `401` (si `MAILSAVIOR_API_KEY` définie),
`500` masqué (message générique).

## Lancer le projet (local)

### Service IA (Python)
```bash
cd MailSaviorAI
python -m venv venv
# Windows : venv\Scripts\activate   |   Linux/Mac : source venv/bin/activate
pip install -r requirements.txt

python make_dataset.py     # génère le dataset synthétique
python train_model.py      # entraîne et sauvegarde model/phishing_model.pkl
python app.py              # démarre l'API sur http://127.0.0.1:8000
```
Swagger : http://127.0.0.1:8000/docs

### Application WPF (C#)
Ouvrir `MailSavior.sln` dans Visual Studio et exécuter `MailSaviorApp`.
L'URL de l'API peut être surchargée via la variable d'environnement `MAILSAVIOR_API_URL`.

### Tests
```bash
cd MailSaviorAI
pip install -r requirements-dev.txt
pytest -q
pytest --cov=app --cov-report=term-missing
```

## Sécurité / confidentialité

- Le corps complet des e-mails n'est **jamais** persisté (feedback et monitoring stockent uniquement
  la longueur du texte).
- `feedback_log.json` et `monitoring.csv` sont ignorés par git (`.gitignore`).
- Authentification API optionnelle par clé (`MAILSAVIOR_API_KEY`).

## Rollback du modèle

Pour revenir à une version précédente du modèle, restaurer l'artefact `model/phishing_model.pkl`
depuis un commit antérieur (`git checkout <commit> -- MailSaviorAI/model/phishing_model.pkl`)
ou relancer `python train_model.py` sur le dataset voulu. La version est tracée par le champ
`model_version` renvoyé par `/health` et `/analyze_email`.
