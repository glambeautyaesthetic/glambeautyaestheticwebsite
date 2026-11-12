"""Area pages (Stratford, East Ham, Plaistow, Beckton) and the Guides section.

Called from build.py. Wording rule for the website: no words starting with "ov" or "ne"
unless they are part of a treatment name, no emojis, and never the word "Botox".
"""
import html
import json
from datetime import date

PUBLISHED = "2026-11-12"
PUBLISHED_TEXT = "12 November 2026"


# ---------------------------------------------------------------- shared pieces
def head(b, title, desc, url, ld):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#53634C">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="Glam Beauty Aesthetics">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{b.SITE}/images/site/hero-portrait.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..700&family=Instrument+Sans:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={b.ASSET_V}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
{b.VERCEL_ANALYTICS}</head>
<body>"""


def tail(b):
    return f"""{b.footer()}

<script src="/assets/site.js?v={b.ASSET_V}" defer></script>
<script src="/assets/depth.js?v={b.ASSET_V}" defer></script>
<script src="/assets/chat.js?v={b.ASSET_V}" defer></script>
</body>
</html>
"""


def crumbs(items):
    lis = []
    for name, href in items:
        lis.append(f'    <li><a href="{href}">{name}</a></li>' if href else f'    <li aria-current="page">{name}</li>')
    return '<nav class="wrap crumbs" aria-label="Breadcrumb">\n  <ol>\n' + "\n".join(lis) + "\n  </ol>\n</nav>"


def crumb_ld(b, items, url):
    out = []
    for i, (name, href) in enumerate(items, 1):
        out.append({"@type": "ListItem", "position": i, "name": html.unescape(name),
                    "item": url if not href else (b.SITE + href if href.startswith("/") else href)})
    return {"@type": "BreadcrumbList", "itemListElement": out}


def chips(b):
    return f"""      <div class="hero-meta rise">
        <span class="status js-status"><span class="status-dot"></span><span class="js-status-text">Open 7 days</span></span>
        <a class="rating-chip" href="#reviews">{b.STARS}<b>{b.REVIEWS['rating']}</b> from {b.REVIEWS['count']} Google reviews</a>
        <span class="cred-chip"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8.4-7 10-4-1.6-7-5.5-7-10V6z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M9 12l2.2 2.2L15.5 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>Level 4 qualified</span>
        <span class="cred-chip"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.8l-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>20+ years' experience</span>
        <span class="cred-chip"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.5 3.5h5v6h6v5h-6v6h-5v-6h-6v-5h6z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>Works with a qualified nurse</span>
      </div>"""


def price_rows(b, services, ids, slug):
    rows = []
    for sid in ids:
        s = services[sid]
        rows.append(f"""          <li class="fm-item">
            <div class="fm-item-name">{s['name']}<span class="fm-item-dur">{s['dur']}</span></div>
            <span class="fm-item-price">{s['price_text']}</span>
            <a class="btn btn-primary js-book" data-cta="{slug}-{sid}" href="{b.BOOK}" aria-label="Book {s['name']}">Book</a>
          </li>""")
    return "\n".join(rows)


def faq_block(faqs):
    return "\n".join(f"""      <details{' open' if i == 0 else ''}>
        <summary>{q}</summary>
        <div class="answer"><p>{a}</p></div>
      </details>""" for i, (q, a) in enumerate(faqs))


def faq_ld(faqs):
    strip = lambda s: html.unescape(s.replace("<strong>", "").replace("</strong>", ""))
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}


def reviews_block(b, keys):
    cards = "\n".join(b.review_card(k) for k in keys)
    return f"""<section class="section t-reviews" id="reviews" aria-labelledby="reviews-title" style="padding-top:0">
  <div class="wrap">
    <div class="rv-head reveal">
      <div>
        <span class="eyebrow">Client reviews</span>
        <h2 class="h2" id="reviews-title" style="margin:0">Kind <em>words.</em></h2>
      </div>
      <a class="rating-lg" href="{b.REVIEWS['google_url']}" target="_blank" rel="noopener"><span class="rv-big">{b.REVIEWS['rating']}</span><span>{b.STARS}<br>From {b.REVIEWS['count']} Google reviews</span></a>
    </div>
    <div class="rv-wall reveal">
{cards}
    </div>
  </div>
</section>"""


def final_cta(b, slug, heading="Ready when <em>you are.</em>"):
    return f"""<section class="section final" aria-labelledby="final-title" data-3d data-tilt>
  <div class="orbs" aria-hidden="true">
    <i style="--d:.25;--s:110px;left:6%;top:14%"></i>
    <i style="--d:.6;--s:42px;left:84%;top:22%"></i>
    <i style="--d:.9;--s:20px;left:72%;top:74%" class="hide-sm"></i>
  </div>
  <div class="wrap reveal">
    <h2 class="h2" id="final-title">{heading}</h2>
    <p>Choose a time that suits you and you're booked. Open seven days a week.</p>
    <div class="ctas">
      <a class="btn btn-light js-book" data-cta="{slug}-final" data-magnetic href="{b.BOOK}">Book now</a>
      <a class="btn btn-ghost" href="{b.WHATSAPP}" target="_blank" rel="noopener" data-cta="{slug}-final-whatsapp">WhatsApp us</a>
    </div>
    <ul class="assure">
      <li>Free consultation</li>
      <li>Level 4 qualified professional</li>
      <li>20+ years' experience</li>
      <li>Working with a qualified nurse</li>
      <li>Secure online booking</li>
      <li>Weekend appointments</li>
      <li>Rated {b.REVIEWS['rating']} on Google</li>
    </ul>
  </div>
