"""
Builds the treatment pages and sitemap for glambeautyaesthetic.com.

    python _build/build.py

Prices, durations and treatment names are read from the menu in index.html,
so after changing a price there, run this again to update every page.
Page copy lives in TREATMENTS below. Don't upload the _build folder.
"""
import html
import sys
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.glambeautyaesthetic.com"
BOOK = "https://facesconsent.com/clinics/glam-beauty-aesthetics-382436/madina?clinicName=madina"
PHONE_INTL = "+447988347194"
PHONE = "07988 347194"
EMAIL = "shania0712@googlemail.com"
INSTAGRAM = "https://www.instagram.com/glam_beauty__aesthetics/"
FACEBOOK = "https://www.facebook.com/profile.php?id=61596324786832"
TIKTOK = "https://www.tiktok.com/@glam_beauty__aesthetics"
ADDRESS_LINES = ["28 Barking Road, Canning Town", "London E16 1EQ"]
STREET, POSTCODE = "28 Barking Road, Canning Town", "E16 1EQ"
MAPS = "https://www.google.com/maps/search/?api=1&query=28+Barking+Road+Canning+Town+London+E16+1EQ"
ASSET_V = "40"
# Vercel Web Analytics (turn on in the Vercel dashboard: Project > Analytics > Enable)
VERCEL_ANALYTICS = '<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)};</script>\n<script defer src="/_vercel/insights/script.js"></script>\n'
import extra_pages
REVIEWS = json.loads((Path(__file__).resolve().parent / "reviews.json").read_text(encoding="utf-8"))
STARS = '<span class="stars" aria-hidden="true">★★★★★</span>'
WHATSAPP = "https://wa.me/447988347194?text=Hi%2C%20I%27d%20like%20to%20ask%20about%20a%20treatment"

# Points on the face drawing (360 x 460 viewBox) used to highlight treatment areas.
P = {
    "forehead": [(180, 118)], "frown": [(180, 166)], "crows": [(112, 190), (248, 190)],
    "undereye": [(144, 214), (216, 214)], "nose": [(180, 236)], "cheeks": [(128, 252), (232, 252)],
    "nasolabial": [(158, 282), (202, 282)], "lips": [(180, 306)], "jaw": [(114, 302), (246, 302)],
    "masseter": [(104, 270), (256, 270)], "chin": [(180, 358)], "neck": [(180, 410)],
}

