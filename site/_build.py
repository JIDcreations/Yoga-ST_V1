"""Builds the static site. Run from this folder: python3 _build.py
Pages keep the URLs of the original WordPress site (/voor-wie/, /onze-lessen/, ...) so search rankings carry over."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
MAIL = "info@yogagroepenpm.be"
TRIAL = f"mailto:{MAIL}?subject=Proefles%20aanvragen"
SIGNUP = f"mailto:{MAIL}?subject=Inschrijving%20yogajaar%202026-2027"
MAPS = "https://www.google.com/maps/search/?api=1&query=Heiveldstraat+350+9040+Sint-Amandsberg"

NAV = [("/voor-wie/", "Voor wie?"), ("/onze-lessen/", "Onze lessen"), ("/wie-zijn-we/", "Wie zijn we?"), ("/contact/", "Contact")]

# ------------------------------------------------------------------ logo (redrawn from the original YGPM mark)
PETALS = [
    "M77.04 44.57 Q93.90 30.27 100 8 Q106.10 30.27 122.96 44.57",
    "M122.96 44.57 Q145 46.38 165.05 34.95 Q153.62 55 155.43 77.04",
    "M155.43 77.04 Q169.73 93.90 192 100 Q169.73 106.10 155.43 122.96",
    "M155.43 122.96 Q153.62 145 165.05 165.05 Q145 153.62 122.96 155.43",
    "M122.96 155.43 Q106.10 169.73 100 192 Q93.90 169.73 77.04 155.43",
    "M77.04 155.43 Q55 153.62 34.95 165.05 Q46.38 145 44.57 122.96",
    "M44.57 122.96 Q30.27 106.10 8 100 Q30.27 93.90 44.57 77.04",
    "M44.57 77.04 Q46.38 55 34.95 34.95 Q55 46.38 77.04 44.57",
]
MONO = '<g fill="currentColor" stroke="none" font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="15" text-anchor="middle"><text x="100" y="95">YG</text><text x="83" y="118">P</text><text x="117" y="118">M</text></g>'


def logo_small():
    return f"""<svg width="40" height="40" viewBox="0 0 200 200" aria-hidden="true" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-linecap="round">
<path d="{' '.join(PETALS)}" stroke-width="7"/><circle cx="100" cy="100" r="60" stroke-width="5"/><path d="M48.04 70 L151.96 70 L100 160 Z" stroke-width="5"/></svg>"""


def logo_hero():
    petals = "".join(f'<path class="draw d1" pathLength="1" d="{d}"/>' for d in PETALS)
    return f"""<div class="hero-art" aria-hidden="true">
  <div class="sun"></div>
  <svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-linecap="butt">
    <circle class="draw d4" pathLength="1" cx="100" cy="100" r="97" stroke-width=".5"/>
    <g stroke-width="2.2">{petals}</g>
    <circle class="draw d2" pathLength="1" cx="100" cy="100" r="60" stroke-width="1.4"/>
    <path class="draw d3" pathLength="1" d="M48.04 70 L151.96 70 L100 160 Z" stroke-width="1.4"/>
    <rect class="draw d4" pathLength="1" x="72" y="74" width="56" height="52" stroke-width="1.1"/>
    {MONO}
  </svg>
</div>"""


# ------------------------------------------------------------------ chrome
def header(active, over_hero=False):
    cur = ' aria-current="page"'
    items = "".join(f'<li><a href="{h}"{cur if h == active else ""}>{t}</a></li>' for h, t in NAV)
    cls = "site-header is-over-hero" if over_hero else "site-header"
    return f"""<a class="skip" href="#main">Naar de inhoud</a>
<div class="scroll-sentinel" aria-hidden="true"></div>
<header class="{cls}">
  <div class="wrap nav">
    <a class="brand" href="/">{logo_small()}<span>Yoga Sint-Amandsberg<small>Yoga Groepen Piet Meyvaert</small></span></a>
    <nav aria-label="Hoofdmenu">
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
      <ul class="menu" id="menu">{items}<li><a class="btn" href="{TRIAL}">Proefles aanvragen</a></li></ul>
    </nav>
  </div>
