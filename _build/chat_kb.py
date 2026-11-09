"""
Knowledge base for the website chat assistant.

build.py calls build_kb() and writes assets/chat-kb.json. Prices, durations and
treatment details are read from the site itself, so the assistant always matches
the price menu. General answers live in GENERAL below — edit them here, then run
`python _build/build.py`.

The text rules here (norm, stem, SYN, PHRASES, STOP) must match assets/chat.js.
"""
import html
import re

# ---------------------------------------------------------------- language rules
STOP = set("""
a an the is are am was were be been being do does did doing i me my mine we us our you your yours u ur
it its this that these those to of in on at for from by with about as into than then so and or but if
can could would should will shall may might must have has had get got getting want wanted wanna need
please pls plz take give now thank? hi? just also any some there here what whats wat wot which how who? when why where?
much many more most very really much tell know let like im ive id dont doesnt isnt cant
""".replace("?", "").split()) - {"thank", "hi", "who", "where"}

# Multi-word phrases joined into one token before matching (raw lowercase, apostrophes removed)
PHRASES = [
    ("how much", "price"), ("how expensive", "price"), ("price list", "price"),
    ("anti wrinkle", "antiwrinkle"), ("antiwrinkle", "antiwrinkle"),
    ("crows feet", "crowsfeet"), ("crow feet", "crowsfeet"),
    ("tear trough", "teartrough"), ("under eye", "undereye"), ("under eyes", "undereye"), ("eye bags", "undereye"),
    ("dark circles", "darkcircle"), ("dark circle", "darkcircle"),
    ("nose job", "rhinoplasty"), ("non surgical rhinoplasty", "rhinoplasty"),
    ("lip flip", "lipflip"), ("gummy smile", "gummysmile"), ("brow lift", "browlift"), ("eyebrow lift", "browlift"),
    ("double chin", "doublechin"), ("love handles", "lovehandle"), ("love handle", "lovehandle"),
    ("hair loss", "hairloss"), ("thinning hair", "hairloss"), ("hair growth", "hairloss"), ("hair thinning", "hairloss"),
    ("spider veins", "spidervein"), ("thread veins", "spidervein"), ("varicose veins", "spidervein"), ("leg veins", "spidervein"),
    ("make up", "makeup"), ("skin booster", "skinbooster"), ("skin boosters", "skinbooster"),
    ("thread lift", "threadlift"), ("face lift", "facelift"), ("glass skin", "glassskin"),
    ("fat dissolving", "fatdissolve"), ("fat dissolve", "fatdissolve"), ("fat dissolver", "fatdissolve"),
    ("opening hours", "hour"), ("opening times", "hour"), ("open now", "hour"),
    ("real person", "human"), ("speak to someone", "human"), ("talk to someone", "human"), ("call back", "human"),
    ("gift card", "voucher"), ("gift voucher", "voucher"), ("side effects", "risk"), ("side effect", "risk"),
    ("where r u", "address"), ("were r u", "address"), ("were are you", "address"), ("where abouts", "address"),
    ("hair removal", "laser"), ("tattoo removal", "tattoo"), ("teeth whitening", "teeth"), ("lash lift", "lash"), ("brow lamination", "lash"),
    ("canning town station", "station"), ("canning town", "address"), ("barking road", "address"), ("nad+", "nad"), ("b 12", "b12"), ("vitamin b12", "b12"),
    ("no cost consultation", "consultation"), ("free consultation", "consultation"), ("complimentary consultation", "consultation"),
    ("no cost", "consultation"), ("level 4", "practitioner"), ("level four", "practitioner"), ("who will treat me", "practitioner"),
    ("good morning", "hello"), ("good afternoon", "hello"), ("good evening", "hello"),
]