</section>"""


def treatment_cards(b, services, slugs):
    out = []
    for r in slugs:
        rt = b.BY_SLUG[r]
        out.append(f'      <a class="related-card" href="/{r}/"><b>{rt["name"]}</b><span>{rt["summary"]}</span><i>From £{b.min_price(rt, services)} →</i></a>')
    return "\n".join(out)


def guide_cards(slugs):
    out = []
    for g in slugs:
        a = GUIDE_BY_SLUG[g]
        out.append(f'      <a class="related-card" href="/guides/{g}/"><b>{a["card_title"]}</b><span>{a["summary"]}</span><i>{a["read"]} min read →</i></a>')
    return "\n".join(out)


def business_ld(b, area=None):
    biz = {
        "@type": ["BeautySalon", "MedicalClinic"], "@id": f"{b.SITE}/#business",
        "name": "Glam Beauty Aesthetics", "url": f"{b.SITE}/", "telephone": b.PHONE_INTL,
        "address": {"@type": "PostalAddress", "streetAddress": b.STREET, "addressLocality": "London",
                    "postalCode": b.POSTCODE, "addressCountry": "GB"},
    }
    if area:
        biz["areaServed"] = [{"@type": "Place", "name": f"{area}, London"}, {"@type": "Place", "name": "Canning Town, London"}]
    return biz


# ---------------------------------------------------------------- area pages
AREAS = [
  {
    "slug": "aesthetics-clinic-stratford", "place": "Stratford", "postcode": "E15",
    "title": "Stratford Aesthetics Clinic, E15 | Glam Beauty Aesthetics",
    "description": "Aesthetics clinic two stops from Stratford on the Jubilee line. Lip filler, anti-wrinkle, skin boosters and facials. Free consultation, open 7 days.",
    "sub": "Two stops from Stratford on the Jubilee line. Natural-looking lip filler, anti-wrinkle injections and skin boosters, with a free consultation first.",
    "fact": ("2 stops", "Jubilee line from Stratford"),
    "intro": "<p>If you live or work around Stratford, Westfield or the Olympic Park, Glam Beauty Aesthetics is a quick trip down the line in Canning Town. It's a calm, private clinic, so you can talk through what you'd like without feeling rushed, and every treatment is planned around your own features.</p>",
    "travel": """<h2>Getting here from Stratford</h2>
<ul>
<li><span><strong>Jubilee line:</strong> two stops from Stratford to Canning Town, via West Ham.</span></li>
<li><span><strong>DLR:</strong> trains from Stratford also stop at Canning Town.</span></li>
<li><span><strong>From the station:</strong> the clinic is at 28 Barking Road, E16 1EQ, a short walk from Canning Town station.</span></li>
</ul>""",
    "popular": "<p>Clients from Stratford most often book lip filler, anti-wrinkle injections and skin boosters. Many also pop in for a Korean glass facial or a vitamin B12 injection on the way home from work.</p>",
    "services": ["lip05", "aw1", "pn", "kgf", "fl1", "b12"],
    "treatments": ["lip-filler-london", "anti-wrinkle-injections-london", "skin-boosters-london", "dermal-fillers-london", "microneedling-london", "tear-trough-filler-london"],
    "reviews": ["saira", "ana", "leila"],
    "faqs": [
      ("How do I get to Glam Beauty Aesthetics from Stratford?", "Take the Jubilee line two stops to Canning Town, or the DLR, which also stops at Canning Town. The clinic is at 28 Barking Road, E16 1EQ, a short walk from the station."),
    ],
  },
  {
    "slug": "aesthetics-clinic-east-ham", "place": "East Ham", "postcode": "E6",
    "title": "East Ham Aesthetics Clinic, E6 | Glam Beauty Aesthetics",
    "description": "Aesthetics clinic straight along Barking Road from East Ham. Lip filler, anti-wrinkle, skin boosters and fat dissolving. Free consultation, open 7 days.",
    "sub": "Straight along Barking Road from East Ham. Natural-looking results from a Level 4 qualified practitioner, with a free consultation first.",
    "fact": ("1 road", "Barking Road from East Ham"),
    "intro": "<p>Barking Road runs all the way from East Ham to our clinic in Canning Town, so it's an easy trip whether you come by bus, car or tube. Every appointment starts with a proper conversation about what you'd like, and treatments are planned to keep you looking like yourself.</p>",
    "travel": """<h2>Getting here from East Ham</h2>
