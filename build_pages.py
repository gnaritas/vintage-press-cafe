#!/usr/bin/env python3
"""Vintage Press Café (Granby CT) — 10-page letterpress-aesthetic site generator.
Single source for all pages; pins the -demo Railway host (canonical/OG/sitemap).
Facts ONLY from card t_b174a69b sources: Patch opening article (hours 7a-2p daily,
address 256 Salmon Brook St, "specialty coffee, loose-leaf tea, breakfast and lunch",
owners' FB quotes), CT Bites Nov-2026 openings (former print shop building, drinks
named after influential women, tagline), OSM node 8474504457 (06035, geo, Granby
Center Historic District), own FB Page (email hello@vintagepresscafe.com self-published).
No phone published -> none on site. No owner names published -> none on site.
No menu items/prices published -> none invented."""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")
ORIGIN = "https://vintage-press-cafe-demo.up.railway.app"
TODAY = datetime.date.today().isoformat()
NAME = "Vintage Press Café"
ADDR1 = "256 Salmon Brook Street"
CITY = "Granby"
STATE = "CT"
ZIP = "06035"
EMAIL = "hello@vintagepresscafe.com"
FB = "https://www.facebook.com/p/Vintage-Press-Caf%C3%A9-61588384241721/"
LAT, LON = 41.9526292, -72.7890159
NAP = f"{ADDR1}, {CITY}, {STATE} {ZIP}"
HOURS_LINE = "Open every day, 7 a.m. to 2 p.m."
MAPSRC = "https://www.google.com/maps?q=256+Salmon+Brook+Street,+Granby,+CT+06035&output=embed"

# ---------------------------------------------------------------- JSON-LD
CAFE = {
    "@type": "CafeRestaurant",
    "@id": ORIGIN + "/#cafe",
    "name": NAME,
    "image": ORIGIN + "/og.png",
    "url": ORIGIN + "/",
    "description": ("Granby's new specialty café — coffee, loose-leaf tea, breakfast and lunch, "
                    "open daily 7 a.m. to 2 p.m. at 256 Salmon Brook Street."),
    "address": {
        "@type": "PostalAddress",
        "streetAddress": ADDR1, "addressLocality": CITY,
        "addressRegion": "CT", "postalCode": ZIP, "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "07:00", "closes": "14:00",
    }],
    "email": EMAIL,
    "sameAs": [FB],
    "hasMenu": {"@id": ORIGIN + "/menu#menu"},
}
WEBSITE = {
    "@type": "WebSite",
    "@id": ORIGIN + "/#website",
    "name": NAME, "url": ORIGIN + "/", "inLanguage": "en",
    "publisher": {"@id": ORIGIN + "/#cafe"},
}

MENU_GRAPH = {
    "@context": "https://schema.org", "@type": "Menu",
    "@id": ORIGIN + "/menu#menu",
    "name": "Vintage Press Café Menu",
    "url": ORIGIN + "/menu",
    "inLanguage": "en",
    "hasMenuSection": [
        {"@type": "MenuSection", "name": "Specialty Coffee",
         "description": "Specialty coffee, every day until 2 p.m."},
        {"@type": "MenuSection", "name": "Loose-Leaf Tea",
         "description": "Loose-leaf tea, steeped all day."},
        {"@type": "MenuSection", "name": "Breakfast",
         "description": "Breakfast from 7 a.m. daily."},
        {"@type": "MenuSection", "name": "Lunch",
         "description": "Lunch served until 2 p.m."},
    ],
}

def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                 "name": n, "item": ORIGIN + p}
                                for i, (n, p) in enumerate(items)]}

def service_node(svc_type, name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service",
            "serviceType": svc_type, "name": name, "description": desc, "url": url,
            "areaServed": {"@type": "City", "name": CITY},
            "provider": {"@id": ORIGIN + "/#cafe"}}

FAQ_ITEMS = [
    ("When are you open?", "Every day, 7 a.m. to 2 p.m."),
    ("What do you serve?", "Specialty coffee, loose-leaf tea, breakfast, and lunch."),
    ("Why are your drinks named after women?", "Every drink on our menu is named after an influential woman from history."),
    ("Where exactly are you?", "256 Salmon Brook Street, Granby, CT 06035 — in Granby Center Historic District."),
    ("Can I email you?", f"Of course — {EMAIL}."),
]
FAQ_GRAPH = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q,
                             "acceptedAnswer": {"@type": "Answer", "text": a}}
                            for q, a in FAQ_ITEMS]}

