#!/usr/bin/env python3
"""
Generator für www.dari-gericht.de
-------------------------------------------------
Alle Seiten werden aus diesem Skript erzeugt, damit Kopf-/Fußzeile,
Kontaktdaten und SEO-Angaben überall identisch sind.

Ändern Sie die Werte im Block KONFIGURATION und führen Sie aus:
    python build.py
(Sie können die HTML-Dateien aber auch direkt in VS Code bearbeiten.)
"""
import json, os, datetime

# ============================ KONFIGURATION ============================
BASE      = "https://www.dari-gericht.de"
NAME      = "Benjamin A. Sadr"
BRAND     = "Dari-Gerichtsübersetzung"
TAGLINE   = "Beglaubigte Übersetzungen für die Justiz"
COURT     = "Landgericht Stuttgart"
PHONE     = "+49 156 78304182"
PHONE_TEL = "+4915678304182"
FAX       = "+49 201 85974647"
EMAIL     = "auftrag@dari-gericht.de"
STREET    = "Emsdettener Straße 10"
CO        = "c/o POSTFLEX PFX-532-971"
ZIP       = "48268"
CITY      = "Greven"
HOURS     = "Mo–Fr 8–20 Uhr, Eilsachen nach Absprache auch am Wochenende"
EXPRESS_PAGES = "ca. 15"   # Seitenumfang, der regelmäßig binnen 24 h möglich ist
TODAY     = datetime.date.today().isoformat()
# ======================================================================

OUT = os.path.dirname(os.path.abspath(__file__))

DOCS = []  # wird unten befüllt

NAV = [
    ("index.html", "Start"),
    ("DOCS", "Dokumente"),
    ("express-uebersetzung-24h.html", "Express 24 h"),
    ("beglaubigte-uebersetzung.html", "Beglaubigung"),
    ("honorar-jveg.html", "Honorar"),
    ("dari-uebersetzer-fuer-uebersetzungsbueros.html", "Für Übersetzungsbüros"),
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": BASE + "/#organisation",
        "name": f"{BRAND} – {NAME}",
        "alternateName": "Dari Übersetzer für Gerichte und Staatsanwaltschaften",
        "description": "Beglaubigte Übersetzungen gerichtlicher und staatsanwaltschaftlicher Schriftstücke aus dem Deutschen ins Dari. Express-Bearbeitung binnen 24 Stunden, Abrechnung nach § 11 JVEG.",
        "url": BASE + "/",
        "logo": BASE + "/images/favicon.svg",
        "image": BASE + "/images/og-image.png",
        "telephone": PHONE,
        "faxNumber": FAX,
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f"{CO}, {STREET}",
            "postalCode": ZIP,
            "addressLocality": CITY,
            "addressCountry": "DE",
        },
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "knowsLanguage": ["de", "prs"],
        "founder": {"@id": BASE + "/#person"},
        "priceRange": "nach JVEG",
        "openingHours": "Mo-Fr 08:00-20:00",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Übersetzungen ins Dari für die Justiz",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": d["name"] + " – Übersetzung ins Dari", "url": f"{BASE}/{d['slug']}"}}
                for d in DOCS
            ],
        },
    }


def person_ld():
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": BASE + "/#person",
        "name": NAME,
        "jobTitle": "Öffentlich bestellter und allgemein beeidigter Übersetzer für die Sprache Dari",
        "sameAs": ["https://www.justiz-dolmetscher.de/Recherche/de/Person/Details/61461"],
        "knowsLanguage": ["de", "prs"],
        "worksFor": {"@id": BASE + "/#organisation"},
        "url": BASE + "/",
    }


def breadcrumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{BASE}/{u}" if u != "index.html" else BASE + "/"}
            for i, (u, n) in enumerate(items)
        ],
    }


def faq_ld(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }


def service_ld(d):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Beglaubigte Übersetzung: {d['name']} ins Dari",
        "serviceType": "Beglaubigte juristische Übersetzung Deutsch–Dari",
        "description": d["desc"],
        "provider": {"@id": BASE + "/#organisation"},
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "audience": {"@type": "Audience", "audienceType": "Gerichte, Staatsanwaltschaften, Behörden, Rechtsanwälte"},
        "url": f"{BASE}/{d['slug']}",
        "offers": {
            "@type": "Offer",
            "priceCurrency": "EUR",
            "description": "Abrechnung nach § 11 JVEG je angefangene 55 Anschläge; Bearbeitung in der Regel binnen 24 Stunden.",
        },
    }


def header(active):
    items = []
    for href, label in NAV:
        if href == "DOCS":
            ac = ' aria-current="page"'
            sub = "".join(
                f'<li><a href="{d["slug"]}"{ac if active == d["slug"] else ""}>{d["name"]}</a></li>'
                for d in DOCS
            )
            items.append(
                f'<li class="has-sub"><button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-dokumente">Dokumente</button>'
                f'<ul class="subnav" id="sub-dokumente">{sub}</ul></li>'
            )
        else:
            cur = ' aria-current="page"' if active == href else ""
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if active == "auftrag-kontakt.html" else ""
    items.append(f'<li><a class="cta-link" href="auftrag-kontakt.html"{cur}>Auftrag erteilen</a></li>')
    return f"""
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="contactbar">
  <div class="wrap">
    <span><span class="lbl">Telefon</span><a href="tel:{PHONE_TEL}">{PHONE}</a></span>
    <span><span class="lbl">Fax</span>{FAX}</span>
    <span><span class="lbl">E-Mail</span><a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{BRAND} – Startseite">
      <span class="brand-mark" aria-hidden="true">§</span>
      <span class="brand-text"><strong>{BRAND}</strong><small>Deutsch – Dari, beglaubigt</small></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="hauptnavigation">Menü</button>
    <nav class="nav" id="hauptnavigation" aria-label="Hauptnavigation">
      <ul>{''.join(items)}</ul>
    </nav>
  </div>
</header>"""


def footer():
    docs = "".join(f'<li><a href="{d["slug"]}">{d["name"]}</a></li>' for d in DOCS)
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h2>{BRAND}</h2>
        <p>{NAME}<br>Öffentlich bestellter und allgemein beeidigter Übersetzer für Dari ({COURT})<br>{CO}<br>{STREET}<br>{ZIP} {CITY}</p>
      </div>
      <div>
        <h2>Dokumente</h2>
        <ul>{docs}</ul>
      </div>
      <div>
        <h2>Leistungen</h2>
        <ul>
          <li><a href="express-uebersetzung-24h.html">Express-Übersetzung 24 h</a></li>
          <li><a href="beglaubigte-uebersetzung.html">Beglaubigte Übersetzung</a></li>
          <li><a href="honorar-jveg.html">Honorar nach § 11 JVEG</a></li>
          <li><a href="auftrag-kontakt.html">Auftrag erteilen</a></li>
          <li><a href="dari-uebersetzer-fuer-uebersetzungsbueros.html">Für Übersetzungsbüros</a></li>
        </ul>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul>
          <li>Tel. <a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li>Fax {FAX}</li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{HOURS}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="jahr">{datetime.date.today().year}</span> {NAME}</span>
      <span><a href="impressum.html">Impressum</a>&nbsp;&nbsp;&nbsp;<a href="datenschutz.html">Datenschutz</a></span>
    </div>
  </div>
</footer>"""


def page(slug, title, desc, body, active=None, ld=None, robots="index, follow"):
    canonical = BASE + "/" if slug == "index.html" else f"{BASE}/{slug}"
    ld_blocks = "".join(
        f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or [])
    )
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="de" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#13233a">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/images/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/style.css?v=2">{ld_blocks}
</head>
<body>
{header(active or slug)}
<main id="inhalt">
{body}
</main>
{footer()}
<script src="js/main.js?v=2" defer></script>
</body>
</html>
"""
    with open(os.path.join(OUT, slug), "w", encoding="utf-8") as f:
        f.write(html)


def breadcrumb_html(items):
    lis = []
    for i, (u, n) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{n}</li>')
        else:
            lis.append(f'<li><a href="{u}">{n}</a></li>')
    return f'<nav class="breadcrumb" aria-label="Brotkrümelnavigation"><ol>{"".join(lis)}</ol></nav>'


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in faq
    ) + "</div>"


def contact_grid():
    return f"""
<div class="contact-grid">
  <div><span class="c-lbl">Direkt anrufen</span><a class="c-val" href="tel:{PHONE_TEL}">{PHONE}</a><p>Für Eilsachen und Rückfragen zum Auftrag.</p></div>
  <div><span class="c-lbl">Per Fax</span><span class="c-val">{FAX}</span><p>Schriftstücke einfach mit Begleitverfügung faxen.</p></div>
  <div><span class="c-lbl">Per E-Mail</span><a class="c-val" href="mailto:{EMAIL}">{EMAIL}</a><p>PDF- oder Word-Datei mit Aktenzeichen und Frist.</p></div>
</div>"""


def aside(d):
    return f"""
<aside class="doc-aside" aria-label="Kurzinformationen">
  <section class="aktenblatt">
    <h2>Aktenblatt</h2>
    <dl>
      <dt>Dokument</dt><dd>{d['name']}</dd>
      <dt>Rechtsgrundlage</dt><dd>{d['law']}</dd>
      <dt>Sprachrichtung</dt><dd>Deutsch → Dari (Afghanistan)</dd>
      <dt>Bearbeitungszeit</dt><dd class="eilt">{d.get('time', 'binnen 24 Stunden')}</dd>
      <dt>Form</dt><dd>Beglaubigt, mit Stempel und Unterschrift</dd>
      <dt>Abrechnung</dt><dd>§ 11 JVEG, kein Expresszuschlag</dd>
    </dl>
  </section>
  <section class="aside-contact">
    <h2>Schriftstück übermitteln</h2>
    <p>Tel. <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
    <p>Fax {FAX}</p>
    <p><a href="mailto:{EMAIL}?subject={d['name'].replace(' ', '%20')}%20%E2%80%93%20%C3%9Cbersetzung%20ins%20Dari">{EMAIL}</a></p>
    <a class="btn btn-primary" href="auftrag-kontakt.html">Auftrag erteilen</a>
  </section>
</aside>"""


