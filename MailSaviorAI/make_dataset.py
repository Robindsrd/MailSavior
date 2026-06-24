"""Génère un dataset SYNTHETIQUE d'emails (phishing / safe) pour MailSavior.

Aucune donnée réelle n'est utilisée : tous les textes sont produits par
combinaison de gabarits. Le résultat est reproductible (ordre déterministe).

Usage :
    python make_dataset.py
Produit : emails_dataset.csv  (colonnes : text,label)
"""
import csv
import itertools
from pathlib import Path

DATASET_PATH = Path(__file__).parent / "emails_dataset.csv"

# --- Gabarits PHISHING (synthétiques) ---------------------------------------
PHISHING_TEMPLATES = [
    "Votre compte {service} a été suspendu, cliquez ici pour vérifier vos informations",
    "Action requise : confirmez votre mot de passe {service} sous 24h ou votre accès sera bloqué",
    "Cher client, une activité suspecte a été détectée. Cliquez sur ce lien pour sécuriser votre compte {service}",
    "Vous avez gagné un {prize} ! Cliquez immédiatement pour réclamer votre gain",
    "Votre colis est bloqué, réglez {amount} de frais de douane via ce lien sécurisé",
    "URGENT : votre facture {service} est impayée, payez maintenant pour éviter la coupure",
    "Votre boîte mail est pleine, validez vos identifiants pour continuer à recevoir vos messages",
    "Mise à jour de sécurité requise : reconnectez-vous à {service} via ce lien",
    "Bonjour, veuillez cliquer sur ce lien pour réinitialiser votre mot de passe immédiatement",
    "Confirmez vos coordonnées bancaires pour recevoir votre remboursement de {amount}",
    "Dernier avertissement : votre compte sera supprimé si vous ne vérifiez pas vos données ici",
    "Votre carte a été débitée de {amount}. Si ce n'est pas vous, cliquez ici pour annuler",
]

# --- Gabarits SAFE (synthétiques) -------------------------------------------
SAFE_TEMPLATES = [
    "Bonjour, la réunion de demain est confirmée à {time} en salle {room}",
    "Salut {name}, peux-tu m'envoyer le compte rendu de la réunion de lundi ?",
    "Merci pour ton retour, je valide la version du document et je te recontacte",
    "Rappel : la formation {service} aura lieu jeudi à {time}, pense à apporter ton ordinateur",
    "Bonjour, voici l'ordre du jour du comité de {time}, n'hésitez pas à ajouter des points",
    "L'équipe support a bien reçu ta demande, nous revenons vers toi rapidement",
    "Bonjour {name}, le rapport mensuel est prêt, tu le trouveras sur le partage interne",
    "Petit point d'organisation : le déjeuner d'équipe est déplacé à {time}",
    "Merci d'avoir participé à l'atelier, les supports seront partagés cette semaine",
    "Bonjour, je confirme ma présence à la réunion projet de {time}",
    "Voici les notes de la session {service}, bonne lecture et bon week-end",
    "Bonjour {name}, peux-tu relire la présentation avant la réunion de {time} ?",
]

SERVICES = ["bancaire", "de messagerie", "client", "professionnel", "interne"]
PRIZES = ["iPhone", "bon d'achat", "voyage", "chèque cadeau"]
AMOUNTS = ["2,99 EUR", "49 EUR", "199 EUR", "1,50 EUR"]
TIMES = ["10h", "14h", "9h30", "16h"]
ROOMS = ["A12", "B3", "Réunion 2", "Open space"]
NAMES = ["Camille", "Alex", "Sam", "Léa", "Noa"]


def _fill(template: str, i: int) -> str:
    return template.format(
        service=SERVICES[i % len(SERVICES)],
        prize=PRIZES[i % len(PRIZES)],
        amount=AMOUNTS[i % len(AMOUNTS)],
        time=TIMES[i % len(TIMES)],
        room=ROOMS[i % len(ROOMS)],
        name=NAMES[i % len(NAMES)],
    )


def build_rows():
    rows = []
    for tpl_idx, tpl in enumerate(PHISHING_TEMPLATES):
        for v in range(len(SERVICES)):
            rows.append((_fill(tpl, tpl_idx + v), "phishing"))
    for tpl_idx, tpl in enumerate(SAFE_TEMPLATES):
        for v in range(len(SERVICES)):
            rows.append((_fill(tpl, tpl_idx + v), "safe"))
    # dédoublonnage en conservant l'ordre
    seen = set()
    unique = []
    for text, label in rows:
        key = (text, label)
        if key not in seen:
            seen.add(key)
            unique.append((text, label))
    return unique


def main():
    rows = build_rows()
    with DATASET_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)
    n_phish = sum(1 for _, l in rows if l == "phishing")
    n_safe = sum(1 for _, l in rows if l == "safe")
    print(f"Dataset écrit : {DATASET_PATH}")
    print(f"Total={len(rows)} | phishing={n_phish} | safe={n_safe}")


if __name__ == "__main__":
    main()