# ---------------------------------------------------------------- shared chrome
NAV = [("Menu", "/menu"), ("Our Story", "/our-story"), ("Visit", "/visit"), ("Contact", "/contact")]

def navlinks(path):
    out = []
    for n, p in [("Home", "/")] + NAV:
        cls = ' class="navlink on"' if p == path else ' class="navlink"'
        out.append('        <a' + cls + ' href="' + p + '">' + n + '</a>\n')
    return "".join(out)

def head(title, desc, path, lds, utility=False):
    ld_blocks = "\n".join(
        '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False) + "</script>"
        for g in lds)
    og = ("" if utility else f"""  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{ORIGIN}{path}">
  <meta property="og:image" content="{ORIGIN}/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{ORIGIN}/og.png">
""")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{ORIGIN}{path}">
{og}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
{ld_blocks}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="strip">Open every day &middot; 7 a.m.&ndash;2 p.m. &middot; {ADDR1}, {CITY}, {STATE} &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div class="navbar">
    <div class="container navrow">
      <a class="brand" href="/"><span class="brandname">{NAME}</span><span class="brandsub">Granby &middot; Connecticut</span></a>
      <nav aria-label="Main">
{navlinks(path)}      </nav>
    </div>
  </div>
</header>
<main id="main">
"""

FOOTER = """</main>
<footer>
  <div class="container footgrid">
    <div class="fcol">
      <p class="fbrand">{NAME}</p>
      <p class="ftag">Vintage vibes. Modern brews.</p>
    </div>
    <div class="fcol">
      <p class="fkick">Find us</p>
      <p>{ADDR1}<br>{CITY}, {STATE} {ZIP}</p>
      <p class="fhours">Open daily 7 a.m.&ndash;2 p.m.</p>
    </div>
    <div class="fcol">
      <p class="fkick">Talk to us</p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><a href="{FB}" rel="noopener">Facebook</a></p>
    </div>
  </div>
  <div class="container footline"><p>{NAME} &middot; {ADDR1}, {CITY}, {STATE} {ZIP}</p></div>
</footer>
</body>
</html>
""".format(NAME=NAME, EMAIL=EMAIL, FB=FB, ADDR1=ADDR1, CITY=CITY, STATE=STATE, ZIP=ZIP)

def plate_cards(cards):
    out = []
    for kicker, title, line, link in cards:
        out.append(f"""      <div class="plate-card">
        <p class="kicker">{kicker}</p>
        <h3>{title}</h3>
        <p>{line}</p>
        <a class="more" href="{link}">Details &rarr;</a>
      </div>""")
    return "\n".join(out)

def crumbs(items):
    parts = ' <span class="sep">/</span> '.join(
        f'<a href="{p}">{n}</a>' if p != "/" or n == "Home" else f'<a href="{p}">{n}</a>'
        for n, p in items)
    return f'      <nav class="crumbs" aria-label="Breadcrumb">{parts}</nav>\n'

# ---------------------------------------------------------------- pages
PAGES = {}

PAGES["index.html"] = ("/", f"{NAME} — Specialty Coffee, Tea, Breakfast & Lunch | Granby CT",
    "Granby's new specialty café: coffee, loose-leaf tea, breakfast and lunch, open daily 7 a.m. to 2 p.m. in a historic former print shop at 256 Salmon Brook Street.",
    [CAFE, WEBSITE], f"""  <section class="hero">
    <div class="container">
      <div class="frame">
        <p class="platemark">No. 256 Salmon Brook &middot; Granby, Connecticut &middot; Opened November 2026</p>
        <h1>Vintage vibes.<br><em>Modern brews.</em></h1>
        <p class="lead">Granby's new café — specialty coffee, loose-leaf tea, and real breakfast and lunch, served daily from 7 a.m. to 2 p.m. in a historic building that once ran as a print shop.</p>
        <p class="ctarow"><a class="btn" href="/menu">See the menu</a> <a class="btn ghost" href="/visit">Visit &amp; directions</a></p>
      </div>
    </div>
  </section>
  <section class="band">
    <div class="container">
      <p class="kicker">The Menu</p>
      <h2>Coffee, tea, breakfast, lunch.</h2>
      <div class="plates">
{plate_cards([
    ("Coffee", "Specialty coffee", "Every day, 7 a.m. until 2 p.m.", "/coffee-and-tea"),
    ("Tea", "Loose-leaf tea", "Steeped all day, never in a hurry.", "/coffee-and-tea"),
    ("Breakfast", "Breakfast", "From 7 a.m., every single day.", "/breakfast-and-lunch"),
    ("Lunch", "Lunch", "Served until 2 p.m. — weekends too.", "/breakfast-and-lunch"),
])}
      </div>
    </div>
  </section>
  <section class="redband">
    <div class="container">
      <h2>Named for women who made history.</h2>
      <p>Every drink on our menu carries the name of an influential woman from history. It's our nod to the women who set things in motion — and it makes for good conversation while you wait for your cup.</p>
    </div>
  </section>
  <section class="quote">
    <div class="container">
      <blockquote>&ldquo;The wait is over, we are open!!&rdquo;</blockquote>
      <cite>The makers of {NAME}, announcing opening on <a href="{FB}" rel="noopener">Facebook</a></cite>
    </div>
  </section>
  <section class="band">
    <div class="container twocol">
      <div>
        <p class="kicker">The Room</p>
        <h2>A print shop, reborn.</h2>
        <p>Our building spent its first life as a working print shop on Salmon Brook Street. The name keeps that alive: impressions made carefully, in the same room that once set type.</p>
        <p><a class="more" href="/our-story">Read our story &rarr;</a></p>
      </div>
      <div class="visitcard">
        <p class="kicker">Visit</p>
        <h3>{ADDR1}</h3>
        <p>{CITY}, {STATE} {ZIP}</p>
        <p class="hours">Open every day<br>7 a.m. &ndash; 2 p.m.</p>
        <p><a class="more" href="/visit">Directions &amp; map &rarr;</a></p>
      </div>
    </div>
  </section>
