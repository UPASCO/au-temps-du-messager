#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique index.html à partir de outils/textes.json et outils/tomes.json.

    python3 outils/construire.py

Le site reste un site statique : ce script n'est utile que pour changer les textes.
Les liens Amazon se règlent dans liens.js, sans relancer ce script.
"""
import html
import json
import os
import re
import struct

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
# Adresse publique du site (sert aux aperçus de partage). À changer quand le domaine est branché.
SITE = "https://upasco.github.io/au-temps-du-messager/"

T = json.load(open(os.path.join(ICI, "textes.json"), encoding="utf-8"))
D = json.load(open(os.path.join(ICI, "tomes.json"), encoding="utf-8"))
TOMES = D["tomes"]
TX = {t["num"]: t for t in T["tomes"]}


def e(s):
    """Texte vers HTML : échappement, espaces insécables à la française, signe ﷺ jamais orphelin."""
    s = html.escape(str(s), quote=False)
    s = s.replace(" ﷺ", "\u00a0ﷺ")
    s = re.sub(r" ([:;?!»])", "\u00a0\\1", s)
    s = s.replace("« ", "«\u00a0")
    s = re.sub(r"n° (\d)", "n°\u00a0\\1", s)
    s = re.sub(r"(\d) (€|×|pages|ans)", "\\1\u00a0\\2", s)
    return s


def a(s):
    """Texte vers valeur d'attribut."""
    return html.escape(str(s), quote=True)


def taille_webp(chemin):
    """Largeur et hauteur d'un fichier webp, sans bibliothèque."""
    with open(os.path.join(RACINE, chemin), "rb") as f:
        b = f.read(40)
    if b[12:16] == b"VP8 ":
        w, h = struct.unpack("<HH", b[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if b[12:16] == b"VP8L":
        n = struct.unpack("<I", b[21:25])[0]
        return (n & 0x3FFF) + 1, ((n >> 14) & 0x3FFF) + 1
    if b[12:16] == b"VP8X":
        return int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1
    raise ValueError(chemin)


ETOILE = ('<svg class="etoile" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
          '<path d="M12 1.2l3.2 3.1h4.5v4.5L22.8 12l-3.1 3.2v4.5h-4.5L12 22.8l-3.2-3.1H4.3v-4.5L1.2 12l3.1-3.2V4.3h4.5z"/></svg>')

H = T["hero"]
out = []
w = out.append

# ------------------------------------------------------------------ en-tête du document
ld = {
    "@context": "https://schema.org", "@type": "BookSeries", "name": "Au temps du Messager",
    "url": SITE, "inLanguage": "fr", "genre": "Bande dessinée historique",
    "description": T["seo"]["description"],
    "author": {"@type": "Person", "name": "Nadir Echaara"},
    "hasPart": [{"@type": "Book", "position": t["num"], "name": t["titre"], "bookFormat": "https://schema.org/Hardcover",
                 "numberOfPages": 80 if t["num"] == 7 else 78, "inLanguage": "fr", "author": {"@type": "Person", "name": "Nadir Echaara"}} for t in TOMES],
}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["r"]}} for q in T["faq"]]}

w(f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{a(T['seo']['title'])}</title>
<meta name="description" content="{a(T['seo']['description'])}">
<meta name="author" content="Nadir Echaara">
<meta name="theme-color" content="#33130A">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Au temps du Messager ﷺ">
<meta property="og:title" content="Au temps du Messager ﷺ : la vie du Prophète ﷺ en bande dessinée">
<meta property="og:description" content="Sans jamais le dessiner. D'après les sources. Sept tomes à lire en famille.">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}assets/partage.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Couverture du tome 1, L'Enfant de La Mecque">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/icone.svg" type="image/svg+xml">
<link rel="preload" href="assets/polices/bigshoulders-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/polices/lora-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/art/tome-1.webp" as="image" fetchpriority="high">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="evitement" href="#contenu">Aller au contenu</a>

