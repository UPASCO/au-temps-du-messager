# Au temps du messager : site web

Site vitrine de la série de tomes « Au temps du messager ».

Site statique (HTML + CSS), sans outil de compilation : ouvrir `index.html` dans un navigateur suffit.

## Modifier le contenu

- Les textes marqués `[À COMPLÉTER]` sont provisoires.
- Chaque tome est un bloc `<article class="tome">` dans `index.html`.
- Les couvertures vont dans `assets/couvertures/` (ex. `tome-1.jpg`) et remplacent le bloc `.couverture` par `<div class="couverture"><img src="assets/couvertures/tome-1.jpg" alt="Couverture du tome 1"></div>`.

## Liens Amazon

Chercher `#LIEN-AMAZON-TOME-` dans `index.html` et remplacer chaque valeur par le vrai lien du tome.
Si ce sont des liens affiliés Amazon Partenaires, décommenter la mention légale en bas de page.

## Suppositions provisoires

- Style « récit d'époque » (tons parchemin, police à empattements), à ajuster.
- Trois tomes affichés en exemple.
- Aucune mise en ligne pour l'instant.