""")

PAGES["menu.html"] = ("/menu", f"The Menu — {NAME}, {CITY} {STATE}",
    "Specialty coffee, loose-leaf tea, breakfast and lunch at Vintage Press Café, Granby CT — served daily 7 a.m. to 2 p.m. Every drink is named after an influential woman from history.",
    [MENU_GRAPH, breadcrumb([("Home", "/"), ("Menu", "/menu")])], f"""  <section class="pagehead">
    <div class="container">
{crumbs([("Home", "/"), ("Menu", "/menu")])}      <p class="kicker">The Menu</p>
      <h1>The menu</h1>
      <p class="lead">Coffee, tea, breakfast, and lunch — served daily from 7 a.m. to 2 p.m. Every drink on our menu is named after an influential woman from history. Ask about the names when you visit.</p>
    </div>
  </section>
  <section class="band">
    <div class="container">
      <div class="plates">
{plate_cards([
    ("Daily", "Specialty coffee", "Every day, 7 a.m. until 2 p.m.", "/coffee-and-tea"),
    ("Daily", "Loose-leaf tea", "Steeped all day, never in a hurry.", "/coffee-and-tea"),
    ("Daily", "Breakfast", "From 7 a.m., every single day.", "/breakfast-and-lunch"),
    ("Daily", "Lunch", "Served until 2 p.m. — weekends too.", "/breakfast-and-lunch"),
])}
      </div>
      <p class="fineprint">Open every day, 7 a.m. to 2 p.m. — {ADDR1}, {CITY}, {STATE} {ZIP}.</p>
    </div>
  </section>
""")

PAGES["coffee-and-tea.html"] = ("/coffee-and-tea", f"Specialty Coffee &amp; Loose-Leaf Tea — {NAME}, {CITY} {STATE}",
    "Specialty coffee and loose-leaf tea at Vintage Press Café, Granby CT — served every day from 7 a.m. to 2 p.m., with drinks named after influential women from history.",
    [service_node("CoffeeShop", "Specialty coffee & loose-leaf tea",
                 "Specialty coffee and loose-leaf tea, served daily 7 a.m. to 2 p.m. at 256 Salmon Brook Street, Granby, CT.",
                 ORIGIN + "/coffee-and-tea"),
     breadcrumb([("Home", "/"), ("Menu", "/menu"), ("Coffee & Tea", "/coffee-and-tea")])], f"""  <section class="pagehead">
    <div class="container">
{crumbs([("Home", "/"), ("Menu", "/menu"), ("Coffee & Tea", "/coffee-and-tea")])}      <p class="kicker">Coffee &amp; Tea</p>
      <h1>Specialty coffee &amp; loose-leaf tea</h1>
      <p class="lead">We brew specialty coffee, and we take tea seriously too — leaves, not bags, steeped to order.</p>
    </div>
  </section>
  <section class="band">
    <div class="container narrow">
      <h2>The coffee</h2>
      <p>Specialty coffee, from open to close: hot, iced, or whatever the bar tells you to try. Served every day between 7 a.m. and 2 p.m.</p>
      <h2>The tea</h2>
      <p>Loose-leaf tea all day long — measured, steeped, and poured while you settle in.</p>
      <h2>Named for history-makers</h2>
      <p>Every drink on our menu — coffee and tea alike — carries the name of an influential woman from history. Ask about the names while you wait; they're good conversation.</p>
      <p class="ctarow"><a class="btn" href="/contact">Ask us anything</a> <a class="btn ghost" href="/breakfast-and-lunch">Breakfast &amp; lunch &rarr;</a></p>
    </div>
  </section>