# =============================== DOKUMENTE ===============================
DOCS.extend([
{
 "slug": "anklageschrift-uebersetzung-dari.html",
 "name": "Anklageschrift",
 "short": "Vollständige oder auszugsweise Übersetzung für die Zustellung an den Angeschuldigten.",
 "law": "§ 187 Abs. 2 GVG, §§ 200, 201 StPO",
 "title": "Anklageschrift ins Dari übersetzen – beglaubigt in 24 h",
 "desc": "Beglaubigte Übersetzung von Anklageschriften ins Dari für Gerichte und Staatsanwaltschaften. Bearbeitung in der Regel binnen 24 Stunden, Abrechnung nach § 11 JVEG.",
 "h1": "Übersetzung von Anklageschriften ins Dari",
 "lead": "Damit die Anklage zugestellt werden und die Erklärungsfrist nach § 201 StPO laufen kann, erhalten Sie die beglaubigte Dari-Übersetzung Ihrer Anklageschrift in der Regel binnen 24 Stunden.",
 "body": f"""
<h2>Warum die Übersetzung erforderlich ist</h2>
<p>§ 187 Abs. 2 GVG nennt Anklageschriften ausdrücklich unter den Unterlagen, deren schriftliche Übersetzung für einen der deutschen Sprache nicht mächtigen Angeschuldigten in der Regel erforderlich ist. Die Vorschrift setzt die Richtlinie 2010/64/EU über das Recht auf Dolmetschleistungen und Übersetzungen in Strafverfahren um und konkretisiert das Recht auf ein faires Verfahren aus Art. 6 Abs. 3 EMRK.</p>
<p>Fehlt die Übersetzung, kann die Zustellung nicht wirksam die Erklärungsfrist auslösen, und der Eröffnungsbeschluss verzögert sich. In Haftsachen gilt zusätzlich das besondere Beschleunigungsgebot – jeder Tag zählt.</p>

<h2>Was übersetzt wird</h2>
<ul>
  <li>Personalien des Angeschuldigten und Angaben zu Verteidigung und Haft</li>
  <li>Anklagesatz mit Tatvorwurf, Tatzeit und Tatort sowie die gesetzlichen Merkmale</li>
  <li>Anzuwendende Strafvorschriften, Beweismittel und Zeugenliste</li>
  <li>Wesentliches Ergebnis der Ermittlungen</li>
  <li>Anträge, insbesondere auf Eröffnung des Hauptverfahrens und Haftfortdauer</li>
</ul>
<p>Ordnet das Gericht eine auszugsweise Übersetzung an, übersetze ich exakt die bezeichneten Teile und kennzeichne dies im Bestätigungsvermerk.</p>

<h2>Strafrechtliche Terminologie im Dari</h2>
<p>Viele Begriffe des deutschen Strafrechts – etwa gefährliche Körperverletzung, Bandendiebstahl oder unerlaubter Aufenthalt – haben im afghanischen Recht keine deckungsgleiche Entsprechung. Ich verwende eine einheitliche, im Dari gebräuchliche Terminologie und setze bei Bedarf den deutschen Fachbegriff in Klammern. So bleibt die Übersetzung für Gericht, Verteidigung und Angeschuldigten gleichermaßen nachvollziehbar.</p>

<h2>Umfang und Lieferzeit</h2>
<p>Anklageschriften bis {EXPRESS_PAGES} Seiten liefere ich regelmäßig binnen 24 Stunden. Bei umfangreichen Wirtschafts- oder Betäubungsmittelverfahren stimme ich vorab eine verbindliche Frist oder Teillieferungen mit Ihnen ab. Vorab erhalten Sie die Übersetzung als PDF per E-Mail; die beglaubigte Ausfertigung folgt per Post.</p>
""",
 "faq": [
  ("Kann die Anklageschrift auch auszugsweise übersetzt werden?", "Ja. Wenn das Gericht eine auszugsweise Übersetzung anordnet, werden nur die bezeichneten Teile übersetzt; der Umfang wird im Bestätigungsvermerk ausgewiesen."),
  ("Wie schnell liegt die Übersetzung vor?", f"Anklageschriften bis {EXPRESS_PAGES} Seiten in der Regel binnen 24 Stunden nach Eingang. Für umfangreichere Anklagen wird eine verbindliche Frist vereinbart."),
  ("Wie wird abgerechnet?", "Ausschließlich nach § 11 JVEG je angefangene 55 Anschläge. Für die Eilbearbeitung wird kein zusätzlicher Zuschlag außerhalb des Gesetzes berechnet."),
 ],
},
{
 "slug": "urteil-uebersetzung-dari.html",
 "name": "Urteil",
 "short": "Strafurteile, Urteile der Verwaltungsgerichte in Asylsachen, Familien- und Zivilurteile.",
 "law": "§ 187 Abs. 2 GVG, § 37 Abs. 3 StPO",
 "title": "Urteil ins Dari übersetzen – beglaubigt, Express 24 h",
 "desc": "Beglaubigte Dari-Übersetzung von Strafurteilen, Asylurteilen der Verwaltungsgerichte und Familienurteilen. Express binnen 24 Stunden, Abrechnung nach JVEG.",
 "h1": "Übersetzung von Urteilen ins Dari",
 "lead": "Nach § 37 Abs. 3 StPO wird ein Urteil zusammen mit seiner Übersetzung zugestellt. Je schneller die Übersetzung vorliegt, desto früher laufen Rechtsmittelfristen und desto eher tritt Rechtskraft ein.",
 "body": f"""
<h2>Strafurteile</h2>
<p>Nicht rechtskräftige Urteile gehören nach § 187 Abs. 2 GVG zu den Unterlagen, deren schriftliche Übersetzung in der Regel erforderlich ist. Ist eine Übersetzung zur Verfügung zu stellen, wird das Urteil gemäß § 37 Abs. 3 StPO gemeinsam mit ihr zugestellt; die Zustellung an die übrigen Verfahrensbeteiligten erfolgt gleichzeitig. Eine verzögerte Übersetzung hält damit das gesamte Verfahren auf.</p>
<p>Übersetzt werden Tenor, Gründe einschließlich Feststellungen, Beweiswürdigung und Strafzumessung sowie die Rechtsmittelbelehrung.</p>

<h2>Urteile der Verwaltungsgerichte in Asylsachen</h2>
<p>Ein großer Teil der Dari-Übersetzungen betrifft asylrechtliche Verfahren afghanischer Staatsangehöriger. Ich übersetze Urteile der Verwaltungsgerichte und Oberverwaltungsgerichte einschließlich der Ausführungen zu Flüchtlingseigenschaft, subsidiärem Schutz und Abschiebungsverboten präzise und in einheitlicher Terminologie.</p>

<h2>Familien- und Zivilurteile</h2>
<p>Auch Urteile und Endentscheidungen der Amts-, Land- und Oberlandesgerichte in Familien- und Zivilsachen übersetze ich beglaubigt ins Dari, etwa wenn eine Partei die Entscheidung verstehen oder im Ausland vorlegen muss.</p>

<h2>Umfang und Lieferzeit</h2>
<p>Urteile bis {EXPRESS_PAGES} Seiten in der Regel binnen 24 Stunden. Längere Urteile liefere ich nach vorab abgestimmter Frist, auf Wunsch in Teilen. Die Rechtsmittelbelehrung wird stets vollständig übersetzt, da sie für die Wahrung der Fristen entscheidend ist.</p>
""",
 "faq": [
  ("Muss jedes Strafurteil übersetzt werden?", "Nach § 187 Abs. 2 GVG ist die schriftliche Übersetzung nicht rechtskräftiger Urteile in der Regel erforderlich, wenn der Angeklagte der deutschen Sprache nicht mächtig ist. Ob im Einzelfall eine Ausnahme vorliegt, entscheidet das Gericht."),
  ("Übersetzen Sie auch Urteile in Asylsachen?", "Ja. Urteile der Verwaltungsgerichte in Asylverfahren gehören zu den häufigsten Aufträgen und werden beglaubigt ins Dari übersetzt."),
  ("Wird die Rechtsmittelbelehrung mit übersetzt?", "Ja, immer vollständig, da sie für den Lauf der Rechtsmittelfristen maßgeblich ist."),
 ],
},
{
 "slug": "beschluss-uebersetzung-dari.html",
 "name": "Beschluss",
 "short": "Haft-, Bewährungs-, Abschiebungshaft- und Familienbeschlüsse sowie Eilbeschlüsse der Verwaltungsgerichte.",
 "law": "§ 187 GVG, §§ 268a, 207 StPO, § 62 AufenthG, FamFG",
 "title": "Beschluss ins Dari übersetzen – beglaubigt in 24 h",
 "desc": "Beglaubigte Übersetzung gerichtlicher Beschlüsse ins Dari: Haftfortdauer, Bewährung, Abschiebungshaft, Familiensachen, VwGO-Eilverfahren. 24-h-Express nach JVEG.",
 "h1": "Übersetzung von Beschlüssen ins Dari",
 "lead": "Beschlüsse greifen oft unmittelbar in die Freiheit oder das Familienleben der Betroffenen ein. Ich übersetze sie beglaubigt und in der Regel binnen 24 Stunden – bei Haftsachen auf Wunsch noch am selben Tag.",
 "body": f"""
<h2>Beschlüsse im Strafverfahren</h2>
<ul>
  <li>Eröffnungsbeschluss (§ 207 StPO) und Beschlüsse über die Haftfortdauer</li>
  <li>Bewährungsbeschlüsse mit Auflagen und Weisungen (§ 268a StPO)</li>
  <li>Widerruf der Strafaussetzung zur Bewährung (§ 56f StGB)</li>
  <li>Beschlüsse über Unterbringung, Beschlagnahme und Durchsuchung</li>
</ul>
<p>Freiheitsentziehende Anordnungen sind nach § 187 Abs. 2 GVG in der Regel schriftlich zu übersetzen. Bei Bewährungsbeschlüssen sorgt eine verständliche Übersetzung der Auflagen dafür, dass der Verurteilte sie tatsächlich erfüllen kann – und Widerrufsverfahren gar nicht erst entstehen.</p>

<h2>Abschiebungshaft und aufenthaltsrechtliche Beschlüsse</h2>
<p>Beschlüsse der Amtsgerichte über Abschiebungs- und Zurückweisungshaft nach § 62 AufenthG in Verbindung mit dem FamFG sind besonders eilbedürftig. Ich übersetze sie vorrangig und, wenn erforderlich, noch am Tag des Eingangs.</p>

<h2>Familien- und Betreuungssachen</h2>
<p>Beschlüsse zu elterlicher Sorge, Umgang, Kindeswohlgefährdung (§ 1666 BGB), Gewaltschutz und Betreuung übersetze ich so, dass die Beteiligten Inhalt und Rechtsbehelfe verstehen.</p>

<h2>Eilbeschlüsse der Verwaltungsgerichte</h2>
<p>Beschlüsse im vorläufigen Rechtsschutz nach § 80 Abs. 5 und § 123 VwGO, insbesondere in Asylsachen, liefere ich mit Vorrang, da die Fristen hier kurz sind.</p>
""",
 "faq": [
  ("Wie schnell werden Haftbeschlüsse übersetzt?", "Beschlüsse in Haftsachen werden vorrangig bearbeitet; kurze Beschlüsse in der Regel noch am Tag des Eingangs, sonst binnen 24 Stunden."),
  ("Werden Auflagen und Weisungen wörtlich übersetzt?", "Ja. Auflagen, Weisungen und Fristen werden wortgetreu und vollständig übertragen, damit der Betroffene sie eindeutig versteht."),
  ("Übersetzen Sie auch Beschlüsse in Familiensachen?", "Ja, Beschlüsse der Familiengerichte zu Sorge, Umgang, Kindeswohl und Gewaltschutz werden beglaubigt ins Dari übersetzt."),
 ],
},
{
 "slug": "strafbefehl-uebersetzung-dari.html",
 "name": "Strafbefehl",
 "short": "Strafbefehl samt Rechtsbehelfsbelehrung, damit die Einspruchsfrist wirksam beginnt.",
 "law": "§ 187 Abs. 2 GVG, §§ 409, 410 StPO",
 "title": "Strafbefehl ins Dari übersetzen – beglaubigt, 24 h",
 "desc": "Beglaubigte Dari-Übersetzung von Strafbefehlen mit Rechtsbehelfsbelehrung für Amtsgerichte und Staatsanwaltschaften. Bearbeitung binnen 24 Stunden nach JVEG.",
 "h1": "Übersetzung von Strafbefehlen ins Dari",
 "lead": "Gegen einen Strafbefehl kann binnen zwei Wochen nach Zustellung Einspruch eingelegt werden (§ 410 Abs. 1 StPO). Damit der Empfänger diese Frist versteht, übersetze ich Strafbefehl und Belehrung beglaubigt binnen 24 Stunden.",
 "body": """
<h2>Warum die Übersetzung erforderlich ist</h2>
<p>Strafbefehle sind in § 187 Abs. 2 GVG ausdrücklich unter den Unterlagen genannt, deren schriftliche Übersetzung in der Regel erforderlich ist. Versteht der Beschuldigte den Strafbefehl nicht, drohen Wiedereinsetzungsanträge und vermeidbare Folgeverfahren.</p>

<h2>Was übersetzt wird</h2>
<ul>
  <li>Personalien, Tatvorwurf und angewendete Strafvorschriften</li>
  <li>Festgesetzte Rechtsfolgen: Geldstrafe mit Tagessatzanzahl und -höhe, Fahrverbot, Entziehung der Fahrerlaubnis, Einziehung</li>
  <li>Kostenentscheidung und Zahlungsmodalitäten</li>
  <li>Rechtsbehelfsbelehrung über den Einspruch nach § 410 StPO</li>
  <li>Hinweis auf die Ersatzfreiheitsstrafe bei Uneinbringlichkeit der Geldstrafe</li>
</ul>

<h2>Kurze Dokumente, kurze Wege</h2>
<p>Strafbefehle umfassen meist nur wenige Seiten. Sie erhalten die Übersetzung in der Regel noch am Tag des Eingangs, spätestens binnen 24 Stunden. Abgerechnet wird nach § 11 JVEG; das gesetzliche Mindesthonorar beträgt 20 Euro je Auftrag.</p>
<p>Bei wiederkehrenden Formulartexten Ihres Gerichts verwende ich durchgehend dieselbe Terminologie – das erleichtert die Prüfung und sorgt für einheitliche Akten.</p>
""",
 "faq": [
  ("Wird die Rechtsbehelfsbelehrung mit übersetzt?", "Ja, immer. Sie ist der wichtigste Teil der Übersetzung, weil sie den Empfänger über die zweiwöchige Einspruchsfrist informiert."),
  ("Was kostet die Übersetzung eines Strafbefehls?", "Die Abrechnung erfolgt nach § 11 JVEG je angefangene 55 Anschläge, mindestens 20 Euro je Auftrag. Eine Orientierung bietet der Honorarrechner auf der Seite Honorar nach JVEG."),
  ("Können mehrere Strafbefehle gesammelt beauftragt werden?", "Ja. Sammelaufträge werden zügig bearbeitet; das Honorar wird für jeden Text gesondert berechnet, wie es § 11 Abs. 3 JVEG vorsieht."),
 ],
},
{
 "slug": "haftbefehl-uebersetzung-dari.html",
 "name": "Haftbefehl",
 "short": "Haft-, Vollstreckungs- und Sicherungshaftbefehle mit Belehrungen – auf Wunsch am selben Tag.",
 "law": "§ 114a, § 114b StPO, § 187 Abs. 2 GVG",
 "time": "auf Wunsch am selben Tag",
 "title": "Haftbefehl ins Dari übersetzen – beglaubigt, am selben Tag",
 "desc": "Beglaubigte Dari-Übersetzung von Haftbefehlen nach § 114a StPO, Vollstreckungs- und Sicherungshaftbefehlen. Vorrangige Bearbeitung, auf Wunsch am selben Tag.",
 "h1": "Übersetzung von Haftbefehlen ins Dari",
 "lead": "Nach § 114a StPO ist dem Beschuldigten eine Abschrift des Haftbefehls in einer für ihn verständlichen Sprache auszuhändigen. Haftbefehle bearbeite ich mit höchster Priorität – auf Wunsch noch am Tag des Eingangs.",
 "body": """
<h2>Rechtlicher Rahmen</h2>
<p>Ist eine Übersetzung bei der Verhaftung nicht sofort möglich, ist sie nach § 114a StPO unverzüglich nachzureichen. Zugleich zählen freiheitsentziehende Anordnungen nach § 187 Abs. 2 GVG zu den Unterlagen, deren schriftliche Übersetzung in der Regel erforderlich ist. Die Belehrung nach § 114b StPO übersetze ich auf Wunsch gleich mit.</p>

<h2>Welche Haftbefehle übersetzt werden</h2>
<ul>
  <li>Untersuchungshaftbefehle (§§ 112 ff. StPO)</li>
  <li>Haftbefehle nach § 230 Abs. 2 StPO bei Ausbleiben in der Hauptverhandlung</li>
  <li>Vollstreckungshaftbefehle (§ 457 StPO)</li>
  <li>Sicherungshaftbefehle im Bewährungswiderrufsverfahren (§ 453c StPO)</li>
  <li>Haftbefehle in Auslieferungs- und Überstellungsverfahren</li>
</ul>

<div class="callout"><p><strong>Eilsache:</strong> Bitte rufen Sie bei Haftsachen zusätzlich zur E-Mail oder zum Fax kurz an. So beginnt die Übersetzung sofort, und Sie erhalten eine verbindliche Uhrzeit für die Lieferung.</p></div>

<h2>Lieferung</h2>
<p>Die Übersetzung erhalten Sie vorab als PDF per E-Mail, damit sie der Justizvollzugsanstalt oder dem Beschuldigten umgehend ausgehändigt werden kann. Die beglaubigte Ausfertigung mit Stempel und Unterschrift folgt per Post.</p>
""",
 "faq": [
  ("Wie schnell wird ein Haftbefehl übersetzt?", "Haftbefehle haben höchste Priorität. Nach telefonischer Ankündigung erfolgt die Übersetzung in der Regel noch am Tag des Eingangs."),
  ("Wird auch die Belehrung nach § 114b StPO übersetzt?", "Ja, auf Wunsch wird die schriftliche Belehrung zusammen mit dem Haftbefehl übersetzt."),
  ("Kann die Übersetzung vorab elektronisch geliefert werden?", "Ja. Sie erhalten die Übersetzung vorab als PDF per E-Mail; die beglaubigte Papierfassung folgt per Post."),
 ],
},
{
 "slug": "ladung-belehrung-uebersetzung-dari.html",
 "name": "Ladung und Belehrung",
 "short": "Ladungen zur Hauptverhandlung, Zeugenladungen, Rechtsmittel- und Bewährungsbelehrungen.",
 "law": "§§ 35a, 216, 268a StPO",
 "title": "Ladung und Belehrung ins Dari übersetzen – 24 h",
 "desc": "Beglaubigte Dari-Übersetzung von Ladungen, Zeugenladungen, Rechtsmittel- und Bewährungsbelehrungen für Gerichte. Schnell, einheitlich, nach JVEG abgerechnet.",
 "h1": "Übersetzung von Ladungen und Belehrungen ins Dari",
 "lead": "Erscheint ein Angeklagter oder Zeuge nicht, weil er die Ladung nicht verstanden hat, platzt der Termin. Eine verständliche Dari-Übersetzung verhindert das – binnen 24 Stunden, oft schneller.",
 "body": """
<h2>Ladungen</h2>
<ul>
  <li>Ladungen des Angeklagten zur Hauptverhandlung mit Hinweis auf die Folgen des Ausbleibens (§ 216 StPO)</li>
  <li>Zeugen- und Sachverständigenladungen</li>
  <li>Ladungen zu Anhörungs- und Erörterungsterminen in Familien- und Verwaltungssachen</li>
  <li>Ladungen zum Haftprüfungstermin</li>
</ul>

<h2>Belehrungen und Merkblätter</h2>
<ul>
  <li>Rechtsmittelbelehrungen (§ 35a StPO) und Rechtsbehelfsbelehrungen</li>
  <li>Belehrungen über Bewährungsauflagen und -weisungen (§ 268a StPO)</li>
  <li>Belehrungen über Beschuldigten- und Zeugenrechte</li>
  <li>Merkblätter zu Bewährungshilfe, Führungsaufsicht und Zahlungserleichterungen</li>
</ul>

<h2>Einheitliche Textbausteine für Ihr Gericht</h2>
<p>Ladungen und Belehrungen bestehen überwiegend aus wiederkehrenden Formulierungen. Auf Wunsch lege ich für Ihr Gericht ein einheitliches Glossar an, damit alle Schriftstücke dieselbe Dari-Terminologie verwenden. Das macht die Übersetzungen für die Empfänger leichter verständlich und für Sie leichter prüfbar.</p>
<p>Da diese Schriftstücke kurz sind, liefere ich sie meist noch am Tag des Eingangs. Abgerechnet wird nach § 11 JVEG, mindestens 20 Euro je Auftrag.</p>
""",
 "faq": [
  ("Lohnt sich die Übersetzung einer einseitigen Ladung?", "Ja. Ein ausgefallener Hauptverhandlungstermin verursacht ein Vielfaches der Kosten. Das gesetzliche Mindesthonorar beträgt 20 Euro je Auftrag."),
  ("Können Belehrungen als Vorlage für künftige Verfahren übersetzt werden?", "Ja. Wiederkehrende Belehrungen und Merkblätter können einmalig übersetzt und anschließend von Ihrem Gericht mehrfach verwendet werden."),
  ("Wie schnell erhalten wir die Übersetzung?", "Kurze Ladungen und Belehrungen in der Regel noch am Tag des Eingangs, spätestens binnen 24 Stunden."),
 ],
},
{
 "slug": "staatsanwaltschaft-schreiben-uebersetzung-dari.html",
 "name": "Schreiben der Staatsanwaltschaft",
 "short": "Einstellungsverfügungen, Anhörungen, Vollstreckungsschreiben und Ladungen zum Strafantritt.",
 "law": "§§ 153a, 170 Abs. 2 StPO, StVollstrO",
 "title": "Schreiben der Staatsanwaltschaft ins Dari übersetzen",
 "desc": "Beglaubigte Dari-Übersetzung von Verfügungen und Schreiben der Staatsanwaltschaft: Einstellung, Auflagen nach § 153a StPO, Vollstreckung, Strafantritt. 24-h-Express.",
 "h1": "Übersetzung von Schreiben der Staatsanwaltschaft ins Dari",
 "lead": "Ob Einstellung gegen Auflage, Zahlungsaufforderung oder Ladung zum Strafantritt: Wer das Schreiben versteht, kann reagieren. Ich übersetze Verfügungen und Schreiben der Staatsanwaltschaft beglaubigt binnen 24 Stunden.",
 "body": """
<h2>Ermittlungsverfahren</h2>
<ul>
  <li>Einstellungsverfügungen nach § 170 Abs. 2 und § 153 StPO</li>
  <li>Einstellungen gegen Auflagen und Weisungen nach § 153a StPO, einschließlich Zahlungsfristen</li>
  <li>Anhörungsschreiben und Vorladungen zur Beschuldigtenvernehmung</li>
  <li>Mitteilungen an Verletzte und Bescheide über Einstellungen</li>
</ul>

<h2>Strafvollstreckung</h2>
<ul>
  <li>Ladungen zum Strafantritt</li>
  <li>Zahlungsaufforderungen zur Geldstrafe und Bescheide über Ratenzahlung</li>
  <li>Hinweise zur Ersatzfreiheitsstrafe (§ 43 StGB) und zur Abwendung durch gemeinnützige Arbeit</li>
  <li>Schreiben zur Vollstreckung von Bewährungsauflagen</li>
</ul>
<div class="note"><p>Gerade bei Geldstrafen führt fehlendes Verständnis häufig zu Ersatzfreiheitsstrafen, die vermeidbar gewesen wären. Eine verständliche Übersetzung der Zahlungsaufforderung entlastet Vollstreckungsbehörde und Justizvollzug gleichermaßen.</p></div>

<h2>Auch für Polizei und Ermittlungsbehörden</h2>
<p>Die gleiche Leistung steht Polizeidienststellen, Zollbehörden und Finanzbehörden im Steuerstrafverfahren zur Verfügung, soweit sie nach dem JVEG Übersetzer heranziehen.</p>
""",
 "faq": [
  ("Übersetzen Sie auch Schreiben aus der Strafvollstreckung?", "Ja, etwa Ladungen zum Strafantritt, Zahlungsaufforderungen und Hinweise zur Ersatzfreiheitsstrafe."),
  ("Können auch Polizeibehörden beauftragen?", "Ja. Polizei, Zoll und Finanzbehörden im Steuerstrafverfahren können ebenfalls beauftragen; die Abrechnung erfolgt nach JVEG."),
  ("Werden Zahlungsfristen besonders hervorgehoben?", "Fristen und Beträge werden exakt so übernommen, wie sie im Original stehen, damit kein Raum für Missverständnisse bleibt."),
 ],
},
])


