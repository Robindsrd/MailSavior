# 03 - Modèle et métriques (C9 / C12)

| Information | Valeur | Source |
|-------------|--------|--------|
| Dataset | `emails_dataset.csv` (synthétique) | `make_dataset.py` |
| Nombre de lignes | 88 | `pd.read_csv` |
| Colonnes | `text`, `label` | `df.columns` |
| Répartition labels | phishing = 44 / safe = 44 (équilibré) | `value_counts()` |
| Train / test | 66 / 22 (split stratifié 75/25, `random_state=42`) | `train_model.py` |
| Algorithme | **TfidfVectorizer (1-2 grammes) + LogisticRegression** | `train_model.py` |
| Artefact | `model/phishing_model.pkl` (joblib, dict `{pipeline, model_version}`) | `joblib.dump` |
| Version | `1.0.0` | constante `MODEL_VERSION` |

## classification_report (jeu de test) — preuve : `exports/classification_report.txt`

```
              precision    recall  f1-score   support
    phishing      1.000     1.000     1.000        11
        safe      1.000     1.000     1.000        11
    accuracy                          1.000        22
```

## Limite connue (à mentionner dans le rapport)

Le dataset est **synthétique et volontairement très séparable** (gabarits phishing vs gabarits
légitimes). Les métriques (100 %) sont donc **optimistes** et ne reflètent pas une performance
en conditions réelles. Le pipeline et la chaîne (entraînement → artefact → API → tests) sont en
revanche **réels et reproductibles**. Une évolution naturelle est de réentraîner sur un corpus
réel anonymisé pour obtenir des métriques représentatives.

## Reproduire

```bash
cd MailSaviorAI
python make_dataset.py
python train_model.py
```

> Vérification anti-« faux modèle » : `app.py` ne contient plus aucun `random`. Le score provient
> de `pipeline.predict_proba`. Test associé : `tests/test_model.py`.