TREATMENTS = [
  {
    "slug": "lip-filler-london",
    "name": "Lip filler",
    "title": "Lip Filler London | From £90 | Glam Beauty Aesthetics",
    "description": "Natural-looking lip filler in London from £90 for 0.5 ml. Add shape, definition and hydration. Open 7 days. Book online at Glam Beauty Aesthetics.",
    "eyebrow": "Dermal fillers · London",
    "h1": "Lip filler", "h1_em": "in London.",
    "summary": "Shape, definition or a little more volume, built gradually so your lips stay in proportion with the rest of your face.",
    "points": ["lips"], "area_label": "Lips",
    "facts": [("30–45 min", "Treatment time"), ("6–12 months", "Typical results"), ("1–3 days", "Swelling settles"), ("0.5 ml", "A natural first step")],
    "services": ["lip05", "fl1", "lipb", "adv", "hy"],
    "body": """
<h2>What lip filler does</h2>
<p>Lip filler is a hyaluronic acid gel, a substance found naturally in your skin. It can add volume, sharpen the border of the lips, correct small asymmetries and hydrate lips that have thinned with age.</p>
<p>The amount and placement are planned around your face. For a first treatment, 0.5 ml is often enough for a subtle change. 1 ml gives more noticeable shape and volume.</p>
<h2>Which option suits you?</h2>
<ul>
<li><span><strong>Lip filler, 0.5 ml (£90):</strong> a subtle first treatment or a top-up.</span></li>
<li><span><strong>Lip filler, 1 ml (£100):</strong> more shape and volume.</span></li>
<li><span><strong>Lip booster with pink blush (£125):</strong> hydration and a soft natural tint rather than added volume.</span></li>
<li><span><strong>Lip flip (£98):</strong> a small anti-wrinkle treatment that turns the top lip slightly outwards, with no filler.</span></li>
</ul>
<h2>Your appointment</h2>
<p>You start by talking through the look you want and your medical history. Most lip fillers contain a local anaesthetic to keep you comfortable, and the treatment takes around 30 minutes. You'll see a difference straight away. Swelling means the final result settles within about two weeks.</p>
<h2>Aftercare</h2>
<p>Some swelling, tenderness and possibly bruising are normal for a few days. For the first 24 hours, avoid lipstick, alcohol, strenuous exercise and heat such as saunas. You'll get aftercare advice before you leave.</p>
""",
    "faqs": [
      ("How long does lip filler last?", "Usually around 6 to 12 months. It varies with the product used, your metabolism and your lifestyle."),
      ("Will my lips look natural?", "That is the aim. Starting with a smaller amount and building gradually is the most reliable way to keep lips in proportion with your face."),
      ("Does lip filler hurt?", "Most people find it uncomfortable rather than painful. Most fillers contain a local anaesthetic that numbs the area as the treatment goes on."),
      ("Can lip filler be dissolved?", "Yes. Hyaluronic acid filler can be dissolved with hyaluronidase, which costs £125 per 1 ml."),
    ],
    "related": ["dermal-fillers-london", "skin-boosters-london", "anti-wrinkle-injections-london"],
  },
  {
    "slug": "anti-wrinkle-injections-london",
    "name": "Anti-wrinkle injections",
    "title": "Anti-Wrinkle Injections London | From £90 | Glam Beauty Aesthetics",
    "description": "Anti-wrinkle injections in London from £90 for one area. Soften forehead lines, frown lines and crow's feet while keeping a natural expression. Book online.",
    "eyebrow": "Anti-wrinkle · London",
    "h1": "Anti-wrinkle injections", "h1_em": "in London.",
    "summary": "Soften forehead lines, frown lines and crow's feet while keeping your natural expression.",
    "points": ["forehead", "frown", "crows"], "area_label": "Forehead, frown lines & eyes",
    "facts": [("20–45 min", "Treatment time"), ("3–4 months", "Typical results"), ("2 weeks", "To full effect"), ("Little to none", "Downtime")],
    "services": ["aw1", "aw2", "aw3", "adv", "mas", "neck", "trap", "hyp"],
    "body": """
<h2>How anti-wrinkle injections work</h2>
<p>Many lines on the upper face come from repeated muscle movement: raising your eyebrows, frowning, smiling. Anti-wrinkle injections relax the specific muscles behind those lines, so the skin above them smooths out.</p>
<p>Anti-wrinkle injections are a prescription-only medicine, so your suitability is assessed before any treatment.</p>
<h2>Areas we treat</h2>
<ul>
<li><span><strong>Forehead lines, frown lines and crow's feet:</strong> 1 area £90, 2 areas £114, 3 areas £150.</span></li>
<li><span><strong>Brow lift, lip flip, gummy smile and downturned mouth corners (DAO):</strong> £98.</span></li>
<li><span><strong>Jaw slimming (masseter) or nose slimming:</strong> £124.</span></li>
<li><span><strong>Neck anti-wrinkle:</strong> £163.</span></li>
<li><span><strong>Traptox, for a slimmer shoulder line:</strong> £228.</span></li>
<li><span><strong>Excessive underarm sweating (hyperhidrosis):</strong> £228.</span></li>
</ul>
<h2>What to expect</h2>
<p>Treatment takes 20 to 45 minutes depending on the number of areas. The injections are very fine and quick, and most people find them easy to tolerate. Results start to show after 3 to 5 days and reach full effect at around two weeks.</p>
<h2>Aftercare</h2>
<p>Stay upright for 4 hours after treatment and avoid rubbing or massaging the area. Skip strenuous exercise, saunas and alcohol for 24 hours.</p>
""",
    "faqs": [
      ("How long do anti-wrinkle injections last?", "Usually around 3 to 4 months, after which muscle movement gradually returns."),
      ("Will I still be able to move my face?", "Yes. The aim is to soften lines, not freeze your expression. The dose is adjusted to how much movement you want to keep."),
      ("How many areas should I have treated?", "Most people start with forehead and frown lines (2 areas, £114) or add crow's feet (3 areas, £150). You'll get a recommendation for your face at your appointment."),
      ("Is there an age limit?", "Yes. By UK law, anti-wrinkle injections for cosmetic reasons are only available to people aged 18 or older."),
    ],
    "related": ["skin-boosters-london", "dermal-fillers-london", "lip-filler-london"],
  },
  {
    "slug": "dermal-fillers-london",
    "name": "Dermal fillers",
    "title": "Dermal Fillers London | Cheeks, Jaw & Chin | Glam Beauty Aesthetics",
    "description": "Dermal fillers in London for cheeks, jawline, chin, nose and smile lines. Contour and restore volume naturally, 1 ml from £100. Open 7 days, book online.",
    "eyebrow": "Facial contouring · London",
    "h1": "Dermal fillers", "h1_em": "in London.",
    "summary": "Contour the cheeks, sharpen the jawline, balance the chin and soften smile lines, with results that suit your face shape.",
    "points": ["cheeks", "jaw", "chin", "nose", "nasolabial"], "area_label": "Cheeks, jaw, chin & nose",
    "facts": [("30–45 min", "Treatment time"), ("6–18 months", "Typical results"), ("A few days", "Mild swelling"), ("From £98", "Per treatment")],
    "services": ["fl1", "chin", "tt", "lip05", "hy"],
    "body": """
<h2>What dermal fillers can do</h2>
<p>As we age, the face loses volume and the contours of the cheeks and jaw soften. Hyaluronic acid fillers restore that structure, and can also define features that have always been less prominent.</p>
<h2>Areas we treat</h2>
<ul>
<li><span><strong>Cheeks:</strong> lift and contour the mid-face.</span></li>
<li><span><strong>Jawline:</strong> a sharper, more defined jaw.</span></li>
<li><span><strong>Chin:</strong> more projection to balance your profile (£98).</span></li>
<li><span><strong>Nose (non-surgical rhinoplasty):</strong> smooth a bump or lift the tip.</span></li>
<li><span><strong>Nasolabial folds:</strong> soften the lines from nose to mouth.</span></li>
<li><span><strong>Under the eyes:</strong> see <a href="/tear-trough-filler-london/">tear trough filler</a>.</span></li>
</ul>
<p>Cheeks, jawline, nose, nasolabial folds and lips are £100 per 1 ml.</p>
<h2>Your appointment</h2>
<p>Your face is looked at as a whole, not one feature at a time, and you agree a plan before any filler is placed. Treatment takes 30 to 45 minutes. Results are visible straight away and settle within about two weeks.</p>
<h2>Aftercare</h2>
<p>Some swelling, tenderness or bruising is normal for a few days. For 24 hours, avoid make-up on the treated area, alcohol, strenuous exercise and heat such as saunas.</p>
""",
    "faqs": [
      ("How long do dermal fillers last?", "Generally 6 to 18 months depending on the area. Cheeks and jawline tend to last longer than areas that move a lot, such as the lips."),
      ("Is a non-surgical nose job permanent?", "No. It reshapes the nose with filler rather than surgery, and results usually last around a year. It can smooth a bump or lift the tip, but it can't make the nose smaller."),
      ("Can filler be reversed?", "Yes. Hyaluronic acid filler can be dissolved with hyaluronidase, which costs £125 per 1 ml."),
    ],
    "related": ["lip-filler-london", "tear-trough-filler-london", "pdo-thread-lift-london"],
  },
  {
    "slug": "tear-trough-filler-london",
    "name": "Tear trough filler",
    "title": "Tear Trough Filler London | £195 | Glam Beauty Aesthetics",
    "description": "Tear trough filler in London to soften under-eye hollows and the look of dark circles, £195 for 1 ml. Under-eye skin booster from £95. Book online.",
    "eyebrow": "Under-eye treatments · London",
    "h1": "Tear trough filler", "h1_em": "in London.",
    "summary": "Soften the hollows under your eyes so you look rested, not tired.",
    "points": ["undereye"], "area_label": "Under the eyes",
    "facts": [("45 min", "Treatment time"), ("9–12 months", "Typical results"), ("Up to 10 days", "Possible bruising"), ("From £95", "Under-eye booster")],
    "services": ["tt", "ue", "hy"],
    "body": """
<h2>What tear trough filler treats</h2>
<p>The tear trough is the groove that runs from the inner corner of the eye towards the cheek. When it deepens, it casts a shadow that makes you look tired even after a good night's sleep. A small amount of soft hyaluronic acid filler fills the hollow and reduces the shadow.</p>
<h2>Is it right for you?</h2>
<p>Tear trough filler works best for hollows and shadows, and it isn't the right choice for everyone. If your concern is mostly puffiness, thin crepey skin or pigmentation, the <strong>under-eye skin booster (£95)</strong> may suit you better, because it improves the skin rather than adding volume. You'll be advised which is right for you at your appointment.</p>
<h2>Your appointment</h2>
<p>The under-eye area is delicate, so treatment is careful and gradual. It takes around 45 minutes. Results are visible straight away and settle within two weeks.</p>
<h2>Aftercare</h2>
<p>Bruising and swelling are more common around the eyes than elsewhere and usually settle within a week to ten days. Avoid make-up on the area, alcohol, exercise and heat for 24 hours.</p>
""",
    "faqs": [
      ("How long does tear trough filler last?", "Often 9 to 12 months, and sometimes longer, because there is little movement in the area."),
      ("Will it get rid of my dark circles?", "It helps when dark circles come from the shadow of a hollow. Dark circles caused by pigmentation respond better to a different approach, such as a skin booster or peel."),
      ("Can it be dissolved?", "Yes. Hyaluronic acid filler can be dissolved with hyaluronidase, which costs £125 per 1 ml."),
    ],
    "related": ["skin-boosters-london", "dermal-fillers-london", "anti-wrinkle-injections-london"],
  },
  {
    "slug": "skin-boosters-london",
    "name": "Skin boosters",
    "title": "Polynucleotides & Skin Boosters London | Glam Beauty Aesthetics",
    "description": "Radiesse, polynucleotides, exosomes, Exo-Tox, NAD+ and under-eye skin boosters in London from £95. Improve texture, firmness and glow. Book online.",
    "eyebrow": "Skin boosters · London",
    "h1": "Skin boosters", "h1_em": "in London.",
    "summary": "Treatments that improve your skin itself: texture, hydration, firmness and glow.",
    "points": [], "whole_face": True, "area_label": "The whole face",
    "facts": [("30–60 min", "Treatment time"), ("2–4 weeks", "Results build"), ("1–2 days", "Small bumps settle"), ("From £95", "Per treatment")],
    "services": ["rad", "pn", "ue", "exo", "exotox", "nad", "lipb"],
    "body": """
<h2>What skin boosters do</h2>
<p>Fillers change shape. Skin boosters change the skin. They support its own repair processes to improve texture, hydration and elasticity, so the result is fresher, healthier-looking skin rather than added volume.</p>
<h2>Our skin boosters</h2>
<ul>
<li><span><strong>Radiesse skin booster (£325):</strong> a collagen-stimulating injectable that helps firm and tighten crepey or loose skin, with results that build gradually as collagen forms.</span></li>
<li><span><strong>Polynucleotides (£125):</strong> help the skin repair and renew itself. Popular for crepey skin and fine lines.</span></li>
<li><span><strong>Under-eye booster (£95):</strong> for dark circles, puffiness and thin skin under the eyes.</span></li>
<li><span><strong>Exosomes (£125):</strong> a regenerative treatment to improve texture and support healing.</span></li>
<li><span><strong>Exo-Tox (£125):</strong> exosomes combined with toxin for a smooth, glass-skin finish.</span></li>
<li><span><strong>NAD+ therapy (£125):</strong> boosts cellular energy to support general skin health.</span></li>
<li><span><strong>Lip booster with pink blush (£125):</strong> hydration and a soft tint for the lips.</span></li>
</ul>
<h2>How many sessions?</h2>
<p>Skin boosters work gradually. Most people see the best results from a course of treatments spaced a few weeks apart, followed by occasional top-ups. You'll get a plan that suits your skin and budget.</p>
<h2>Aftercare</h2>
<p>Small bumps, redness or tiny bruises at the injection points are normal and usually fade within a day or two. Avoid make-up for 12 hours, and exercise, alcohol and heat for 24 hours. Wear SPF every day.</p>
""",
    "faqs": [
      ("What's the difference between a skin booster and filler?", "Filler adds volume and changes shape. A skin booster improves the quality of the skin itself, such as hydration, texture and firmness, without changing your features."),
      ("When will I see results?", "Usually gradually across 2 to 4 weeks as your skin responds, improving further with each session in a course."),
      ("Can I combine skin boosters with other treatments?", "Often, yes. Skin boosters pair well with anti-wrinkle injections and microneedling. Ask at your appointment which combination suits you."),
    ],
    "related": ["microneedling-london", "tear-trough-filler-london", "anti-wrinkle-injections-london"],
  },
  {
    "slug": "pdo-thread-lift-london",
    "name": "PDO thread lift",
    "title": "PDO Thread Lift London | From £163 | Glam Beauty Aesthetics",
    "description": "PDO mono thread lift in London from £163 for one area, or £228 for full face and neck. Tighten skin and boost collagen without surgery. Book online.",
    "eyebrow": "Thread lifts · London",
    "h1": "PDO thread lift", "h1_em": "in London.",
    "summary": "Fine, dissolvable threads that tighten skin and stimulate collagen, without surgery.",
    "points": ["jaw", "cheeks", "neck"], "area_label": "Jawline, cheeks & neck",
    "facts": [("45–90 min", "Treatment time"), ("6–9 months", "Typical results"), ("4–8 weeks", "Firmness builds"), ("From £163", "Per treatment")],
    "services": ["pdo1", "pdo2"],
    "body": """
<h2>What a PDO mono thread lift does</h2>
<p>PDO (polydioxanone) threads are very fine, dissolvable threads placed just under the skin through a tiny entry point. Mono threads are smooth threads laid in a mesh pattern. As your body absorbs them during the following months, they stimulate fresh collagen, which tightens and firms the skin.</p>
<p>Mono threads improve firmness and skin quality. They give a subtle tightening rather than a dramatic lift, and they are not a replacement for a surgical facelift.</p>
<h2>Areas we treat</h2>
<ul>
<li><span><strong>One area (£163):</strong> for example the jowls, jawline, cheeks, under the chin or the neck.</span></li>
<li><span><strong>Full face and neck (£228):</strong> all-round firming and support.</span></li>
</ul>
<h2>Your appointment</h2>
<p>A single area takes about 45 minutes, and full face and neck around 90 minutes. The area is numbed first to keep you comfortable. Firmness continues to improve during the following 4 to 8 weeks as collagen builds.</p>
<h2>Aftercare</h2>
<p>Mild swelling, tenderness and bruising are common for a few days. For one to two weeks, avoid strenuous exercise, saunas, facial massage and dental treatment, and try not to make very big facial expressions.</p>
""",
    "faqs": [
      ("What's the difference between threads and filler?", "Filler restores volume. Threads tighten and firm the skin. The two are often combined for a fuller result."),
      ("How long do PDO thread results last?", "The threads dissolve across several months. The collagen they stimulate keeps the skin firmer for around 6 to 9 months, depending on your skin."),
      ("Is a thread lift painful?", "The area is numbed first. Most people feel some pressure and mild discomfort rather than pain."),
    ],
    "related": ["dermal-fillers-london", "skin-boosters-london", "anti-wrinkle-injections-london"],
  },
  {
    "slug": "fat-dissolving-london",
    "name": "Fat dissolving",
    "title": "Fat Dissolving Injections London | From £98 | Glam Beauty Aesthetics",
    "description": "Fat dissolving injections in London for the double chin, arms, love handles, thighs and tummy, from £98. Non-surgical with minimal downtime. Book online.",
    "eyebrow": "Body contouring · London",
    "h1": "Fat dissolving", "h1_em": "in London.",
    "summary": "Non-surgical injections that break down small pockets of stubborn fat that diet and exercise haven't shifted.",
    "points": ["chin"], "area_label": "Chin, plus arms, waist, thighs & tummy",
    "facts": [("30–60 min", "Treatment time"), ("2–4 sessions", "Usual course"), ("4–6 weeks", "Results show"), ("From £98", "Per session")],
    "services": ["fd1", "fd2", "fd3"],
    "body": """
<h2>How fat dissolving works</h2>
<p>Fat dissolving injections contain ingredients that break down the membrane of fat cells in the treated area. Your body then clears the released fat naturally during the following weeks.</p>
<h2>Who it's for</h2>
<p>Fat dissolving is for small, stubborn areas of fat. It is not a weight-loss treatment, and it works best for people who are close to their goal weight.</p>
<h2>Areas and prices</h2>
<ul>
<li><span><strong>Under the chin or face:</strong> £98 per session.</span></li>
<li><span><strong>Arms or love handles:</strong> £130 per session.</span></li>
<li><span><strong>Thighs or tummy:</strong> £163 per session.</span></li>
</ul>
<h2>Your appointment</h2>
<p>The area is assessed and marked before treatment. Most areas respond best to a course of two to four sessions, spaced several weeks apart, for the best result.</p>
<h2>Aftercare</h2>
<p>Swelling, redness, tenderness and a warm feeling in the area are normal and can last several days. Under the chin, swelling can be quite noticeable at first. Drink plenty of water, and avoid alcohol and strenuous exercise for 48 hours.</p>
""",
    "faqs": [
      ("Are the results permanent?", "Fat cells that are destroyed don't come back. The remaining fat cells can still grow if you gain weight, so a stable lifestyle helps keep results."),
      ("How soon will I see results?", "Changes usually show from around 4 to 6 weeks after a session, and build with each session in the course."),
      ("Is it painful?", "Most people feel a stinging or warm sensation during and shortly after treatment, which settles during the following hours."),
    ],
    "related": ["dermal-fillers-london", "anti-wrinkle-injections-london", "pdo-thread-lift-london"],
  },
  {
    "slug": "microneedling-london",
    "name": "Microneedling &amp; peels",
    "title": "Microneedling, Facials & Peels London | From £50 | Glam Beauty",
    "description": "Microneedling, Korean glass facials, dermaplaning, hair growth therapy and Cosmelan peels in London from £50. Brighter, smoother skin. Book online.",
    "eyebrow": "Skin treatments · London",
    "h1": "Microneedling &amp; peels", "h1_em": "in London.",
    "summary": "Treatments for texture, brightness, pigmentation and thinning hair.",
    "points": [], "whole_face": True, "area_label": "Face and scalp",
    "facts": [("45–60 min", "Treatment time"), ("3–6 sessions", "Microneedling course"), ("1–2 days", "Redness settles"), ("From £50", "Per treatment")],
    "services": ["kgf", "mv", "hg", "derm", "cos"],
    "body": """
<h2>Multi-vitamin microneedling</h2>
<p>Microneedling (£120) creates tiny channels in the skin using a pen with ultra-fine points. This prompts the skin to repair itself and produce fresh collagen, and helps a vitamin serum absorb more deeply. It helps with dull skin, uneven texture, open pores and mild scarring.</p>
<h2>Hair growth therapy</h2>
<p>For thinning hair, scalp injections are combined with microneedling (£125) to stimulate the hair follicles. It is usually done as a course, and results build gradually across several months.</p>
<h2>Dermaplaning</h2>
<p>Dermaplaning (£59) is a gentle exfoliation with a sterile blade that removes dead skin and fine facial hair. Skin looks brighter straight away, make-up goes on more smoothly, and there's no downtime.</p>
<h2>Korean glass facial</h2>
<p>The Korean glass facial (£50) is a multi-step hydrating facial inspired by Korean skincare. It cleanses, gently exfoliates and deeply hydrates the skin for a smooth, dewy, light-reflecting “glass skin” finish. There's no downtime, so it's a lovely treat before an event.</p>
<h2>Cosmelan peel</h2>
<p>Cosmelan (£553, aftercare products included) is a professional depigmentation peel for stubborn melasma, sun spots and uneven tone. The mask is applied in clinic and removed at home several hours later, followed by a home-care routine. Expect redness and peeling for several days. Results develop during the following weeks.</p>
<h2>Aftercare</h2>
<p>After microneedling, expect redness similar to mild sunburn for a day or two. Avoid make-up for 24 hours, and exercise, swimming and heat for 48 hours. Wear SPF 50 daily after any of these treatments.</p>
""",
    "faqs": [
      ("How many microneedling sessions are recommended?", "Usually a course of 3 to 6 sessions, about four weeks apart, depending on your skin and goals."),
      ("Is Cosmelan suitable for darker skin?", "Cosmelan is designed for use across skin types. Your skin will be assessed first to make sure it's suitable."),
      ("Can I have dermaplaning before an event?", "Yes. It's a popular pre-event treatment because there's no downtime and make-up sits more smoothly afterwards."),
    ],
    "related": ["skin-boosters-london", "bridal-hair-makeup-london", "anti-wrinkle-injections-london"],
  },
  {
    "slug": "bridal-hair-makeup-london",
    "name": "Bridal hair &amp; makeup",
    "title": "Bridal Hair & Makeup London | From £228 | Glam Beauty Aesthetics",
    "description": "Bridal hair and makeup in London from £228, plus glam makeup from £59 and hair & makeup from £98 for events. Weekend appointments. Book online.",
    "eyebrow": "Bridal &amp; occasions · London",
    "h1": "Bridal hair &amp; makeup", "h1_em": "in London.",
    "summary": "Hair and makeup for your wedding day, events and photoshoots, made to last from the first photo to the last dance.",
    "points": [], "whole_face": True, "area_label": "Hair & makeup",
    "facts": [("1–3 hours", "Appointment time"), ("From £228", "Bridal"), ("From £59", "Glam makeup"), ("7 days", "Including weekends")],
    "services": ["bridal", "hm", "gm"],
    "body": """
<h2>Bridal hair &amp; makeup</h2>
<p>Your bridal look is planned around you: your dress, your style and the feel of the day. The three-hour appointment covers full makeup and hairstyling, so nothing feels rushed on the morning.</p>
<h2>Hair and makeup for events</h2>
<ul>
<li><span><strong>Glam makeup (£59, 1 hour):</strong> full-face makeup for parties, nights out and photoshoots.</span></li>
<li><span><strong>Hair &amp; makeup (£98, 2 hours):</strong> professional styling and makeup together.</span></li>
</ul>
<h2>Getting your skin wedding-ready</h2>
<p>If you'd like your skin at its best on the day, start early. <a href="/skin-boosters-london/">Skin boosters</a>, <a href="/microneedling-london/">microneedling</a> and <a href="/anti-wrinkle-injections-london/">anti-wrinkle injections</a> take time to settle, so book them several weeks to a few months ahead. Dermaplaning a few days before is a good final step.</p>
<h2>Booking your date</h2>
<p>Weekend dates in spring and summer fill up quickly, so it's worth booking as soon as your date is set. We're open on Saturdays and Sundays.</p>
""",
    "faqs": [
      ("When should I book bridal hair and makeup?", "As soon as your wedding date is set, especially for a weekend in spring or summer."),
      ("Are you open at weekends?", "Yes. We're open Saturday and Sunday from 9:30am to 4pm."),
      ("Can I have aesthetic treatments before my wedding?", "Yes, with enough time for results to settle. Plan injectable treatments at least 2 to 4 weeks before the day, and skin courses a few months ahead."),
    ],
    "related": ["skin-boosters-london", "microneedling-london", "lip-filler-london"],
  },
]