<ul>
<li><span><strong>By road:</strong> come straight along Barking Road towards Canning Town. The clinic is at number 28, E16 1EQ.</span></li>
<li><span><strong>By tube:</strong> take the District or Hammersmith &amp; City line from East Ham to West Ham, then the Jubilee line one stop to Canning Town.</span></li>
<li><span><strong>From the station:</strong> the clinic is a short walk from Canning Town station.</span></li>
</ul>""",
    "popular": "<p>Popular choices for clients from East Ham include anti-wrinkle injections, lip filler, fat dissolving and polynucleotide skin boosters. If you're not sure where to start, the free consultation is the best first step.</p>",
    "services": ["aw2", "lip05", "fd1", "pn", "tt", "glu"],
    "treatments": ["anti-wrinkle-injections-london", "lip-filler-london", "fat-dissolving-london", "skin-boosters-london", "pdo-thread-lift-london", "dermal-fillers-london"],
    "reviews": ["sally", "zara", "hasan"],
    "faqs": [
      ("How do I get to Glam Beauty Aesthetics from East Ham?", "Barking Road runs from East Ham to Canning Town, and the clinic is at 28 Barking Road, E16 1EQ. By tube, take the District or Hammersmith &amp; City line to West Ham, then the Jubilee line one stop to Canning Town."),
    ],
  },
  {
    "slug": "aesthetics-clinic-plaistow", "place": "Plaistow", "postcode": "E13",
    "title": "Plaistow Aesthetics Clinic, E13 | Glam Beauty Aesthetics",
    "description": "Aesthetics clinic a short trip from Plaistow along Barking Road. Lip filler, anti-wrinkle, skin boosters and microneedling. Free consultation, open 7 days.",
    "sub": "A short trip from Plaistow along Barking Road. Personalised treatments from a Level 4 qualified practitioner, with a free consultation first.",
    "fact": ("2 stops", "From Plaistow station"),
    "intro": "<p>Barking Road runs through Plaistow on its way to Canning Town, so our clinic is only a few minutes away. Whether you'd like softer lines, fuller lips or brighter skin, we'll talk it through with you first and only suggest what suits your face.</p>",
    "travel": """<h2>Getting here from Plaistow</h2>
<ul>
<li><span><strong>By road:</strong> head west along Barking Road towards Canning Town. The clinic is at number 28, E16 1EQ.</span></li>
<li><span><strong>By tube:</strong> take the District or Hammersmith &amp; City line one stop from Plaistow to West Ham, then the Jubilee line one stop to Canning Town.</span></li>
<li><span><strong>From the station:</strong> the clinic is a short walk from Canning Town station.</span></li>
</ul>""",
    "popular": "<p>Clients from Plaistow often book skin treatments such as microneedling, dermaplaning and the Korean glass facial, as well as lip filler and anti-wrinkle injections.</p>",
    "services": ["mv", "kgf", "derm", "lip05", "aw1", "exo"],
    "treatments": ["microneedling-london", "skin-boosters-london", "lip-filler-london", "anti-wrinkle-injections-london", "tear-trough-filler-london", "bridal-hair-makeup-london"],
    "reviews": ["patricia", "osadiawa", "leila"],
    "faqs": [
      ("How do I get to Glam Beauty Aesthetics from Plaistow?", "Barking Road runs through Plaistow to Canning Town, and the clinic is at 28 Barking Road, E16 1EQ. By tube, take the District or Hammersmith &amp; City line one stop to West Ham, then the Jubilee line one stop to Canning Town."),
    ],
  },
  {
    "slug": "aesthetics-clinic-beckton", "place": "Beckton", "postcode": "E6",
    "title": "Beckton Aesthetics Clinic, E6 | Glam Beauty Aesthetics",
    "description": "Aesthetics clinic direct from Beckton on the DLR, no change. Lip filler, anti-wrinkle, skin boosters and thread lifts. Free consultation, open 7 days.",
    "sub": "Direct from Beckton on the DLR, with no change. Natural-looking treatments planned around your features, with a free consultation first.",
    "fact": ("Direct", "DLR from Beckton, no change"),
    "intro": "<p>The DLR runs straight from Beckton to Canning Town, so our clinic is easy to reach from Beckton and across the Royal Docks. You'll get time to ask questions, a clear plan and honest advice about what will suit you.</p>",
    "travel": """<h2>Getting here from Beckton</h2>
