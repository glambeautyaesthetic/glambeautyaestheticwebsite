/* Depth effects: scroll-linked 3D and pointer tilt.
   - Elements with data-3d get --p (-1..1: below centre → above centre) and --pa (|p|)
     as they pass through the screen. CSS turns these into 3D transforms.
   - Elements with data-tilt get --mx / --my (-1..1) from the mouse, eased.
   Turned off entirely for people who prefer reduced motion. */
(function () {
  "use strict";
  if (!window.matchMedia || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  document.documentElement.classList.add("d3-on");

  var scrollEls = [].slice.call(document.querySelectorAll("[data-3d]"));
  var ticking = false;

  function updateScroll() {
    ticking = false;
    var vh = window.innerHeight;
    for (var i = 0; i < scrollEls.length; i++) {
      var el = scrollEls[i], r = el.getBoundingClientRect();
      if (r.bottom < -300 || r.top > vh + 300) continue;
      var p = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);
      p = Math.max(-1, Math.min(1, p));
      el.style.setProperty("--p", p.toFixed(3));
      el.style.setProperty("--pa", Math.abs(p).toFixed(3));
    }
  }
  function requestScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(updateScroll); }
  }
  window.addEventListener("scroll", requestScroll, { passive: true });
  window.addEventListener("resize", requestScroll);
  updateScroll();

  /* Pointer tilt: only on devices with a precise pointer (mouse / trackpad). */
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  [].slice.call(document.querySelectorAll("[data-tilt]")).forEach(function (el) {
    var tx = 0, ty = 0, cx = 0, cy = 0, running = false;
    function loop() {
      cx += (tx - cx) * 0.08;
      cy += (ty - cy) * 0.08;
      el.style.setProperty("--mx", cx.toFixed(3));
      el.style.setProperty("--my", cy.toFixed(3));
      if (Math.abs(tx - cx) > 0.001 || Math.abs(ty - cy) > 0.001) window.requestAnimationFrame(loop);
      else running = false;
    }
    function kick() { if (!running) { running = true; window.requestAnimationFrame(loop); } }
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width) * 2 - 1;
      ty = ((e.clientY - r.top) / r.height) * 2 - 1;
      kick();
    });
    el.addEventListener("pointerleave", function () { tx = 0; ty = 0; kick(); });
  });

  /* Magnetic buttons: key Book buttons lean gently toward the cursor. */
  [].slice.call(document.querySelectorAll("[data-magnetic]")).forEach(function (el) {
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect();
      var dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
      el.style.transform = "translate(" + (dx * 0.18).toFixed(1) + "px," + (dy * 0.28).toFixed(1) + "px)";
    });
    el.addEventListener("pointerleave", function () { el.style.transform = ""; });
  });
})();
