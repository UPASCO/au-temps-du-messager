# Au temps du Messager ﷺ : le site de la collection

Site vitrine de la collection de sept bandes dessinées « Au temps du Messager ﷺ » de Nadir Echaara.
Son rôle : donner envie, faire feuilleter le tome 1, et envoyer le visiteur vers les pages Amazon.

Site statique (un `index.html`, un `style.css`, un `script.js`), sans bibliothèque, sans cookie, sans traceur.
Les polices et les images sont hébergées dans le dépôt : le site n'appelle aucun service extérieur.

## Mettre les liens Amazon

Un seul fichier à modifier : **`liens.js`**.

```js
tomes: {
  1: { broche: "https://www.amazon.fr/dp/XXXXXXXXXX", relie: "https://www.amazon.fr/dp/YYYYYYYYYY" },
  2: { broche: "", relie: "" },
```

- Tant qu'un lien est vide, le tome affiche « Lien Amazon à venir » et propose d'être prévenu par courriel.
- Dès que le lien du tome 1 est rempli, le bouton d'ouverture et le bouton collant du téléphone deviennent « Voir le tome 1 sur Amazon ».
- Seules les adresses `https://` d'Amazon sont acceptées (amazon.fr, amazon.com.be, amzn.eu…).
- L'adresse de contact se change au même endroit (`contact`).
- Si les liens sont des liens affiliés (Amazon Partenaires), ajouter dans le pied de page de `outils/construire.py` la mention :
  « En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. »

## Mettre le site en ligne (GitHub Pages)

1. Dans GitHub : **Settings**, puis **Pages**.
2. « Build and deployment » : source **Deploy from a branch**, branche **main**, dossier **/ (root)**, puis **Save**.
3. Après une à deux minutes, le site est à l'adresse `https://upasco.github.io/au-temps-du-messager/`.

Pour brancher le domaine `www.autempsdumessager.com` (une fois réservé) : même écran, champ « Custom domain »,
puis chez le vendeur du domaine un enregistrement `CNAME` de `www` vers `upasco.github.io`.
Changer ensuite la ligne `SITE = "…"` en haut de `outils/construire.py` et relancer le script, pour que les aperçus de partage
(WhatsApp, Instagram, Facebook) pointent vers la bonne adresse.

## Changer un texte

Les textes sont dans `outils/textes.json`, les données des tomes dans `outils/tomes.json`.

```
python3 outils/construire.py
```

Le script refait `index.html` et refuse d'écrire la page si une règle est oubliée : une mention du Prophète ﷺ sans le
signe ﷺ, un tiret long, ou un mot interdit.

## Les règles que le site respecte, comme les livres

- Le Prophète ﷺ n'est jamais dessiné : ni silhouette, ni main, ni ombre, ni objet, ni lumière à sa place. Sa famille proche, les
  autres prophètes et les anges ne sont pas dessinés ; les compagnons, seulement de dos.
- Le signe ﷺ suit chaque mention du Prophète ﷺ, dans les textes, les titres et les descriptions d'images.
- Aucune parole inventée ; les références (al-Bukhârî n° 3445, n° 109, n° 4770) viennent des livres.
- Rien n'affirme qu'un savant ou une institution a relu ou approuvé la collection.
- Aucun avis, aucune note, aucun chiffre de ventes ; aucune mention d'âge de lecture.
- Les animations ne touchent jamais le signe ﷺ, un verset ou une formule ; pas de halo, pas de son, pas d'effet sur les scènes de bataille.
- Les pages montrées en exemple évitent celle de la grotte de Hirâ' et les charges de cavalerie.

## Ce qu'il y a dans la page

1. Ouverture : le ciel passe de l'aube du tome 1 à la nuit étoilée du tome 2 pendant le défilement.
2. La promesse en trois points.
3. « Ouvrez le tome 1 » : les quatre premières pages, en album qui se feuillette (grand écran) ou à faire glisser (téléphone).
4. Les sept tomes et les trois témoins inventés.
5. La frise des sept tomes : le fond prend la couleur de chaque couverture ; trois pages à agrandir par tome ; boutons Amazon.
6. « Raconter avec respect » : les règles et les notions clés.
7. Les sources, dans l'ordre des siècles.
8. Le dossier de fin de volume, « À lire ensemble », le mot de l'auteur.
9. Les questions des parents.
10. L'éventail des sept couvertures et l'appel final.

Le site reste lisible sans JavaScript, au clavier, et sans animation pour les personnes qui les ont désactivées.

## Fichiers

```
index.html            la page (fabriquée par outils/construire.py)
style.css, script.js  la mise en forme et les comportements
liens.js              les liens Amazon et l'adresse de contact
assets/couvertures    les sept premières de couverture
assets/art            les illustrations de l'ouverture (tomes 1 et 2)
assets/planches       les pages montrées (mini/ : vignettes)
assets/personnages    Jamal, Sami, Leyna
assets/polices        Big Shoulders, Lora, Caveat (licence SIL OFL)
assets/partage.jpg    l'image des aperçus de partage
outils/               textes, données et script de fabrication
```

© Nadir Echaara. Textes et images : tous droits réservés.