</header>"""


def closing(title="Kom een les proberen."):
    pages = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("/", "Home")] + NAV)
    return f"""<section class="closing on-saffron" aria-labelledby="closing-title">
  <div class="wrap">
    <div class="closing-grid">
      <h2 id="closing-title">{title}</h2>
      <div>
        <p>In september kun je een proefles volgen, zolang er plaats is. Die kost &euro;&nbsp;6, te betalen aan de lesgever. Schrijf je daarna in, dan vervalt dat bedrag.</p>
        <a class="btn" href="{TRIAL}">Proefles aanvragen</a>
      </div>
    </div>
    <footer class="footer">
      <div><h3>Yoga Groepen Piet Meyvaert vzw</h3><p>Traditionele yoga in Sint-Amandsberg, sinds 1980.</p></div>
      <div><h3>Pagina&rsquo;s</h3><ul>{pages}</ul></div>
      <div><h3>Lessen</h3><ul><li>Heiveldstraat 350</li><li>9040 Sint-Amandsberg</li><li><a href="{MAPS}" target="_blank" rel="noopener">Route plannen</a></li></ul></div>
      <div><h3>Contact</h3><ul><li><a href="mailto:{MAIL}">{MAIL}</a></li></ul></div>
      <div class="footer-legal"><span>Maatschappelijke zetel: Magergoedkouter 22, 9041 Oostakker</span><span>Ondernemingsnummer 0420.501.532, RPR Gent</span></div>
    </footer>
  </div>
</section>"""


def page(path, title, desc, active, body, over_hero=False):
    html = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#d1711d">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
{header(active, over_hero)}
<main id="main">
{body}
</main>
<script src="/assets/main.js" defer></script>
</body>
</html>
"""
    # Relative paths so the site works both hosted and opened straight from disk (file://)
    prefix = "../" if path else ""
    html = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{prefix}', html)
    html = html.replace('href=""', 'href="./"')
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


# ------------------------------------------------------------------ shared blocks
DAYS = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"]
# (day, part, time, teacher, status label or None when full)
LESSONS = [
    ("Maandag", "avond", "19u00", "Griet Noels", None),
    ("Maandag", "avond", "20u30", "Griet Noels", None),
    ("Dinsdag", "avond", "18u45", "Ineke van Dam", None),
    ("Dinsdag", "avond", "20u15", "Luc Bulckaert", None),
    ("Woensdag", "ochtend", "10u00", "Johan Schamps", None),
    ("Woensdag", "avond", "18u45", "Johan Schamps", "Nog 1 plaats vrij"),
    ("Vrijdag", "ochtend", "10u00", "Anne Logiest", "Nog 8 plaatsen vrij"),
]


def lesson_html(day, part, time, who, status):
    cls = "lesson is-open" if status else "lesson is-full"
    label = status or "Volzet"
    return (f'<div class="{cls}"><time>{time}</time><span class="who">{who}</span>'
            f'<span class="status">{label}</span></div>')


def week():
    # DOM is day-major (reads well on mobile and for screen readers); desktop lays it out as columns.
    out = ['<div class="week" role="list" aria-label="Lesrooster per dag">',
           '<div class="week-day week-corner" aria-hidden="true"></div>',
           '<div class="week-part" aria-hidden="true">Ochtend</div>',
           '<div class="week-part week-row-end" aria-hidden="true">Avond</div>']
    for day in DAYS:
        items = {p: [l for l in LESSONS if l[0] == day and l[1] == p] for p in ("ochtend", "avond")}
        empty = not items["ochtend"] and not items["avond"]
        out.append(f'<div class="week-day{" is-empty-day" if empty else ""}" role="listitem">{day}</div>')
        for p in ("ochtend", "avond"):
            ls = items[p]
            end = " week-row-end" if p == "avond" else ""
            if ls:
                out.append(f'<div class="week-cell{end}">' + "".join(lesson_html(*l) for l in ls) + "</div>")
            elif empty and p == "ochtend":
                out.append(f'<div class="week-cell is-empty{end}"><span class="week-empty">Geen les</span></div>')
            else:
                out.append(f'<div class="week-cell is-empty{end}"></div>')
    out.append("</div>")
    return "\n".join(out)