# Single words mapped to the word the knowledge base uses (keys are already stemmed)
SYN = {
    "botox": "antiwrinkle", "tox": "antiwrinkle", "toxin": "antiwrinkle", "wrinkle": "antiwrinkle", "botulinum": "antiwrinkle",
    "bottox": "antiwrinkle", "baby": "antiwrinkle",
    "lip": "lip", "pout": "lip", "plump": "lip",
    "poly": "polynucleotide", "polynucleotide": "polynucleotide", "pn": "polynucleotide", "polynucleotides": "polynucleotide",
    "exosome": "exosome", "exo": "exosome",
    "cost": "price", "pricing": "price", "fee": "price", "expensive": "price", "cheap": "price", "cheapest": "price",
    "afford": "price", "affordable": "price", "rate": "price", "£": "price", "quote": "price",
    "location": "address", "e16": "address", "dlr": "station", "jubilee": "station", "located": "address", "where": "address", "direction": "address", "map": "address",
    "postcode": "address", "situated": "address",
    "tube": "station", "underground": "station", "train": "station", "nearest": "station",
    "phone": "contact", "number": "contact", "call": "contact", "telephone": "contact", "ring": "contact", "mobile": "contact",
    "email": "email", "mail": "email",
    "insta": "instagram", "ig": "instagram",
    "appointment": "book", "booking": "book", "reserve": "book", "slot": "book", "availability": "book",
    "available": "book", "schedule": "book", "appt": "book", "session": "book",
    "open": "hour", "opening": "hour", "close": "hour", "closing": "hour", "closed": "hour", "today": "hour",
    "tomorrow": "hour", "weekend": "hour", "saturday": "hour", "sunday": "hour", "monday": "hour", "tuesday": "hour",
    "wednesday": "hour", "thursday": "hour", "friday": "hour", "late": "hour",
    "pregnant": "pregnancy", "breastfeeding": "pregnancy", "nursing": "pregnancy", "breastfeed": "pregnancy",
    "hurt": "pain", "painful": "pain", "sore": "pain", "numbing": "pain", "numb": "pain", "ouch": "pain", "anaesthetic": "pain",
    "men": "male", "man": "male", "guy": "male", "boyfriend": "male", "husband": "male", "gent": "male",
    "wedding": "bridal", "bride": "bridal", "mua": "makeup", "bridesmaid": "bridal",
    "jowl": "sag", "sagging": "sag", "saggy": "sag", "droopy": "sag", "loose": "sag", "tighten": "sag", "tightening": "sag",
    "dermapen": "microneedling", "needling": "microneedling", "microneedle": "microneedling",
    "prp": "hairloss", "bald": "hairloss", "balding": "hairloss",
    "acne": "scar", "scarring": "scar", "pore": "pore",
    "melasma": "pigmentation", "spot": "pigmentation", "sunspot": "pigmentation", "hyperpigmentation": "pigmentation",
    "armpit": "underarm", "sweat": "sweating", "sweaty": "sweating", "hyperhidrosis": "sweating",
    "traptox": "trap", "shoulder": "trap", "barbie": "trap", "trapezius": "trap",
    "belly": "tummy", "stomach": "tummy", "abdomen": "tummy", "abs": "tummy",
    "dissolving": "dissolve", "dissolved": "dissolve", "dissolver": "dissolve", "remove": "removal", "reverse": "removal",
    "hyaluronidase": "removal", "undo": "removal",
    "masseter": "masseter", "grinding": "masseter", "jaw": "jawline",
    "cheekbone": "cheek", "contouring": "contour",
    "smile": "nasolabial", "nasolabial": "nasolabial", "laugh": "nasolabial",
    "circle": "darkcircle", "hollow": "undereye", "puffy": "undereye", "puffiness": "undereye", "bag": "undereye",
    "tired": "undereye", "eye": "undereye",
    "thanks": "thank", "facial": "facial", "hydrafacial": "facial", "shot": "injection", "jab": "injection", "treat": "treatment", "thankyou": "thank", "ty": "thank", "cheers": "thank",
    "hey": "hello", "hi": "hello", "hiya": "hello", "hii": "hello", "helo": "hello", "morning": "hello", "salam": "hello",
    "bye": "bye", "goodbye": "bye", "cya": "bye",
    "person": "human", "someone": "human", "agent": "human", "staff": "human", "real": "human", "speak": "human", "talk": "human",
    "practitioner": "practitioner", "therapist": "practitioner", "doctor": "practitioner", "nurse": "practitioner",
    "injector": "practitioner", "qualified": "practitioner", "qualification": "practitioner", "trained": "practitioner",
    "experience": "practitioner", "experienced": "practitioner", "madina": "practitioner", "shania": "practitioner",
    "safe": "risk", "safety": "risk", "dangerous": "risk", "complication": "risk",
    "nervous": "nervous", "anxious": "nervous", "scared": "nervous", "worried": "nervous", "afraid": "nervous",
    "needle": "nervous", "first": "nervous",
    "deposit": "payment", "pay": "payment", "card": "payment", "cash": "payment", "klarna": "payment",
    "finance": "payment", "instalment": "payment",
    "cancel": "cancel", "cancellation": "cancel", "reschedule": "cancel", "rearrange": "cancel",
    "gift": "voucher", "present": "voucher", "groupon": "voucher",
    "park": "parking", "car": "parking",
    "review": "review", "rating": "review", "reviews": "review", "rated": "review", "google": "review", "testimonial": "review",
    "consultation": "consultation", "consult": "consultation", "assessment": "consultation", "complimentary": "consultation",
    "downtime": "downtime", "recovery": "downtime", "swelling": "downtime", "bruising": "downtime", "bruise": "downtime",
    "aftercare": "aftercare", "after": "aftercare",
    "natural": "natural", "overdone": "natural", "fake": "natural", "subtle": "natural",
    "last": "last", "permanent": "last", "long": "last",
    "age": "age", "old": "age", "teen": "age", "teenager": "age", "minimum": "age", "18": "age", "under18": "age",
    "treatment": "treatment", "service": "treatment", "offer": "treatment", "menu": "treatment", "procedure": "treatment",
    "makeup": "makeup", "glam": "makeup",
}

