# fichier : generate_data_for_d3.py

import json
from arbre_genealogique import Famille

# Construire un noeud de personne avec ses mariages
def construire_noeud_avec_mariages(personne, famille):
    noeud = {
        "name": f"{personne.prenom} {personne.nom}",
        "date": personne.date_naissance,
        "profession": personne.profession,
        "spouses": []
    }

    mariages = famille.get_mariages_de(personne.id)
    for mariage in mariages:
        if mariage.conjoint_1 == personne.id:
            conjoint_id = mariage.conjoint_2
        else:
            conjoint_id = mariage.conjoint_1

        if conjoint_id not in famille.membres:
            continue

        conjoint = famille.membres[conjoint_id]
        enfants = [famille.membres[eid] for eid in mariage.enfants if eid in famille.membres]

        union = {
            "name": f"{conjoint.prenom} {conjoint.nom}",
            "date": conjoint.date_naissance,
            "profession": conjoint.profession,
            "children": [construire_noeud_avec_mariages(enfant, famille) for enfant in enfants]
        }
        noeud["spouses"].append(union)

    return noeud

# Chargement
famille = Famille()
famille.charger_depuis_json("famille.json")
famille.charger_mariages_depuis_json("mariages.json")

# Identifier les racines (personnes sans parents)
racines = [p for p in famille.membres.values() if not p.parents]

# Construction du graphe hiérarchique
if len(racines) == 1:
    arbre_d3 = construire_noeud_avec_mariages(racines[0], famille)
elif len(racines) > 1:
    arbre_d3 = {
        "name": "Famille",
        "children": [construire_noeud_avec_mariages(r, famille) for r in racines]
    }
else:
    raise Exception("Aucune racine trouvée dans les membres de la famille.")

# Écriture dans le fichier JSON D3
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(arbre_d3, f, ensure_ascii=False, indent=4)

print("data.json généré avec les mariages et enfants par union.")