BY_SLUG = {t["slug"]: t for t in TREATMENTS}


def read_services():
    """Read every treatment row from the price menu in index.html."""
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<li class="svc" id="([^"]+)">(.*?)</li>', src, re.S):
        sid, row = m.group(1), m.group(2)
        def grab(cls):
            g = re.search(r'class="%s"[^>]*>(.*?)</' % cls, row, re.S)
            return g.group(1).strip() if g else ""
        price_text = grab("svc-price")
        out[sid] = {
            "id": sid, "name": grab("svc-name"), "price_text": price_text,
            "price": re.sub(r"[^0-9.]", "", price_text),
            "desc": grab("svc-desc"), "dur": grab("svc-dur"),
        }
    return out


def book_url(label):
    return f"{BOOK}{'&amp;' if '?' in BOOK else '?'}utm_source=website&amp;utm_medium=book_button&amp;utm_content={label}"


ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5" stroke="currentColor" stroke-width="1.4"/></svg>'


def face_svg(t):
    marks = []
    if t.get("whole_face"):
        marks.append('<ellipse class="hl-area" cx="180" cy="220" rx="112" ry="178"/>')
    for key in t["points"]:
        for x, y in P[key]:
            marks.append(f'<circle class="hl-ring" cx="{x}" cy="{y}" r="16"/><circle class="hl-dot" cx="{x}" cy="{y}" r="4.5"/>')
    return f"""<svg viewBox="0 0 360 460" aria-hidden="true">
  <path class="fm-soft" d="M180 40 C100 38 62 100 66 190 C70 280 62 360 44 436"/>
  <path class="fm-soft" d="M180 40 C260 38 298 100 294 190 C290 280 298 360 316 436"/>
  <ellipse class="fm-blush" cx="128" cy="262" rx="30" ry="18"/><ellipse class="fm-blush" cx="232" cy="262" rx="30" ry="18"/>
  <path class="fm-face" d="M180 58 C120 58 88 105 88 175 C88 215 92 250 104 285 C118 330 145 372 180 382 C215 372 242 330 256 285 C268 250 272 215 272 175 C272 105 240 58 180 58 Z"/>
  <path class="fm-face" d="M116 168 C134 155 158 155 168 164"/><path class="fm-face" d="M244 168 C226 155 202 155 192 164"/>
  <path class="fm-face" d="M122 192 C135 181 155 181 166 193 C155 200 135 200 122 192 Z"/><path class="fm-face" d="M238 192 C225 181 205 181 194 193 C205 200 225 200 238 192 Z"/>
  <circle cx="144" cy="191" r="4.5" fill="#2A1622"/><circle cx="216" cy="191" r="4.5" fill="#2A1622"/>
  <path class="fm-face" d="M178 204 C177 228 171 248 166 260 C172 268 188 268 194 260"/>
  <path class="fm-face" d="M152 305 C162 297 172 296 180 300 C188 296 198 297 208 305 C196 309 164 309 152 305 Z"/><path class="fm-face" d="M152 305 C162 323 198 323 208 305"/>
  <path class="fm-face" d="M150 370 L148 428 C120 444 76 450 30 460"/><path class="fm-face" d="M210 370 L212 428 C240 444 284 450 330 460"/>
  {''.join(marks)}
</svg>"""