STARS = "★★★★★"


def stem(t):
    if len(t) > 4 and t.endswith("ies"):
        return t[:-3] + "y"
    if len(t) > 3 and t.endswith("s") and not t.endswith(("ss", "us")):
        return t[:-1]
    return t


def norm(text):
    s = text.lower().replace("&", " and ").replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9+£ ]+", " ", s)
    s = " " + re.sub(r"\s+", " ", s).strip() + " "
    for a, b in PHRASES:
        s = re.sub(r"(?<![a-z0-9])" + re.escape(a) + r"(?![a-z0-9])", b, s)
    out = []
    for t in s.split():
        if t in STOP:
            continue
        t = stem(t)
        t = SYN.get(t, t)
        if t in STOP or (len(t) < 2 and t != "£"):
            continue
        out.append(t)
    return out


def kw(*pairs):
    """kw(("text", weight), ...) -> {token: weight}"""
    k = {}
    for text, w in pairs:
        for t in norm(text):
            k[t] = max(k.get(t, 0), w)
        # also index each word on its own, so "tear" finds "tear trough"
        for raw in re.sub(r"[^a-z0-9+£ ]+", " ", text.lower().replace("'", "")).split():
            if raw in STOP:
                continue
            t = SYN.get(stem(raw), stem(raw))
            if t not in STOP and len(t) > 2 and t not in k:
                k[t] = w * 0.6
    return k


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