""")

PAGES["breakfast-and-lunch.html"] = ("/breakfast-and-lunch", f"Breakfast &amp; Lunch — {NAME}, {CITY} {STATE}",
    "Breakfast from 7 a.m. and lunch until 2 p.m., every day at Vintage Press Café, 256 Salmon Brook Street, Granby CT.",
    [service_node("FoodService", "Breakfast & lunch",
                 "Breakfast from 7 a.m. and lunch until 2 p.m., served every day at 256 Salmon Brook Street, Granby, CT.",
                 ORIGIN + "/breakfast-and-lunch"),
     breadcrumb([("Home", "/"), ("Menu", "/menu"), ("Breakfast & Lunch", "/breakfast-and-lunch")])], f"""  <section class="pagehead">
    <div class="container">
{crumbs([("Home", "/"), ("Menu", "/menu"), ("Breakfast & Lunch", "/breakfast-and-lunch")])}      <p class="kicker">Breakfast &amp; Lunch</p>
      <h1>Breakfast to lunch, every day</h1>
      <p class="lead">Breakfast starts at 7 a.m. and we keep serving through lunch until 2 p.m. — seven days a week.</p>
    </div>
  </section>
  <section class="band">
    <div class="container narrow">
      <h2>Mornings</h2>
      <p>Coffee in hand, something hot on the table, no rush. The early shift is ours — doors open at 7 a.m., even on weekends.</p>
      <h2>Noon</h2>
      <p>The same room that starts your morning also feeds you lunch. Stay for the afternoon — we're open until 2 p.m. and the coffee stays hot.</p>
      <h2>Any day will do</h2>
      <p>Open every single day, {HOURS_LINE.lower()}. Pull up a chair before the morning crowd or slip in at midday.</p>
      <p class="ctarow"><a class="btn" href="/contact">Ask us anything</a> <a class="btn ghost" href="/coffee-and-tea">Coffee &amp; tea &rarr;</a></p>
    </div>
  </section>
""")

PAGES["our-story.html"] = ("/our-story", f"Our Story — {NAME}, {CITY} {STATE}",
    "Vintage Press Café opened in November 2026 in a historic Granby building that once ran as a print shop — specialty coffee, loose-leaf tea, breakfast and lunch.",
    [{"@context": "https://schema.org", "@type": "AboutPage", "name": f"Our Story — {NAME}",
      "url": ORIGIN + "/our-story", "about": {"@id": ORIGIN + "/#cafe"}, "inLanguage": "en"},
     breadcrumb([("Home", "/"), ("Our Story", "/our-story")])], f"""  <section class="pagehead">
    <div class="container">
{crumbs([("Home", "/"), ("Our Story", "/our-story")])}      <p class="kicker">Our Story</p>
      <h1>A print shop, reborn.</h1>
      <p class="lead">{NAME} opened in November 2026 at {ADDR1} — a historic {CITY} building that spent its first life as a working print shop.</p>
    </div>
  </section>
  <section class="band">
    <div class="container narrow">
      <h2>Why &ldquo;Vintage Press&rdquo;</h2>
      <p>The name came from the walls. Salmon Brook Street runs through Granby Center Historic District — the district named for the town's old village center — and this building made its living in printing long before it made ours. A press makes careful impressions, one at a time. So do we, just with coffee instead of ink.</p>
      <h2>The menu has a memory too</h2>
      <p>Every drink is named after an influential woman from history — our nod to the women who set things in motion. The building remembers presses; the menu remembers the women who made history move.</p>
      <h2>Fresh out of the gate</h2>
      <blockquote>&ldquo;We are so excited to finally welcome you to {NAME}!&rdquo;</blockquote>
      <cite class="inline">— the café team, on its first week on <a href="{FB}" rel="noopener">Facebook</a></cite>
      <p>Follow along there for hours, menu news, and whatever we're pouring next.</p>
      <p class="ctarow"><a class="btn" href="/visit">Visit &amp; directions</a> <a class="btn ghost" href="/menu">See the menu &rarr;</a></p>
    </div>
  </section>