def min_price(t, services):
    prices = [float(services[s]["price"]) for s in t["services"] if services[s]["price"]]
    return int(min(prices))


def header(consult_href="#contact"):
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="promo" role="region" aria-label="Offer">
  <div class="wrap promo-in">
    <span class="promo-star" aria-hidden="true">✦</span>
    <p><b class="gold-shine">Free consultation</b><span class="promo-sub">Talk through your goals with our practitioner before you decide</span></p>
    <a class="promo-link" href="{consult_href}" data-consult="top-bar">Request yours <span aria-hidden="true">→</span></a>
  </div>
</div>
<header class="site-header" id="top">
  <span class="progress" aria-hidden="true"></span>
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="Glam Beauty Aesthetics home">
      <span class="brand-glam">Glam</span>
      <span class="brand-sub">Beauty Aesthetics</span>
    </a>
    <nav aria-label="Main">
      <ul class="nav-links" id="nav-links">
        <li><a href="/#face-map">Find a treatment</a></li>
        <li><a href="/#treatments">Prices</a></li>
        <li><a href="/#reviews">Reviews</a></li>
        <li><a href="/#about">About</a></li>
        <li><a href="/#results">Results</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a class="nav-phone" href="tel:{PHONE_INTL}" data-cta="header-call">{PHONE}</a>
      <a class="btn btn-primary js-book" data-cta="header" href="{BOOK}">Book now</a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>"""


def footer():
    links = "\n".join(f'          <li><a href="/{t["slug"]}/">{t["name"]}</a></li>' for t in TREATMENTS)
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/" style="margin-bottom:16px"><span class="brand-glam">Glam</span><span class="brand-sub">Beauty Aesthetics</span></a>
        <p style="margin:0;max-width:32ch">Aesthetics clinic in London for anti-wrinkle, fillers, skin boosters, thread lifts and bridal makeup.</p>
      </div>
      <div>
        <h2>Treatments</h2>
        <ul>
{links}
        </ul>
      </div>
      <div>
        <h2>Clinic</h2>
        <ul>
          <li><a href="/#treatments">Full price list</a></li>
          <li><a href="/#about">About</a></li>
          <li><a href="/#results">Results</a></li>
          <li><a href="/#faq">FAQs</a></li>
          <li><a href="/guides/">Guides</a></li>
          <li><a href="/#contact">Contact us</a></li>
          <li><a class="js-book" data-cta="footer" href="{BOOK}">Book online</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li>{', '.join(ADDRESS_LINES)}</li>
          <li class="footer-areas">Close to <a href="/aesthetics-clinic-stratford/">Stratford</a>, <a href="/aesthetics-clinic-east-ham/">East Ham</a>, <a href="/aesthetics-clinic-plaistow/">Plaistow</a> and <a href="/aesthetics-clinic-beckton/">Beckton</a></li>
          <li><a href="tel:{PHONE_INTL}" data-cta="footer-call">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li class="footer-social"><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram" data-cta="footer-instagram"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a><a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook" data-cta="footer-facebook"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4V10.5H7.8v3h2.6V21h3.1z"/></svg></a><a href="{TIKTOK}" target="_blank" rel="noopener" aria-label="TikTok" data-cta="footer-tiktok"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M16.6 5.82A4.28 4.28 0 0 1 15.54 3h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5c-1.42 0-2.6-1.16-2.6-2.6 0-1.72 1.66-3.01 3.37-2.48V9.66c-3.45-.46-6.47 2.22-6.47 5.64 0 3.33 2.76 5.7 5.69 5.7 3.14 0 5.69-2.55 5.69-5.7V9.01a7.35 7.35 0 0 0 4.3 1.38V7.3s-1.88.09-3.24-1.48z"/></svg></a></li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <span>© <span id="year">{date.today().year}</span> Glam Beauty Aesthetics. All rights reserved. <a href="/privacy-policy/">Privacy policy</a></span>
      <span>Results vary from person to person. Injectable treatments are for clients aged 18 or older.</span>
    </div>
    <p class="footer-mark" aria-hidden="true" data-word="Glam"></p>
  </div>
</footer>

<div class="mbar" id="mbar" aria-label="Quick booking">
  <a class="btn btn-primary js-book" data-cta="mobile-bar" href="{BOOK}">Book now</a>
  <a class="btn btn-ghost" href="{WHATSAPP}" target="_blank" rel="noopener" data-cta="mobile-whatsapp">WhatsApp</a>
  <a class="btn btn-ghost" href="tel:{PHONE_INTL}" data-cta="mobile-call" aria-label="Call the clinic">Call</a>
</div>"""