# ---------------------------------------------------------------- extra words per treatment / service
PAGE_WORDS = {
    "lip-filler-london": "lip filler lips pout plump volume lipflip",
    "anti-wrinkle-injections-london": "antiwrinkle botox wrinkle lines forehead frown crowsfeet 11s",
    "dermal-fillers-london": "dermal filler cheek jawline chin nose rhinoplasty nasolabial contour",
    "tear-trough-filler-london": "teartrough tear trough undereye darkcircle hollow",
    "skin-boosters-london": "skinbooster skin booster polynucleotide exosome exotox nad glow hydration",
    "pdo-thread-lift-london": "pdo threadlift thread lift sag facelift jowl",
    "fat-dissolving-london": "fatdissolve fat dissolve doublechin tummy thigh arm lovehandle",
    "microneedling-london": "microneedling peel cosmelan dermaplaning pigmentation scar pore texture",
    "bridal-hair-makeup-london": "bridal makeup hair wedding occasion event party",
}
SVC_WORDS = {
    "aw1": "antiwrinkle one 1 area", "aw2": "antiwrinkle two 2 areas forehead frown 11s",
    "aw3": "antiwrinkle three 3 areas forehead frown crowsfeet",
    "adv": "gummysmile lipflip browlift dao mouth corners advanced",
    "mas": "masseter jawline slimming nose slimming", "neck": "neck necklace lines",
    "trap": "trap shoulder", "hyp": "sweating underarm",
    "lip05": "lip filler half 0.5 ml", "fl1": "filler 1ml cheek jawline nose rhinoplasty nasolabial lip contour",
    "chin": "chin filler profile", "tt": "teartrough tear trough undereye darkcircle hollow",
    "hy": "removal dissolve filler hyaluronidase",
    "pn": "polynucleotide skinbooster", "ue": "undereye darkcircle booster",
    "exo": "exosome skinbooster", "exotox": "exotox exosome glassskin", "nad": "nad nad+ energy skin",
    "lipb": "lip booster pink blush hydration",
    "mv": "microneedling vitamin texture pore scar", "hg": "hairloss scalp microneedling",
    "derm": "dermaplaning peach fuzz facial hair exfoliation", "cos": "cosmelan peel pigmentation",
    "pdo1": "pdo threadlift thread one area sag", "pdo2": "pdo threadlift thread full face neck sag",
    "fd1": "fatdissolve doublechin chin face fat", "fd2": "fatdissolve arm lovehandle fat", "fd3": "fatdissolve thigh tummy fat",
    "b12": "b12 vitamin energy injection", "glu": "glutathione antioxidant brightening",
    "scl": "spidervein sclerotherapy legs", "gm": "makeup glam party event",
    "hm": "hair makeup styling", "bridal": "bridal wedding hair makeup",
}
SVC_PAGE = {
    "aw1": "anti-wrinkle-injections-london", "aw2": "anti-wrinkle-injections-london", "aw3": "anti-wrinkle-injections-london",
    "adv": "anti-wrinkle-injections-london", "mas": "anti-wrinkle-injections-london", "neck": "anti-wrinkle-injections-london",
    "trap": "anti-wrinkle-injections-london", "hyp": "anti-wrinkle-injections-london",
    "lip05": "lip-filler-london", "lipb": "lip-filler-london", "fl1": "dermal-fillers-london", "chin": "dermal-fillers-london",
    "tt": "tear-trough-filler-london", "hy": "dermal-fillers-london", "ue": "tear-trough-filler-london",
    "pn": "skin-boosters-london", "exo": "skin-boosters-london", "exotox": "skin-boosters-london", "nad": "skin-boosters-london",
    "mv": "microneedling-london", "hg": "microneedling-london", "derm": "microneedling-london", "cos": "microneedling-london",
    "pdo1": "pdo-thread-lift-london", "pdo2": "pdo-thread-lift-london",
    "fd1": "fat-dissolving-london", "fd2": "fat-dissolving-london", "fd3": "fat-dissolving-london",
    "gm": "bridal-hair-makeup-london", "hm": "bridal-hair-makeup-london", "bridal": "bridal-hair-makeup-london",
}