<ul>
<li><span><strong>DLR:</strong> take the DLR from Beckton towards Canning Town. It's direct, with stops including Royal Albert, Prince Regent and Custom House on the way.</span></li>
<li><span><strong>From the station:</strong> the clinic is at 28 Barking Road, E16 1EQ, a short walk from Canning Town station.</span></li>
</ul>""",
    "popular": "<p>Clients from Beckton and the Royal Docks often choose skin boosters, PDO thread lifts, lip filler and anti-wrinkle injections. Bridal hair and makeup is also popular for weddings across East London.</p>",
    "services": ["pn", "rad", "pdo1", "lip05", "aw3", "bridal"],
    "treatments": ["skin-boosters-london", "pdo-thread-lift-london", "lip-filler-london", "anti-wrinkle-injections-london", "dermal-fillers-london", "bridal-hair-makeup-london"],
    "reviews": ["toni", "vahideh", "yushrah"],
    "faqs": [
      ("How do I get to Glam Beauty Aesthetics from Beckton?", "Take the DLR from Beckton to Canning Town. It's direct, with no change. The clinic is at 28 Barking Road, E16 1EQ, a short walk from Canning Town station."),
    ],
  },
]

AREA_SHARED_FAQS = [
  ("Is the consultation really free?", "Yes. You can talk through your goals, ask questions and get a personalised plan before you decide, with no cost and no pressure to book."),
  ("Are you open at weekends?", "Yes, we're open seven days a week, including Saturday and Sunday from 9:30am to 4pm."),
  ("Who carries out the treatments?", "Treatments are carried out by a Level 4 qualified practitioner with more than 20 years' experience in the beauty industry, working together with a qualified nurse."),
  ("How do I book?", "Tap Book now to choose your treatment and a time online, or call or WhatsApp us on 07988 347194."),
]

AREA_WHY = """<h2>Why clients choose us</h2>
<ul>
<li><span><strong>Free consultation</strong> before any treatment, with no pressure to book.</span></li>
<li><span><strong>Level 4 qualified</strong> practitioner with more than 20 years' experience in the beauty industry.</span></li>
<li><span>Working together with a <strong>qualified nurse</strong> for extra peace of mind.</span></li>
<li><span><strong>Rated 5.0 on Google</strong> from 85 reviews.</span></li>
<li><span><strong>Open seven days</strong>, with weekend appointments.</span></li>
</ul>"""


def area_page(b, a, services):
    url = f"{b.SITE}/{a['slug']}/"
    slug = a["slug"]
    place = a["place"]
    crumb_items = [("Home", "/"), ("Areas we serve", "/#visit"), (place, None)]
    faqs = a["faqs"] + AREA_SHARED_FAQS
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url, "url": url, "name": a["title"], "description": a["description"],
         "inLanguage": "en-GB", "about": {"@id": f"{b.SITE}/#business"}},
        business_ld(b, place),
        crumb_ld(b, crumb_items, url),
        faq_ld(faqs),
    ]}
    fv, fl = a["fact"]
    return f"""{head(b, a['title'], a['description'], url, ld)}
{b.header()}

<main id="main">
{crumbs(crumb_items)}

<section class="hero t-hero p-hero" aria-labelledby="page-title" data-3d data-tilt>
  <div class="orbs" aria-hidden="true">
    <i style="--d:.2;--s:120px;left:70%;top:6%"></i>
    <i style="--d:.4;--s:64px;left:-2%;top:82%" class="hide-sm"></i>
  </div>
  <div class="wrap">
    <span class="eyebrow rise">{place} · {a['postcode']}</span>
    <h1 id="page-title" class="hero-display"><span class="line"><span>Aesthetics clinic</span></span> <em class="line"><span>close to {place}.</span></em></h1>
    <p class="hero-sub rise">{a['sub']}</p>
    <div class="hero-ctas rise">
      <a class="btn btn-primary js-book" data-cta="{slug}-hero" data-magnetic href="{b.BOOK}">Book an appointment {b.ARROW}</a>
      <a class="btn btn-consult" href="#contact" data-consult="{slug}-hero"><span class="star" aria-hidden="true">✦</span> Free consultation</a>
    </div>
{chips(b)}
  </div>
</section>

<div class="proof" aria-label="At a glance">
  <div class="wrap">
    <ul>
      <li><b>{fv}</b><span>{fl}</span></li>
      <li><b>Free</b><span>Consultation</span></li>
      <li><b>7 days</b><span>Weekends included</span></li>
      <li><b>{b.REVIEWS['rating']}</b><span>From {b.REVIEWS['count']} Google reviews</span></li>
    </ul>
  </div>
</div>

<section class="section" aria-label="About the clinic">
  <div class="wrap t-grid">
    <article class="prose reveal">
<h2>Your local aesthetics clinic</h2>
{a['intro']}
{a['travel']}
<h2>Popular treatments</h2>
{a['popular']}
{AREA_WHY}
      <p style="margin-top:28px"><a class="btn btn-primary js-book" data-cta="{slug}-body" href="{b.BOOK}" style="color:#fff">Book an appointment {b.ARROW}</a></p>
    </article>
    <aside class="t-card" id="prices" aria-labelledby="prices-title">
      <h2 id="prices-title">Popular prices</h2>
      <p>Book online in a minute, any time. Not sure which? <a href="#contact" data-consult="{slug}-card">Start with a free consultation →</a></p>
      <ul class="fm-list">
{price_rows(b, services, a['services'], slug)}
      </ul>
      <p class="t-card-foot"><a href="/#treatments">See the full price list →</a></p>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="treat-title" style="padding-top:0">
  <div class="wrap">
    <span class="eyebrow">Treatments</span>
    <h2 class="h2" id="treat-title" style="margin-bottom:28px">Find your <em>treatment.</em></h2>
    <div class="related-grid reveal">
{treatment_cards(b, services, a['treatments'])}
    </div>
  </div>
</section>

{reviews_block(b, a['reviews'])}