""")

VISIT_FAQ = "\n".join(
    f'      <div class="faq"><p class="fq">{q}</p><p class="fa">{a}</p></div>'
    for q, a in FAQ_ITEMS)
PAGES["visit.html"] = ("/visit", f"Visit — Hours, Directions &amp; Map — {NAME}, {CITY} {STATE}",
    "Vintage Press Café is open every day 7 a.m. to 2 p.m. at 256 Salmon Brook Street, Granby, CT 06035 — map, hours, and answers to common questions.",
    [{"@context": "https://schema.org", "@type": "WebPage", "name": f"Visit — {NAME}",
      "url": ORIGIN + "/visit", "inLanguage": "en"},
     FAQ_GRAPH, breadcrumb([("Home", "/"), ("Visit", "/visit")])], f"""  <section class="pagehead">
    <div class="container">
{crumbs([("Home", "/"), ("Visit", "/visit")])}      <p class="kicker">Visit</p>
      <h1>Find us on Salmon Brook.</h1>
      <p class="lead">{HOURS_LINE} at {ADDR1}, {CITY}, {STATE} {ZIP} — inside Granby Center Historic District.</p>
    </div>
  </section>
  <section class="band">
    <div class="container twocol">
      <div>
        <h2>Hours</h2>
        <dl class="hourslist">
          <dt>Monday to Sunday</dt><dd>7 a.m. &ndash; 2 p.m.</dd>
        </dl>
        <h2>Address</h2>
        <p>{ADDR1}<br>{CITY}, {STATE} {ZIP}</p>
        <h2>Email</h2>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <h2>Social</h2>
        <p><a href="{FB}" rel="noopener">Follow us on Facebook</a></p>
        <p class="fineprint">Hours as listed at opening; the Facebook page carries any changes.</p>
      </div>
      <div>
        <div class="mapwrap">
          <iframe src="{MAPSRC}" title="Map showing {NAME} at {ADDR1}, {CITY}, {STATE}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        <p class="fineprint">Salmon Brook Street runs through Granby Center Historic District, the district named for the town's old village center.</p>
      </div>
    </div>
  </section>
  <section class="band">
    <div class="container narrow">
      <p class="kicker">Good to know</p>
      <h2>Questions, answered</h2>
{VISIT_FAQ}
    </div>
  </section>
""")

PAGES["contact.html"] = ("/contact", f"Contact — {NAME}, {CITY} {STATE}",
    "Contact Vintage Press Café in Granby CT: send a note through the form or email hello@vintagepresscafe.com. Open daily 7 a.m. to 2 p.m.",
    [{"@context": "https://schema.org", "@type": "ContactPage", "name": f"Contact — {NAME}",
      "url": ORIGIN + "/contact", "inLanguage": "en"},
     breadcrumb([("Home", "/"), ("Contact", "/contact")])], f"""  <section class="pagehead">
    <div class="container">
{crumbs([("Home", "/"), ("Contact", "/contact")])}      <p class="kicker">Contact</p>
      <h1>Say hello.</h1>
      <p class="lead">Questions about hours, the menu, or a table for the morning crew? Write to us — we read everything.</p>
    </div>
  </section>
  <section class="band">
    <div class="container twocol">
      <div>
        <form class="cform" method="post" action="/contact">
          <p class="field"><label for="f-name">Name<input id="f-name" name="name" type="text" maxlength="120" required></label></p>
          <p class="field"><label for="f-phone">Phone <span class="opt">(optional)</span><input id="f-phone" name="phone" type="tel" maxlength="60"></label></p>
          <p class="field"><label for="f-email">Email <span class="opt">(optional)</span><input id="f-email" name="email" type="email" maxlength="120"></label></p>
          <p class="field"><label for="f-msg">Message<textarea id="f-msg" name="message" rows="5" maxlength="4000" required></textarea></label></p>
          <p><button class="btn" type="submit">Send message</button></p>
        </form>
      </div>
      <div>
        <h2>Other ways</h2>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p><a href="{FB}" rel="noopener">Message us on Facebook</a></p>
        <h2>Find us</h2>
        <p>{ADDR1}<br>{CITY}, {STATE} {ZIP}</p>
        <p class="hours">{HOURS_LINE}</p>
      </div>
    </div>
  </section>
