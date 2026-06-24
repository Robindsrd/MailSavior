# Synthèse Rapport 3 - MailSavior

## État général
- Branche analysée : main
- Commit de départ : 0b940a2
- Date de vérification : 2026-06-24
- Environnement : Windows 11, Python 3.14.2, scikit-learn 1.8.0, FastAPI 0.128.7

## Modèle IA
- Artefact : MailSaviorAI/model/phishing_model.pkl (joblib)
- Algorithme : TfidfVectorizer (1-2 grammes) + LogisticRegression
- Dataset : emails_dataset.csv — 88 lignes synthétiques (44 phishing / 44 safe)
- Métriques principales : accuracy 1.00 sur 22 cas de test (dataset synthétique → optimiste)
- Limites connues : dataset synthétique très séparable ; à réentraîner sur corpus réel anonymisé

## API
- Routes valides : /health, /analyze_email, /feedback, /feedbacks
- Schéma de réponse : { label, suspicion_score, model_version }
- Sécurité active : auth optionnelle par clé (MAILSAVIOR_API_KEY), CORS restreint, 500 masqué
- Erreurs testées : 422 (vide), 401 (sans clé), 503 (modèle absent)

## WPF
- Écran principal : OK (code revu ; capture à produire)
- Analyse phishing : OK (code revu ; capture à produire)
- Analyse safe : OK (code revu ; capture à produire)
- Feedback : OK (minimisé, sans corps d'e-mail)

## Monitoring
- Support : CSV (monitoring.csv)
- Données collectées : timestamp, request_id, version, label, score, latence, statut HTTP, longueur
- Données volontairement exclues : corps complet de l'e-mail

## Tests et CI
- Nombre de tests : 13 (tous verts)
- Commande : pytest -v / pytest --cov=app
- Résultat : 13 passed, couverture app.py = 89 %
- CI : .github/workflows/rapport3-ci.yml (capture verte à produire après push)

## Points restants
- P0 : aucun (score aléatoire supprimé, contrat unifié, secrets/données perso traités)
- P1 : purge de l'historique git à finaliser (force-push à coordonner) ; captures WPF + CI verte
- P2 : réentraîner sur dataset réel anonymisé pour des métriques représentatives
