# Captures à réaliser

Ces images ne peuvent pas être générées dans l'environnement d'audit (pas de SDK .NET pour le
WPF, pas d'accès au compte GitHub). Mode opératoire pour chacune :

| Fichier | Comment l'obtenir |
|---------|-------------------|
| api_swagger.png | API lancée → ouvrir `http://127.0.0.1:8000/docs` |
| api_health_200.png | `http://127.0.0.1:8000/health` dans le navigateur (ou capture de logs/api_responses.log) |
| api_analyze_200.png | Swagger « Try it out » sur `/analyze_email` |
| api_analyze_422.png | Swagger avec `{"text":""}` |
| api_auth_401_ou_403.png | API lancée avec `MAILSAVIOR_API_KEY`, appel sans en-tête |
| wpf_dashboard.png | Visual Studio → lancer MailSaviorApp → UserDashboard |
| wpf_result_phishing.png | Coller l'e-mail PHISHING de `demo_inputs.txt` → Analyser |
| wpf_result_safe.png | Coller l'e-mail SAFE → Analyser |
| wpf_error_api_unavailable.png | Arrêter l'API puis cliquer Analyser |
| wpf_feedback_sent.png | Cliquer Oui/Non → message de confirmation |
| monitoring_dashboard_ou_csv.png | Ouvrir `MailSaviorAI/monitoring.csv` (ou exports/monitoring_sample.csv) |
| pytest_result.png | `pytest -v` dans le terminal |
| coverage_result.png | `pytest --cov=app --cov-report=term-missing` |
| github_actions_green.png | Onglet Actions sur GitHub après push |

> Règle : masquer toute donnée sensible. N'utiliser que les e-mails synthétiques fournis.