# ---------------------------------------------------------------- Contact form
# Where enquiries are sent: the Google Sheets "Web app URL" (ends in /exec, see _build/google-sheets-form.gs).
# A Formspree form URL also works.
# and in index.html (the form's action attribute). While it's empty, the form opens the
# visitor's email app with their message ready to send.
CONTACT_ENDPOINT = "https://script.google.com/macros/s/AKfycbwIjtgiQsnvn0LkyGlpMt7sK_cE1ZwWVC9FIpgAC4C3sEN_JkNySS9qnvRZRg2UnWRsVA/exec"

TREATMENT_OPTIONS = [
    ("Face", ["Anti-wrinkle injections", "Lip filler", "Dermal fillers (cheeks, jaw, chin, nose)", "Tear trough filler", "PDO thread lift"]),
    ("Skin", ["Skin boosters & polynucleotides", "Microneedling & peels", "Korean glass facial", "Hair growth therapy"]),
    ("Body & wellness", ["Fat dissolving", "Leg vein treatment", "Vitamin injections"]),
    ("Occasions", ["Bridal hair & makeup", "Glam makeup"]),
]
CONTACT_SELECT = {
    "lip-filler-london": "Lip filler",
    "anti-wrinkle-injections-london": "Anti-wrinkle injections",
    "dermal-fillers-london": "Dermal fillers (cheeks, jaw, chin, nose)",
    "tear-trough-filler-london": "Tear trough filler",
    "skin-boosters-london": "Skin boosters & polynucleotides",
    "pdo-thread-lift-london": "PDO thread lift",
    "fat-dissolving-london": "Fat dissolving",
    "microneedling-london": "Microneedling & peels",
    "bridal-hair-makeup-london": "Bridal hair & makeup",
}


def contact_section(source="home", selected=None):
    opts = ['<option value="Free consultation">Free consultation</option>', '<option value="Not sure yet">Not sure yet, I\'d like advice</option>']
    for group, items in TREATMENT_OPTIONS:
        inner = "".join(
            f'<option value="{html.escape(v)}"{" selected" if v == selected else ""}>{html.escape(v)}</option>' for v in items)
        opts.append(f'<optgroup label="{html.escape(group)}">{inner}</optgroup>')
    options = "\n            ".join(opts)
    page_label = html.escape(selected or "Home page")
    return f"""<section class="section contact" id="contact" aria-labelledby="contact-title">
  <div class="wrap contact-grid">
    <div class="contact-intro reveal">
      <span class="eyebrow">Contact us</span>
      <h2 class="h2" id="contact-title">Ask us <em>anything.</em></h2>
      <p class="lede">Request your <strong class="hl-gold">free consultation</strong> here, or ask anything before you book. Send a message and we'll get back to you the way you prefer.</p>
      <ul class="contact-alt">
        <li><span>Call</span><a href="tel:{PHONE_INTL}" data-cta="{source}-contact-call">{PHONE}</a></li>
        <li><span>WhatsApp</span><a href="{WHATSAPP}" target="_blank" rel="noopener" data-cta="{source}-contact-whatsapp">Message us</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul>
      <p class="contact-book">Already know what you'd like? <a class="js-book" data-cta="{source}-contact-book" href="{BOOK}">Book online now →</a></p>
    </div>
    <div class="form-card reveal">
      <form class="enquiry" id="enquiry-form" action="{CONTACT_ENDPOINT}" method="POST" novalidate
            data-email="{EMAIL}" data-whatsapp="{PHONE_INTL.lstrip('+')}" data-source="{source}">
        <input type="hidden" name="_subject" value="Website enquiry">
        <input type="hidden" name="page" value="{page_label}">
        <div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
        <div class="f-row two">
          <div class="field">
            <label for="f-name">Full name</label>
            <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-err">
            <p class="f-err" id="f-name-err"></p>
          </div>
          <div class="field">
            <label for="f-phone">Phone</label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="f-phone-err">
            <p class="f-err" id="f-phone-err"></p>
          </div>
        </div>
        <div class="field">
          <label for="f-email">Email</label>
          <input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="f-email-err">
          <p class="f-err" id="f-email-err"></p>
        </div>
        <div class="field">
          <label for="f-treatment">Treatment you're interested in</label>
          <select id="f-treatment" name="treatment">
            {options}
          </select>
        </div>
        <fieldset class="field">
          <legend>How should we contact you?</legend>
          <div class="f-chips">
            <label class="f-chip"><input type="radio" name="contact_method" value="phone call" checked><span>Phone call</span></label>
            <label class="f-chip"><input type="radio" name="contact_method" value="WhatsApp"><span>WhatsApp</span></label>
            <label class="f-chip"><input type="radio" name="contact_method" value="email"><span>Email</span></label>
          </div>
        </fieldset>
        <div class="field">
          <label for="f-msg">Your message <span class="opt">(optional)</span></label>
          <textarea id="f-msg" name="message" rows="4" placeholder="Tell us what you'd like to change, or ask a question." aria-describedby="f-msg-hint"></textarea>
          <p class="f-hint" id="f-msg-hint">Please don't include detailed medical information. We'll go through that with you in person.</p>
        </div>
        <label class="f-check"><input type="checkbox" id="f-consent" name="consent" value="yes" required aria-describedby="f-consent-err"><span>I'm happy for Glam Beauty Aesthetics to contact me about this enquiry. My details won't be used for anything else. See our <a href="/privacy-policy/">privacy policy</a>.</span></label>
        <p class="f-err" id="f-consent-err"></p>
        <div class="f-actions">
          <button type="submit" class="btn btn-primary f-send">Send enquiry {ARROW}</button>
          <button type="button" class="btn btn-ghost f-wa">Use WhatsApp instead</button>
        </div>
        <p class="f-status" role="status" aria-live="polite"></p>
      </form>
      <div class="f-done" hidden tabindex="-1">
        <span class="eyebrow">Enquiry sent</span>
        <h3>Thank you<span class="f-done-name"></span>.</h3>
        <p class="f-done-text">We've received your message and will be in touch by <span class="f-done-method">phone</span>.</p>
        <p>If you already know what you'd like, you can choose a time and book online now.</p>
        <a class="btn btn-primary js-book" data-cta="{source}-contact-success" href="{BOOK}">Book online {ARROW}</a>
      </div>
    </div>
  </div>
</section>"""


