/* Au temps du Messager ﷺ : comportements du site. JavaScript natif, aucune bibliothèque. */
(function () {
  "use strict";
  var doc = document;
  var calme = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var L = window.LIENS || { tomes: {} };
  var contact = L.contact || "contact@autempsdumessager.com";

  function $(sel, racine) { return (racine || doc).querySelector(sel); }
  function $$(sel, racine) { return Array.prototype.slice.call((racine || doc).querySelectorAll(sel)); }
  function lienValide(u) { return typeof u === "string" && /^https:\/\/([a-z0-9-]+\.)*(amazon\.[a-z.]{2,6}|amzn\.(to|eu|com))\//i.test(u.trim()); }
  function el(nom, attrs, texte) {
    var n = doc.createElement(nom);
    for (var k in attrs) { if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]); }
    if (texte) n.textContent = texte;
    return n;
  }

  /* ------------------------------------------------------------ liens Amazon (réglés dans liens.js) */
  function liensDuTome(n) {
    var t = (L.tomes && L.tomes[n]) || {};
    return { relie: lienValide(t.relie) ? t.relie.trim() : "", broche: lienValide(t.broche) ? t.broche.trim() : "" };
  }
  function boutonAmazon(url, libelle) {
    return el("a", { "class": "bouton bouton-or", href: url, target: "_blank", rel: "noopener" }, libelle);
  }
  function prevenir(n) {
    var sujet = encodeURIComponent("Tome " + n + " : prévenez-moi");
    return el("a", { "class": "prevenir", href: "mailto:" + contact + "?subject=" + sujet }, "Être prévenu par courriel quand il sera en ligne");
  }
  $$("[data-achat]").forEach(function (boite) {
    var n = boite.getAttribute("data-achat");
    var style = boite.getAttribute("data-style") || "";
    var l = liensDuTome(n);
    boite.textContent = "";
    if (!l.relie && !l.broche) {
      boite.appendChild(el("span", { "class": "indispo" }, "Lien Amazon à venir"));
      if (style !== "compact") boite.appendChild(prevenir(n));
      return;
    }
    var ligne = el("div", { "class": "achat-ligne" });
    if (l.relie && l.broche && style !== "compact" && style !== "grand") {
      ligne.appendChild(boutonAmazon(l.relie, "Album relié sur Amazon"));
      var b = boutonAmazon(l.broche, "Broché sur Amazon");
      b.className = "bouton bouton-trait";
      ligne.appendChild(b);
    } else {
      ligne.appendChild(boutonAmazon(l.relie || l.broche, "Voir le tome " + n + " sur Amazon"));
    }
    boite.appendChild(ligne);
    if (style !== "compact") {
      boite.appendChild(el("p", { "class": "achat-note" }, l.relie ? "Album relié : 24,99 €. Même contenu en broché grand format." : "Broché grand format, 78 pages."));
    }
  });

  var t1 = liensDuTome(1);
  var lienT1 = t1.relie || t1.broche;
  var hero = $("[data-achat-hero]");
  if (hero && lienT1) {
    hero.textContent = "";
    hero.appendChild(boutonAmazon(lienT1, "Voir le tome 1 sur Amazon"));
    hero.appendChild(el("a", { "class": "bouton bouton-trait", href: "#feuilleter" }, "Feuilleter les premières pages"));
  }
  var collant = $("#collant");
  if (collant && lienT1) {
    collant.textContent = "";
    collant.appendChild(boutonAmazon(lienT1, "Tome 1 sur Amazon"));
  }
  $$("[data-contact]").forEach(function (a) { a.href = "mailto:" + contact; a.textContent = contact; });
  var annee = $("#annee");
  if (annee) annee.textContent = String(new Date().getFullYear());

  /* ------------------------------------------------------------ ouverture : de l'aube à la veillée */
  var ouverture = $(".ouverture");
  var barre = $("#barre");
  var enAttente = false;
  function mesurer() {
    enAttente = false;
    var y = window.scrollY || window.pageYOffset;
    if (barre) barre.classList.toggle("pleine", y > window.innerHeight * 0.6);
    if (ouverture && !calme) {
      var r = ouverture.getBoundingClientRect();
      var course = r.height - window.innerHeight;
      var p = course > 0 ? Math.min(1, Math.max(0, -r.top / course)) : 0;
      ouverture.style.setProperty("--p", p.toFixed(3));
    }
  }
  function auDefilement() { if (!enAttente) { enAttente = true; window.requestAnimationFrame(mesurer); } }
  window.addEventListener("scroll", auDefilement, { passive: true });
  window.addEventListener("resize", auDefilement, { passive: true });
  mesurer();

  /* ------------------------------------------------------------ apparitions, fonds des tomes, frise, bouton collant */
  var IO = "IntersectionObserver" in window;
  if (IO) {
    var voir = new IntersectionObserver(function (es) {
      es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("vu"); voir.unobserve(x.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    $$(".r").forEach(function (n, i) { n.style.transitionDelay = (i % 3) * 90 + "ms"; voir.observe(n); });

    var fonds = $$(".fond"), puces = $$("[data-frise]");
    var tomeIci = new IntersectionObserver(function (es) {
      es.forEach(function (x) {
        if (!x.isIntersecting) return;
        var n = x.target.getAttribute("data-tome");
        fonds.forEach(function (f) { f.classList.toggle("on", f.getAttribute("data-fond") === n); });
        puces.forEach(function (a) {
          var ici = a.getAttribute("data-frise") === n;
          a.classList.toggle("ici", ici);
          if (ici) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    $$(".tome").forEach(function (t) { tomeIci.observe(t); });

    var eventail = $(".eventail");
    if (eventail) {
      new IntersectionObserver(function (es, o) {
        es.forEach(function (x) { if (x.isIntersecting) { eventail.classList.add("ouvert"); o.disconnect(); } });
      }, { threshold: 0.35 }).observe(eventail);
    }

    if (collant) {
      collant.hidden = false;
      var cache = {};
      var majCollant = function () {
        var masque = cache.ouverture || cache.final || cache.pied || cache.extrait;
        collant.classList.toggle("visible", !masque);
      };
      var veille = new IntersectionObserver(function (es) {
        es.forEach(function (x) { cache[x.target.getAttribute("data-veille")] = x.isIntersecting; });
        majCollant();
      }, { threshold: 0.15 });
      [[".scene", "ouverture"], [".final", "final"], [".pied", "pied"], [".extrait", "extrait"]].forEach(function (c) {
        var n = $(c[0]);
        if (n) { n.setAttribute("data-veille", c[1]); cache[c[1]] = c[1] === "ouverture"; veille.observe(n); }
      });
    }
  } else {
    $$(".r").forEach(function (n) { n.classList.add("vu"); });
    var ev = $(".eventail");
    if (ev) ev.classList.add("ouvert");
  }

  /* ------------------------------------------------------------ l'album qui se feuillette */
  var album = $("#album");
  if (album) {
    var feuilles = $$(".feuille", album);
    var prec = $("#album-prec"), suiv = $("#album-suiv"), compteur = $("#album-compteur");
    var etat = 0;
    var libelles = ["Page 1 sur 4", "Pages 2 et 3 sur 4", "Page 4 sur 4"];
    var poser = function () {
      feuilles.forEach(function (f, i) { f.classList.toggle("tournee", i < etat); });
      album.setAttribute("data-etat", String(etat));
      prec.disabled = etat === 0;
      suiv.disabled = etat === feuilles.length;
      compteur.textContent = libelles[etat];
      // seules les pages visibles restent atteignables au clavier
      $$(".recto .page", album).forEach(function (b, i) { b.tabIndex = i >= etat && i === etat ? 0 : -1; });
      $$(".verso .page", album).forEach(function (b, i) { b.tabIndex = i === etat - 1 ? 0 : -1; });
    };
    prec.addEventListener("click", function () { if (etat > 0) { etat -= 1; poser(); } });
    suiv.addEventListener("click", function () { if (etat < feuilles.length) { etat += 1; poser(); } });
    album.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { suiv.click(); } else if (e.key === "ArrowLeft") { prec.click(); }
    });
    poser();
  }

  /* ------------------------------------------------------------ la loupe (image agrandie) */
  var loupe = $("#loupe");
  if (loupe && typeof loupe.showModal === "function") {
    var img = $("#loupe-img"), legende = $("#loupe-legende");
    doc.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("[data-loupe]") : null;
      if (!b) return;
      img.src = b.getAttribute("data-loupe");
      img.alt = b.getAttribute("data-legende") || "";
      legende.textContent = b.getAttribute("data-legende") || "";
      loupe.showModal();
      loupe.scrollTop = 0;
    });
    loupe.addEventListener("click", function (e) { if (e.target === loupe) loupe.close(); });
    loupe.addEventListener("close", function () { img.removeAttribute("src"); });
  }
})();