<section class="section" id="faq" aria-labelledby="faq-title" style="padding-top:0">
  <div class="wrap faq-grid">
    <div class="reveal">
      <span class="eyebrow">Questions</span>
      <h2 class="h2" id="faq-title">Visiting from {place}, <em>answered.</em></h2>
      <p class="lede" style="margin-bottom:28px">Anything else, call <a href="tel:{b.PHONE_INTL}" data-cta="{slug}-faq-call">{b.PHONE}</a>. More answers in our <a href="/guides/">treatment guides</a>.</p>
      <a class="btn btn-primary js-book" data-cta="{slug}-faq" href="{b.BOOK}">Book now</a>
    </div>
    <div class="faq reveal">
{faq_block(faqs)}
    </div>
  </div>
</section>

{b.contact_section(slug)}

{b.visit_section()}

{final_cta(b, slug)}
</main>

{tail(b)}"""


# ---------------------------------------------------------------- guides
GUIDES = [
  {
    "slug": "how-long-does-lip-filler-last",
    "title": "How Long Does Lip Filler Last? | Glam Beauty Aesthetics",
    "description": "How long lip filler lasts, what affects it, signs it's fading and when to top up. A clear guide from a London aesthetics clinic.",
    "card_title": "How long does lip filler last?",
    "h1": "How long does", "h1_em": "lip filler last?",
    "summary": "Usually around 6 to 12 months. Here's what affects it, how to tell it's fading and when to top up.",
    "read": 4, "treatment": "lip-filler-london", "services": ["lip05", "fl1", "lipb", "hy"],
    "points": [
      "Lip filler usually lasts around 6 to 12 months.",
      "How long it lasts depends on the product, the amount and your own metabolism.",
      "Your first treatment may fade a little sooner than later top-ups.",
      "Hyaluronic acid filler can be dissolved if you ever change your mind.",
    ],
    "body": """<h2>The short answer</h2>
<p>Most people find their lip filler lasts around <strong>6 to 12 months</strong>. Lip filler is a hyaluronic acid gel, a substance found naturally in your skin, and your body gradually breaks it down over time. That's why results fade softly rather than disappearing all at once.</p>
<h2>What affects how long it lasts</h2>
<ul>
<li><span><strong>The product:</strong> some fillers are softer and more flexible, others are firmer. Your practitioner chooses one to suit the look you want.</span></li>
<li><span><strong>The amount:</strong> a subtle 0.5 ml treatment may fade a little sooner than a fuller 1 ml treatment.</span></li>
<li><span><strong>Your metabolism:</strong> everyone breaks down hyaluronic acid at a slightly different rate.</span></li>
<li><span><strong>Movement:</strong> lips move all day as you talk, eat and smile, so lip filler tends to fade faster than filler in less mobile areas such as the chin or cheeks.</span></li>
<li><span><strong>Lifestyle:</strong> very frequent intense exercise and smoking are often linked with results fading sooner.</span></li>
</ul>
<h2>Your first treatment</h2>
<p>Many clients find their first lip filler fades a little sooner than later treatments. Starting with a smaller amount and building gradually is still the most reliable way to keep your lips in proportion with your face.</p>
<h2>Signs your filler is fading</h2>
<p>You may notice your lips looking slightly less defined at the border, a little less full, or less hydrated. There's no fixed timetable, so it's simply a case of booking a top-up when you'd like to refresh the look.</p>
<h2>Topping up</h2>
<p>A top-up is usually a smaller amount than your first treatment. At Glam Beauty Aesthetics, lip filler starts from £90 for 0.5 ml, and a 1 ml treatment is £100. If you'd prefer hydration and a soft tint rather than added volume, the lip booster with pink blush is £125.</p>
<h2>Can lip filler be dissolved?</h2>
<p>Yes. Hyaluronic acid filler can be dissolved with an enzyme called hyaluronidase. It's £125 per 1 ml, and it's always discussed with you first.</p>""",
    "faqs": [
      ("How long does lip filler last?", "Usually around 6 to 12 months, depending on the product, the amount used and your own metabolism."),
      ("Does lip filler last longer the more you have?", "Many clients find later treatments last a little longer than their first, but the aim is always to keep your lips in proportion rather than to keep adding volume."),
      ("How much does a lip filler top-up cost?", "Lip filler starts from £90 for 0.5 ml at Glam Beauty Aesthetics, and 1 ml is £100."),
    ],
  },
  {
    "slug": "lip-filler-swelling-aftercare",
    "title": "Lip Filler Swelling and Aftercare | Glam Beauty Aesthetics",
    "description": "What to expect after lip filler, day by day: swelling, bruising, when the final result shows and simple aftercare tips from a London clinic.",
    "card_title": "Lip filler swelling and aftercare",
    "h1": "Lip filler swelling", "h1_em": "and aftercare.",
    "summary": "What to expect in the days after lip filler, when the final result shows, and how to look after your lips.",
    "read": 4, "treatment": "lip-filler-london", "services": ["lip05", "fl1", "lipb"],
    "points": [
      "Swelling is usually most noticeable for the first 1 to 2 days.",
      "Most swelling settles within about a week.",
      "Your final result shows at around two weeks.",
      "Avoid lipstick, alcohol, strenuous exercise and heat for the first 24 hours.",
    ],
    "body": """<h2>Day by day</h2>