def visit_section():
    return f"""<section class="section visit" id="visit" aria-labelledby="visit-title">
  <div class="wrap visit-grid">
    <div class="reveal">
      <span class="eyebrow">Visit</span>
      <h2 class="h2" id="visit-title">Open <em>seven days.</em></h2>
      <p class="status js-status" style="margin:0 0 18px"><span class="status-dot"></span><span class="js-status-text">Open 7 days</span></p>
      <table class="hours" id="hours" aria-label="Opening hours">
        <tbody>
          <tr data-day="1" data-open="10:00" data-close="17:30"><th scope="row">Monday</th><td>10:00am – 5:30pm</td></tr>
          <tr data-day="2" data-open="09:30" data-close="17:30"><th scope="row">Tuesday</th><td>9:30am – 5:30pm</td></tr>
          <tr data-day="3" data-open="10:00" data-close="17:30"><th scope="row">Wednesday</th><td>10:00am – 5:30pm</td></tr>
          <tr data-day="4" data-open="10:00" data-close="17:30"><th scope="row">Thursday</th><td>10:00am – 5:30pm</td></tr>
          <tr data-day="5" data-open="10:00" data-close="17:30"><th scope="row">Friday</th><td>10:00am – 5:30pm</td></tr>
          <tr data-day="6" data-open="09:30" data-close="16:00"><th scope="row">Saturday</th><td>9:30am – 4:00pm</td></tr>
          <tr data-day="0" data-open="09:30" data-close="16:00"><th scope="row">Sunday</th><td>9:30am – 4:00pm</td></tr>
        </tbody>
      </table>
    </div>
    <div class="reveal">
      <address style="font-style:normal">
        <ul class="contact-list" style="margin-top:8px">
          <li><span>Address</span><a href="{MAPS}" target="_blank" rel="noopener" data-cta="directions">{ADDRESS_LINES[0]},<br>{ADDRESS_LINES[1]}</a></li>
          <li><span>Phone</span><a href="tel:{PHONE_INTL}" data-cta="visit-call">{PHONE}</a></li>
          <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span>WhatsApp</span><a href="{WHATSAPP}" target="_blank" rel="noopener" data-cta="visit-whatsapp">Message us on WhatsApp</a></li>
          <li><span>Instagram</span><a href="{INSTAGRAM}" target="_blank" rel="noopener">@glam_beauty__aesthetics</a></li>
          <li><span>Facebook</span><a href="{FACEBOOK}" target="_blank" rel="noopener">Glam Beauty Aesthetics</a></li>
          <li><span>TikTok</span><a href="{TIKTOK}" target="_blank" rel="noopener">@glam_beauty__aesthetics</a></li>
        </ul>
      </address>
      <a class="btn btn-primary js-book" data-cta="visit" href="{BOOK}">Book your visit {ARROW}</a>
    </div>
  </div>
</section>"""


def review_card(key):
    r = REVIEWS["reviews"][key]
    tag = html.escape(r["tag"])
    tag_html = f'<a class="rv-tag" href="{r["link"]}">{tag}</a>' if r["link"] else f'<span class="rv-tag">{tag}</span>'
    return f"""      <figure class="rv-card">
        <span class="rv-src">Google review</span>
        <blockquote><p>\u201c{html.escape(r["text"])}\u201d</p></blockquote>
        <figcaption class="rv-meta"><b>{html.escape(r["name"])}</b>{tag_html}</figcaption>
      </figure>"""


def reviews_section(t):
    keys = REVIEWS["pages"].get(t["slug"], [])
    if not keys:
        return ""
    cards = "\n".join(review_card(k) for k in keys)
    return f"""<section class="section t-reviews" id="reviews" aria-labelledby="reviews-title" style="padding-top:0">
  <div class="wrap">
    <div class="rv-head reveal">
      <div>
        <span class="eyebrow">Client reviews</span>
        <h2 class="h2" id="reviews-title" style="margin:0">Kind <em>words.</em></h2>
      </div>
      <a class="rating-lg" href="{REVIEWS['google_url']}" target="_blank" rel="noopener"><span class="rv-big">{REVIEWS['rating']}</span><span>{STARS}<br>From {REVIEWS['count']} Google reviews</span></a>
    </div>
    <div class="rv-wall reveal">
{cards}
    </div>
  </div>
</section>"""


def schema(t, services, url):
    plain = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s))
    business = {
        "@type": ["BeautySalon", "MedicalClinic"], "@id": f"{SITE}/#business",
        "name": "Glam Beauty Aesthetics", "url": f"{SITE}/", "telephone": PHONE_INTL,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "London",
                    "postalCode": POSTCODE, "addressCountry": "GB"},
    }
    graph = [
        {
            "@type": "Service", "@id": f"{url}#service", "name": plain(t["name"]),
            "serviceType": plain(t["name"]), "description": t["description"], "url": url,
            "provider": business, "areaServed": {"@type": "City", "name": "London"},
            "offers": [{
                "@type": "Offer", "name": plain(services[s]["name"]), "price": services[s]["price"],
                "priceCurrency": "GBP", "url": f"{url}#prices",
            } for s in t["services"]],
        },
        {
            "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Treatments", "item": f"{SITE}/#treatments"},
                {"@type": "ListItem", "position": 3, "name": plain(t["name"]), "item": url},
            ],
        },
        {
            "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in t["faqs"]
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def page(t, services):
    url = f"{SITE}/{t['slug']}/"
    slug = t["slug"]
    from_price = min_price(t, services)
    name_plain = html.unescape(t["name"])

    facts = "\n".join(f"      <li><b>{v}</b><span>{l}</span></li>" for v, l in t["facts"])

    rows = []
    for sid in t["services"]:
        s = services[sid]
        rows.append(f"""          <li class="fm-item">
            <div class="fm-item-name">{s['name']}<span class="fm-item-dur">{s['dur']}</span></div>
            <span class="fm-item-price">{s['price_text']}</span>
            <a class="btn btn-primary js-book" data-cta="{slug}-{sid}" href="{BOOK}" aria-label="Book {s['name']}">Book</a>
          </li>""")

    faqs = "\n".join(f"""      <details{' open' if i == 0 else ''}>
        <summary>{q}</summary>
        <div class="answer"><p>{a}</p></div>
      </details>""" for i, (q, a) in enumerate(t["faqs"]))

    related = []
    for r in t["related"]:
        rt = BY_SLUG[r]
        related.append(f"""      <a class="related-card" href="/{r}/"><b>{rt['name']}</b><span>{rt['summary']}</span><i>From £{min_price(rt, services)} →</i></a>""")

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['description']}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#53634C">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="Glam Beauty Aesthetics">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['description']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/site/hero-portrait.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..700&family=Instrument+Sans:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<script type="application/ld+json">
{schema(t, services, url)}
</script>
{VERCEL_ANALYTICS}</head>
<body>
{header()}