# =============================== STARTSEITE ===============================
def build_home():
    register = "".join(
        f'<li><a href="{d["slug"]}"><span class="r-name">{d["name"]}</span><span class="r-desc">{d["short"]}</span><span class="r-law">{d["law"]}</span></a></li>'
        for d in DOCS
    )
    faq = [
        ("Wer kann Sie beauftragen?", "Gerichte aller Gerichtsbarkeiten, Staatsanwaltschaften, Polizei- und Vollstreckungsbehörden, Rechtsanwältinnen und Rechtsanwälte sowie Übersetzungsbüros, die einen beeidigten Dari-Übersetzer benötigen. Die Abrechnung gegenüber Justizbehörden erfolgt nach JVEG."),
        ("Wie schnell erhalten wir die Übersetzung?", f"Schriftstücke bis {EXPRESS_PAGES} Seiten in der Regel binnen 24 Stunden nach Eingang, Haftsachen auf Wunsch am selben Tag. Die Übersetzung kommt vorab als PDF per E-Mail, die beglaubigte Ausfertigung per Post."),
        ("Kostet die Eilbearbeitung extra?", "Nein. Es wird ausschließlich nach § 11 JVEG abgerechnet. Einen Expresszuschlag außerhalb des Gesetzes gibt es nicht."),
        ("Ist die Übersetzung beglaubigt?", f"Ja. Jede Übersetzung wird von mir als öffentlich bestelltem und allgemein beeidigtem Übersetzer ({COURT}) mit Bestätigungsvermerk, Stempel und Unterschrift versehen und fest mit einer Kopie des Ausgangsdokuments verbunden."),
        ("In welcher Form können wir Dokumente schicken?", "Per E-Mail als PDF oder Word-Datei, per Fax oder per Post. Editierbare Dateien senken nach § 11 Abs. 1 JVEG das Honorar."),
        ("Sind die Unterlagen vertraulich?", "Ja. Als allgemein beeidigter Übersetzer bin ich zur Verschwiegenheit verpflichtet. Unterlagen werden ausschließlich für den Auftrag verwendet und nach Abschluss gelöscht bzw. vernichtet, soweit keine Aufbewahrungspflichten bestehen."),
    ]
    body = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <h1>Beglaubigte Dari-Übersetzungen für Gerichte und Staatsanwaltschaften</h1>
      <p class="lead">Anklageschriften, Urteile, Beschlüsse und Haftbefehle – übersetzt von einem öffentlich bestellten und beeidigten Übersetzer, geliefert binnen 24 Stunden, abgerechnet nach § 11 JVEG.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="auftrag-kontakt.html">Schriftstück übermitteln</a>
        <a class="btn btn-secondary" href="tel:{PHONE_TEL}">Anrufen: {PHONE}</a>
      </div>
      <p class="hero-note">Kein Expresszuschlag. Vorab als PDF per E-Mail, beglaubigte Ausfertigung per Post.</p>
    </div>
    <div class="sheet" aria-hidden="true">
      <div class="sheet-head"><span>Az. 4 KLs 112 Js 0000/26</span><span>Seite 1</span></div>
      <div class="sheet-lines"><span></span><span></span><span></span><span></span></div>
      <p class="dari-line" lang="fa-AF">ترجمهٔ رسمی و تأییدشده از زبان آلمانی به زبان دری</p>
      <p class="vermerk">Die Richtigkeit und Vollständigkeit der vorstehenden Übersetzung aus der deutschen in die Dari-Sprache wird hiermit bescheinigt.<em>{NAME}, öffentlich bestellter und allgemein beeidigter Übersetzer, {COURT}</em></p>
      <div class="stamp"><b>EILT</b><small>Rückgabe binnen 24 Std.</small></div>
      <div class="seal">Beglaubigt<br>Dari</div>
    </div>
  </div>
