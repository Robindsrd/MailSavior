# MailSavior

MailSavior est une application de cybersécurité pour le secteur de la santé, conçue pour détecter et bloquer les attaques de phishing localement grâce à l'intelligence artificielle.

## Technologies

- **Frontend / Backend principal** : C# (.NET 8, WPF)
- **Moteur IA** : Python (modèle RoBERTa via HuggingFace)
- **Base de données** : SQLite
- **Authentification** : LDAP / Active Directory
- **Conteneurisation IA (optionnelle)** : Docker

## Fonctionnalités principales

- Détection automatique de phishing avec score
- Interface utilisateur et administrateur
- Feedback utilisateur pour améliorer le modèle IA
- Authentification sécurisée via LDAP
- Archivage local sécurisé

## Structure

- `MailSaviorApp/` : application desktop en C# WPF
- `MailSaviorAI/` : microservice Python avec API REST pour analyse des emails
- `docker-compose.yml` : configuration pour déploiement

## Lancer le projet (local)


### Partie venv

### Partie Python IA
```bash
cd MailSaviorAI
pip install -r requirements.txt
python app.py
```

### Partie C# (Visual Studio)
Ouvrir `MailSaviorApp.sln` et exécuter l'application.