<header class="barre" id="barre">
  <a class="marque" href="#accueil">Au temps du Messager&nbsp;ﷺ</a>
  <nav aria-label="Sections de la page">
    <a href="#feuilleter">Feuilleter</a>
    <a href="#tomes">Les sept tomes</a>
    <a href="#respect">Nos règles</a>
    <a href="#questions">Questions</a>
  </nav>
</header>

<main id="contenu">
""")

# ------------------------------------------------------------------ ouverture
w(f"""<section class="ouverture" id="accueil" aria-labelledby="titre-site">
  <div class="scene">
    <img class="ciel ciel-1" src="assets/art/tome-1.webp" width="1024" height="1536" alt="" fetchpriority="high" decoding="async">
    <img class="ciel ciel-2" src="assets/art/tome-2.webp" width="1024" height="1536" alt="" loading="lazy" decoding="async">
    <div class="etoiles" aria-hidden="true"></div>
    <div class="voile" aria-hidden="true"></div>
    <div class="ouverture-texte">
      <p class="surtitre">{e(H['surtitre'])}</p>
      <h1 id="titre-site">Au temps du Messager&nbsp;<span class="signe">ﷺ</span></h1>
      <p class="promesse-couv">La vie du Prophète&nbsp;ﷺ en bande dessinée. <span>Sans jamais le dessiner.</span> <span>D'après les sources.</span></p>
      <p class="accroche">{e(H['sous_texte'])}</p>
      <div class="actions" data-achat-hero>
        <a class="bouton bouton-or" href="#feuilleter">{e(H['bouton_secondaire'])}</a>
        <a class="bouton bouton-trait" href="#tomes">Voir les sept tomes</a>
      </div>
    </div>
    <a class="livre-hero" href="#tome-1" aria-label="Le tome 1, L'Enfant de La Mecque">
      <img src="assets/couvertures/tome-1.webp" width="760" height="1075" alt="Couverture du tome 1, L'Enfant de La Mecque : {a(TOMES[0]['visuel'])}." decoding="async">
    </a>
    <p class="note-main descendre" aria-hidden="true">la nuit tombe, grand-père raconte…</p>
  </div>
</section>
""")

# ------------------------------------------------------------------ la promesse
w('<section class="promesse" aria-label="Ce que promet la collection">\n  <ol class="trois">\n')
for p in T["promesse"]:
    w(f'    <li class="r">{ETOILE}<h2>{e(p["titre"])}</h2><p>{e(p["texte"])}</p></li>\n')
w('  </ol>\n</section>\n\n')

# ------------------------------------------------------------------ l'extrait à feuilleter
EX = D["extrait"]
tailles = [taille_webp(x["img"]) for x in EX]
alts = ["Tome 1, première page : La Mecque vers 610, la terrasse de grand-père Jamal.",
        "Tome 1, deuxième page.", "Tome 1, troisième page.", "Tome 1, quatrième page."]


def page_img(i, cls=""):
    x = EX[i]
    ww, hh = tailles[i]
    return (f'<button class="page {cls}" type="button" data-loupe="{a(x["img"])}" data-legende="{a(alts[i])}" aria-label="Agrandir : {a(alts[i])}">'
            f'<img src="{a(x["img"])}" width="{ww}" height="{hh}" alt="{a(alts[i])}" loading="lazy" decoding="async"></button>')


fin_extrait = f"""<div class="fin-extrait">
        {ETOILE}
        <p class="note-main">Et l'histoire commence…</p>
        <p>La suite est dans le tome 1, <strong>L'Enfant de La Mecque</strong> : 51 pages de bande dessinée et un dossier pour en parler en famille.</p>
        <div data-achat="1" data-style="compact"><span class="indispo">Lien Amazon à venir</span></div>
      </div>"""

w(f"""<section class="extrait" id="feuilleter" aria-labelledby="titre-extrait">
  <div class="tetiere r">
    <h2 id="titre-extrait">Ouvrez le tome 1</h2>
    <p>Les quatre premières pages, comme dans l'album. Touchez une page pour l'agrandir.</p>
  </div>

  <div class="album" id="album" data-etat="0" aria-roledescription="album à feuilleter">
    <div class="album-fond" aria-hidden="true"></div>
    <div class="album-fin">{fin_extrait}</div>
    <div class="feuille" data-feuille="0">
      <div class="recto">{page_img(0)}</div>
      <div class="verso">{page_img(1)}</div>
    </div>
    <div class="feuille" data-feuille="1">
      <div class="recto">{page_img(2)}</div>
      <div class="verso">{page_img(3)}</div>
    </div>
  </div>
  <div class="album-commandes">
    <button type="button" class="tourner" id="album-prec" disabled>Page précédente</button>
    <p class="compteur" id="album-compteur" aria-live="polite">Page 1 sur 4</p>
    <button type="button" class="tourner" id="album-suiv">Page suivante</button>
  </div>

  <div class="defile" tabindex="0" aria-label="Les quatre premières pages du tome 1, à faire défiler">
    {page_img(0)}
    {page_img(1)}
    {page_img(2)}
    {page_img(3)}
    <div class="defile-fin">{fin_extrait}</div>
  </div>
  <p class="note-main glisser" aria-hidden="true">fais glisser pour tourner les pages</p>