""")

PAGES["privacy.html"] = ("/privacy", f"Privacy — {NAME}, {CITY} {STATE}",
    "How Vintage Press Café handles the information you send through this site: form details only, no cookies, no trackers, no selling.",
    [{"@context": "https://schema.org", "@type": "WebPage", "name": f"Privacy — {NAME}",
      "url": ORIGIN + "/privacy", "inLanguage": "en"}], f"""  <section class="pagehead">
    <div class="container">
      <p class="kicker">Fine Print</p>
      <h1>Privacy</h1>
      <p class="lead">Short version: this site collects only what you choose to send us.</p>
    </div>
  </section>
  <section class="band">
    <div class="container narrow">
      <h2>What we collect</h2>
      <p>The contact form asks for your name, and optionally your phone and email, plus your message. We use it for one thing only: answering you.</p>
      <h2>No trackers</h2>
      <p>This site sets no cookies of its own, runs no analytics, and loads no third-party scripts. Pages that show a location map load Google Maps inside a frame, and Google may set its own cookies there — see <a href="https://policies.google.com/privacy" rel="noopener">Google's privacy policy</a>.</p>
      <h2>Where your message goes</h2>
      <p>Form messages are delivered straight to the café's inbox, and only the café team reads them. Ask and we'll delete yours: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <p class="fineprint">Last updated {TODAY}.</p>
    </div>
  </section>
""")

PAGES["thanks.html"] = ("/thanks", f"Thank You — {NAME}, {CITY} {STATE}",
    "Thanks for reaching out to Vintage Press Café in Granby CT — we'll answer as soon as we can.",
    [], f"""  <section class="pagehead">
    <div class="container center">
      <p class="kicker">Received</p>
      <h1>Your message is on its way.</h1>
      <p class="lead">Thank you for writing. We'll answer by email or Facebook as soon as we can — usually the same day we're open, 7 a.m. to 2 p.m.</p>
      <p class="ctarow"><a class="btn" href="/">Back to the café</a> <a class="btn ghost" href="/menu">See the menu &rarr;</a></p>
    </div>
  </section>
""")

PAGES["404.html"] = ("/404", f"Page Not Found — {NAME}, {CITY} {STATE}",
    "That page isn't on the Vintage Press Café site — head back home, to the menu, or plan a visit.",
    [], f"""  <section class="pagehead">
    <div class="container center">
      <p class="kicker">Error 404 &middot; Out of Type</p>
      <h1>This page never made it to press.</h1>
      <p class="lead">The link may be mistyped, or the page moved. Start over from here:</p>
      <p class="ctarow"><a class="btn" href="/">Home</a> <a class="btn ghost" href="/menu">Menu &rarr;</a> <a class="btn ghost" href="/visit">Visit &rarr;</a></p>
    </div>
  </section>
""")

# ---------------------------------------------------------------- stylesheet
CSS = """/* Vintage Press Cafe — letterpress identity: ink on paper, double rules, plate marks.
   No third-party anything. */
:root{
  --paper:#f5efe3; --paper2:#ece3d1; --ink:#1c1917; --ink2:#2b2521;
  --red:#b23a25; --muted:#6d6459; --line:#d9cfba; --creamtxt:#f8f4ea;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --mono:ui-monospace,"Menlo",Consolas,"Liberation Mono",monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:var(--serif);font-size:1.06rem;line-height:1.65;color:var(--ink);
  background:var(--paper);
  background-image:radial-gradient(rgba(28,25,23,.06) 1px, transparent 1.5px);
  background-size:14px 14px;
}
.container{max-width:1080px;margin:0 auto;padding:0 clamp(1rem,4vw,2rem)}
.narrow{max-width:720px;margin-left:auto;margin-right:auto}
.skip{position:absolute;left:-9999px}
.skip:focus{left:1rem;top:1rem;background:var(--ink);color:var(--creamtxt);padding:.6rem 1rem;z-index:9}

/* header */
.strip{background:var(--ink);color:var(--creamtxt);font-family:var(--mono);
  font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;
  text-align:center;padding:.55rem 1rem;line-height:1.7}