<ul>
<li><span><strong>Day 1 to 2:</strong> swelling is usually at its most noticeable. Lips can look bigger than the final result and may feel firm or slightly uneven. This is normal.</span></li>
<li><span><strong>Day 3 to 4:</strong> swelling starts to settle and your lips begin to look softer and more even.</span></li>
<li><span><strong>Day 5 to 7:</strong> most swelling has gone. Any small bruises are usually fading too.</span></li>
<li><span><strong>Around 2 weeks:</strong> the filler has settled and you see your final result. This is the best time to judge the shape.</span></li>
</ul>
<p>Everyone heals a little differently, so don't worry if your timeline is slightly longer or shorter.</p>
<h2>Bruising</h2>
<p>Small bruises can appear where the filler was placed. They usually fade within a few days to a week. If you have an event coming up, book your treatment at least two weeks before.</p>
<h2>Aftercare for the first 24 hours</h2>
<ul>
<li><span>Avoid lipstick and lip products.</span></li>
<li><span>Avoid alcohol and strenuous exercise.</span></li>
<li><span>Avoid heat such as saunas, steam rooms and hot yoga.</span></li>
<li><span>Try not to press, massage or kiss firmly on the lips.</span></li>
<li><span>A cold compress wrapped in a clean cloth can help with swelling.</span></li>
</ul>
<p>You'll get aftercare advice before you leave, and you can contact us any time with questions.</p>
<h2>When to contact us straight away</h2>
<p>Contact the clinic straight away, or seek urgent medical help, if you notice pain that is getting worse rather than better, skin that turns pale, white, blue or dusky, or any changes to your vision. These are rare, but they need to be checked quickly.</p>""",
    "faqs": [
      ("How long does lip filler swelling last?", "Swelling is usually most noticeable for the first 1 to 2 days and mostly settles within about a week. The final result shows at around two weeks."),
      ("Is it normal for lips to look lumpy after filler?", "Some firmness or unevenness in the first few days is common while swelling settles. If you're worried, contact the clinic and we'll check."),
      ("When can I wear lipstick after lip filler?", "Wait at least 24 hours before using lipstick or other lip products."),
    ],
  },
  {
    "slug": "when-do-anti-wrinkle-injections-work",
    "title": "When Do Anti-Wrinkle Injections Work? | Glam Beauty Aesthetics",
    "description": "When anti-wrinkle injections start working, when you see the full result, how long they last and the aftercare to follow. A guide from a London clinic.",
    "card_title": "When do anti-wrinkle injections start working?",
    "h1": "When do anti-wrinkle", "h1_em": "injections work?",
    "summary": "Results start after 3 to 5 days and reach full effect at around two weeks. Here's the full timeline.",
    "read": 3, "treatment": "anti-wrinkle-injections-london", "services": ["aw1", "aw2", "aw3", "adv"],
    "points": [
      "You'll usually see the first changes after 3 to 5 days.",
      "The full effect shows at around two weeks.",
      "Results usually last around 3 to 4 months.",
      "Stay upright for 4 hours and avoid rubbing the area after treatment.",
    ],
    "body": """<h2>The timeline</h2>