</section>

<section class="facts" aria-label="Auf einen Blick">
  <div class="wrap">
    <dl>
      <div><dt>Beeidigt und öffentlich bestellt</dt><dd>{COURT}</dd></div>
      <div><dt>Bearbeitung</dt><dd>binnen 24 Stunden</dd></div>
      <div><dt>Abrechnung</dt><dd>§ 11 JVEG</dd></div>
      <div><dt>Sprachrichtung</dt><dd>Deutsch – Dari</dd></div>
    </dl>
  </div>
</section>

<section class="section" id="dokumente" aria-labelledby="h-dok">
  <div class="wrap">
    <div class="section-intro">
      <h2 id="h-dok">Diese Schriftstücke übersetze ich</h2>
      <p>Spezialisiert auf Straf-, Asyl- und Familienverfahren mit Beteiligten aus Afghanistan. Jede Dokumentart hat eigene Anforderungen – wählen Sie für Details die passende Seite.</p>
    </div>
    <ul class="register">{register}</ul>
  </div>
</section>

<section class="section section-alt" aria-labelledby="h-ablauf">
  <div class="wrap">
    <div class="section-intro">
      <h2 id="h-ablauf">So läuft ein Auftrag ab</h2>
      <p>Ohne Formular und ohne Registrierung. Ihre übliche Übersendungsverfügung genügt.</p>
    </div>
    <ol class="steps">
      <li><h3>Übermitteln</h3><p>Schriftstück per E-Mail, Fax oder Post senden – mit Aktenzeichen und gewünschter Frist.</p></li>
      <li><h3>Eingang bestätigt</h3><p>Sie erhalten binnen kurzer Zeit eine Bestätigung mit verbindlichem Liefertermin.</p></li>
      <li><h3>Vorab per E-Mail</h3><p>Die fertige Übersetzung kommt binnen 24 Stunden als PDF für die sofortige Zustellung.</p></li>
      <li><h3>Beglaubigt per Post</h3><p>Die Ausfertigung mit Stempel, Unterschrift und Kostenrechnung nach JVEG folgt per Post.</p></li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="h-leist">
  <div class="wrap split">
    <div>
      <h2 id="h-leist">Express ohne Aufpreis</h2>
      <p>Verzögerte Übersetzungen halten Zustellungen, Fristen und Haftprüfungen auf. Deshalb ist die Bearbeitung binnen 24 Stunden bei mir der Normalfall – nicht die Ausnahme. Haftbefehle und Beschlüsse in Haftsachen bearbeite ich auf Wunsch noch am Tag des Eingangs.</p>
      <p><a href="express-uebersetzung-24h.html">Mehr zur Express-Übersetzung</a></p>
    </div>
    <div>
      <h2>Beglaubigt und gerichtsfest</h2>
      <p>Jede Übersetzung trägt einen Bestätigungsvermerk über Richtigkeit und Vollständigkeit, Stempel und Unterschrift und ist fest mit einer Kopie des Ausgangstextes verbunden. Namen werden einheitlich und nach Vorgabe der Akte transkribiert.</p>
      <p><a href="beglaubigte-uebersetzung.html">Mehr zur beglaubigten Übersetzung</a></p>
    </div>
  </div>