SEQUENCE = [
    ("Lichaamsoefeningen en houdingen", "We werken de spanning in het lichaam weg. De spanning in je hoofd neemt vanzelf mee af."),
    ("Ademhaling", "Aandacht voor de adem tijdens elke oefening, en aparte ademhalingsoefeningen die het zenuwstelsel versterken."),
    ("Diepe ontspanning", "Van buiten naar binnen: lichaam en geest ontspannen tot in hun diepere lagen."),
    ("Concentratie en meditatie", "Leren loslaten, om tot innerlijke rust en vrede te komen."),
]


def sequence():
    return '<ol class="sequence">' + "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in SEQUENCE) + "</ol>"


TEAM = [
    ("griet", "Griet Noels", "Maandagavond"),
    ("ineke", "Ineke van Dam", "Dinsdagavond, eerste les"),
    ("luc", "Luc Bulckaert", "Dinsdagavond, tweede les"),
    ("johan", "Johan Schamps", "Woensdag"),
    ("anne", "Anne Logiest", "Vrijdagochtend"),
]


def team():
    return '<ul class="team">' + "".join(
        f'<li><img src="/assets/img/teacher-{k}.jpg" alt="Portret van {n}" width="640" height="800" loading="lazy"><h3>{n}</h3><p>{d}</p></li>'
        for k, n, d in TEAM) + "</ul>"


def room(heading_level="h2"):
    return f"""<section class="room" aria-labelledby="room-title">
  <img src="/assets/img/studio.jpg" alt="De yogazaal: kurkvloer, houten balken, gele muren en een rij witte matjes" width="1087" height="815" loading="lazy">
  <div class="room-card">
    <{heading_level} id="room-title">De blokhut achter de bibliotheek</{heading_level}>
    <p>Heiveldstraat 350, 9040 Sint-Amandsberg. Met de bus: lijn 12a of 12b, halte Vinkenlaan.</p>
    <p><a class="accent-link" href="{MAPS}" target="_blank" rel="noopener">Route plannen</a></p>
  </div>
</section>"""


SCHEDULE_INTRO = "Van maandag 7 september 2026 tot vrijdag 18 juni 2027. Geen les tijdens de schoolvakanties en op wettelijke feestdagen."

# ------------------------------------------------------------------ Home
page("", "Yoga Sint-Amandsberg | Yoga Groepen Piet Meyvaert",
     "Traditionele yoga in Sint-Amandsberg sinds 1980. Eenvoudige, rustige lessen voor iedereen in de blokhut achter de bibliotheek.",
     "/", f"""
<section class="hero on-saffron">
  {logo_hero()}
  <div class="wrap">
    <div class="hero-copy">
      <h1>Op je beide voeten leren staan.</h1>
      <p>Traditionele yoga in Sint-Amandsberg, sinds 1980. Eenvoudig, rustig en voor iedereen.</p>
      <div class="hero-actions">
        <a class="btn" href="#lesrooster">Bekijk het lesrooster</a>
        <a class="text-link" href="{TRIAL}">Proefles aanvragen</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="lesrooster" aria-labelledby="rooster-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="rooster-title">Lesrooster 2026-2027</h2>
      <p>{SCHEDULE_INTRO}</p>
    </div>
    {week()}
    <p class="week-note">Een jaar yoga kost &euro;&nbsp;180. <a class="accent-link" href="/onze-lessen/">Zo schrijf je in</a></p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="iedereen-title">
  <div class="wrap feature">
    <figure><img src="/assets/img/class-seniors.jpg" alt="Een groep oudere cursisten strekt de armen boven het hoofd tijdens een les" width="1800" height="1012" loading="lazy"></figure>
    <div class="feature-copy">
      <h2 id="iedereen-title">Yoga is voor iedereen.</h2>
      <p>Jong of oud, soepel of stijf: de oefeningen zijn eenvoudig en iedereen doet ze op zijn eigen manier. Yoga wordt vaak acrobatisch voorgesteld. Bij ons blijft het eenvoudig.</p>
      <p><a class="accent-link" href="/voor-wie/">Wat is yoga, en voor wie?</a></p>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="les-title">
  <div class="wrap">
    <div class="section-head"><h2 id="les-title">Zo verloopt een les</h2></div>
    {sequence()}
  </div>
</section>

{room()}

<section class="section" aria-labelledby="team-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="team-title">Onze lesgevers</h2>
      <p>Vijf ervaren lesgevers, elk met een vast moment in de week.</p>
    </div>
    {team()}
  </div>
</section>

{closing()}
""", over_hero=True)

