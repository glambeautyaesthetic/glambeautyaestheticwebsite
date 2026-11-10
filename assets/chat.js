/* Glam Assistant: a small on-site chat that answers from assets/chat-kb.json.
   No AI service: answers come only from the clinic's own information, and the
   matching is tolerant of typos ("fillr" → "filler", "botx" → "botox"). */
(function () {
  "use strict";

  /* ================================================================ Engine */
  function createEngine(kb) {
    var STOP = new Set(kb.stop), SYN = kb.syn;
    var PHRASES = kb.phrases.map(function (p) {
      return [new RegExp("(^|[^a-z0-9])" + p[0].replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![a-z0-9])", "g"), p[1]];
    });
    var entries = kb.entries, byId = {}, df = {}, N = entries.length;
    entries.forEach(function (e) {
      byId[e.id] = e;
      Object.keys(e.k).forEach(function (t) { df[t] = (df[t] || 0) + 1; });
    });
    var vocab = Object.keys(df);
    var KNOWN = new Set(vocab);
    Object.keys(SYN).forEach(function (k) { KNOWN.add(k); });
    kb.stop.forEach(function (k) { KNOWN.add(k); });
    kb.phrases.forEach(function (p) { p[0].split(" ").forEach(function (w) { KNOWN.add(w); }); });
    var knownList = Array.from(KNOWN);
    var vocabSet = new Set(vocab);

    function stem(t) {
      if (t.length > 4 && /ies$/.test(t)) return t.slice(0, -3) + "y";
      if (t.length > 3 && /s$/.test(t) && !/(ss|us)$/.test(t)) return t.slice(0, -1);
      return t;
    }
    function prep(text) {
      return String(text).toLowerCase().replace(/&/g, " and ").replace(/[’']/g, "")
        .replace(/[^a-z0-9+£ ]+/g, " ").replace(/\s+/g, " ").trim();
    }
    /* Same steps as norm() in _build/chat_kb.py */
    function norm(text) {
      var s = " " + prep(text) + " ";
      PHRASES.forEach(function (p) { s = s.replace(p[0], "$1" + p[1]); });
      var out = [];
      s.split(" ").forEach(function (t) {
        if (!t || STOP.has(t)) return;
        t = stem(t);
        t = Object.prototype.hasOwnProperty.call(SYN, t) ? SYN[t] : t;
        if (STOP.has(t) || (t.length < 2 && t !== "£")) return;
        out.push(t);
      });
      return out;
    }
    /* Optimal string alignment distance (Damerau–Levenshtein with adjacent swaps) */
    function dist(a, b, max) {
      if (Math.abs(a.length - b.length) > max) return max + 1;
      var prev2 = null, prev = [], cur, i, j;
      for (j = 0; j <= b.length; j++) prev[j] = j;
      for (i = 1; i <= a.length; i++) {
        cur = [i];
        var rowMin = i;
        for (j = 1; j <= b.length; j++) {
          var cost = a[i - 1] === b[j - 1] ? 0 : 1;
          var v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
          if (prev2 && i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, prev2[j - 2] + 1);
          cur[j] = v;
          if (v < rowMin) rowMin = v;
        }
        if (rowMin > max) return max + 1;
        prev2 = prev; prev = cur;
      }
      return prev[b.length];
    }
    function allowed(len) { return len <= 3 ? 0 : len <= 5 ? 1 : len <= 9 ? 2 : 3; }

    /* Fix a misspelt word using the clinic's own vocabulary */
    function correct(word) {
      var w = word, s = stem(word);
      if (KNOWN.has(w) || KNOWN.has(s) || /^[0-9+£]+$/.test(w)) return null;
      var max = allowed(s.length);
      if (!max) return null;
      var best = null, bestD = max + 1;
      for (var i = 0; i < knownList.length; i++) {
        var c = knownList[i];
        if (c.length < 3) continue;
        if (s.length < 10 && c[0] !== s[0]) continue;      /* first letter must match on shorter words */
        var d = dist(s, c, Math.min(max, bestD));
        /* On a tie, prefer the same length (a swapped pair of letters), then words the answers use */
        if (d < bestD || (d === bestD && best && (
            Math.abs(c.length - s.length) < Math.abs(best.length - s.length) ||
            (c.length === best.length && vocabSet.has(c) && !vocabSet.has(best))))) { best = c; bestD = d; }
      }
      if (best && bestD <= max) return best;
      /* Partial words: "micro" → "microneedling" */
      if (s.length >= 4) {
        var pre = vocab.filter(function (c) { return c.indexOf(s) === 0; }).sort(function (a, b) { return a.length - b.length; });
        if (pre.length) return pre[0];
      }
      return null;
    }

    function analyse(text) {
      var raw = prep(text).split(" ").filter(Boolean), fixed = [], corrections = [];
      raw.forEach(function (w) {
        var c = correct(w);
        if (c) { fixed.push(c); if (!STOP.has(c)) corrections.push([w, c]); }
        else fixed.push(w);
      });
      var tokens = [], seen = {};
      norm(fixed.join(" ")).forEach(function (t) { if (!seen[t]) { seen[t] = 1; tokens.push(t); } });
      var fuzzy = {};
      corrections.forEach(function (c) { norm(c[1]).forEach(function (t) { fuzzy[t] = 1; }); });
      return { tokens: tokens, fuzzy: fuzzy, corrections: corrections };
    }

    function idf(t) { return Math.log(1 + N / (df[t] || 0.5)); }

    function ask(text) {
      var q = analyse(text), total = 0;
      if (!q.tokens.length) return { entry: null, conf: 0, alts: [], corrections: q.corrections };
      q.tokens.forEach(function (t) { total += idf(t); });
      var scored = entries.map(function (e) {
        var s = 0, m = 0;
        q.tokens.forEach(function (t) {
          var w = e.k[t];
          if (!w) return;
          var f = q.fuzzy[t] ? 0.85 : 1;
          s += w * idf(t) * f; m += idf(t) * f;
        });
        return { e: e, s: s * (e.p || 1), c: m / total };
      }).filter(function (x) { return x.s > 0; });
      scored.sort(function (a, b) { return b.s - a.s || b.c - a.c; });
      if (!scored.length) return { entry: null, conf: 0, alts: [], corrections: q.corrections };
      var top = scored[0], alts = [], titles = {};
      titles[top.e.t] = 1;
      for (var i = 1; i < scored.length && alts.length < 3; i++) {
        if (scored[i].c >= 0.3 && !titles[scored[i].e.t]) { titles[scored[i].e.t] = 1; alts.push(scored[i].e); }
      }
      return { entry: top.e, conf: top.c, alts: alts, corrections: q.corrections };
    }

    return { ask: ask, byId: byId, analyse: analyse, prep: prep };
  }

  if (typeof module !== "undefined" && module.exports) { module.exports = { createEngine: createEngine }; }
  if (typeof document === "undefined") return;

  /* ================================================================ UI */
  var KB_URL = "/assets/chat-kb.json?v=25";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var engine = null, kb = null, loading = null, started = false;

  function track(name, label) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: name, cta_location: label });
    if (typeof window.gtag === "function") window.gtag("event", name, { cta_location: label });
  }
  function load() {
    if (loading) return loading;
    loading = fetch(KB_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) { kb = data; engine = createEngine(data); return engine; });
    return loading;
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function svg(path, vb) {
    var ns = "http://www.w3.org/2000/svg", s = document.createElementNS(ns, "svg"), p = document.createElementNS(ns, "path");
    s.setAttribute("viewBox", vb || "0 0 24 24"); s.setAttribute("aria-hidden", "true"); s.setAttribute("fill", "none");
    p.setAttribute("d", path); p.setAttribute("stroke", "currentColor"); p.setAttribute("stroke-width", "1.6");
    p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round");
    s.appendChild(p); return s;
  }

  /* ---------- build the widget ---------- */
  var root = el("div", "chat");
  var fab = el("button", "chat-fab");
  fab.type = "button";
  fab.setAttribute("aria-label", "Open chat: ask us a question");
  fab.setAttribute("aria-expanded", "false");
  fab.setAttribute("aria-controls", "chat-panel");
  var icoChat = svg("M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 4v-4h0A1.5 1.5 0 0 1 4 14.5z");
  icoChat.classList.add("ico-chat");
  var icoClose = svg("M6 9l6 6 6-6");
  icoClose.classList.add("ico-close");
  fab.appendChild(icoChat); fab.appendChild(icoClose); fab.appendChild(el("span", "chat-dot"));

  var teaser = el("div", "chat-teaser"); teaser.hidden = true;
  var teaserBtn = el("button", "chat-teaser-open"); teaserBtn.type = "button";
  teaserBtn.appendChild(el("span", null, "Questions about a treatment or price? "));
  teaserBtn.appendChild(el("b", null, "Ask me"));
  var teaserX = el("button", "chat-teaser-x", "×"); teaserX.type = "button"; teaserX.setAttribute("aria-label", "Dismiss");
  teaser.appendChild(teaserBtn); teaser.appendChild(teaserX);

  var panel = el("section", "chat-panel"); panel.id = "chat-panel"; panel.hidden = true;
  panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Glam Assistant chat");
  var head = el("header", "chat-head");
  head.appendChild(el("span", "chat-avatar", "G"));
  var ht = el("div", "chat-title");
  ht.appendChild(el("b", null, "Glam Assistant"));
  ht.appendChild(el("span", null, "Instant answers, any time"));
  head.appendChild(ht);
  var closeBtn = el("button", "chat-x"); closeBtn.type = "button"; closeBtn.setAttribute("aria-label", "Minimise chat");
  closeBtn.appendChild(svg("M6 9l6 6 6-6"));
  head.appendChild(closeBtn);
  var log = el("div", "chat-log"); log.setAttribute("role", "log"); log.setAttribute("aria-live", "polite");
  var form = el("form", "chat-form");
  var lab = el("label", "sr-only", "Type your question"); lab.setAttribute("for", "chat-input");
  var input = el("input"); input.id = "chat-input"; input.type = "text"; input.autocomplete = "off";
  input.maxLength = 200; input.placeholder = "Ask about treatments, prices, hours…";
  input.setAttribute("enterkeyhint", "send");
  var send = el("button", "chat-send"); send.type = "submit"; send.setAttribute("aria-label", "Send");
  send.appendChild(svg("M4 12h15M13 6l6 6-6 6"));
  form.appendChild(lab); form.appendChild(input); form.appendChild(send);
  var foot = el("p", "chat-foot", "Automated answers from our clinic information. For medical advice, please speak to your practitioner.");
  panel.appendChild(head); panel.appendChild(log); panel.appendChild(form); panel.appendChild(foot);
  root.appendChild(teaser); root.appendChild(panel); root.appendChild(fab);
  document.body.appendChild(root);

  /* ---------- messages ---------- */
  function scrollDown() { log.scrollTop = log.scrollHeight; }
  function userMsg(text) {
    var m = el("div", "msg msg-user"); m.appendChild(el("p", null, text)); log.appendChild(m); scrollDown();
  }
  function typing() {
    var t = el("div", "msg msg-bot msg-typing"); t.setAttribute("aria-label", "Typing");
    t.appendChild(el("i")); t.appendChild(el("i")); t.appendChild(el("i"));
    log.appendChild(t); scrollDown(); return t;
  }
  function linkFor(l, id) {
    var a = el("a", "chat-link chat-link-" + l[2], l[0]);
    var href = l[1];
    if (l[2] === "book") {
      href = kb.book + "?utm_source=website&utm_medium=chat&utm_content=" + encodeURIComponent(id);
      a.classList.add("js-book"); a.setAttribute("data-cta", "chat-" + id);
    } else if (l[2] === "wa" || l[2] === "tel") {
      a.setAttribute("data-cta", "chat-" + id);
    }
    a.href = href;
    if (/^https?:/.test(href)) { a.target = "_blank"; a.rel = "noopener"; }
    if (l[2] === "page") a.addEventListener("click", function () { close(false); });
    return a;
  }
  function chips(list, label) {
    var wrap = el("div", "chat-chips");
    if (label) wrap.appendChild(el("span", "chat-chips-label", label));
    list.forEach(function (c) {
      var b = el("button", "chat-chip", c.label); b.type = "button";
      b.addEventListener("click", function () { c.go(); });
      wrap.appendChild(b);
    });
    return wrap;
  }

  /* London time, for opening hours */
  function londonNow() {
    var parts = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/London", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
    var o = {}; parts.forEach(function (p) { o[p.type] = p.value; });
    return { day: { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }[o.weekday], min: (+o.hour % 24) * 60 + (+o.minute) };
  }
  function fmt(t) { var p = t.split(":"), h = +p[0]; return (h % 12 || 12) + (p[1] !== "00" ? ":" + p[1] : "") + (h < 12 ? "am" : "pm"); }
  function toMin(t) { var p = t.split(":"); return +p[0] * 60 + +p[1]; }
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  function hoursBlock() {
    var now = londonNow(), wrap = el("div", "chat-hours"), today = null;
    kb.hours.forEach(function (h) { if (h[0] === now.day) today = h; });
    var status;
    if (today && now.min >= toMin(today[1]) && now.min < toMin(today[2])) status = "We're open now, until " + fmt(today[2]) + ".";
    else if (today && now.min < toMin(today[1])) status = "We open today at " + fmt(today[1]) + ".";
    else {
      var next = null; kb.hours.forEach(function (h) { if (h[0] === (now.day + 1) % 7) next = h; });
      status = "We're closed now and open tomorrow at " + fmt(next[1]) + ". You can still book online any time.";
    }
    wrap.appendChild(el("p", null, status));
    var tbl = el("ul", "chat-items");
    kb.hours.forEach(function (h) {
      var li = el("li", h[0] === now.day ? "is-today" : null);
      li.appendChild(el("span", null, DAYS[h[0]] + (h[0] === now.day ? " (today)" : "")));
      li.appendChild(el("b", null, fmt(h[1]) + " – " + fmt(h[2])));
      tbl.appendChild(li);
    });
    wrap.appendChild(tbl);
    return wrap;
  }

  function botAnswer(e, note) {
    var m = el("div", "msg msg-bot");
    if (note) m.appendChild(el("p", "msg-note", note));
    e.a.forEach(function (p) { m.appendChild(p === "{hours}" ? hoursBlock() : el("p", null, p)); });
    if (e.items && e.items.length) {
      var ul = el("ul", "chat-items");
      e.items.forEach(function (it) {
        var li = el("li");
        var n = el("span", null, it[0]);
        if (it[2]) n.appendChild(el("small", null, it[2]));
        li.appendChild(n); li.appendChild(el("b", null, it[1]));
        ul.appendChild(li);
      });
      m.appendChild(ul);
    }
    if (e.links && e.links.length) {
      var row = el("div", "chat-links");
      e.links.forEach(function (l) { row.appendChild(linkFor(l, e.id)); });
      m.appendChild(row);
    }
    log.appendChild(m);
    return m;
  }
  function showEntry(e, note) {
    botAnswer(e, note);
    track("chat_answer", e.id);
    scrollDown();
  }
  function botText(lines, links, id) {
    botAnswer({ id: id || "info", a: lines, links: links || [] });
  }

  function respond(text) {
    var r = engine.ask(text);
    var note = null;
    if (r.corrections.length && r.entry) {
      var fixes = {};
      r.corrections.forEach(function (c) { fixes[c[0]] = c[1]; });
      note = "Showing answers for “" + engine.prep(text).split(" ").map(function (w) { return fixes[w] || w; }).join(" ") + "”";
    }
    if (r.entry && r.conf >= 0.5) {
      showEntry(r.entry, note);
      if (r.conf < 0.75 && r.alts.length) log.appendChild(chips(r.alts.slice(0, 2).map(altChip), "Or did you mean:"));
    } else if (r.entry && r.conf >= 0.3) {
      showEntry(r.entry, "I think you're asking about " + r.entry.t.toLowerCase() + ".");
      if (r.alts.length) log.appendChild(chips(r.alts.map(altChip), "Not quite? Try:"));
    } else {
      track("chat_unanswered", "fallback");
      botText(kb.fallback.a, kb.fallback.links, "fallback");
      log.appendChild(chips(kb.start.map(startChip)));
    }
    scrollDown();
  }
  function altChip(e) { return { label: e.t, go: function () { userMsg(e.t); reply(function () { showEntry(e); }); } }; }
  function startChip(label) { return { label: label, go: function () { ask(label); } }; }

  function reply(fn) {
    var t = typing();
    setTimeout(function () { t.remove(); fn(); }, reduce ? 0 : 420 + Math.random() * 300);
  }
  function ask(text) {
    text = String(text).trim();
    if (!text) return;
    userMsg(text);
    track("chat_question", "asked");
    load().then(function () { reply(function () { respond(text); }); })
      .catch(function () {
        botText(["Sorry, I can't load my answers right now. Please message us on WhatsApp or call " + "07988 347194" + "."],
          [["Call 07988 347194", "tel:+447988347194", "tel"]]);
      });
  }
  function greet() {
    if (started) return;
    started = true;
    var m = el("div", "msg msg-bot");
    m.appendChild(el("p", null, "Hi, I'm the Glam Assistant. Ask me about treatments, prices, opening hours or booking."));
    log.appendChild(m);
    load().then(function () { log.appendChild(chips(kb.start.map(startChip), "Popular questions")); scrollDown(); }).catch(function () {});
  }

  /* ---------- open / close ---------- */
  var lastFocus = null;
  function open() {
    lastFocus = document.activeElement;
    hideTeaser(true);
    panel.hidden = false;
    root.classList.add("is-open");
    fab.setAttribute("aria-expanded", "true");
    fab.setAttribute("aria-label", "Minimise chat");
    greet();
    requestAnimationFrame(function () { panel.classList.add("is-in"); });
    setTimeout(function () { input.focus({ preventScroll: true }); }, 60);
    if (window.matchMedia("(max-width: 560px)").matches) document.documentElement.classList.add("chat-lock");
    track("chat_open", location.pathname);
  }
  function close(refocus) {
    panel.classList.remove("is-in");
    root.classList.remove("is-open");
    fab.setAttribute("aria-expanded", "false");
    fab.setAttribute("aria-label", "Open chat: ask us a question");
    document.documentElement.classList.remove("chat-lock");
    setTimeout(function () { panel.hidden = true; }, reduce ? 0 : 260);
    if (refocus !== false && lastFocus && lastFocus.focus) lastFocus.focus();
  }
  fab.addEventListener("click", function () { root.classList.contains("is-open") ? close() : open(); });
  closeBtn.addEventListener("click", function () { close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.classList.contains("is-open")) close(); });
  form.addEventListener("submit", function (e) { e.preventDefault(); var v = input.value; input.value = ""; ask(v); });

  /* ---------- gentle prompt after a short while (once per visit) ---------- */
  function seenTeaser() { try { return sessionStorage.getItem("glamChatTeaser") === "1"; } catch (e) { return false; } }
  function hideTeaser(remember) {
    teaser.classList.remove("is-in");
    setTimeout(function () { teaser.hidden = true; }, 250);
    if (remember) { try { sessionStorage.setItem("glamChatTeaser", "1"); } catch (e) {} }
  }
  teaserBtn.addEventListener("click", open);
  teaserX.addEventListener("click", function () { hideTeaser(true); });
  if (!seenTeaser()) {
    setTimeout(function () {
      if (root.classList.contains("is-open") || seenTeaser()) return;
      teaser.hidden = false;
      requestAnimationFrame(function () { teaser.classList.add("is-in"); });
      setTimeout(function () { if (!root.classList.contains("is-open")) hideTeaser(false); }, 12000);
    }, 9000);
  }
  /* Load answers in the background once the page is idle, so the first reply is instant */
  (window.requestIdleCallback || function (f) { setTimeout(f, 2500); })(function () { load().catch(function () {}); });
})();
