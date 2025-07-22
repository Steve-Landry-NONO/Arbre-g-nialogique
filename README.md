Arbre Généalogique Interactif avec Mariages Polygamiques

Ce projet permet de visualiser dynamiquement un arbre généalogique complexe avec gestion des **mariages explicites** (y compris polygamie), en utilisant **D3.js**.

##  Fonctionnalités

- Représentation des **personnes** (sexe H/F, nom, profession...)
- Représentation des **nœuds de mariage** distincts
- Les **enfants sont reliés à leur union**, pas directement aux parents
- Couleurs différenciées :
  -  Homme (bleu)
  -  Femme (rouge)
  -  Mariage (gris)
- Affichage interactif : glisser-déposer, survol, zoom possible

##  Structure des données (`data.json`)

```json
{
  "nodes": [
    { "id": "H1", "type": "personne", "name": "Jean", "sexe": "H" },
    { "id": "F1", "type": "personne", "name": "Claire", "sexe": "F" },
    { "id": "M1", "type": "mariage" },
    { "id": "E1", "type": "personne", "name": "Enfant 1", "sexe": "H" }
  ],
  "links": [
    { "source": "H1", "target": "M1" },
    { "source": "F1", "target": "M1" },
    { "source": "M1", "target": "E1" }
  ]
}
```

##  Technologies utilisées
- HTML/CSS
- [D3.js](https://d3js.org/) (v7)
- JavaScript vanilla

##  Lancer le projet

1. Cloner le repo
2. Ouvrir `index.html` dans ton navigateur

```bash
python3 -m http.server
```
Ou ouvrir manuellement le fichier `index.html`

##  Auteurs & Crédits
- Conception : @Steve-Landry-NONO
- Visualisation : D3.js + design sur mesure

## Améliorations possibles
- Ajout de dates de mariage et lieux
- Vue centrée sur une branche familiale
- Filtres par génération, nom ou sexe

---

 Projet personnel pour cartographier fidèlement une grande famille (200+ membres, polygamie comprise).