def build_kb(b, services, home_html):
    """b = the build module (constants and TREATMENTS); services = price menu rows."""
    E = []
    book = ["Book now", b.BOOK, "book"]
    wa = ["WhatsApp us", b.WHATSAPP, "wa"]
    call = [f"Call {b.PHONE}", f"tel:{b.PHONE_INTL}", "tel"]
    by_slug = {t["slug"]: t for t in b.TREATMENTS}
    plain = lambda s: strip_tags(s)

    # Treatment pages: overview with prices
    for t in b.TREATMENTS:
        name = plain(t["name"])
        items = [[plain(services[s]["name"]), plain(services[s]["price_text"]), services[s]["dur"]] for s in t["services"]]
        facts = "; ".join(f"{l.lower()}: {v}" for v, l in t["facts"][:3])
        E.append({
            "id": "page-" + t["slug"], "t": name,
            "k": kw((name, 3), (PAGE_WORDS[t["slug"]], 2), (plain(t["eyebrow"]), 1), (t["summary"], 0.5), ("price", 0.6)),
            "a": [t["summary"], f"At a glance ({facts})."],
            "items": items,
            "links": [[f"About {name.lower() if not name.startswith('PDO') else name}", f"/{t['slug']}/", "page"], book],
        })
        for i, (q, a) in enumerate(t["faqs"]):
            E.append({
                "id": f"faq-{t['slug']}-{i}", "t": q,
                "k": kw((q, 2), (name, 1.2), (PAGE_WORDS[t["slug"]], 1)),
                "a": [a], "links": [[f"About {name.lower() if not name.startswith('PDO') else name}", f"/{t['slug']}/", "page"], book],
            })

    # Every priced service
    for sid, s in services.items():
        name = plain(s["name"])
        page = SVC_PAGE.get(sid)
        links = [book]
        if page:
            pn = plain(by_slug[page]["name"])
            links.insert(0, [f"About {pn.lower() if not pn.startswith('PDO') else pn}", f"/{page}/", "page"])
        E.append({
            "id": "svc-" + sid, "t": name,
            "k": kw((name, 2.5), (SVC_WORDS.get(sid, ""), 2), (plain(s["desc"]), 0.6), ("price", 0.8)),
            "a": [f"{name} is {plain(s['price_text'])} and takes about {s['dur']}.", plain(s["desc"])],
            "links": links,
        })

    # Home page FAQs
    for i, m in enumerate(re.finditer(r"<details[^>]*>\s*<summary>(.*?)</summary>\s*<div class=\"answer\"><p>(.*?)</p>", home_html, re.S)):
        q, a = plain(m.group(1)), plain(m.group(2))
        E.append({"id": f"faq-home-{i}", "t": q, "k": kw((q, 2)), "a": [a], "links": [book]})

    # General answers
    rating, count, gurl = b.REVIEWS["rating"], b.REVIEWS["count"], b.REVIEWS["google_url"]
    G = [
        ("hello", "Hello", "hello hey hi", [
            "Hello! I can help with treatments, prices, opening hours, booking and aftercare. What would you like to know?"], [], 1.0),
        ("thanks", "Thank you", "thank", ["You're welcome! Is there anything else I can help with?"], [book], 1.0),
        ("bye", "Goodbye", "bye", ["Thanks for stopping by. When you're ready, you can book online any time."], [book], 1.0),
        ("hours", "Opening hours", "hour", ["{hours}"], [book, call], 1.0),
        ("address", "Where we are", "address clinic",
         [f"We're at {b.ADDRESS_LINES[0]}, {b.ADDRESS_LINES[1]}, a few minutes' walk from Canning Town station (Jubilee line and DLR)."],
         [["Get directions", b.MAPS, "url"], book], 1.0),
        ("station", "Closest station", "station",
         ["Our closest station is Canning Town (Jubilee line and DLR), a few minutes' walk away."], [["Get directions", b.MAPS, "url"]], 1.0),
        ("parking", "Parking", "parking",
         ["We're on Barking Road in Canning Town, a few minutes from Canning Town station. For parking advice, give us a call before your visit."],
         [call, ["Get directions", b.MAPS, "url"]], 1.0),
        ("contact", "Contact us", "contact",
         [f"You can call us on {b.PHONE}, message us on WhatsApp, or email {b.EMAIL}. You can also send a question through the form on our website."],
         [call, wa, ["Send a message", "/#contact", "page"]], 1.0),
        ("human", "Speak to someone", "human",
         ["Of course. The quickest way to reach a person is WhatsApp or a call. You can also leave your details in our contact form and we'll get back to you."],
         [wa, call, ["Contact form", "/#contact", "page"]], 1.0),
        ("email", "Email", "email", [f"Our email is {b.EMAIL}."], [[f"Email us", f"mailto:{b.EMAIL}", "mail"]], 1.0),
        ("whatsapp", "WhatsApp", "whatsapp", ["Yes, you can message us on WhatsApp."], [wa], 1.0),
        ("instagram", "Instagram", "instagram", ["Follow us on Instagram @glam_beauty__aesthetics for recent work."],
         [["Open Instagram", b.INSTAGRAM, "url"]], 1.0),
        ("book", "How to book", "book online",
         ["You can book online in about a minute. Tap Book now, choose your treatment and a time that suits you, and confirm. We're open seven days a week."],
         [book, wa], 1.0),
        ("cancel", "Changing a booking", "cancel book",
         ["To change or cancel an appointment, please contact us as early as you can by phone or WhatsApp."], [wa, call], 1.0),
        ("payment", "Payment and deposits", "payment",
         ["Any deposit is shown when you book online. For questions about payment options, give us a call or send a WhatsApp."],
         [book, wa], 1.0),
        ("voucher", "Gift vouchers", "voucher",
         ["For gift vouchers or vouchers you've bought elsewhere, please message us on WhatsApp or call and we'll help."], [wa, call], 1.0),
        ("prices", "Prices", "price",
         ["Treatments start at £20. A few favourites:"], [["See the full price list", "/#treatments", "page"], book], 0.9),
        ("treatments", "Our treatments", "treatment",
         ["We offer anti-wrinkle injections, lip and dermal fillers, tear trough filler, skin boosters (including polynucleotides and exosomes), PDO thread lifts, fat dissolving, microneedling, peels, hair growth therapy, vitamin injections, and bridal hair and makeup."],
         [["Find your treatment", "/#face-map", "page"], ["Full price list", "/#treatments", "page"]], 0.9),
        ("consultation", "Free consultation", "consultation advice",
         ["Yes, your consultation is free, with no obligation to go ahead. You'll talk through what you'd like to change and your medical history, and leave with a clear plan and price."],
         [["Request a consultation", "/?consult=1#contact", "page"], ["Ask on WhatsApp", "https://wa.me/447988347194?text=Hi%2C%20I%27d%20like%20to%20book%20a%20free%20consultation.", "wa"]], 1.0),
        ("practitioner", "Who does the treatments", "practitioner who",
         [f"Treatments are carried out by our Level 4 advanced qualified professional, who explains everything before starting. Clients often mention how clearly everything is explained: we're rated {rating} from {count} Google reviews.",
          "If you'd like to know more about her training, just ask on WhatsApp."],
         [["Read reviews", "/#reviews", "page"], wa], 1.0),
        ("reviews", "Reviews", "review",
         [f"We're rated {rating} out of 5 from {count} reviews on Google. Clients often mention feeling at ease and how clearly everything is explained."],
         [["Read reviews", "/#reviews", "page"], ["See them on Google", gurl, "url"]], 1.0),
        ("age", "Age limit", "age",
         ["By UK law, anti-wrinkle injections and dermal fillers for cosmetic reasons are only available to people aged 18 or older."], [book], 1.0),
        ("pregnancy", "Pregnancy and breastfeeding", "pregnancy",
         ["Most injectable and skin treatments aren't suitable during pregnancy or while breastfeeding. Please mention it when you get in touch so your practitioner can advise."],
         [wa], 1.0),
        ("male", "Treatments for men", "male",
         ["Yes, we treat men as well as women. Anti-wrinkle injections, jaw slimming, skin boosters, microneedling and hair growth therapy are all suitable for men."],
         [book], 1.0),
        ("pain", "Does it hurt?", "pain",
         ["Most treatments are quick and well tolerated. Many fillers contain a local anaesthetic, and numbing cream can be used where it's suitable. Several clients describe their treatment as almost pain-free in their reviews."],
         [book], 1.0),
        ("nervous", "Feeling anxious", "nervous",
         ["That's completely normal, especially for a first treatment. Everything is explained before anything starts, you can ask as many questions as you like, and you'll be checked on throughout."],
         [["Read reviews", "/#reviews", "page"], wa], 1.0),
        ("risk", "Safety and side effects", "risk",
         ["Every treatment carries some risk, most commonly swelling, redness or bruising for a few days, and rarely more serious reactions. Your practitioner will explain the risks of your treatment and check your medical history before starting."],
         [wa], 1.0),
        ("downtime", "Downtime", "downtime",
         ["Most injectable treatments have little downtime. You may have mild swelling, redness or bruising for a few days. Each treatment page lists its typical downtime."],
         [["Find your treatment", "/#face-map", "page"]], 1.0),
        ("aftercare", "Aftercare", "aftercare",
         ["You'll get aftercare advice before you leave. As a general guide after injectables: avoid make-up on the area, alcohol, strenuous exercise and heat such as saunas for 24 hours."],
         [wa], 0.9),
        ("natural", "Natural results", "natural look result",
         ["That's our aim with every treatment: to enhance your natural beauty, not change it. The amount and placement are planned around your features, so you look refreshed rather than \"done\"."],
         [book], 1.0),
        ("facial", "Facials and skin treatments", "facial glow skin",
         ["We focus on advanced skin treatments rather than classic facials. Popular choices are dermaplaning (£59) for an instant glow, multi-vitamin microneedling (£120) for texture, and skin boosters such as polynucleotides (£125)."],
         [["Microneedling & peels", "/microneedling-london/", "page"], ["Skin boosters", "/skin-boosters-london/", "page"], book], 1.0),
        ("notoffered", "Not on our menu",
         "laser tattoo tatoo teeth tooth whitening nail manicure pedicure gel acrylic lash eyelash extension wax waxing threading massage tan spray piercing haircut barber ipl hifu coolsculpting",
         ["That isn't on our treatment menu at the moment. If you'd like to check, message us on WhatsApp.",
          "Our treatments include anti-wrinkle injections, lip and dermal fillers, skin boosters, microneedling and peels, PDO thread lifts, fat dissolving, and bridal hair and makeup."],
         [["See all treatments", "/#treatments", "page"], wa], 1.0),
        ("about", "About the clinic", "clinic about glam beauty aesthetics",
         ["Glam Beauty Aesthetics is a London clinic for non-surgical facial contouring, medical-grade skin treatments, and bridal hair and makeup. We're open seven days a week."],
         [["About us", "/#about", "page"], book], 0.8),
    ]
    for gid, title, words, answer, links, pri in G:
        e = {"id": "gen-" + gid, "t": title, "k": kw((words, 3)), "a": answer, "links": links}
        if pri != 1.0:
            e["p"] = pri
        E.append(e)

    # The "Prices" answer lists the starting price of each main treatment
    for e in E:
        if e["id"] == "gen-prices":
            e["items"] = [[plain(t["name"]), "from £%d" % b.min_price(t, services), ""] for t in b.TREATMENTS]

    return {
        "v": 1,
        "book": b.BOOK,
        "hours": [[1, "10:00", "17:30"], [2, "09:30", "17:30"], [3, "10:00", "17:30"], [4, "10:00", "17:30"],
                  [5, "10:00", "17:30"], [6, "09:30", "16:00"], [0, "09:30", "16:00"]],
        "stop": sorted(STOP), "phrases": PHRASES, "syn": SYN,
        "start": ["Free consultation", "Prices", "Opening hours", "How do I book?", "Lip filler", "Where are you?"],
        "fallback": {
            "a": ["Sorry, I don't have an answer for that one yet. Try asking about a treatment, prices, opening hours or booking, or message us and we'll help."],
            "links": [wa, call],
        },
        "entries": E,
    }
