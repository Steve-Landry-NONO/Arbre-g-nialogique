# fichier: arbre_genealogique.py

import json
import uuid

class Personne:
    def __init__(self, prenom, nom, date_naissance=None, sexe=None, profession=None, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.prenom = prenom
        self.nom = nom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.profession = profession
        self.parents = []  # liste d’IDs
        self.enfants = []  # liste d’IDs

    def to_dict(self):
        return {
            "id": self.id,
            "prenom": self.prenom,
            "nom": self.nom,
            "date_naissance": self.date_naissance,
            "sexe": self.sexe,
            "profession": self.profession,
            "parents": self.parents,
            "enfants": self.enfants,
        }

    @staticmethod
    def from_dict(data):
        p = Personne(
            prenom=data["prenom"],
            nom=data["nom"],
            date_naissance=data.get("date_naissance"),
            sexe=data.get("sexe"),
            profession=data.get("profession"),
            id=data.get("id")
        )
        p.parents = data.get("parents", [])
        p.enfants = data.get("enfants", [])
        return p

class Mariage:
    def __init__(self, id_mariage, conjoint_1, conjoint_2, enfants=None):
        self.id = id_mariage
        self.conjoint_1 = conjoint_1  # ID Personne
        self.conjoint_2 = conjoint_2  # ID Personne
        self.enfants = enfants if enfants else []  # Liste d’IDs Personne

    def to_dict(self):
        return {
            "id": self.id,
            "conjoint_1": self.conjoint_1,
            "conjoint_2": self.conjoint_2,
            "enfants": self.enfants
        }

    @staticmethod
    def from_dict(data):
        return Mariage(
            id_mariage=data["id"],
            conjoint_1=data["conjoint_1"],
            conjoint_2=data["conjoint_2"],
            enfants=data.get("enfants", [])
        )


class Famille:
    def __init__(self):
        self.membres = {}  # id: Personne
        self.mariages = {}  # id: Mariage

    def ajouter_personne(self, personne):
        self.membres[personne.id] = personne

    def charger_depuis_json(self, chemin_fichier):
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for p_data in data:
                p = Personne.from_dict(p_data)
                self.ajouter_personne(p)

    def charger_mariages_depuis_json(self, chemin_fichier):
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for m_data in data:
                mariage = Mariage.from_dict(m_data)
                self.mariages[mariage.id] = mariage

    def ajouter_mariage(self, mariage):
        self.mariages[mariage.id] = mariage

    def get_mariages_de(self, personne_id):
        return [m for m in self.mariages.values() if m.conjoint_1 == personne_id or m.conjoint_2 == personne_id]

    def sauvegarder_vers_json(self, chemin_fichier):
        data = [p.to_dict() for p in self.membres.values()]
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def afficher_arbre(self):
        def afficher_descendants(personne_id, niveau=0):
            personne = self.membres.get(personne_id)
            if personne:
                print("    " * niveau + f"{personne.prenom} {personne.nom} ({personne.date_naissance})")
                for enfant_id in personne.enfants:
                    afficher_descendants(enfant_id, niveau + 1)

        racines = [p for p in self.membres.values() if not p.parents]
        for racine in racines:
            afficher_descendants(racine.id)


if __name__ == "__main__":
    famille = Famille()
    famille.charger_depuis_json("famille.json")
    famille.charger_mariages_depuis_json("mariages.json")
    famille.afficher_arbre()
    # Pour ajouter une personne :
    # nouvelle = Personne("Nouveau", "Nom")
    # famille.ajouter_personne(nouvelle)
    # famille.sauvegarder_vers_json("famille.json")