</section>

""")

# ------------------------------------------------------------------ les trois témoins
TE = T["temoins"]
w(f"""<section class="temoins" id="temoins" aria-labelledby="titre-temoins">
  <div class="temoins-texte">
    <h2 id="titre-temoins" class="r">{e(T['serie']['titre'])}</h2>
""")
for p in T["serie"]["paragraphes"]:
    w(f'    <p class="r">{e(p)}</p>\n')
w(f"""  </div>
  <div class="trio">
    <h3 class="r">{e(TE['titre'])}</h3>
    <p class="trio-intro r">{e(TE['intro'])}</p>
    <ul>
      <li class="r"><img src="assets/personnages/jamal.webp" width="508" height="485" alt="Grand-père Jamal, turban blanc et barbe blanche." loading="lazy" decoding="async"><p><strong>Jamal</strong> {e(TE['jamal'])}</p></li>
      <li class="r"><img src="assets/personnages/sami.webp" width="245" height="245" alt="Sami, turban bleu." loading="lazy" decoding="async"><p><strong>Sami</strong> {e(TE['sami'])}</p></li>
      <li class="r"><img src="assets/personnages/leyna.webp" width="245" height="245" alt="Leyna, voile vert." loading="lazy" decoding="async"><p><strong>Leyna</strong> {e(TE['leyna'])}</p></li>
    </ul>
  </div>
</section>

""")

# ------------------------------------------------------------------ les sept tomes
w('<section class="voyage" id="tomes" aria-labelledby="titre-tomes">\n  <div class="fonds" aria-hidden="true"><div class="fonds-colle">\n')
for t in TOMES:
    w(f'    <div class="fond{" on" if t["num"] == 1 else ""}" data-fond="{t["num"]}" style="--c:{t["couleur"]};--s:{t["sombre"]}"></div>\n')
w('  </div></div>\n')
w("""  <div class="voyage-tete">
    <h2 id="titre-tomes">Les sept tomes</h2>
    <p>De l'année de l'Éléphant, vers 570, au pèlerinage d'adieu, en 632. Commencez par le tome 1.</p>
  </div>
  <nav class="frise" aria-label="Aller à un tome">
    <ol>
