# fichier : app.py

import streamlit as st
from arbre_genealogique import Famille
import json
import networkx as nx
from pyvis.network import Network
import tempfile
import os

# Chargement des données
famille = Famille()
famille.charger_depuis_json("famille.json")

# Création du graphe orienté
G = nx.DiGraph()
labels = {}

for p in famille.membres.values():
    label = f"{p.prenom} {p.nom}\n({p.date_naissance})"
    labels[p.id] = label
    G.add_node(p.id, label=label, title=f"{p.prenom} {p.nom}<br>Date de naissance: {p.date_naissance}<br>Profession: {p.profession}")
    for enfant_id in p.enfants:
        G.add_edge(p.id, enfant_id)

# Utilisation de Pyvis pour créer une visualisation interactive
net = Network(height="600px", width="100%", directed=True)
net.from_nx(G)

# Options visuelles (centrage, physique, interaction)
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

# Sauvegarder le graphe HTML temporairement
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    net.save_graph(f.name)
    tmp_path = f.name

# Afficher dans Streamlit
st.set_page_config(page_title="Arbre Généalogique", layout="wide")
st.title(" Arbre Généalogique de la Famille")
st.markdown("Cliquez sur un individu pour voir ses enfants. Survolez pour voir les détails.")

with open(tmp_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

st.components.v1.html(html_content, height=650, scrolling=True)

# Nettoyage du fichier temporaire
os.unlink(tmp_path)