.strip a{color:var(--creamtxt)}
.strip a:hover{color:#f0bfae}
.navbar{background:var(--paper);border-bottom:5px double var(--ink)}
.navrow{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.8rem;padding-top:.9rem;padding-bottom:.9rem}
.brand{text-decoration:none;display:flex;flex-direction:column;line-height:1.15}
.brandname{font-family:var(--serif);font-size:1.45rem;color:var(--ink);letter-spacing:.02em}
.brandsub{font-family:var(--mono);font-size:.62rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin-top:.3rem}
nav{display:flex;flex-wrap:wrap;gap:clamp(.8rem,2.5vw,1.8rem);align-items:center}
.navlink{font-family:var(--mono);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink);text-decoration:none;border-bottom:2px solid transparent;padding-bottom:.15rem}
.navlink:hover{color:var(--red);border-bottom-color:var(--red)}
.navlink.on{border-bottom-color:var(--ink)}

/* type */
h1{font-size:clamp(2.1rem,6vw,4rem);line-height:1.08;font-weight:600;letter-spacing:-.01em}
h2{font-size:clamp(1.5rem,3.4vw,2.3rem);line-height:1.15;font-weight:600;margin-bottom:.9rem}
h3{font-size:1.22rem;line-height:1.25;font-weight:600;margin-bottom:.5rem}
h1 em{color:var(--red);font-style:normal}
p{margin-bottom:1rem}
.kicker{font-family:var(--mono);font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:var(--red);margin-bottom:.9rem}
.lead{font-size:clamp(1.05rem,2vw,1.3rem);line-height:1.55;max-width:46rem;margin:1rem auto 0}
.pagehead .lead{margin-left:0}
.fineprint{font-family:var(--mono);font-size:.74rem;letter-spacing:.04em;color:var(--muted);line-height:1.7;margin-top:1.4rem}

/* sections */
section{padding-block:clamp(2.6rem,7vw,5rem)}
.pagehead{border-bottom:5px double var(--ink);padding-block:clamp(2.2rem,5vw,3.4rem)}
.pagehead.center{text-align:center}
.center .lead{margin-left:auto;margin-right:auto}
.band h2{margin-top:1.2rem}
.narrow h2{margin-top:1.6rem}
.narrow h2:first-of-type{margin-top:0}
.twocol{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:clamp(1.6rem,4vw,3.5rem);align-items:start}
.twocol h2{margin-top:1.2rem}
.twocol h2:first-child{margin-top:0}

/* hero */
.hero{padding-block:clamp(2.4rem,6vw,4.4rem)}
.frame{border:3px double var(--ink);background:var(--paper2);padding:clamp(2rem,6vw,4.4rem);text-align:center}
.platemark{font-family:var(--mono);font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:1.4rem}
.frame h1{margin:0 auto;max-width:22ch}
.frame .lead{margin-top:1.3rem}
.ctarow{display:flex;flex-wrap:wrap;gap:.9rem;justify-content:center;margin-top:1.8rem}

/* buttons */
.btn{display:inline-block;font-family:var(--mono);font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;
  background:var(--ink);color:var(--creamtxt);border:1px solid var(--ink);
  padding:.85rem 1.6rem;text-decoration:none}
.btn:hover{background:var(--red);border-color:var(--red);color:#fff}
.btn.ghost{background:transparent;color:var(--ink)}
.btn.ghost:hover{background:var(--ink);color:var(--creamtxt);border-color:var(--ink)}

/* plate cards */
.plates{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.2rem;margin-top:2rem}
.plate-card{border:1px solid var(--ink);background:var(--paper);padding:1.6rem 1.5rem 1.4rem}
.plate-card:hover{border-color:var(--red)}
.plate-card .kicker{margin-bottom:.7rem}
.plate-card p{margin-bottom:.9rem;color:var(--muted)}
.more{font-family:var(--mono);font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--red);text-decoration:none;border-bottom:1px solid var(--red)}
.more:hover{color:var(--ink);border-bottom-color:var(--ink)}