</section>

<section class="section section-alt" id="uebersetzer" aria-labelledby="h-person">
  <div class="wrap profile">
    <div class="photo-slot" style="border:0;padding:0;background:none">
      <img src="images/portrait.jpg" srcset="images/portrait.jpg 480w, images/portrait@2x.jpg 960w" sizes="(max-width: 700px) 14rem, 16rem" alt="{NAME}, öffentlich bestellter und allgemein beeidigter Übersetzer für Dari" width="480" height="600" loading="lazy">
    </div>
    <div>
      <h2 id="h-person">{NAME}</h2>
      <p><strong>Öffentlich bestellter und allgemein beeidigter Übersetzer für die Sprache Dari, {COURT}</strong></p>
      <p>Dari ist meine Muttersprache, Deutsch die Sprache meiner Ausbildung und meines Berufs. Seit 2017 arbeite ich als Sprachmittler für deutsche Behörden und Einrichtungen – zunächst als freiberuflicher Dolmetscher für das Polizeipräsidium München, später als Sprach- und Kulturmediator für das Bayerische Zentrum für Transkulturelle Medizin und als Übersetzer für die AWO München.</p>
      <p>Mein Studium der Politik- und Kulturwissenschaften des Nahen Ostens an der Ludwig-Maximilians-Universität München habe ich 2020 mit dem Bachelor abgeschlossen; 2021 folgte die Prüfung zum staatlich geprüften Übersetzer an der Hessischen Lehrkräfteakademie. Als Verwaltungsassistent am Generalkonsulat von Afghanistan in Bonn war ich von 2020 bis 2022 in der Aktenverwaltung tätig und habe dort afghanische Urkunden und Verwaltungsvorgänge aus erster Hand kennengelernt – ein Wissen, das mir heute bei Übersetzungen aus dem Dari ins Deutsche zugutekommt.</p>
      <p>Seit 2024 bin ich vom {COURT} als Übersetzer für Dari öffentlich bestellt und allgemein beeidigt. Neben Dari spreche ich Paschtu und Farsi als Muttersprachen sowie fließend Englisch; die öffentliche Bestellung gilt für Dari.</p>
      <p>Mein Anspruch an jede Übersetzung: Sie soll für die Empfänger verständlich sein, ohne an juristischer Genauigkeit zu verlieren.</p>
      <p><a href="https://www.justiz-dolmetscher.de/Recherche/de/Person/Details/61461" rel="noopener">Eintrag in der Dolmetscher- und Übersetzerdatenbank der Justiz ansehen</a></p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="h-honorar">
  <div class="wrap split">
    <div>
      <h2 id="h-honorar">Honorar nach § 11 JVEG</h2>
      <p>Abgerechnet wird je angefangene 55 Anschläge nach den gesetzlichen Sätzen – transparent und prüfbar. Bei Übersetzungen aus dem Deutschen ins Dari zählt nach § 11 Abs. 2 JVEG der deutsche Ausgangstext.</p>
      <p><a href="honorar-jveg.html">Sätze und Honorarrechner ansehen</a></p>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Text liegt vor als</th><th class="num">regulär</th><th class="num">besonders erschwert</th></tr></thead>
        <tbody>
          <tr><td>editierbare Datei</td><td class="num">1,95 €</td><td class="num">2,15 €</td></tr>
          <tr><td>Scan, Fax oder Papier</td><td class="num">2,15 €</td><td class="num">2,30 €</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="h-faq">
  <div class="wrap">
    <div class="section-intro"><h2 id="h-faq">Häufige Fragen von Geschäftsstellen</h2></div>
    {faq_html(faq)}
    <p style="margin-top:1.5rem">Sie sind ein Übersetzungsbüro? <a href="dari-uebersetzer-fuer-uebersetzungsbueros.html">Informationen zur Zusammenarbeit für Übersetzungsbüros</a></p>
  </div>
</section>

<section class="section" aria-labelledby="h-kontakt">
  <div class="wrap">
    <div class="section-intro">
      <h2 id="h-kontakt">Schriftstück übermitteln</h2>
      <p>{HOURS}. Für Haftsachen bitte zusätzlich kurz anrufen.</p>
    </div>
    {contact_grid()}
  </div>
</section>
"""
    page("index.html",
         "Dari-Übersetzer für Gerichte – beglaubigt, Express 24 h",
         "Beeidigter Übersetzer für Dari: beglaubigte Übersetzung von Anklageschriften, Urteilen, Beschlüssen und Haftbefehlen binnen 24 Stunden. Abrechnung nach § 11 JVEG.",
         body,
         ld=[org_ld(), person_ld(), faq_ld(faq)])


# =============================== DOKUMENTSEITEN ===============================
def build_docs():
    for d in DOCS:
        crumbs = [("index.html", "Start"), ("index.html#dokumente", "Dokumente"), (d["slug"], d["name"])]
        others = "".join(f'<li><a href="{o["slug"]}">{o["name"]} ins Dari übersetzen</a></li>' for o in DOCS if o is not d)
        body = f"""
<div class="page-head">
  <div class="wrap">
    {breadcrumb_html(crumbs)}
    <h1>{d['h1']}</h1>
    <p class="lead">{d['lead']}</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="auftrag-kontakt.html">{d['name']} übermitteln</a>
      <a class="btn btn-secondary" href="tel:{PHONE_TEL}">{PHONE}</a>
    </div>
  </div>
</div>
<div class="wrap doc-layout">
  <article class="doc-body">
    {d['body']}
    <h2>Beglaubigung und Abrechnung</h2>
    <p>Die Übersetzung wird von mir als öffentlich bestelltem und allgemein beeidigtem Übersetzer ({COURT}) mit Bestätigungsvermerk, Stempel und Unterschrift versehen. Abgerechnet wird ausschließlich nach <a href="honorar-jveg.html">§ 11 JVEG</a> – auch bei Eilbearbeitung ohne Aufschlag. Einzelheiten zur Form finden Sie unter <a href="beglaubigte-uebersetzung.html">beglaubigte Übersetzung</a>, zum Ablauf unter <a href="express-uebersetzung-24h.html">Express-Übersetzung</a>.</p>
    <h2>Häufige Fragen</h2>
    {faq_html(d['faq'])}
    <h2>Weitere Schriftstücke</h2>
    <ul class="related">{others}</ul>
  </article>
  {aside(d)}
</div>
"""
        page(d["slug"], d["title"], d["desc"], body,
             ld=[service_ld(d), breadcrumb_ld([("index.html", "Start"), (d["slug"], d["name"])]), faq_ld(d["faq"])])


# =============================== LEISTUNGSSEITEN ===============================
def simple_page(slug, title, desc, h1, lead, content, crumb, faq=None, aside_html=""):
    crumbs = [("index.html", "Start"), (slug, crumb)]
    faq_part = f"<h2>Häufige Fragen</h2>{faq_html(faq)}" if faq else ""
    side = aside_html or f"""
<aside class="doc-aside" aria-label="Kontakt">
  <section class="aside-contact">
    <h2>Schriftstück übermitteln</h2>
    <p>Tel. <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
    <p>Fax {FAX}</p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <a class="btn btn-primary" href="auftrag-kontakt.html">Auftrag erteilen</a>
  </section>
</aside>"""
    body = f"""
<div class="page-head">
  <div class="wrap">
    {breadcrumb_html(crumbs)}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</div>
<div class="wrap doc-layout">
  <article class="doc-body">{content}{faq_part}</article>
  {side}
</div>"""
    ld = [breadcrumb_ld(crumbs)]
    if faq:
        ld.append(faq_ld(faq))
    page(slug, title, desc, body, ld=ld)


def build_service_pages():
    simple_page(
        "express-uebersetzung-24h.html",
        "Express-Übersetzung Dari binnen 24 h – für Gerichte",
        "Dari-Übersetzungen für Justiz und Behörden binnen 24 Stunden, Haftsachen am selben Tag. Beglaubigt, vorab per E-Mail, ohne Expresszuschlag – Abrechnung nach JVEG.",
        "Express-Übersetzung ins Dari binnen 24 Stunden",
        "In Strafsachen hängen Zustellungen, Fristen und Haftprüfungen an der Übersetzung. Deshalb ist die Lieferung binnen 24 Stunden der Standard – ohne Aufpreis.",
        f"""
<h2>Lieferzeiten</h2>
<div class="table-wrap"><table>
  <thead><tr><th>Schriftstück</th><th>Übliche Lieferzeit</th></tr></thead>
  <tbody>
    <tr><td>Haftbefehl, Beschluss in Haftsachen, Abschiebungshaft</td><td>auf Wunsch am Tag des Eingangs</td></tr>
    <tr><td>Strafbefehl, Ladung, Belehrung, kurze Verfügung</td><td>meist am Tag des Eingangs</td></tr>
    <tr><td>Anklageschrift, Urteil, Beschluss bis {EXPRESS_PAGES} Seiten</td><td>binnen 24 Stunden</td></tr>
    <tr><td>Umfangreiche Anklagen und Urteile</td><td>verbindliche Frist nach Absprache, Teillieferung möglich</td></tr>
  </tbody>