# ------------------------------------------------------------------ Voor wie?
page("voor-wie", "Wat is yoga, en voor wie? | Yoga Sint-Amandsberg",
     "Traditionele yoga: lichaamshoudingen, ademhaling, diepe ontspanning en meditatie. Eenvoudig en geschikt voor iedereen, jong of oud.",
     "/voor-wie/", f"""
<section class="page-head">
  <div class="wrap">
    <h1>Wat is yoga, en voor wie?</h1>
    <p class="lede">Een oeroude wetenschap die je de middelen geeft om zelf zorg te dragen voor je lichamelijke, geestelijke en spirituele welzijn.</p>
  </div>
</section>

<figure class="wide-photo"><img src="/assets/img/group-meditation.jpg" alt="Een groep mensen van verschillende leeftijden mediteert met de handen voor de borst" width="1800" height="1012"></figure>

<section class="section">
  <div class="wrap prose-grid">
    <h2>Terug naar je ware natuur</h2>
    <div class="measure">
      <p>Yoga gaat ervan uit dat we allemaal lijden aan vereenzelviging: we denken dat we ons lichaam zijn, of onze geest. Daardoor lijden we aan allerlei kwalen, zowel lichamelijke als psychische.</p>
      <p>Yoga probeert die verstoring te doorbreken en ons terug te brengen tot onze ware natuur. Praktisch gezien streeft echte yoga naar &eacute;&eacute;n ding: het vermogen om altijd kalm en evenwichtig te zijn.</p>
    </div>
  </div>
</section>

<section class="statement on-saffron">
  <div class="wrap">
    <blockquote>
      <p>&ldquo;Het doel van yoga is de mens te herstellen in zijn oorspronkelijke staat van volmaakte zaligheid.&rdquo;</p>
      <cite>Swami Chidananda</cite>
    </blockquote>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose-grid" style="margin-bottom:var(--space-m)">
      <h2>Hoe doen we dat?</h2>
      <div class="measure">
        <p>We ontspannen lichaam en geest volledig, om ruimte te geven aan wie we echt zijn. Wie de fysieke spanning wegwerkt, ziet de psychische spanning vanzelf afnemen. Dat eenvoudige principe is ook wetenschappelijk aangetoond.</p>
        <p class="muted">Alle oefeningen zijn uiteindelijk een middel: je leert lichaam en geest loslaten, om via concentratie en meditatie tot innerlijke rust te komen. Elke les bestaat uit vier delen.</p>
      </div>
    </div>
    {sequence()}
  </div>
</section>

<section class="section" style="padding-top:0" id="voor-wie">
  <div class="wrap feature">
    <figure><img src="/assets/img/relaxation.jpg" alt="Iemand ligt ontspannen op de rug op een yogamat" width="1800" height="1200" loading="lazy"></figure>
    <div class="feature-copy">
      <h2>Yoga is geschikt voor iedereen.</h2>
      <p>De meeste oefeningen zijn eenvoudig. Jong of oud, ieder met zijn eigen beperkingen doet ze op een aangepaste manier.</p>
      <p>Yoga wordt vaak nogal acrobatisch voorgesteld. Bij ons is het eerder eenvoudig: niet op je hoofd leren staan, maar op je beide voeten.</p>
      <p><a class="accent-link" href="/onze-lessen/">Bekijk het lesrooster</a></p>
    </div>
  </div>
</section>

{closing()}
""")

