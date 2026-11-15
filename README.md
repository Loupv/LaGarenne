# Carnet de faune — La Garenne

Petite webapp qui recense les animaux du parc animalier La Garenne (Le Vaud, VD), pour le public et les naturalistes :

- catalogue des espèces du parc, par secteur ;
- une fiche ludique par espèce (39), avec un mode « Je découvre » et un mode naturaliste, des fun facts et un mini-quiz ;
- plan du parc avec les numéros du plan officiel 2023 et sa légende ;
- « Nos pensionnaires » : les animaux du parc, un par un (nom, histoire, caractère) ;
- « Espèces en chiffres » : poids, taille, espérance de vie dans la nature et en captivité ;
- un quiz infini (choix simple et réponses multiples) sur les pensionnaires et les espèces.

Site statique, sans build : `index.html` + `dc-runtime.js` + `assets/`. Pour le voir en local :

```bash
python3 -m http.server 8765
```

## Modifier le site

La source est le canevas Claude Design `source/canvas/project/Main.dc.html` (données, textes et logique). `index.html` en est l'export :

```bash
python3 source/build.py
```

Les photos sources sont dans `source/photos/`. Le dossier `ressources/` (documents du parc) reste local et n'est jamais publié.

Photos © La Garenne, utilisées avec son accord.