</table></div>
<p>Die Frist beginnt mit dem Eingang des vollständigen, lesbaren Schriftstücks. Eingänge nach 20 Uhr gelten als am Folgetag eingegangen, Haftsachen ausgenommen.</p>

<h2>Wie die Eilbearbeitung funktioniert</h2>
<ol>
  <li>Sie senden das Schriftstück per E-Mail oder Fax und nennen Aktenzeichen und Frist.</li>
  <li>Sie erhalten eine Eingangsbestätigung mit verbindlichem Liefertermin.</li>
  <li>Die fertige Übersetzung kommt vorab als PDF per E-Mail – sie kann sofort zugestellt oder ausgehändigt werden.</li>
  <li>Die beglaubigte Ausfertigung mit Stempel und Unterschrift folgt per Post, zusammen mit der Kostenrechnung nach JVEG.</li>
</ol>

<div class="callout"><p><strong>Haftsachen:</strong> Bitte rufen Sie zusätzlich unter <a href="tel:{PHONE_TEL}">{PHONE}</a> an. So beginnt die Arbeit sofort und Sie erhalten eine konkrete Uhrzeit.</p></div>

<h2>Kein Expresszuschlag</h2>
<p>Abgerechnet wird ausschließlich nach § 11 JVEG. Das Gesetz nennt eine besondere Eilbedürftigkeit als einen der Umstände, unter denen eine Übersetzung als besonders erschwert gelten kann; ob der erhöhte Satz anzuwenden ist, entscheidet die heranziehende Stelle. Darüber hinaus wird nichts berechnet.</p>
""",
        "Express 24 h",
        faq=[
            ("Gilt die 24-Stunden-Frist auch am Wochenende?", "Haftsachen und angekündigte Eilsachen werden nach Absprache auch am Wochenende bearbeitet. Bitte vorher telefonisch ankündigen."),
            ("Was kostet die Eilbearbeitung?", "Es fällt kein zusätzlicher Zuschlag an. Abgerechnet wird ausschließlich nach § 11 JVEG."),
            ("Bekommen wir die Übersetzung auch elektronisch?", "Ja, vorab als PDF per E-Mail. Die beglaubigte Papierfassung folgt per Post."),
        ],
    )

    simple_page(
        "beglaubigte-uebersetzung.html",
        "Beglaubigte Übersetzung Deutsch–Dari für die Justiz",
        f"Beglaubigte Übersetzungen ins Dari von einem öffentlich bestellten und beeidigten Übersetzer ({COURT}): Bestätigungsvermerk, Stempel, Unterschrift, einheitliche Transkription von Namen.",
        "Beglaubigte Übersetzungen ins Dari",
        f"Jede Übersetzung wird von mir als öffentlich bestelltem und allgemein beeidigtem Übersetzer ({COURT}) mit einem Bestätigungsvermerk über ihre Richtigkeit und Vollständigkeit versehen.",
        f"""
<h2>Bestandteile der beglaubigten Übersetzung</h2>
<ul>
  <li>Vollständige Übersetzung des Schriftstücks oder der vom Gericht bezeichneten Auszüge</li>
  <li>Bestätigungsvermerk über Richtigkeit und Vollständigkeit</li>
  <li>Stempel, Datum und eigenhändige Unterschrift</li>
  <li>Feste Verbindung mit einer Kopie des deutschen Ausgangstextes</li>
  <li>Kennzeichnung unleserlicher Stellen, Stempel, Siegel und handschriftlicher Zusätze</li>
</ul>

<h2>Musterformulierung des Bestätigungsvermerks</h2>
<div class="note"><p>„Die Richtigkeit und Vollständigkeit der vorstehenden Übersetzung aus der deutschen in die Dari-Sprache wird hiermit bescheinigt.“<br>{NAME}, öffentlich bestellter und allgemein beeidigter Übersetzer für die Sprache Dari, {COURT}</p></div>

<h2>Namen und Schreibweisen</h2>
<p>Afghanische Namen werden in deutschen Akten oft unterschiedlich transkribiert. Ich übernehme in der Übersetzung die Schreibweise, die in der Akte, im Pass oder im Aufenthaltstitel verwendet wird, und gebe auf Wunsch zusätzlich die Dari-Schreibweise an. Nennen Sie mir bei der Übersendung gern die maßgebliche Schreibweise.</p>

<h2>Anzahl der Ausfertigungen</h2>
<p>Teilen Sie mir mit, wie viele beglaubigte Ausfertigungen benötigt werden – etwa für Angeklagten, Verteidigung und Akte. Weitere Ausfertigungen werden nach § 7 JVEG abgerechnet.</p>

<h2>Vertraulichkeit</h2>
<p>Gerichtliche Schriftstücke enthalten besonders schutzwürdige Daten. Ich bin zur Verschwiegenheit verpflichtet, verwende die Unterlagen ausschließlich für den jeweiligen Auftrag und lösche bzw. vernichte sie nach Abschluss, soweit keine Aufbewahrungspflichten bestehen.</p>
""",
        "Beglaubigung",
        faq=[
            ("Wer darf Übersetzungen für Gerichte beglaubigen?", "Beglaubigen dürfen Übersetzer, die von der zuständigen Stelle des jeweiligen Bundeslandes ermächtigt bzw. beeidigt sind. Die Bestätigung gilt bundesweit."),
            ("Erhalten wir auch eine elektronische Fassung?", "Ja. Vorab erhalten Sie die Übersetzung als PDF per E-Mail; maßgeblich ist die beglaubigte Papierausfertigung."),
            ("Wie werden afghanische Namen geschrieben?", "Wie in der Akte bzw. im Ausweisdokument. Auf Wunsch wird die Dari-Schreibweise ergänzt."),
        ],
    )

    calc = """
<form class="calc" id="jveg-rechner" novalidate>
  <div class="row">
    <label for="anschlaege">Anschläge des deutschen Ausgangstextes (mit Leerzeichen)</label>
    <input type="number" id="anschlaege" name="anschlaege" min="1" step="1" value="5500" inputmode="numeric">
    <p class="hint">In Word: Überprüfen › Wörter zählen › „Zeichen (mit Leerzeichen)“. Eine volle Textseite hat etwa 2.500–3.000 Anschläge.</p>
  </div>
  <fieldset>
    <legend>Das Schriftstück liegt vor als</legend>
    <label><input type="radio" name="textform" value="editierbar" checked> editierbare Datei (z. B. Word, durchsuchbares PDF)</label>
    <label><input type="radio" name="textform" value="nicht"> Scan, Fax oder Papier</label>
  </fieldset>
  <fieldset>
    <legend>Besondere Erschwernis</legend>
    <label><input type="checkbox" name="erschwert"> besonders erschwert nach § 11 Abs. 1 S. 3 JVEG</label>
  </fieldset>
  <output id="rechner-ergebnis" for="anschlaege" aria-live="polite"></output>
</form>"""

    simple_page(
        "honorar-jveg.html",
        "Honorar nach § 11 JVEG – Dari-Übersetzung für Gerichte",
        "Dari-Übersetzungen werden nach § 11 JVEG abgerechnet: 1,95 € bzw. 2,15 € je 55 Anschläge, erschwert 2,15 € bzw. 2,30 €, mindestens 20 €. Mit Honorarrechner.",
        "Honorar nach § 11 JVEG",
        "Für Gerichte, Staatsanwaltschaften und Behörden rechne ich ausschließlich nach dem Justizvergütungs- und -entschädigungsgesetz ab. Keine Pauschalen, keine Expresszuschläge.",
        f"""
<h2>Gesetzliche Sätze</h2>
<div class="table-wrap"><table>
  <thead><tr><th>Honorar je angefangene 55 Anschläge</th><th class="num">regulär</th><th class="num">besonders erschwert</th></tr></thead>
  <tbody>
    <tr><td>Text in editierbarer elektronischer Form (Grundhonorar)</td><td class="num">1,95 €</td><td class="num">2,15 €</td></tr>
    <tr><td>Text nicht editierbar, z. B. Scan, Fax, Papier (erhöhtes Honorar)</td><td class="num">2,15 €</td><td class="num">2,30 €</td></tr>
    <tr><td>Mindesthonorar je Auftrag</td><td class="num" colspan="2">20,00 €</td></tr>
  </tbody>
</table></div>
<p>Stand: § 11 JVEG in der Fassung des KostBRÄG 2025, gültig seit 1. Juni 2025.</p>

<h2>Wie gezählt wird</h2>
<p>Grundsätzlich ist der Text in der Zielsprache maßgebend. Werden jedoch nur in der Ausgangssprache lateinische Schriftzeichen verwendet, zählt der Ausgangstext (§ 11 Abs. 2 JVEG). Da Dari in arabischer Schrift geschrieben wird, richtet sich das Honorar bei Übersetzungen aus dem Deutschen ins Dari nach den Anschlägen des deutschen Ausgangstextes – das ist für Sie vorab exakt bestimmbar.</p>
<p>Sind mehrere Texte zu übersetzen, wird das Honorar für jeden Text gesondert bestimmt (§ 11 Abs. 3 JVEG).</p>

<h2>Wann der erhöhte Satz in Betracht kommt</h2>
<p>§ 11 Abs. 1 S. 3 JVEG nennt als Beispiele für eine besonders erschwerte Übersetzung die häufige Verwendung von Fachausdrücken, schwere Lesbarkeit, besondere Eilbedürftigkeit und eine in Deutschland selten vorkommende Fremdsprache. Ob diese Voraussetzungen vorliegen, beurteilt die heranziehende Stelle im Einzelfall. In der Kostenrechnung weise ich die Gründe nachvollziehbar aus.</p>

<h2>Senken Sie die Kosten: editierbare Datei senden</h2>
<p>Liegt das Schriftstück als Word-Datei oder durchsuchbares PDF vor, gilt der niedrigere Grundsatz. Senden Sie daher nach Möglichkeit die Datei aus Ihrem Fachverfahren statt eines Scans.</p>

<h2>Honorarrechner</h2>
<p>Zur unverbindlichen Orientierung vor der Beauftragung:</p>
{calc}