<main id="main">
<nav class="wrap crumbs" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/#treatments">Treatments</a></li>
    <li aria-current="page">{t['name']}</li>
  </ol>
</nav>

<section class="hero t-hero" aria-labelledby="page-title" data-3d data-tilt>
  <div class="orbs" aria-hidden="true">
    <i style="--d:.2;--s:120px;left:44%;top:6%"></i>
    <i style="--d:.4;--s:64px;left:-2%;top:82%" class="hide-sm"></i>
  </div>
  <div class="orbs front" aria-hidden="true">
    <i style="--d:.9;--s:30px;left:92%;top:72%"></i>
    <i style="--d:1;--s:16px;left:50%;top:60%" class="hide-sm"></i>
  </div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="eyebrow rise">{t['eyebrow']}</span>
      <h1 id="page-title" class="hero-display"><span class="line"><span>{t['h1']}</span></span> <em class="line"><span>{t['h1_em']}</span></em></h1>
      <p class="hero-sub rise">{t['summary']}</p>
      <div class="hero-ctas rise">
        <a class="btn btn-primary js-book" data-cta="{slug}-hero" data-magnetic href="{BOOK}">Book {html.escape(name_plain if name_plain.startswith('PDO') else name_plain.lower())} {ARROW}</a>
        <a class="btn btn-consult" href="#contact" data-consult="{slug}-hero"><span class="star" aria-hidden="true">✦</span> Free consultation</a>
      </div>
      <div class="hero-meta rise">
        <span class="status js-status"><span class="status-dot"></span><span class="js-status-text">Open 7 days</span></span>
        <a class="rating-chip" href="#reviews">{STARS}<b>{REVIEWS['rating']}</b> from {REVIEWS['count']} Google reviews</a>
        <span class="cred-chip"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8.4-7 10-4-1.6-7-5.5-7-10V6z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M9 12l2.2 2.2L15.5 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>Level 4 qualified</span>
        <span class="cred-chip"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.8l-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>20+ years' experience</span>
        <span class="cred-chip"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.5 3.5h5v6h6v5h-6v6h-5v-6h-6v-5h6z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>Works with a qualified nurse</span>
      </div>
    </div>
    <figure class="t-face rise">
      <div class="t-face-frame">{face_svg(t)}</div>
      <figcaption><b>Treatment area</b><span>{t['area_label']}</span></figcaption>
    </figure>
  </div>
</section>

<div class="proof" aria-label="At a glance">
  <div class="wrap">
    <ul>
{facts}
    </ul>
  </div>
</div>

<section class="section" aria-label="About this treatment">
  <div class="wrap t-grid">
    <article class="prose reveal">
{t['body'].strip()}
      <p style="margin-top:28px"><a class="btn btn-primary js-book" data-cta="{slug}-body" href="{BOOK}" style="color:#fff">Book an appointment {ARROW}</a></p>
    </article>
    <aside class="t-card" id="prices" aria-labelledby="prices-title">
      <h2 id="prices-title">Prices</h2>
      <p>Book online in a minute, any time. Not sure which? <a href="#contact" data-consult="{slug}-card">Start with a free consultation →</a></p>
      <ul class="fm-list">
{chr(10).join(rows)}
      </ul>
      <p class="t-card-foot">Questions first? Call <a href="tel:{PHONE_INTL}" data-cta="{slug}-card-call">{PHONE}</a>.</p>
    </aside>
  </div>
</section>

{reviews_section(t)}

<section class="section" id="faq" aria-labelledby="faq-title" style="padding-top:0">
  <div class="wrap faq-grid">
    <div class="reveal">
      <span class="eyebrow">Questions</span>
      <h2 class="h2" id="faq-title">{t['name']}, <em>answered.</em></h2>
      <p class="lede" style="margin-bottom:28px">Anything else, call <a href="tel:{PHONE_INTL}" data-cta="{slug}-faq-call">{PHONE}</a>.{extra_pages.guides_links_html(slug)}</p>
      <a class="btn btn-primary js-book" data-cta="{slug}-faq" href="{BOOK}">Book now</a>
    </div>
    <div class="faq reveal">
{faqs}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="related-title" style="padding-top:0">
  <div class="wrap">
    <span class="eyebrow">Often combined with</span>
    <h2 class="h2" id="related-title" style="margin-bottom:28px">Related <em>treatments.</em></h2>
    <div class="related-grid reveal">
{chr(10).join(related)}
    </div>
  </div>
</section>

{contact_section(slug, CONTACT_SELECT.get(slug))}

{visit_section()}

<section class="section final" aria-labelledby="final-title" data-3d data-tilt>
  <div class="orbs" aria-hidden="true">
    <i style="--d:.25;--s:110px;left:6%;top:14%"></i>
    <i style="--d:.6;--s:42px;left:84%;top:22%"></i>
    <i style="--d:.9;--s:20px;left:72%;top:74%" class="hide-sm"></i>
  </div>
  <div class="wrap reveal">
    <h2 class="h2" id="final-title">Ready when <em>you are.</em></h2>
    <p>Choose a time that suits you and you're booked. Open seven days a week.</p>
    <div class="ctas">
      <a class="btn btn-light js-book" data-cta="{slug}-final" data-magnetic href="{BOOK}">Book now</a>
      <a class="btn btn-ghost" href="{WHATSAPP}" target="_blank" rel="noopener" data-cta="{slug}-final-whatsapp">WhatsApp us</a>
    </div>
    <ul class="assure">
      <li>Free consultation</li>
      <li>Level 4 qualified professional</li>
      <li>20+ years' experience</li>
      <li>Working with a qualified nurse</li>
      <li>Secure online booking</li>
      <li>Weekend appointments</li>
      <li>Rated {REVIEWS['rating']} on Google</li>
    </ul>
  </div>
</section>
</main>

{footer()}

<script src="/assets/site.js?v={ASSET_V}" defer></script>
<script src="/assets/depth.js?v={ASSET_V}" defer></script>
<script src="/assets/chat.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- Privacy policy
PRIVACY_UPDATED = "9 November 2026"

