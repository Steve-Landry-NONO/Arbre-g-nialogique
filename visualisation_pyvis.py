# fichier : visualisation_pyvis.py

from arbre_genealogique import Famille
import networkx as nx
from pyvis.network import Network
import webbrowser
import os

# Charger la famille
famille = Famille()
famille.charger_depuis_json("famille.json")

# Créer un graphe orienté
G = nx.DiGraph()

# Ajouter les noeuds et les arêtes
for personne in famille.membres.values():
    label = f"{personne.prenom} {personne.nom}\n({personne.date_naissance})"
    G.add_node(personne.id, label=label, title=f"{personne.prenom} {personne.nom}<br>Date de naissance: {personne.date_naissance}<br>Profession: {personne.profession}")
    for enfant_id in personne.enfants:
        G.add_edge(personne.id, enfant_id)

# Créer la visualisation avec Pyvis
net = Network(height="750px", width="100%", directed=True)
net.from_nx(G)

# Options d'affichage (mode hiérarchique, interaction, etc.)
net.set_options('''
var options = {
  "nodes": {
    "font": {
      "size": 16
    },
    "shape": "box",
    "margin": 10
  },
  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      }
    }
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "sortMethod": "directed"
    }
  },
  "interaction": {
    "hover": true
  },
  "physics": {
    "enabled": false
  }
}
''')

# Sauvegarder le fichier HTML
html_path = "arbre_genealogique.html"
net.save_graph(html_path)
print(f"Visualisation générée : {html_path}")

# Ouvrir dans le navigateur
webbrowser.open('file://' + os.path.realpath(html_path))