<ul>
<li><span><strong>Straight after:</strong> you may see small bumps where the injections went in. These usually settle within about 20 minutes.</span></li>
<li><span><strong>Day 3 to 5:</strong> the treated muscles start to relax and lines begin to soften.</span></li>
<li><span><strong>Around 2 weeks:</strong> you see the full effect. This is the right time to review your result.</span></li>
<li><span><strong>3 to 4 months:</strong> movement gradually returns and lines slowly reappear, which is when most people book again.</span></li>
</ul>
<h2>How they work</h2>
<p>Many lines on the upper face come from repeated movement, such as raising your eyebrows or frowning. Anti-wrinkle injections relax the specific muscles behind those lines, so the skin above them smooths out while you keep a natural expression.</p>
<p>Anti-wrinkle injections are a prescription-only medicine, so your suitability is always assessed at a consultation before any treatment.</p>
<h2>Aftercare</h2>
<ul>
<li><span>Stay upright for 4 hours after treatment.</span></li>
<li><span>Avoid rubbing or massaging the treated area.</span></li>
<li><span>Skip strenuous exercise, saunas and alcohol for 24 hours.</span></li>
</ul>
<h2>Prices</h2>
<p>At Glam Beauty Aesthetics, anti-wrinkle injections are £90 for one area, £114 for two areas and £150 for three areas (forehead, frown lines and crow's feet).</p>""",
    "faqs": [
      ("How long do anti-wrinkle injections take to work?", "You'll usually see the first changes after 3 to 5 days, with the full effect at around two weeks."),
      ("How long do anti-wrinkle injections last?", "Usually around 3 to 4 months, after which muscle movement gradually returns."),
      ("Can I exercise after anti-wrinkle injections?", "Avoid strenuous exercise, saunas and alcohol for 24 hours after treatment."),
    ],
  },
  {
    "slug": "skin-boosters-vs-dermal-fillers",
    "title": "Skin Boosters vs Dermal Fillers | Glam Beauty Aesthetics",
    "description": "The difference between skin boosters and dermal fillers, what each one does and how to choose. A clear guide from a London aesthetics clinic.",
    "card_title": "Skin boosters vs dermal fillers",
    "h1": "Skin boosters vs", "h1_em": "dermal fillers.",
    "summary": "Fillers add shape and volume. Skin boosters improve the quality of your skin. Here's how to tell which suits you.",
    "read": 4, "treatment": "skin-boosters-london", "services": ["pn", "rad", "exo", "fl1"],
    "points": [
      "Dermal fillers add volume and shape to specific areas.",
      "Skin boosters improve hydration, texture, glow and fine lines across the skin.",
      "Skin boosters are usually a course. Fillers are usually a single treatment.",
      "Many people combine both for a balanced, natural result.",
    ],
    "body": """<h2>The main difference</h2>
<p><strong>Dermal fillers</strong> add volume and shape to a specific area, such as the lips, cheeks, jawline or chin. <strong>Skin boosters</strong> don't change your shape. Instead they improve the quality of the skin itself: hydration, texture, firmness and glow.</p>
<h2>Dermal fillers</h2>
<ul>
<li><span><strong>Best for:</strong> fuller lips, defined cheekbones, a sharper jawline, a balanced chin or softer lines around the mouth.</span></li>
<li><span><strong>How they work:</strong> a hyaluronic acid gel is placed precisely to add structure.</span></li>
<li><span><strong>Results:</strong> visible straight away, settling at around two weeks.</span></li>
<li><span><strong>Price:</strong> dermal filler is £100 per 1 ml, and lip filler starts from £90 for 0.5 ml.</span></li>
</ul>
<h2>Skin boosters</h2>
<ul>
<li><span><strong>Best for:</strong> dull or dehydrated skin, fine lines, crepey texture, dark circles and an overall lack of glow.</span></li>
<li><span><strong>How they work:</strong> they are spread across the skin to hydrate it and support your own collagen.</span></li>
<li><span><strong>Results:</strong> build gradually, usually over a course of treatments.</span></li>
<li><span><strong>Options:</strong> polynucleotides (£125), exosomes (£125) and Radiesse (£325), which supports collagen for firmer skin.</span></li>
</ul>
<h2>Which one suits you?</h2>
<p>If you'd like to change a shape, such as fuller lips or a more defined jaw, a filler is usually the answer. If your main concern is how your skin looks and feels, a skin booster is the better place to start. Many clients combine both: a skin booster for healthy, glowing skin and a small amount of filler for definition.</p>
<p>The easiest way to decide is a free consultation, where we look at your skin and features and suggest a plan that suits you.</p>""",
    "faqs": [
      ("What is the difference between skin boosters and fillers?", "Dermal fillers add volume and shape to specific areas. Skin boosters improve the quality of the skin itself, such as hydration, texture and glow."),
      ("Can I have skin boosters and filler together?", "Yes. Many clients combine them for a balanced result. Your practitioner will plan the timing with you at your consultation."),
      ("How many skin booster sessions will I have?", "Skin boosters usually work best as a course. Your practitioner will recommend the right number at your free consultation."),
    ],
  },
]
GUIDE_BY_SLUG = {g["slug"]: g for g in GUIDES}

# Treatment page slug -> guides to link from that page
TREATMENT_GUIDES = {
    "lip-filler-london": ["how-long-does-lip-filler-last", "lip-filler-swelling-aftercare"],
    "anti-wrinkle-injections-london": ["when-do-anti-wrinkle-injections-work"],
    "skin-boosters-london": ["skin-boosters-vs-dermal-fillers"],
    "dermal-fillers-london": ["skin-boosters-vs-dermal-fillers"],
}