# ------------------------------------------------------------------ Onze lessen
page("onze-lessen", "Onze lessen | Yoga Sint-Amandsberg",
     "Lesrooster 2026-2027, prijs, inschrijving en praktische info voor de yogalessen van YGPM in Sint-Amandsberg.",
     "/onze-lessen/", f"""
<section class="page-head">
  <div class="wrap">
    <h1>Onze lessen</h1>
    <p class="lede">Zeven lessen per week, verspreid over vier dagen, in een rustige zaal in Sint-Amandsberg.</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="Lesrooster">
  <div class="wrap">
    {week()}
    <p class="week-note">{SCHEDULE_INTRO}</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="inschrijven-title">
  <div class="wrap">
    <div class="section-head"><h2 id="inschrijven-title">Inschrijven</h2></div>
    <div class="facts">
      <div>
        <h3>Prijs en betaling</h3>
        <dl>
          <div><dt class="price">&euro;&nbsp;180</dt><dd>voor het hele yogajaar 2026-2027</dd></div>
          <div><dt>Rekeningnummer</dt><dd>BE43 3900 4014 2901<br>Yoga Groepen Piet Meyvaert</dd></div>
          <div><dt>Verzekering</dt><dd>Wie correct ingeschreven is, is automatisch verzekerd via YGPM.</dd></div>
        </dl>
      </div>
      <div>
        <h3>Zo schrijf je in</h3>
        <dl>
          <div><dt>Stuur een mail</dt><dd>naar <a class="accent-link" href="{SIGNUP}">{MAIL}</a> met je naam en de les die je wil volgen.</dd></div>
          <div><dt>Eerst proberen?</dt><dd>In september 2026 kun je een proefles aanvragen, zolang er plaats is. Je betaalt &euro;&nbsp;6 aan de lesgever. Schrijf je daarna in, dan vervalt dat bedrag.</dd></div>
        </dl>
        <p style="margin-top:28px"><a class="btn" href="{SIGNUP}">Inschrijven via mail</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" id="praktisch" aria-labelledby="praktisch-title">
  <div class="wrap feature">
    <figure><img src="/assets/img/hands.jpg" alt="Handen rusten op de knie&euml;n in kleermakerszit" width="1400" height="1050" loading="lazy"></figure>
    <div class="feature-copy">
      <h2 id="praktisch-title">Goed om te weten</h2>
      <p><strong>Kledij en materiaal.</strong> Draag gemakkelijke, loszittende kledij. Breng best een matje en een stevige handdoek mee. Gebruik je een matje van de zaal, dan is een handdoek of plaid verplicht.</p>
      <p><strong>Stilte.</strong> Bij het binnenkomen van de zaal vragen we je de stilte te bewaren.</p>
      <p><strong>Vakanties.</strong> De lessen lopen van september tot en met juni en volgen de schoolvakanties.</p>
    </div>
  </div>
</section>

{room()}

{closing()}
""")

