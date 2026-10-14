// Menu, More menu, theme toggle, footer year, email copy button, notes filter and the engagement stages (data/projects.json).
// Loaded with defer. The theme is applied before first paint by a tiny inline script allowed by hash in the CSP.
(function () {
  "use strict";
  var root = document.documentElement;

  // Mobile menu
  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
        menuBtn.focus();
      }
    });
  }

  // Theme: system by default; a manual choice is remembered
  var themeBtn = document.querySelector(".theme-btn");
  function current() {
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function label() {
    var next = current() === "dark" ? "light" : "dark";
    themeBtn.setAttribute("aria-label", "Switch to " + next + " mode");
    themeBtn.setAttribute("title", "Switch to " + next + " mode");
  }
  if (themeBtn) {
    root.dataset.theme = current();
    label();
    themeBtn.addEventListener("click", function () {
      root.dataset.theme = current() === "dark" ? "light" : "dark";
      try { localStorage.setItem("theme", root.dataset.theme); } catch (e) { /* storage blocked */ }
      label();
    });
  }

  // Footer year (2026 is in the HTML as the fallback)
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());

  // Copy email to the clipboard, with a visible confirmation
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    var status = document.getElementById(btn.getAttribute("aria-describedby"));
    btn.hidden = false;
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      function done(ok) {
        if (status) status.textContent = ok ? "Copied" : "Press Ctrl+C to copy";
        setTimeout(function () { if (status) status.textContent = ""; }, 2500);
      }
      // Fallback when the Clipboard API is missing or denied: select the visible address, then try
      // the older copy command; if that fails too, the selection makes "Press Ctrl+C" true.
      function fallback() {
        var shown = btn.closest(".card") && btn.closest(".card").querySelector('a[href^="mailto:"]');
        if (!shown || !window.getSelection) return done(false);
        var range = document.createRange();
        range.selectNodeContents(shown);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
        done(ok);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
      } else {
        fallback();
      }
    });
  });

  // "More" menu: a disclosure button (desktop); on phones its links are a group inside the menu
  var more = document.querySelector(".site-nav .more");
  var moreBtn = more && more.querySelector(".more-btn");
  if (more && moreBtn) {
    var setMore = function (open) {
      more.classList.toggle("open", open);
      moreBtn.setAttribute("aria-expanded", open ? "true" : "false");
    };
    moreBtn.addEventListener("click", function () { setMore(!more.classList.contains("open")); });
    document.addEventListener("click", function (e) { if (!more.contains(e.target)) setMore(false); });
    more.addEventListener("focusout", function (e) { if (e.relatedTarget && !more.contains(e.relatedTarget)) setMore(false); });
    more.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && more.classList.contains("open")) {
        e.stopPropagation();
        setMore(false);
        moreBtn.focus();
      }
    });
  }

  // Notes: category filter chips (shown only with JavaScript; every note is listed without it)
  var chips = document.querySelector(".chips");
  var noteList = document.querySelector("[data-notes]");
  if (chips && noteList) {
    chips.hidden = false;
    var noteStatus = document.querySelector(".notes-empty");
    chips.addEventListener("click", function (e) {
      var chip = e.target.closest(".chip");
      if (!chip) return;
      var filter = chip.getAttribute("data-filter");
      chips.querySelectorAll(".chip").forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      var shown = 0;
      noteList.querySelectorAll("li").forEach(function (li) {
        var match = !filter || li.getAttribute("data-category") === filter;
        li.hidden = !match;
        if (match) shown += 1;
      });
      if (noteStatus) noteStatus.textContent = shown + (shown === 1 ? " note" : " notes") + (filter ? " in " + filter : "");
    });
  }

  // Engagement stages, one data file for every page
  var lists = document.querySelectorAll("[data-stages]");
  if (!lists.length || !window.fetch) return;
  var base = document.body.getAttribute("data-root") || "";
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }
  function href(url) {
    return /^https?:/.test(url) ? url : base + url;
  }
  fetch(base + "data/projects.json")
    .then(function (r) { return r.json(); })
    .then(function (data) {
      lists.forEach(function (list) {
        var compact = list.classList.contains("compact");
        list.textContent = "";
        data.stages.forEach(function (s) {
          var li = el("li", "stage");
          li.dataset.status = s.status;
          var top = el("div", "stage-top");
          top.appendChild(el("span", "stage-num", String(s.stage)));
          top.appendChild(el("span", "tag" + (s.status === "Live" ? " live" : ""), s.status));
          li.appendChild(top);
          li.appendChild(el("h3", null, s.name));
          li.appendChild(el("p", null, compact ? s.summary : s.delivers));
          if (!compact && s.links && s.links.length) {
            var links = el("div", "links");
            s.links.forEach(function (l) {
              var a = el("a", null, l.label + " →");
              a.href = href(l.url);
              if (/^https?:/.test(l.url)) a.rel = "noopener noreferrer";
              links.appendChild(a);
            });
            li.appendChild(links);
            if (s.links.some(function (l) { return l.label === "Live app"; })) {
              li.appendChild(el("p", "small wake-note", "Free hosting: if the app is asleep, click ‘wake up’ and give it about 30 seconds."));
            }
          }
          list.appendChild(li);
        });
      });
    })
    .catch(function () { /* the static fallback list stays */ });
})();