def guide_page(b, g, services):
    url = f"{b.SITE}/guides/{g['slug']}/"
    slug = g["slug"]
    t = b.BY_SLUG[g["treatment"]]
    crumb_items = [("Home", "/"), ("Guides", "/guides/"), (g["card_title"], None)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": f"{url}#article", "headline": g["card_title"], "description": g["description"],
         "url": url, "mainEntityOfPage": url, "inLanguage": "en-GB",
         "datePublished": PUBLISHED, "dateModified": PUBLISHED,
         "image": f"{b.SITE}/images/site/hero-portrait.jpg",
         "author": {"@type": "Organization", "name": "Glam Beauty Aesthetics", "url": f"{b.SITE}/"},
         "publisher": {"@id": f"{b.SITE}/#business"}},
        business_ld(b),
        crumb_ld(b, crumb_items, url),
        faq_ld(g["faqs"]),
    ]}
    points = "\n".join(f"<li><span>{p}</span></li>" for p in g["points"])
    others = [x["slug"] for x in GUIDES if x["slug"] != slug]
    tname = html.unescape(t["name"])
    return f"""{head(b, g['title'], g['description'], url, ld)}
{b.header("/?consult=1#contact")}

<main id="main">
{crumbs(crumb_items)}

<section class="hero t-hero p-hero" aria-labelledby="page-title">
  <div class="wrap">
    <span class="eyebrow rise">Guide · {tname}</span>
    <h1 id="page-title" class="hero-display"><span class="line"><span>{g['h1']}</span></span> <em class="line"><span>{g['h1_em']}</span></em></h1>
    <p class="hero-sub rise">{g['summary']}</p>
    <p class="guide-meta rise">By Glam Beauty Aesthetics · <time datetime="{PUBLISHED}">{PUBLISHED_TEXT}</time> · {g['read']} min read</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="Guide">
  <div class="wrap t-grid guide-grid">
    <article class="prose">
      <div class="key-points">
        <h2>Key points</h2>
        <ul>
{points}
        </ul>
      </div>
{g['body'].strip()}
      <h2>Questions</h2>
      <div class="faq">
{faq_block(g['faqs'])}
      </div>
      <p class="guide-note">This guide is general information, not medical advice. Everyone is different, so your practitioner will talk you through what suits you at your free consultation.</p>
      <p style="margin-top:28px"><a class="btn btn-primary js-book" data-cta="guide-{slug}-body" href="{b.BOOK}" style="color:#fff">Book an appointment {b.ARROW}</a></p>
    </article>
    <aside class="t-card" aria-labelledby="card-title">
      <h2 id="card-title">{tname}</h2>
      <p>{t['summary']} <a href="/{t['slug']}/">Read more →</a></p>
      <ul class="fm-list">
{price_rows(b, services, g['services'], 'guide-' + slug)}
      </ul>
      <p class="t-card-foot">Not sure yet? <a href="/?consult=1#contact" data-consult="guide-{slug}">Book a free consultation →</a></p>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="more-title" style="padding-top:0">
  <div class="wrap">
    <span class="eyebrow">Guides</span>
    <h2 class="h2" id="more-title" style="margin-bottom:28px">More <em>answers.</em></h2>
    <div class="related-grid reveal">
{guide_cards(others)}
    </div>
  </div>
</section>

{final_cta(b, 'guide-' + slug)}
</main>

{tail(b)}"""


def guides_index(b, services):
    url = f"{b.SITE}/guides/"
    title = "Aesthetics Treatment Guides | Glam Beauty Aesthetics"
    desc = "Clear answers about lip filler, anti-wrinkle injections, skin boosters and aftercare, from a Level 4 qualified aesthetics clinic in London."
    crumb_items = [("Home", "/"), ("Guides", None)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
         "hasPart": [{"@type": "Article", "headline": g["card_title"], "url": f"{b.SITE}/guides/{g['slug']}/"} for g in GUIDES]},
        crumb_ld(b, crumb_items, url),
    ]}
    return f"""{head(b, title, desc, url, ld)}
{b.header("/?consult=1#contact")}

<main id="main">
{crumbs(crumb_items)}

<section class="hero t-hero p-hero" aria-labelledby="page-title">
  <div class="wrap">
    <span class="eyebrow rise">Guides</span>
    <h1 id="page-title" class="hero-display"><span class="line"><span>Treatment guides</span></span> <em class="line"><span>and answers.</span></em></h1>
    <p class="hero-sub rise">Honest, clear answers to the questions clients ask us most, from how long results last to what to expect afterwards.</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="All guides">
  <div class="wrap">
    <div class="related-grid guides-grid">
{guide_cards([g['slug'] for g in GUIDES])}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="areas-title" style="padding-top:0">
  <div class="wrap">
    <span class="eyebrow">Visit us</span>
    <h2 class="h2" id="areas-title" style="margin-bottom:18px">Canning Town, <em>E16.</em></h2>
    <p class="lede" style="max-width:60ch">We're at 28 Barking Road, a short walk from Canning Town station, and easy to reach from <a href="/aesthetics-clinic-stratford/">Stratford</a>, <a href="/aesthetics-clinic-east-ham/">East Ham</a>, <a href="/aesthetics-clinic-plaistow/">Plaistow</a> and <a href="/aesthetics-clinic-beckton/">Beckton</a>.</p>
  </div>
</section>

{final_cta(b, 'guides')}
</main>

{tail(b)}"""


def guides_links_html(slug):
    """Small 'read the guide' line for a treatment page FAQ intro."""
    gs = TREATMENT_GUIDES.get(slug)
    if not gs:
        return ""
    links = " and ".join(f'<a href="/guides/{g}/">{GUIDE_BY_SLUG[g]["card_title"].rstrip("?").lower()}</a>' for g in gs)
    return f' Read our guides on {links}.'


def all_urls(b):
    return ([f"{b.SITE}/{a['slug']}/" for a in AREAS] + [f"{b.SITE}/guides/"] +
            [f"{b.SITE}/guides/{g['slug']}/" for g in GUIDES])


def write_all(b, services):
    for a in AREAS:
        out = b.ROOT / a["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(area_page(b, a, services), encoding="utf-8")
        print("wrote", out.relative_to(b.ROOT))
    gdir = b.ROOT / "guides"
    gdir.mkdir(exist_ok=True)
    (gdir / "index.html").write_text(guides_index(b, services), encoding="utf-8")
    print("wrote guides/index.html")
    for g in GUIDES:
        out = gdir / g["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(guide_page(b, g, services), encoding="utf-8")
        print("wrote", out.relative_to(b.ROOT))