<h2>Kostenrechnung</h2>
<p>Mit der beglaubigten Ausfertigung erhalten Sie eine prüffähige Kostenrechnung mit Aktenzeichen, Anschlagzahl, angewandtem Satz und gegebenenfalls Auslagen für Ausfertigungen (§ 7 JVEG) und Porto. Die Umsatzsteuer wird erstattet, soweit sie anfällt (§ 12 Abs. 1 S. 2 Nr. 4 JVEG).</p>
<div class="note"><p>Rechtsanwältinnen und Rechtsanwälte sowie andere Auftraggeber außerhalb der Justiz erhalten auf Anfrage ein individuelles Angebot, das sich an den JVEG-Sätzen orientiert.</p></div>
""",
        "Honorar nach JVEG",
        faq=[
            ("Wird der deutsche oder der Dari-Text gezählt?", "Bei Übersetzungen aus dem Deutschen ins Dari zählt nach § 11 Abs. 2 S. 2 JVEG der deutsche Ausgangstext, weil nur dieser lateinische Schriftzeichen verwendet."),
            ("Gibt es ein Mindesthonorar?", "Ja. Für eine oder mehrere Übersetzungen aufgrund desselben Auftrags beträgt das Honorar mindestens 20 Euro (§ 11 Abs. 3 JVEG)."),
            ("Fällt für Express ein Zuschlag an?", "Nein. Abgerechnet wird ausschließlich nach den gesetzlichen Sätzen."),
        ],
    )


# =============================== AUFTRAG / KONTAKT ===============================
def build_contact():
    mail_body = (
        "Aktenzeichen:%0D%0A"
        "Gericht / Behörde:%0D%0A"
        "Dokumentart (z. B. Anklageschrift, Urteil):%0D%0A"
        "Gewünschte Frist:%0D%0A"
        "Anzahl beglaubigter Ausfertigungen:%0D%0A"
        "Schreibweise des Namens laut Akte:%0D%0A"
        "Lieferanschrift für die Ausfertigung:%0D%0A"
        "Ansprechpartner/in und Durchwahl:%0D%0A"
    ).replace(" ", "%20")
    content = f"""
<h2>Drei Wege, ein Schriftstück zu übermitteln</h2>
{contact_grid()}
<p style="margin-top:1.5rem"><a class="btn btn-primary" href="mailto:{EMAIL}?subject=%C3%9Cbersetzungsauftrag%20Deutsch%20%E2%80%93%20Dari&amp;body={mail_body}">E-Mail mit Auftragsvorlage öffnen</a></p>

<h2>Diese Angaben helfen</h2>
<ul>
  <li>Aktenzeichen und Bezeichnung des Gerichts oder der Behörde</li>
  <li>Dokumentart und gegebenenfalls Umfang der auszugsweisen Übersetzung</li>
  <li>Gewünschte Frist, insbesondere bei Haftsachen</li>
  <li>Anzahl der beglaubigten Ausfertigungen</li>
  <li>Maßgebliche Schreibweise des Namens laut Akte oder Ausweis</li>
  <li>Lieferanschrift und Ansprechpartner der Geschäftsstelle</li>
</ul>
<p>Eine übliche Übersendungsverfügung genügt – ein besonderes Formular ist nicht erforderlich.</p>

<h2>Postanschrift</h2>
<p>{NAME}<br>{BRAND}<br>{CO}<br>{STREET}<br>{ZIP} {CITY}</p>

<h2>Erreichbarkeit</h2>
<p>{HOURS}. Für Haftsachen und Eilsachen rufen Sie bitte zusätzlich an, damit die Bearbeitung sofort beginnt.</p>
<div class="note"><p>Bitte senden Sie Originale nur, wenn dies ausdrücklich erforderlich ist. In der Regel genügt eine Kopie, ein Scan oder die Datei aus Ihrem Fachverfahren.</p></div>
"""
    simple_page(
        "auftrag-kontakt.html",
        "Auftrag erteilen – Dari-Übersetzung per E-Mail, Fax, Telefon",
        "Schriftstücke zur Dari-Übersetzung per E-Mail, Fax oder Post übermitteln. Direkter Telefonkontakt für Eilsachen und Haftsachen. Beglaubigt, binnen 24 Stunden.",
        "Auftrag erteilen",
        "Senden Sie das Schriftstück mit Aktenzeichen und Frist per E-Mail, Fax oder Post. Sie erhalten umgehend eine Eingangsbestätigung mit verbindlichem Liefertermin.",
        content, "Auftrag erteilen", aside_html="<span></span>",
    )



# =============================== FÜR ÜBERSETZUNGSBÜROS ===============================
def build_agencies():
    mail_body = (
        "Sprachrichtung (Deutsch-Dari / Dari-Deutsch):%0D%0A"
        "Dokumentart:%0D%0A"
        "Aktenzeichen / Geschäftszeichen (falls vorhanden):%0D%0A"
        "Umfang (Seiten oder Anschläge):%0D%0A"
        "Gewünschter Liefertermin:%0D%0A"
        "Lieferform (PDF / beglaubigt per Post):%0D%0A"
        "Schreibweise der Namen laut Ausweis/Akte:%0D%0A"
        "Besondere Vorgaben des Endkunden:%0D%0A"
        "Rechnungsanschrift:%0D%0A"
    ).replace(" ", "%20")
    faq = [
        ("Liefern Sie neutral, ohne eigenen Briefkopf?", "Ja. Auf Wunsch liefere ich die Übersetzung ohne eigenen Briefkopf und ohne Werbung. Bei beglaubigten Übersetzungen sind Bestätigungsvermerk, Name, Stempel und Unterschrift des Übersetzers allerdings gesetzlich vorgeschrieben."),
        ("Übersetzen Sie auch aus dem Dari ins Deutsche?", "Ja. Neben gerichtlichen Unterlagen ins Dari übersetze ich afghanische Urkunden und Dokumente beglaubigt ins Deutsche, etwa Tazkira, Geburts- und Heiratsurkunden, Zeugnisse und Führerscheine."),
        ("Wie wird abgerechnet?", "Nach einer vereinbarten Preisbasis, in der Regel je Normzeile oder Seite. Sie erhalten vorab ein verbindliches Angebot. Für regelmäßige Zusammenarbeit vereinbaren wir feste Konditionen."),
        ("Unterzeichnen Sie eine Vertraulichkeitsvereinbarung?", "Ja. Auf Wunsch unterzeichne ich eine Vertraulichkeitsvereinbarung bzw. einen Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO."),
    ]
    content = f"""
<h2>Welche Aufträge ich übernehme</h2>
<div class="cols3">
  <div>
    <h3>Gerichtliche Unterlagen</h3>
    <ul><li>Anklageschriften</li><li>Strafbefehle</li><li>Urteile</li><li>Beschlüsse</li><li>Ladungen und Belehrungen</li><li>Verfügungen</li></ul>
  </div>
  <div>
    <h3>Staatsanwaltschaft und Polizei</h3>
    <ul><li>Schreiben der Staatsanwaltschaft</li><li>Ermittlungsunterlagen</li><li>Vernehmungsprotokolle</li><li>Polizeiberichte</li><li>Rechtshilfeunterlagen</li></ul>
  </div>
  <div>
    <h3>Weitere rechtliche Dokumente</h3>
    <ul><li>Klageschriften und anwaltliche Schriftsätze</li><li>Bescheide von Behörden</li><li>Vollmachten</li><li>Anlagen und Nachweise</li><li>Afghanische Urkunden (Dari → Deutsch)</li></ul>
  </div>
</div>

<h2>Sprachrichtungen</h2>
<p><strong>Deutsch → Dari:</strong> gerichtliche, staatsanwaltschaftliche und behördliche Schriftstücke, die einem Betroffenen in seiner Sprache zugänglich gemacht werden müssen.</p>
<p><strong>Dari → Deutsch:</strong> afghanische Urkunden und Dokumente für Standesämter, Ausländerbehörden, Gerichte und Arbeitgeber, auf Wunsch beglaubigt.</p>

<h2>Warum Büros mit mir zusammenarbeiten</h2>
<ul>
  <li>Öffentlich bestellter und allgemein beeidigter Übersetzer für Dari ({COURT}) – beglaubigte Übersetzungen werden bundesweit anerkannt</li>
  <li>Spezialisiert auf gerichtliche und behördliche Unterlagen</li>
  <li>Dari als Muttersprache, einheitliche juristische Terminologie</li>
  <li>Einheitliche Schreibweise von Namen und Ortsangaben nach Ihren Vorgaben</li>
  <li>Verbindliche Liefertermine, Express binnen 24 Stunden möglich</li>
  <li>Direkter Kontakt zum Übersetzer, ohne Zwischenstellen</li>
  <li>Lieferung als PDF per E-Mail und/oder beglaubigt per Post</li>
</ul>

<div class="note"><p><strong>Sie bleiben Ansprechpartner Ihres Kunden.</strong> Ich arbeite zuverlässig im Hintergrund und liefere ausschließlich an Ihr Büro. Kontakt zu Ihren Endkunden nehme ich nicht auf.</p></div>

<h2>So funktioniert die Zusammenarbeit</h2>
<ol class="steps">
  <li><h3>Unterlagen senden</h3><p>Dokumente per E-Mail als PDF, Word-Datei oder Scan schicken.</p></li>
  <li><h3>Angebot erhalten</h3><p>Ich prüfe Umfang und Frist und nenne Preis und verbindlichen Liefertermin.</p></li>
  <li><h3>Übersetzung</h3><p>Nach Ihrer Freigabe übersetze ich sorgfältig und vertraulich.</p></li>
  <li><h3>Lieferung</h3><p>Als PDF und/oder beglaubigt per Post – an Ihr Büro oder direkt an die von Ihnen genannte Stelle.</p></li>
</ol>

<h2>Diese Angaben beschleunigen die Bearbeitung</h2>
<ul>
  <li>Sprachrichtung und Dokumentart</li>
  <li>Aktenzeichen oder Geschäftszeichen, falls vorhanden</li>
  <li>Umfang der Unterlagen</li>
  <li>Gewünschter Liefertermin und Lieferform</li>
  <li>Schreibweise der Namen laut Ausweis oder Akte</li>
  <li>Besondere Vorgaben Ihres Endkunden</li>
  <li>Rechnungsanschrift</li>
