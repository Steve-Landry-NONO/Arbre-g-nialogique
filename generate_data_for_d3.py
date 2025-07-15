# fichier : generate_data_for_d3.py

import json
from arbre_genealogique import Famille

# Fonction récursive pour convertir un membre en format D3
def construire_noeud(personne, famille):
    noeud = {
        "name": f"{personne.prenom} {personne.nom}",
        "date": personne.date_naissance,
        "profession": personne.profession
    }
    enfants = [famille.membres[eid] for eid in personne.enfants if eid in famille.membres]
    if enfants:
        noeud["children"] = [construire_noeud(enfant, famille) for enfant in enfants]
    return noeud

# Charger les données existantes
famille = Famille()
famille.charger_depuis_json("famille.json")

# Trouver la ou les racines (personnes sans parents)
racines = [p for p in famille.membres.values() if not p.parents]

# Générer les arbres hiérarchiques (généralement une seule racine)
if len(racines) == 1:
    arbre_d3 = construire_noeud(racines[0], famille)
elif len(racines) > 1:
    arbre_d3 = {
        "name": "Famille",
        "children": [construire_noeud(r, famille) for r in racines]
    }
else:
    raise Exception("Aucune racine trouvée dans l'arbre !")

# Sauvegarder au format D3
with open("visualisation_d3/data.json", "w", encoding="utf-8") as f:
    json.dump(arbre_d3, f, ensure_ascii=False, indent=4)

print(" data.json pour D3.js généré avec succès.")