# ------------------------------------------------------------------ Wie zijn we?
page("wie-zijn-we", "Wie zijn we? | Yoga Sint-Amandsberg",
     "Yoga Groepen Piet Meyvaert werd in 1980 opgericht. Maak kennis met onze vijf lesgevers en het bestuur.",
     "/wie-zijn-we/", f"""
<section class="page-head">
  <div class="wrap">
    <h1>Wie zijn we?</h1>
    <p class="lede">Yoga Groepen Piet Meyvaert is een vzw, in 1980 opgericht door Piet Meyvaert. Sinds zijn overlijden in 2006 draagt de vereniging zijn naam.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap prose-grid">
    <h2>Niet op je hoofd, maar op je beide voeten</h2>
    <div class="measure">
      <p>YGPM volgt de traditionele yogaleer. Yoga is voor ons niet op je hoofd leren staan, maar op je beide voeten leren staan.</p>
      <p>De yogahoudingen (asana&rsquo;s) zijn geen doel op zich. Ze zijn het middel om door te dringen tot het wezen van yoga: de vereniging van de yogi met zijn wezenlijke staat van bestaan, bewustzijn en zaligheid.</p>
      <p class="muted">Daarom gaat er in elke les veel aandacht naar de ademhaling, de verbinding tussen lichaam en geest. Het resultaat is een ontspannen lichaam en een ontspannen geest, voor jong en oud.</p>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="team-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="team-title">Onze lesgevers</h2>
      <p>Voor de lessen rekent YGPM op vijf ervaren lesgevers.</p>
    </div>
    {team()}
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="bestuur-title">
  <div class="wrap">
    <div class="section-head"><h2 id="bestuur-title">Bestuur</h2></div>
    <ul class="board">
      <li><strong>Anne Morez</strong><span>Bestuurster</span></li>
      <li><strong>Johan Schamps</strong><span>Bestuurder</span></li>
      <li><strong>Mariejeanne Dirkx</strong><span>Bestuurster</span></li>
      <li><strong>Peter Willequet</strong><span>Bestuurder</span></li>
    </ul>
  </div>
</section>

{closing()}
""")

# ------------------------------------------------------------------ Contact
page("contact", "Contact | Yoga Sint-Amandsberg",
     "Vragen over de yogalessen van YGPM in Sint-Amandsberg? Mail naar info@yogagroepenpm.be.",
     "/contact/", f"""
<section class="page-head">
  <div class="wrap">
    <h1>Contact</h1>
    <p class="lede">Vragen over de lessen? Mail ons tijdens het yogajaar, we antwoorden zo snel mogelijk.</p>
    <p style="margin-top:var(--space-m)"><a class="mail-big" href="mailto:{MAIL}">{MAIL}</a></p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap facts">
    <div>
      <h2 class="facts-title">Waar de lessen doorgaan</h2>
      <dl>
        <div><dt>Blokhut achter de bibliotheek</dt><dd>Heiveldstraat 350<br>9040 Sint-Amandsberg</dd></div>
        <div><dt>Met de bus</dt><dd>Lijn 12a of 12b, halte Vinkenlaan</dd></div>
        <div><dd><a class="accent-link" href="{MAPS}" target="_blank" rel="noopener">Route plannen</a></dd></div>
      </dl>
    </div>
    <div>
      <h2 class="facts-title">De vereniging</h2>
      <dl>
        <div><dt>Yoga Groepen Piet Meyvaert vzw</dt><dd>Maatschappelijke zetel: Magergoedkouter 22, 9041 Oostakker</dd></div>
        <div><dt>Ondernemingsnummer</dt><dd>0420.501.532, RPR Gent, afdeling Gent</dd></div>
      </dl>
    </div>
  </div>
</section>

{closing()}
""")

# ------------------------------------------------------------------ Redirects for the old blog-post URLs
for old in ["stilte", "de-lessen", "yogafeest"]:
    d = ROOT / old
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(
        '<!doctype html><html lang="nl"><head><meta charset="utf-8"><title>Doorverwijzing</title>'
        '<link rel="canonical" href="../onze-lessen/#praktisch"><meta http-equiv="refresh" content="0; url=../onze-lessen/#praktisch">'
        '</head><body><p><a href="../onze-lessen/#praktisch">Ga naar onze lessen</a></p></body></html>', encoding="utf-8")

print("built")