""")
for t in TOMES:
    w(f'      <li><a href="#tome-{t["num"]}" data-frise="{t["num"]}" style="--c:{t["couleur"]}"><span class="n">{t["num"]}</span><span class="per">{e(t["periode"])}</span></a></li>\n')
w('    </ol>\n  </nav>\n\n')

for t in TOMES:
    n = t["num"]
    x = TX[n]
    w(f"""  <article class="tome" id="tome-{n}" data-tome="{n}" style="--c:{t['couleur']};--s:{t['sombre']}" aria-labelledby="titre-tome-{n}">
    <div class="tome-couv">
      <button class="couv" type="button" data-loupe="assets/couvertures/tome-{n}.webp" data-legende="{a('Tome ' + str(n) + ', ' + t['titre'])}" aria-label="Agrandir la couverture du tome {n}">
        <img src="assets/couvertures/tome-{n}.webp" width="760" height="1075" alt="Couverture du tome {n}, {a(t['titre'])} : {a(t['visuel'])}." loading="lazy" decoding="async">
      </button>
    </div>
    <div class="tome-texte">
      <p class="tome-rep"><span class="tome-num">Tome {n}</span> <span class="tome-per">{e(t['periode'])}</span></p>
      <h3 id="titre-tome-{n}">{e(t['titre'])}</h3>
      <p class="tome-accroche">{e(x['accroche'])}</p>
      <p class="tome-resume">{e(x['resume'])}</p>
      <dl class="tome-reperes">
        <div><dt>Ce que l'on découvre du Prophète&nbsp;ﷺ</dt><dd>{e(x['qualite'])}</dd></div>
        <div><dt>Le moment fort</dt><dd>{e(x['moment'])}</dd></div>
      </dl>
      <ul class="tome-pages" aria-label="Trois pages du tome {n}">
""")
    for p in t["pages"]:
        leg = f"Tome {n}, {t['titre']}, page {p['page']}"
        mini = p["img"].replace("assets/planches/", "assets/planches/mini/")
        mw, mh = taille_webp(mini)
        w(f'        <li><button type="button" data-loupe="{a(p["img"])}" data-legende="{a(leg)}" aria-label="Agrandir : {a(leg)}"><img src="{a(mini)}" width="{mw}" height="{mh}" alt="{a(leg)}." loading="lazy" decoding="async"></button></li>\n')
    w(f"""      </ul>
      <div class="tome-achat" data-achat="{n}"><span class="indispo">Lien Amazon à venir</span></div>
    </div>
  </article>

""")
w('</section>\n\n')

# ------------------------------------------------------------------ raconter avec respect
R_ = T["respect"]
w(f"""<section class="respect" id="respect" aria-labelledby="titre-respect">
  <div class="respect-tete">
    {ETOILE}
    <h2 id="titre-respect">{e(R_['titre'])}</h2>
    <p>{e(R_['intro'])}</p>
  </div>
  <ol class="regles">
""")
for p in R_["points"]:
    w(f'    <li class="r"><h3>{e(p["titre"])}</h3><p>{e(p["texte"])}</p></li>\n')
w('  </ol>\n</section>\n\n')

# ------------------------------------------------------------------ les sources
S_ = T["sources"]
w(f"""<section class="sources" id="sources" aria-labelledby="titre-sources">
  <div class="tetiere r">
    <h2 id="titre-sources">{e(S_['titre'])}</h2>
    <p>{e(S_['intro'])}</p>
  </div>
  <ol class="siecles">
""")
for s in S_["etapes"]:
    w(f'    <li class="r"><p class="quand">{e(s["date"])}</p><h3>{e(s["nom"])}</h3><p>{e(s["role"])}</p></li>\n')
w(f'  </ol>\n  <p class="sources-note r">{e(S_["note"])}</p>\n</section>\n\n')

# ------------------------------------------------------------------ le dossier, la famille, l'auteur
DO, FA, AU = T["dossier"], T["famille"], T["auteur"]
w(f"""<section class="dossier" aria-labelledby="titre-dossier">
  <div class="dossier-col">
    <h2 id="titre-dossier" class="r">{e(DO['titre'])}</h2>
    <p class="r">{e(DO['intro'])}</p>
    <ul class="dossier-liste">
""")
for x in DO["elements"]:
    w(f'      <li class="r">{ETOILE}<span>{e(x)}</span></li>\n')
w(f"""    </ul>
  </div>
  <div class="dossier-col famille">
    <h2 class="r">{e(FA['titre'])}</h2>
    <p class="r">{e(FA['texte'])}</p>
    <figure class="mot-auteur r">
      <blockquote><p>{e(AU['texte'])}</p></blockquote>
      <figcaption>{e(AU['signature'])}</figcaption>
    </figure>
  </div>
</section>

