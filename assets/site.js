(function(){
  "use strict";
  var BOOK_URL = "https://marketplace.getglossa.com/studios/glam-beauty-aesthetics";
  var SITE = "https://glambeautyaesthetics.co.uk/";
  var $ = function(s, r){ return (r||document).querySelector(s); };
  var $$ = function(s, r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); };

  /* ---------- Click tracking (GA4 / Tag Manager ready) ----------
     Every booking button sends a "book_click" event with where it was clicked.
     Calls send "call_click". Add your GA4 or GTM snippet in <head> to collect them. */
  window.dataLayer = window.dataLayer || [];
  function track(name, label){
    var data = { event: name, cta_location: label };
    window.dataLayer.push(data);
    if (typeof window.gtag === "function") window.gtag("event", name, { cta_location: label });
  }
  $$(".js-book").forEach(function(a){
    var label = a.getAttribute("data-cta") || "unknown";
    a.href = BOOK_URL + "?utm_source=website&utm_medium=book_button&utm_content=" + encodeURIComponent(label);
  });
  document.addEventListener("click", function(e){
    var a = e.target.closest("a");
    if (!a) return;
    if (a.classList.contains("js-book")) track("book_click", a.getAttribute("data-cta") || "unknown");
    else if (a.href.indexOf("tel:") === 0) track("call_click", a.getAttribute("data-cta") || "unknown");
    else if (a.href.indexOf("wa.me") !== -1) track("whatsapp_click", a.getAttribute("data-cta") || "unknown");
  });

  /* ---------- Header + mobile menu + mobile booking bar ---------- */
  var header = $(".site-header"), mbar = $("#mbar"), hero = $(".hero");
  function onScroll(){
    var y = window.scrollY;
    header.classList.toggle("scrolled", y > 8);
    mbar.classList.toggle("show", y > hero.offsetHeight * 0.6);
    var max = document.documentElement.scrollHeight - window.innerHeight;
    header.style.setProperty("--prog", max > 0 ? Math.min(1, y / max).toFixed(4) : 0);
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  var toggle = $(".menu-toggle"), links = $("#nav-links");
  toggle.addEventListener("click", function(){
    var open = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", open);
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    links.classList.toggle("open", open);
  });
  $$("#nav-links a").forEach(function(a){ a.addEventListener("click", function(){
    toggle.setAttribute("aria-expanded", "false"); links.classList.remove("open");
  }); });

  /* ---------- Live opening status (London time) ---------- */
  var rows = $$("#hours tr");
  var hours = {};
  rows.forEach(function(r){ hours[r.dataset.day] = { open: r.dataset.open, close: r.dataset.close, row: r }; });
  function toMin(t){ var p = t.split(":"); return (+p[0]) * 60 + (+p[1]); }
  function fmt(t){
    var p = t.split(":"), h = +p[0], m = p[1];
    var s = (h % 12 || 12) + (m !== "00" ? ":" + m : "");
    return s + (h < 12 ? "am" : "pm");
  }
  function londonNow(){
    var parts = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/London", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
    var o = {}; parts.forEach(function(p){ o[p.type] = p.value; });
    var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return { day: days[o.weekday], min: (+o.hour % 24) * 60 + (+o.minute) };
  }
  function updateStatus(){
    var now = londonNow(), today = hours[now.day], text, open = false;
    rows.forEach(function(r){ r.classList.remove("today"); });
    if (today) today.row.classList.add("today");
    if (today && now.min >= toMin(today.open) && now.min < toMin(today.close)) {
      open = true; text = "Open now, until " + fmt(today.close);
    } else if (today && now.min < toMin(today.open)) {
      text = "Opens today at " + fmt(today.open);
    } else {
      var next = hours[(now.day + 1) % 7];
      text = "Opens tomorrow at " + fmt(next.open) + " · book online now";
    }
    $$(".js-status").forEach(function(el){
      el.classList.toggle("is-open", open);
      $(".js-status-text", el).textContent = text;
    });
  }
  if (rows.length) { updateStatus(); setInterval(updateStatus, 60000); }

  /* ---------- Face map ----------
     Each area lists treatment IDs from the price menu, so names and prices
     always come from one place: the menu. */
  var ZONES = {
    forehead:  { title: "Forehead & frown lines", line: "Smooth horizontal forehead lines and the ‘11s’ between the brows.", ids: ["aw1","aw2","aw3","adv"], page: "anti-wrinkle-injections-london", more: "anti-wrinkle injections" },
    eyes:      { title: "Eyes", line: "Soften under-eye hollows, dark circles and crow’s feet.", ids: ["tt","ue","aw3","adv"], page: "tear-trough-filler-london", more: "under-eye treatments" },
    nose:      { title: "Nose", line: "Smooth a bump or refine the shape without surgery.", ids: ["fl1","mas"], page: "dermal-fillers-london", more: "non-surgical nose reshaping" },
    cheeks:    { title: "Cheeks", line: "Restore lift and contour to the mid-face.", ids: ["fl1","pdo1","pdo2","pn"], page: "dermal-fillers-london", more: "cheek and dermal fillers" },
    lips:      { title: "Lips", line: "Add shape, volume or hydration, as subtle as you like.", ids: ["lip05","fl1","lipb","adv","hy"], page: "lip-filler-london", more: "lip filler" },
    jaw:       { title: "Jawline", line: "Sharpen the jawline or slim a square jaw.", ids: ["fl1","mas","adv","pdo1"], page: "dermal-fillers-london", more: "jawline filler" },
    chin:      { title: "Chin", line: "Balance your profile or reduce fullness under the chin.", ids: ["chin","fd1"], page: "dermal-fillers-london", more: "chin filler" },
    neck:      { title: "Neck", line: "Soften horizontal lines and firm the neck.", ids: ["neck","pdo2"], page: "pdo-thread-lift-london", more: "neck treatments" },
    skin:      { title: "Skin", line: "Brighter, smoother, more even skin.", ids: ["kgf","rad","pn","exo","exotox","mv","nad","derm","cos"], page: "skin-boosters-london", more: "skin boosters" },
    scalp:     { title: "Hair loss", line: "Encourage thicker, healthier hair growth.", ids: ["hg"], page: "microneedling-london", more: "hair growth therapy" },
    shoulders: { title: "Shoulders", line: "Slim the shoulder line and ease tension.", ids: ["trap"], page: "anti-wrinkle-injections-london", more: "Traptox" },
    underarms: { title: "Excessive sweating", line: "Significantly reduce underarm sweating.", ids: ["hyp"], page: "anti-wrinkle-injections-london", more: "sweating treatment" },
    body:      { title: "Body fat", line: "Target stubborn fat on the arms, waist, thighs or tummy.", ids: ["fd2","fd3","fd1"], page: "fat-dissolving-london", more: "fat dissolving" },
    legs:      { title: "Leg veins", line: "Reduce the look of spider veins.", ids: ["scl"] },
    wellness:  { title: "Wellness", line: "Quick vitamin and antioxidant injections.", ids: ["b12","glu"] },
    occasions: { title: "Hair & makeup", line: "Hair and makeup for events and your wedding day.", ids: ["gm","hm","bridal"], page: "bridal-hair-makeup-london", more: "bridal hair & makeup" }
  };
  var panel = $("#fm-panel"), list = $("#fm-list"), pTitle = $("#fm-panel-title"), pLine = $("#fm-panel-line");
  var triggers = $$("[data-zone]");
  var mq = window.matchMedia("(max-width: 860px)");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function svcData(id){
    var li = document.getElementById(id);
    if (!li) return null;
    return {
      id: id,
      name: $(".svc-name", li).textContent,
      price: $(".svc-price", li).textContent,
      dur: $(".svc-dur", li).textContent
    };
  }
  function renderZone(key, fromUser){
    var z = ZONES[key]; if (!z) return;
    triggers.forEach(function(t){ t.setAttribute("aria-pressed", t.dataset.zone === key ? "true" : "false"); });
    function fill(){
      pTitle.textContent = z.title;
      pLine.textContent = z.line;
      list.innerHTML = "";
      z.ids.forEach(function(id){
        var s = svcData(id); if (!s) return;
        var li = document.createElement("li"); li.className = "fm-item";
        var name = document.createElement("div"); name.className = "fm-item-name"; name.textContent = s.name;
        var dur = document.createElement("span"); dur.className = "fm-item-dur"; dur.textContent = s.dur; name.appendChild(dur);
        var price = document.createElement("span"); price.className = "fm-item-price"; price.textContent = s.price;
        var a = document.createElement("a"); a.className = "btn btn-primary js-book"; a.textContent = "Book";
        a.setAttribute("data-cta", "facemap-" + key + "-" + id);
        a.href = BOOK_URL + "?utm_source=website&utm_medium=book_button&utm_content=" + encodeURIComponent("facemap-" + key + "-" + id);
        a.setAttribute("aria-label", "Book " + s.name);
        li.appendChild(name); li.appendChild(price); li.appendChild(a);
        list.appendChild(li);
      });
      var more = $("#fm-more");
      if (more) {
        more.hidden = !z.page;
        if (z.page) { more.href = "/" + z.page + "/"; more.textContent = "More about " + z.more + " →"; }
      }
      panel.classList.remove("swap");
    }
    if (reduce || !fromUser) { fill(); }
    else { panel.classList.add("swap"); setTimeout(fill, 180); }
    if (fromUser) {
      track("facemap_select", key);
      if (mq.matches) {
        var top = panel.getBoundingClientRect().top;
        if (top > window.innerHeight * 0.75 || top < 60) panel.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
      }
    }
  }
  triggers.forEach(function(t){ t.addEventListener("click", function(){ renderZone(t.dataset.zone, true); }); });
  if (panel) renderZone("lips", false);

  /* ---------- Treatment menu filter ---------- */
  var filterBtns = $$("[data-filter]"), cats = $$(".cat");
  filterBtns.forEach(function(b){
    b.addEventListener("click", function(){
      var f = b.dataset.filter;
      filterBtns.forEach(function(x){ x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      cats.forEach(function(c){ c.hidden = !(f === "all" || c.dataset.cat === f); });
      track("menu_filter", f);
    });
  });

  /* ---------- Gallery lightbox ---------- */
  var lb = $("#lightbox"), lbImg = $("#lb-img"), lbCap = $("#lb-cap");
  $$(".gallery button, .clinic-grid button").forEach(function(b){
    b.addEventListener("click", function(){
      lbImg.src = b.dataset.full; lbImg.alt = $("img", b).alt; lbCap.textContent = b.dataset.caption + (b.closest(".gallery") ? " · Results vary from person to person." : "");
      if (typeof lb.showModal === "function") lb.showModal(); else window.open(b.dataset.full, "_blank");
    });
  });
  if (lb) {
    $("#lb-close").addEventListener("click", function(){ lb.close(); });
    lb.addEventListener("click", function(e){ if (e.target === lb) lb.close(); });
  }

  /* ---------- Scroll reveal ---------- */
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    $$(".reveal").forEach(function(el){ io.observe(el); });
  } else {
    $$(".reveal").forEach(function(el){ el.classList.add("in"); });
  }

  $("#year").textContent = new Date().getFullYear();

  /* ---------- Contact form ----------
     Sends to the form's action URL (e.g. Formspree). With no action set, it opens the
     visitor's email app with the message filled in. "Send on WhatsApp" opens a chat instead. */
  var form = $("#enquiry-form");
  if (form) {
    var done = form.parentNode.querySelector(".f-done");
    var statusEl = $(".f-status", form), sendBtn = $(".f-send", form);
    var f = {
      name: $("#f-name", form), phone: $("#f-phone", form), email: $("#f-email", form),
      treatment: $("#f-treatment", form), msg: $("#f-msg", form), consent: $("#f-consent", form)
    };
    var rules = {
      name: function(v){ return v.trim().length >= 2 ? "" : "Enter your name."; },
      phone: function(v){ var d = v.replace(/[^0-9]/g, ""); return d.length >= 10 && d.length <= 13 ? "" : "Enter a phone number, for example 07700 900123."; },
      email: function(v){ return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : "Enter an email address, for example name@example.com."; },
      consent: function(_, el){ return el.checked ? "" : "Tick the box so we can reply to you."; }
    };
    function check(key){
      var el = f[key], msg = rules[key](el.value, el), err = document.getElementById(el.id + "-err");
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg;
      return msg;
    }
    Object.keys(rules).forEach(function(key){
      var el = f[key];
      el.addEventListener(key === "consent" ? "change" : "blur", function(){ if (el.value || key === "consent") check(key); });
      el.addEventListener("input", function(){ if (el.getAttribute("aria-invalid") === "true") check(key); });
    });
    /* Message box grows as you type, up to a limit, then scrolls */
    function grow(){
      var ta = f.msg; ta.style.height = "auto";
      var h = Math.min(ta.scrollHeight + 2, 420);
      ta.style.height = Math.max(h, 120) + "px";
      ta.classList.toggle("is-max", ta.scrollHeight + 2 > 420);
    }
    f.msg.addEventListener("input", grow);
    f.msg.addEventListener("focus", grow);
    function method(){ var r = $("input[name=contact_method]:checked", form); return r ? r.value : "phone call"; }
    function firstName(){ return f.name.value.trim().split(/\s+/)[0]; }
    function showDone(text){
      var n = firstName();
      $(".f-done-name", done).textContent = n ? ", " + n : "";
      if (text) $(".f-done-text", done).textContent = text;
      else $(".f-done-method", done).textContent = method();
      form.hidden = true; done.hidden = false; done.focus();
      track("contact_submit", (form.getAttribute("data-source") || "unknown") + " | " + f.treatment.value);
    }
    function summary(){
      return "Name: " + f.name.value.trim() + "\nPhone: " + f.phone.value.trim() + "\nEmail: " + f.email.value.trim() +
        "\nTreatment: " + f.treatment.value + "\nContact me by: " + method() + (f.msg.value.trim() ? "\n\n" + f.msg.value.trim() : "");
    }
    form.addEventListener("submit", function(e){
      e.preventDefault();
      statusEl.textContent = "";
      if ($("input[name=_gotcha]", form).value) { showDone(); return; }
      var firstBad = null;
      Object.keys(rules).forEach(function(key){ if (check(key) && !firstBad) firstBad = f[key]; });
      if (firstBad) { statusEl.textContent = "Check the highlighted fields, then send again."; firstBad.focus(); return; }
      var endpoint = form.getAttribute("action") || "";
      if (endpoint.indexOf("http") !== 0) {
        var subject = "Website enquiry: " + f.treatment.value;
        window.location.href = "mailto:" + form.getAttribute("data-email") + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(summary());
        showDone("Your email app should have opened with your message ready. Press send and we'll reply by " + method() + ".");
        return;
      }
      sendBtn.disabled = true;
      var label = sendBtn.firstChild.nodeValue; sendBtn.firstChild.nodeValue = "Sending\u2026 ";
      /* Google Sheets (Apps Script): send as a simple form post and read Google's reply,
         so "Thank you" only shows once the row is really saved. Formspree replies with JSON too. */
      var toSheets = endpoint.indexOf("script.google.com") !== -1;
      fetch(endpoint, toSheets
          ? { method: "POST", body: new URLSearchParams(new FormData(form)) }
          : { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function(r){ if (!r.ok) throw new Error(r.status); return toSheets ? r.json() : null; })
        .then(function(data){ if (toSheets && !(data && data.ok)) throw new Error("not saved"); showDone(); })
        .catch(function(){ statusEl.textContent = "Your enquiry didn't send. Try again, or call 07988 347194."; })
        .then(function(){ sendBtn.disabled = false; sendBtn.firstChild.nodeValue = label; });
    });
    $(".f-wa", form).addEventListener("click", function(){
      var text = "Hi, " + (f.name.value.trim() ? "I'm " + f.name.value.trim() + ". " : "") +
        "I'm interested in " + (f.treatment.value === "Not sure yet" ? "a treatment and would like some advice" : (/^[A-Z]{2}/.test(f.treatment.value) ? f.treatment.value : f.treatment.value.charAt(0).toLowerCase() + f.treatment.value.slice(1))) + "." +
        (f.msg.value.trim() ? " " + f.msg.value.trim() : "");
      if (f.treatment.value === "Free consultation") {
        text = "Hi, " + (f.name.value.trim() ? "I'm " + f.name.value.trim() + ". " : "") + "I'd like to book a free consultation." +
          (f.msg.value.trim() ? " " + f.msg.value.trim() : "");
      }
      track("whatsapp_click", (form.getAttribute("data-source") || "unknown") + "-form");
      window.open("https://wa.me/" + form.getAttribute("data-whatsapp") + "?text=" + encodeURIComponent(text), "_blank", "noopener");
    });
  }

  /* ---------- Free consultation buttons ----------
     They jump to the contact form with "Free consultation" already chosen. */
  function chooseConsult(){ var sel = $("#f-treatment"); if (sel) sel.value = "Free consultation"; }
  $$("[data-consult]").forEach(function(a){
    a.addEventListener("click", function(){
      chooseConsult();
      track("consult_click", a.getAttribute("data-consult"));
      setTimeout(function(){ var n = $("#f-name"); if (n) n.focus({ preventScroll: true }); }, 700);
    });
  });
  if (/[?&]consult=1/.test(location.search)) chooseConsult();

  /* ---------- Review slider ---------- */
  var slider = $(".rv-slider");
  if (slider) {
    var slides = $$(".rv-slide", slider), cur = 0, paused = false;
    var countEl = $(".rv-count", slider), bar = $(".rv-bar", slider);
    var pad = function(n){ return (n < 10 ? "0" : "") + n; };
    var auto = !reduce;
    function runBar(){
      bar.classList.remove("run"); void bar.offsetWidth;
      if (auto) { bar.classList.add("run"); $("i", bar).style.animationPlayState = paused ? "paused" : "running"; }
    }
    function go(n){
      slides[cur].classList.remove("is-active"); slides[cur].setAttribute("aria-hidden", "true");
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add("is-active"); slides[cur].removeAttribute("aria-hidden");
      countEl.textContent = pad(cur + 1) + " / " + pad(slides.length);
      runBar();
    }
    $("i", bar).addEventListener("animationend", function(){ go(cur + 1); });
    $$("[data-rv]", slider).forEach(function(b){
      b.addEventListener("click", function(){ go(cur + (b.getAttribute("data-rv") === "next" ? 1 : -1)); track("review_nav", b.getAttribute("data-rv")); });
    });
    function setPaused(p){ paused = p; $("i", bar).style.animationPlayState = p ? "paused" : "running"; }
    slider.addEventListener("mouseenter", function(){ setPaused(true); });
    slider.addEventListener("mouseleave", function(){ setPaused(false); });
    slider.addEventListener("focusin", function(){ setPaused(true); });
    slider.addEventListener("focusout", function(){ setPaused(false); });
    var sx = null;
    slider.addEventListener("pointerdown", function(e){ sx = e.clientX; });
    slider.addEventListener("pointerup", function(e){
      if (sx === null) return; var dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1));
    });
    runBar();
  }

  /* Ribbon prices come from the price menu, so they never go out of date */
  $$("[data-price]").forEach(function(el){
    var row = document.getElementById(el.getAttribute("data-price"));
    if (row) el.textContent = "from " + $(".svc-price", row).textContent.replace(/^from\s*/i, "");
  });

  /* ---------- Structured data built from the page ----------
     Prices and FAQs are read from the menu and FAQ above, so Google always
     sees the same prices as visitors. Edit the HTML, not this script. */
  /* Home page only: subpages carry their own static schema. */
  if (!cats.length || !$("#faq-list")) return;
  var catalog = {
    "@context": "https://schema.org",
    "@type": "OfferCatalog",
    "@id": SITE + "#treatments",
    "name": "Treatments and prices",
    "itemListElement": cats.map(function(c){
      return {
        "@type": "OfferCatalog",
        "name": $(".cat-title", c).textContent,
        "itemListElement": $$(".svc", c).map(function(li){
          var price = $(".svc-price", li).textContent.replace(/[^0-9.]/g, "");
          return {
            "@type": "Offer",
            "price": price,
            "priceCurrency": "GBP",
            "url": SITE + "#" + li.id,
            "itemOffered": { "@type": "Service", "name": $(".svc-name", li).textContent, "description": $(".svc-desc", li).textContent, "provider": { "@id": SITE + "#business" } }
          };
        })
      };
    })
  };
  var faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": $$("#faq-list details").map(function(d){
      return { "@type": "Question", "name": $("summary", d).textContent.trim(), "acceptedAnswer": { "@type": "Answer", "text": $(".answer", d).textContent.trim() } };
    })
  };
  [catalog, faq].forEach(function(obj){
    var s = document.createElement("script"); s.type = "application/ld+json";
    s.textContent = JSON.stringify(obj); document.head.appendChild(s);
  });
})();
