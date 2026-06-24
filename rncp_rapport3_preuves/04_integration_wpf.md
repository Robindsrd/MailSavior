# 04 - Intégration WPF (C10)

## Parcours utilisateur

1. Connexion (LDAP/AD) → `MainWindow`.
2. `UserDashboard` : saisie du texte d'un e-mail.
3. Clic « Analyser » → POST `/analyze_email` (HttpClient réutilisé, timeout 10 s).
4. Affichage : **verdict textuel** + score % + version du modèle.
5. Feedback « Oui / Non » → POST `/feedback` (minimisé : pas de corps d'e-mail).
6. `FeedbackWindow` : historique agrégé via GET `/feedbacks`.

## Points techniques corrigés (réf. fichiers)

| Sujet | Avant | Après |
|-------|-------|-------|
| URL API | en dur, 2 formes (`127.0.0.1` et `localhost`) | `ApiConfig.BaseUrl` centralisé (+ env `MAILSAVIOR_API_URL`) |
| HttpClient | recréé à chaque clic | `static readonly` réutilisé |
| Timeout | aucun | 10 s (`ApiConfig.Timeout`) |
| Chargement | aucun | bouton désactivé + « Analyse en cours... » |
| Erreurs | exception brute affichée | messages distincts (timeout / connexion / indispo) |
| Réponse | lisait `suspicion_score` seul | lit `label` + `suspicion_score` + `model_version` |
| Accessibilité | couleur seule | verdict en toutes lettres (`⚠ PHISHING` / `✓ Message sûr`) + couleur |
| Feedback | envoyait le texte complet | envoie `suspicion_score, feedback, predicted_label, text_length` |

Fichiers : `MailSaviorApp/UserDashboard.xaml(.cs)`, `FeedbackWindow.xaml(.cs)`,
`ApiConfig.cs`, `AnalysisFeedback.cs`.

## Captures à produire (build Visual Studio requis)

Voir `captures/README.md`. L'environnement d'audit n'a pas de SDK .NET : la compilation et les
captures se font sur le poste de développement. Le code a été revu (cohérent avec le contrat API).