""")

# ------------------------------------------------------------------ questions
w('<section class="questions" id="questions" aria-labelledby="titre-questions">\n  <h2 id="titre-questions" class="r">Les questions des parents</h2>\n  <div class="faq">\n')
for q in T["faq"]:
    rep = e(q["r"]).replace("contact@autempsdumessager.com", '<a href="mailto:contact@autempsdumessager.com" data-contact>contact@autempsdumessager.com</a>')
    w(f'    <details><summary>{e(q["q"])}</summary><p>{rep}</p></details>\n')
w('  </div>\n</section>\n\n')

# ------------------------------------------------------------------ l'appel final
FI = T["final"]
w(f"""<section class="final" aria-labelledby="titre-final">
  <ul class="eventail" aria-label="Les sept couvertures">
""")
for t in TOMES:
    n = t["num"]
    w(f'    <li style="--i:{n - 4}"><a href="#tome-{n}" aria-label="Tome {n}, {a(t["titre"])}"><img src="assets/couvertures/tome-{n}.webp" width="760" height="1075" alt="" loading="lazy" decoding="async"></a></li>\n')
w(f"""  </ul>
  <h2 id="titre-final">{e(FI['titre']).replace('grand-père Jamal', '<span class="nb">grand-père Jamal</span>')}</h2>
  <p>{e(FI['texte'])}</p>
  <div class="final-achat" data-achat="1" data-style="grand"><span class="indispo">Lien Amazon à venir</span></div>
</section>
</main>

<footer class="pied">
  <p class="pied-marque">Au temps du Messager&nbsp;ﷺ</p>
  <p>{e(T['pied']['mention'])}</p>
  <p>{e(T['pied']['signe'])}</p>
  <p>Pour nous écrire : <a href="mailto:contact@autempsdumessager.com" data-contact>contact@autempsdumessager.com</a></p>
  <p class="pied-legal">Site édité par Nadir Echaara. Hébergement : GitHub Pages. Ce site ne dépose aucun cookie et ne mesure pas votre visite. © <span id="annee">2026</span> Nadir Echaara, tous droits réservés. Amazon est une marque d'Amazon.com, Inc. ou de ses filiales.</p>
</footer>

<div class="collant" id="collant" hidden>
  <a class="bouton bouton-or" href="#feuilleter">Feuilleter le tome 1</a>
</div>

<dialog class="loupe" id="loupe" aria-label="Image agrandie">
  <form method="dialog"><button class="fermer" aria-label="Fermer">Fermer</button></form>
  <img id="loupe-img" alt="">
  <p id="loupe-legende"></p>
</dialog>

<script src="liens.js"></script>
<script src="script.js"></script>
</body>
</html>
""")

page = "".join(out)


def apostrophes(doc):
    """Apostrophes typographiques dans le texte visible (ni dans les balises, ni dans les scripts)."""
    morceaux = re.split(r"(<script.*?</script>|<[^>]+>)", doc, flags=re.S)
    return "".join(m if m.startswith("<") else m.replace("'", "’") for m in morceaux)


page = apostrophes(page)

# ------------------------------------------------------------------ contrôles avant écriture
texte = re.sub(r"<script.*?</script>", " ", page, flags=re.S)
texte_nu = html.unescape(re.sub(r"<[^>]+>", " ", texte))
fautes = []
for m in re.finditer(r"(Prophète|Muhammad|Messager de Dieu|al-Amîn)(?![\s\u00a0]*ﷺ)", html.unescape(texte)):
    ctx = html.unescape(texte)[max(0, m.start() - 40):m.end() + 25].replace("\n", " ")
    if "Son Messager" in ctx or "du Messager\u00a0" in ctx or "du Messager&" in ctx:
        continue
    fautes.append("sans ﷺ : " + ctx)
for mot in ("—", "–", "validé", "approuvé", "certifié", "best-seller", "planche", "cartouche", "intelligence artificielle", "dès 8", " IA "):
    if mot in texte_nu:
        fautes.append("mot interdit : " + mot)
if fautes:
    print("\n".join(fautes))
    raise SystemExit("index.html non écrit : corriger outils/textes.json")
open(os.path.join(RACINE, "index.html"), "w", encoding="utf-8").write(page)
print("index.html écrit :", len(page), "caractères,", len(TOMES), "tomes")