</ul>
<p><a class="btn btn-primary" href="mailto:{EMAIL}?subject=Anfrage%20%C3%9Cbersetzungsb%C3%BCro%20%E2%80%93%20Dari&amp;body={mail_body}">Anfrage mit Vorlage per E-Mail senden</a></p>

<h2>Vertraulichkeit</h2>
<p>Gerichtliche und staatsanwaltschaftliche Unterlagen enthalten besonders schutzwürdige personen- und verfahrensbezogene Daten. Alle Dokumente werden vertraulich behandelt, ausschließlich für den jeweiligen Auftrag verwendet und nach Abschluss gelöscht bzw. vernichtet, soweit keine Aufbewahrungspflichten bestehen. Auf Wunsch unterzeichne ich eine Vertraulichkeitsvereinbarung oder einen Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO.</p>

<h2>Konditionen</h2>
<p>Sie erhalten ein individuelles Angebot nach Sichtung der Unterlagen – eine zehnseitige Anklageschrift und eine achtzigseitige Ermittlungsakte lassen sich nicht pauschal bepreisen. Abgerechnet wird transparent nach vereinbarter Preisbasis. Für Büros mit regelmäßigem Dari-Bedarf vereinbaren wir gern feste Konditionen.</p>
"""
    simple_page(
        "dari-uebersetzer-fuer-uebersetzungsbueros.html",
        "Dari-Übersetzer für Übersetzungsbüros – beglaubigt, zuverlässig",
        f"Beeidigter Dari-Übersetzer ({COURT}) als Partner für Übersetzungsbüros: Gerichtsunterlagen und Urkunden Deutsch–Dari, beglaubigt, vertraulich, termingerecht.",
        "Dari-Übersetzungen für Übersetzungsbüros",
        "Sie haben einen Auftrag für Dari erhalten und benötigen einen beeidigten Übersetzer? Ich übernehme die Übersetzung zuverlässig, termingerecht und auf Wunsch beglaubigt – im Hintergrund, mit Ihnen als Ansprechpartner Ihres Kunden.",
        content, "Für Übersetzungsbüros", faq=faq,
    )

# =============================== RECHTLICHES ===============================
def build_legal():
    imp = f"""
<div class="wrap legal">
  {breadcrumb_html([("index.html", "Start"), ("impressum.html", "Impressum")])}
  <h1>Impressum</h1>
  <h2>Angaben gemäß § 5 DDG</h2>
  <p>{NAME}<br>{BRAND}<br>{CO}<br>{STREET}<br>{ZIP} {CITY}<br>Deutschland</p>
  <h2>Kontakt</h2>
  <p>Telefon: <a href="tel:{PHONE_TEL}">{PHONE}</a><br>Fax: {FAX}<br>E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <h2>Berufsbezeichnung und berufsrechtliche Regelungen</h2>
  <p>Berufsbezeichnung: Öffentlich bestellter und allgemein beeidigter Übersetzer für die Sprache Dari<br>Zuständige Stelle: {COURT} (Az. 316-II/5/2571)<br>Die Berufsbezeichnung wurde in der Bundesrepublik Deutschland verliehen.<br>Eintrag in der <a href="https://www.justiz-dolmetscher.de/Recherche/de/Person/Details/61461" rel="noopener">Dolmetscher- und Übersetzerdatenbank der Justiz</a></p>
  <h2>Umsatzsteuer</h2>
  <p>[Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG eintragen – oder diesen Abschnitt entfernen, falls nicht vorhanden.]</p>
  <h2>Verantwortlich für den Inhalt</h2>
  <p>{NAME}, Anschrift wie oben</p>
  <h2>Verbraucherstreitbeilegung</h2>
  <p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
  <h2>Haftung für Inhalte und Links</h2>
  <p>Die Inhalte dieser Website wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann jedoch keine Gewähr übernommen werden. Gesetzesangaben dienen der allgemeinen Information und ersetzen keine Rechtsberatung.</p>
</div>"""
    page("impressum.html", f"Impressum – {BRAND}", f"Impressum von {BRAND}, {NAME}, beeidigter Übersetzer für Dari.", imp, robots="noindex, follow")

    ds = f"""
<div class="wrap legal">
  {breadcrumb_html([("index.html", "Start"), ("datenschutz.html", "Datenschutz")])}
  <h1>Datenschutzerklärung</h1>
  <h2>1. Verantwortlicher</h2>
  <p>{NAME}, {CO}, {STREET}, {ZIP} {CITY}<br>E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a>, Telefon: {PHONE}</p>
  <h2>2. Hosting dieser Website (Vercel)</h2>
  <p>Diese Website wird bei der Vercel Inc., USA („Vercel“), gehostet. Sie verwendet keine Cookies, keine Analyse- oder Trackingdienste und lädt keine Inhalte weiterer Drittanbieter wie externe Schriftarten, Karten oder Videos. Beim Aufruf verarbeitet Vercel technisch notwendige Daten (IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browsertyp) in Server-Logfiles, um die Website auszuliefern und ihre Sicherheit zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; mein berechtigtes Interesse liegt in einer sicheren und zuverlässigen Bereitstellung der Website.</p>
  <p>Dabei können personenbezogene Daten in die USA übermittelt werden. Vercel ist nach dem EU-US Data Privacy Framework zertifiziert; die Übermittlung erfolgt auf Grundlage des Angemessenheitsbeschlusses der EU-Kommission (Art. 45 DSGVO) sowie ergänzend der EU-Standardvertragsklauseln. Mit Vercel besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO. Weitere Informationen: <a href="https://vercel.com/legal/privacy-policy" rel="noopener">Datenschutzhinweise von Vercel</a>.</p>

  <h2>3. E-Mail (Spaceship) und Domain (checkdomain)</h2>
  <p>Die Domain dieser Website ist bei der checkdomain GmbH, Lübeck, registriert; deren Nameserver übernehmen die technische Zuordnung der Domain. Das E-Mail-Postfach wird von der Spaceship, Inc., USA („Spaceship“), bereitgestellt. Wenn Sie mir eine E-Mail senden, werden deren Inhalt, Anhänge und Metadaten auf den Servern von Spaceship gespeichert und verarbeitet. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (Vertragsanbahnung und -durchführung) bzw. Art. 6 Abs. 1 lit. f DSGVO. Eine Übermittlung in die USA erfolgt auf Grundlage geeigneter Garantien nach Art. 44 ff. DSGVO, insbesondere der EU-Standardvertragsklauseln. Weitere Informationen: <a href="https://www.spaceship.com/legal/privacy-policy/" rel="noopener">Datenschutzhinweise von Spaceship</a>.</p>

  <h2>4. Kontaktaufnahme und Übersetzungsaufträge</h2>
  <p>Wenn Sie per E-Mail, Fax, Telefon oder Post Kontakt aufnehmen oder Schriftstücke zur Übersetzung übermitteln, verarbeite ich die darin enthaltenen Daten ausschließlich zur Bearbeitung des Auftrags (Art. 6 Abs. 1 lit. b, c und e DSGVO). Gerichtliche Schriftstücke können besondere Kategorien personenbezogener Daten und Daten über Straftaten enthalten (Art. 9, Art. 10 DSGVO); diese werden ausschließlich im Rahmen der Heranziehung durch die jeweilige Stelle und unter Wahrung der Verschwiegenheitspflicht verarbeitet.</p>
  <h2>5. Speicherdauer</h2>
  <p>Übersetzungsunterlagen werden nach Abschluss des Auftrags gelöscht bzw. vernichtet, soweit keine gesetzlichen Aufbewahrungspflichten, insbesondere nach Handels- und Steuerrecht, entgegenstehen. Rechnungsdaten werden für die Dauer der gesetzlichen Fristen aufbewahrt.</p>
  <h2>6. Ihre Rechte</h2>
  <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch (Art. 15–21 DSGVO) sowie das Recht auf Beschwerde bei einer Datenschutz-Aufsichtsbehörde (Art. 77 DSGVO).</p>
  <h2>7. Sicherheit der E-Mail-Übermittlung</h2>
  <p>E-Mails werden transportverschlüsselt (TLS) übertragen, soweit Ihr Server dies unterstützt. Für besonders sensible Unterlagen kann auf Wunsch eine verschlüsselte Übermittlung vereinbart werden.</p>
  <p><em>Stand: {TODAY}</em></p>
</div>"""
    page("datenschutz.html", f"Datenschutz – {BRAND}", f"Datenschutzerklärung von {BRAND}: keine Cookies, kein Tracking, vertrauliche Verarbeitung gerichtlicher Schriftstücke.", ds, robots="noindex, follow")

    nf = f"""
<div class="wrap legal">
  <h1>Seite nicht gefunden</h1>
  <p>Die aufgerufene Adresse existiert nicht oder wurde verschoben. Wählen Sie die gewünschte Dokumentart oder senden Sie Ihr Schriftstück direkt.</p>
  <ul>{''.join(f'<li><a href="{d["slug"]}">{d["name"]}</a></li>' for d in DOCS)}</ul>
  <div class="btn-row"><a class="btn btn-primary" href="auftrag-kontakt.html">Auftrag erteilen</a><a class="btn btn-secondary" href="index.html">Zur Startseite</a></div>
</div>"""
    page("404.html", f"Seite nicht gefunden – {BRAND}", "Die angeforderte Seite wurde nicht gefunden.", nf, robots="noindex, follow")


def build_sitemap():
    urls = [("", "1.0", "weekly")]
    urls += [(d["slug"], "0.9", "monthly") for d in DOCS]
    urls += [("express-uebersetzung-24h.html", "0.8", "monthly"),
             ("beglaubigte-uebersetzung.html", "0.8", "monthly"),
             ("honorar-jveg.html", "0.8", "monthly"),
             ("dari-uebersetzer-fuer-uebersetzungsbueros.html", "0.8", "monthly"),
             ("auftrag-kontakt.html", "0.7", "yearly")]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, p, c in urls:
        xml.append(f"  <url><loc>{BASE}/{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>")
    xml.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")


if __name__ == "__main__":
    build_home()
    build_docs()
    build_service_pages()
    build_contact()
    build_agencies()
    build_legal()
    build_sitemap()
    print("Fertig:", len(DOCS) + 10, "Seiten erzeugt.")