/* bands */
.redband{background:var(--red);color:var(--creamtxt)}
.redband .kicker{color:var(--creamtxt)}
.redband p{max-width:46rem;font-size:1.12rem;line-height:1.6;margin-bottom:0}
.redband h2{color:#fff}
.quote{background:var(--ink);color:var(--creamtxt)}
.quote blockquote{font-style:italic;font-size:clamp(1.4rem,3vw,2.1rem);line-height:1.35;max-width:40rem;margin:0 auto .9rem;text-align:center}
.quote cite{display:block;text-align:center;font-family:var(--mono);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:#cfc4ad;font-style:normal}
.quote cite a{color:#f0bfae}
cite.inline{display:block;font-family:var(--mono);font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:1.2rem}

/* story quote */
.band blockquote{font-style:italic;font-size:1.35rem;line-height:1.4;border-left:3px solid var(--red);padding-left:1.2rem;margin:1.4rem 0 .4rem;max-width:38rem}

/* visit */
.hourslist{margin-bottom:1.6rem}
.hourslist dt{font-family:var(--mono);font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin-top:.8rem}
.hourslist dd{font-size:1.2rem}
.hours{font-size:1.15rem}
.visitcard{border:3px double var(--ink);background:var(--paper2);padding:2rem 1.8rem}
.mapwrap{border:3px double var(--ink);background:var(--paper2);aspect-ratio:16/10;width:100%;min-height:320px}
.mapwrap iframe{width:100%;height:100%;border:0;display:block}
.faq{border-bottom:1px solid var(--line);padding:1.1rem 0}
.faq:last-of-type{border-bottom:0}
.fq{font-family:var(--mono);font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);margin-bottom:.4rem}
.fa{color:var(--muted);margin-bottom:0}

/* contact form */
.cform .field{margin-bottom:1.2rem}
.cform label{display:flex;flex-direction:column;gap:.45rem;font-family:var(--mono);
  font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink)}
.cform .opt{color:var(--muted);text-transform:none;letter-spacing:.04em}
.cform input,.cform textarea{font-family:var(--serif);font-size:1rem;color:var(--ink);
  background:var(--paper2);border:1px solid var(--ink);padding:.8rem .9rem;width:100%}
.cform input:focus,.cform textarea:focus{outline:2px solid var(--red);outline-offset:1px}
.cform button{cursor:pointer}

/* breadcrumbs */
.crumbs{font-family:var(--mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:1.4rem;color:var(--muted)}
.crumbs a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--line)}
.crumbs a:hover{color:var(--red);border-bottom-color:var(--red)}
.crumbs .sep{margin:0 .45rem;color:var(--line)}

/* footer */
footer{background:var(--ink);color:var(--creamtxt);padding-top:clamp(2.4rem,5vw,3.6rem);margin-top:1rem}
.footgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:clamp(1.6rem,4vw,3rem)}
.fcol{margin-bottom:1.6rem}
.fbrand{font-family:var(--serif);font-size:1.35rem;margin-bottom:.4rem}
.ftag{font-family:var(--mono);font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:#c9a24f;margin-bottom:0}
.fkick{font-family:var(--mono);font-size:.7rem;letter-spacing:.22em;text-transform:uppercase;color:#cfc4ad;margin-bottom:.7rem}
.fcol p{margin-bottom:.7rem;color:var(--creamtxt)}
.fhours{font-family:var(--mono);font-size:.78rem;letter-spacing:.08em}
.fcol a{color:var(--creamtxt)}
.fcol a:hover{color:#f0bfae}
.footline{border-top:1px solid #3a332c;margin-top:.6rem;padding:1.1rem 0}
.footline p{font-family:var(--mono);font-size:.7rem;letter-spacing:.08em;color:#a89e8b;margin:0;text-align:center}

@media (max-width:640px){
  .navrow{flex-direction:column;text-align:center}
  nav{justify-content:center}
  .twocol{grid-template-columns:1fr}
  /* aspect-ratio + min-height couples height back into min-content WIDTH (512px
     at 320px tall) and blows the mobile grid track — decouple: fixed height, no ratio */
  .mapwrap{aspect-ratio:auto;height:320px;min-height:0}
}
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#1c1917"/><text x="32" y="43" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-size="30" fill="#f8f4ea">VP</text></svg>
"""

def main():
    os.makedirs(PUBLIC, exist_ok=True)
    for fname, (path, title, desc, lds, body) in PAGES.items():
        utility = fname in ("thanks.html", "404.html")
        html = head(title, desc, path, lds, utility) + body + FOOTER
        with open(os.path.join(PUBLIC, fname), "w", encoding="utf-8") as f:
            f.write(html)
    with open(os.path.join(PUBLIC, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(PUBLIC, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON)
    with open(os.path.join(PUBLIC, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nDisallow:\n\nSitemap: " + ORIGIN + "/sitemap.xml\n")
    urls = ["", "/menu", "/coffee-and-tea", "/breakfast-and-lunch", "/our-story",
            "/visit", "/contact", "/privacy"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{ORIGIN}{u if u else '/'}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>\n")
    with open(os.path.join(PUBLIC, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))
    print("generated", len(PAGES), "pages + css/favicon/robots/sitemap")

if __name__ == "__main__":
    main()
