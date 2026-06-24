# 06 - Monitoring du modèle (C11)

Support : fichier `monitoring.csv` (généré à l'exécution, ignoré par git).
Écriture via un middleware FastAPI à chaque appel `/analyze_email`.

## Colonnes

`created_at, request_id, model_version, predicted_label, suspicion_score, latency_ms, http_status, text_length, feedback_correct`

## Extrait réel (preuve : `exports/monitoring_sample.csv`)

```
created_at,request_id,model_version,predicted_label,suspicion_score,latency_ms,http_status,text_length,feedback_correct
2026-06-24T18:42:37+00:00,req-8ce08f9a,1.0.0,phishing,0.7768,2.9,200,71,
2026-06-24T18:42:37+00:00,req-f19293ae,1.0.0,safe,0.3444,1.7,200,62,
2026-06-24T18:43:02+00:00,req-7f2c860b,1.0.0,phishing,0.7303,1.9,200,39,
```

## Données volontairement EXCLUES (confidentialité)

- Le **corps de l'e-mail** n'est jamais stocké (ni monitoring, ni feedback).
- Seules sont conservées : longueur du texte, label prédit, score, latence, statut HTTP, version.
- Les feedbacks (`feedback_log.json`) suivent le même principe : `feedback_correct` permet de
  suivre les désaccords utilisateurs sans conserver le texte.

## Métriques exploitables

- **latence** (latency_ms) : détecter une dégradation technique.
- **distribution phishing/safe** (predicted_label) : dérive d'usage.
- **score moyen** (suspicion_score) : niveau de confiance.
- **statuts HTTP** : taux d'erreurs.
- **feedback_correct** : taux d'accord modèle / utilisateur.