PRIVACY_SECTIONS = [
  ("who-we-are", "Who we are", f"""
<p>Glam Beauty Aesthetics ("we", "us") is an aesthetics clinic at {ADDRESS_LINES[0]}, {ADDRESS_LINES[1]}. We decide how and why your personal information is used, which makes us the "controller" of that information under UK data protection law.</p>
<p>If you have any questions about this policy or your information, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_INTL}">{PHONE}</a>.</p>
"""),
  ("what-we-collect", "What we collect", """
<ul>
<li><span><strong>When you send an enquiry through our website:</strong> your name, phone number, email address, the treatment you're interested in, how you'd like us to contact you, and your message.</span></li>
<li><span><strong>When you call, WhatsApp, email or message us on Instagram, Facebook or TikTok:</strong> the details you share with us and our conversation.</span></li>
<li><span><strong>When you book online:</strong> bookings are made through Faces (facesconsent.com), our booking provider. Faces collects your booking details and shares them with us so we can manage your appointment.</span></li>
<li><span><strong>When you come for treatment:</strong> your contact details, date of birth, medical history, consultation notes, consent forms and treatment records. With your permission, we also take photographs of the treated area.</span></li>
<li><span><strong>When you visit our website:</strong> our website itself doesn't use cookies or tracking tools. Some features load content from other companies; see <a href="#other-companies">Other companies on our website</a>.</span></li>
</ul>
"""),
  ("health-information", "Your health information", """
<p>Information about your health is "special category" data, which the law protects more strongly. We only collect the health information required to treat you safely, we use it only for your care, and we keep it confidential.</p>
<p>We ask for your explicit consent to collect and use your health information when you complete your consultation form. Please don't send detailed medical information through our website form; we'll go through it with you in person.</p>
"""),
  ("how-we-use-it", "How we use it, and why we're allowed to", """
<div class="p-table" role="table" aria-label="How we use your information">
  <div class="p-row p-head" role="row"><span role="columnheader">What we use it for</span><span role="columnheader">Our legal reason</span></div>
  <div class="p-row" role="row"><span role="cell">Replying to your enquiry</span><span role="cell">Our legitimate interest in answering your question, and taking steps you've asked for before you book</span></div>
  <div class="p-row" role="row"><span role="cell">Booking and managing your appointments, including reminders</span><span role="cell">To carry out our agreement with you</span></div>
  <div class="p-row" role="row"><span role="cell">Carrying out your treatment safely and keeping treatment records</span><span role="cell">To carry out our agreement with you, and your explicit consent for health information</span></div>
  <div class="p-row" role="row"><span role="cell">Before and after photos for your treatment record</span><span role="cell">Your consent</span></div>
  <div class="p-row" role="row"><span role="cell">Using your photos or review on our website or social media</span><span role="cell">Only with your separate, written consent, which you can withdraw at any time</span></div>
  <div class="p-row" role="row"><span role="cell">Handling complaints, insurance claims and legal requirements</span><span role="cell">Legal obligations, and our legitimate interest in protecting our business</span></div>
</div>
<p>We don't send marketing messages unless you've asked to receive them, and you can ask us to stop at any time.</p>
"""),
  ("sharing", "Who we share it with", """
<p>We don't sell your information. We only share it with:</p>
<ul>
<li><span><strong>Faces</strong>, which runs our online booking.</span></li>
<li><span><strong>Google</strong>, which provides our email and stores enquiries from our website form in a private Google Sheet.</span></li>
<li><span><strong>WhatsApp (Meta)</strong>, if you choose to message us there.</span></li>
<li><span><strong>Our insurers and professional advisers</strong>, if we have to deal with a claim or complaint.</span></li>
<li><span><strong>Emergency services or your GP</strong>, in an emergency, or with your permission.</span></li>
</ul>
<p>These companies may only use your information as the law allows and, where they act for us, only to provide their service to us.</p>
"""),
  ("other-companies", "Other companies on our website", """
<ul>
<li><span><strong>Google Fonts:</strong> our fonts load from Google's servers, which receive your device's IP address to deliver them.</span></li>
<li><span><strong>Google Maps:</strong> the map on our home page is provided by Google, which may set cookies when the map loads.</span></li>
<li><span><strong>Links to Faces, WhatsApp, Instagram, Facebook and TikTok:</strong> when you follow these links, those companies' own privacy policies apply.</span></li>
</ul>
"""),
  ("transfers", "Information stored outside the UK", """
<p>Some of the companies above, such as Google and Meta, may store or process information outside the UK, including in the United States. When they do, they use safeguards recognised under UK law, such as the UK International Data Transfer Addendum or the UK Extension to the EU–US Data Privacy Framework.</p>
"""),
  ("how-long", "How long we keep it", """
<ul>
<li><span><strong>Enquiries that don't lead to a booking:</strong> up to 12 months.</span></li>
<li><span><strong>Client and treatment records, including consultation forms and photos:</strong> 8 years after your last treatment, in line with guidance for clinical records and our insurance requirements.</span></li>
<li><span><strong>Messages and emails:</strong> as long as they help us look after you, then deleted.</span></li>
</ul>
"""),
  ("security", "Keeping it safe", """
<p>We keep paper records locked away and digital records protected by passwords and two-step sign-in where available. Only the people looking after you can see it.</p>
"""),
  ("your-rights", "Your rights", f"""
<p>You have the right to:</p>
<ul>
<li><span>ask for a copy of the information we hold about you;</span></li>
<li><span>ask us to correct anything that's wrong or incomplete;</span></li>
<li><span>ask us to delete your information, unless we have to keep it by law;</span></li>
<li><span>ask us to limit how we use it, or object to how we use it;</span></li>
<li><span>ask us to send your information to you or another provider;</span></li>
<li><span>withdraw your consent at any time, where we rely on it.</span></li>
</ul>
<p>To use any of these rights, email <a href="mailto:{EMAIL}">{EMAIL}</a>. It's free, and we'll reply within one month.</p>
"""),
  ("complaints", "Complaints", """
<p>If you're unhappy with how we've handled your information, please tell us first so we can put it right. You can also complain to the Information Commissioner's Office (ICO), the UK's data protection regulator, at <a href="https://ico.org.uk/make-a-complaint/" target="_blank" rel="noopener">ico.org.uk</a> or on 0303 123 1113.</p>
"""),
  ("changes", "Changes to this policy", f"""
<p>We'll update this page if anything changes. This version was last updated on {PRIVACY_UPDATED}.</p>
"""),
]


def privacy_page():
    url = f"{SITE}/privacy-policy/"
    title = "Privacy Policy | Glam Beauty Aesthetics"
    desc = "How Glam Beauty Aesthetics collects, uses and protects your personal information, and your rights under UK data protection law."
    toc = "\n".join(f'          <li><a href="#{sid}">{t}</a></li>' for sid, t, _ in PRIVACY_SECTIONS)
    body = "\n".join(f'<section class="p-sec" id="{sid}" aria-labelledby="{sid}-h">\n<h2 id="{sid}-h">{t}</h2>{content}</section>'
                     for sid, t, content in PRIVACY_SECTIONS)
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
         "dateModified": date.today().isoformat(), "isPartOf": {"@id": f"{SITE}/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Privacy policy", "item": url}]},
    ]}, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#53634C">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..700&family=Instrument+Sans:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<script type="application/ld+json">
{ld}
</script>
{VERCEL_ANALYTICS}</head>
<body>
{header("/?consult=1#contact")}

<main id="main">
<nav class="wrap crumbs" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li aria-current="page">Privacy policy</li>
  </ol>
</nav>

<section class="hero t-hero p-hero" aria-labelledby="page-title">
  <div class="wrap">
    <span class="eyebrow rise">Your information</span>
    <h1 id="page-title" class="hero-display"><span class="line"><span>Privacy</span></span> <em class="line"><span>policy.</span></em></h1>
    <p class="hero-sub rise">What we collect, why we use it, and how you stay in control of it. Last updated {PRIVACY_UPDATED}.</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="Privacy policy">
  <div class="wrap p-grid">
    <aside class="p-toc" aria-labelledby="toc-title">
      <h2 id="toc-title">On this page</h2>
      <ol>
{toc}
      </ol>
      <p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </aside>
    <article class="prose p-body">
{body}
    </article>
  </div>
</section>
</main>

{footer()}

<script src="/assets/site.js?v={ASSET_V}" defer></script>
<script src="/assets/depth.js?v={ASSET_V}" defer></script>
<script src="/assets/chat.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def sitemap():
    today = date.today().isoformat()
    urls = [f"{SITE}/"] + [f"{SITE}/{t['slug']}/" for t in TREATMENTS] + extra_pages.all_urls(sys.modules[__name__]) + [f"{SITE}/privacy-policy/"]
    body = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def main():
    services = read_services()
    missing = [s for t in TREATMENTS for s in t["services"] if s not in services]
    if missing:
        raise SystemExit(f"These treatment IDs aren't in the index.html menu: {missing}")
    for t in TREATMENTS:
        out = ROOT / t["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(t, services), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
    out = ROOT / "privacy-policy" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(privacy_page(), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))
    extra_pages.write_all(sys.modules[__name__], services)
    import chat_kb
    kb = chat_kb.build_kb(sys.modules[__name__], services, (ROOT / "index.html").read_text(encoding="utf-8"))
    (ROOT / "assets" / "chat-kb.json").write_text(json.dumps(kb, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("wrote assets/chat-kb.json with", len(kb["entries"]), "answers")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("wrote sitemap.xml with", sitemap().count("<loc>"), "pages")


if __name__ == "__main__":
    main()
