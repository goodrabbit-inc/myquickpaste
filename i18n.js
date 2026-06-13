(function () {
  "use strict";
  var SUPPORTED = ["ja", "en"];
  var DEFAULT = "ja";
  var STORAGE_KEY = "mqp-lang";
  function resolveLang(pref) {
    if (pref && SUPPORTED.indexOf(pref) !== -1) return pref;
    var nav = (navigator.language || "ja").slice(0, 2).toLowerCase();
    if (SUPPORTED.indexOf(nav) !== -1) return nav;
    return DEFAULT;
  }
  function get(obj, path) {
    return path.split(".").reduce(function (o, k) {
      return o && o[k] !== undefined ? o[k] : null;
    }, obj);
  }
  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function fillList(id, items) {
    var ul = document.getElementById(id);
    if (!ul || !items) return;
    ul.innerHTML = items.map(function (item) { return "<li>" + escapeHtml(item) + "</li>"; }).join("");
  }
  function fillCards(id, items) {
    var div = document.getElementById(id);
    if (!div || !items) return;
    div.innerHTML = items.map(function (item) {
      return '<article class="card"><h3>' + escapeHtml(item.title) + "</h3><p>" + escapeHtml(item.text) + "</p></article>";
    }).join("");
  }
  function setText(id, text) {
    var el = document.getElementById(id);
    if (el && text) el.textContent = text;
  }
  function apply(t) {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var val = get(t, key);
      if (val != null) el.textContent = val;
    });
    fillList("problem-list", t.problem && t.problem.items);
    setText("problem-solution", t.problem && t.problem.solution);
    fillCards("benefits-grid", t.benefits && t.benefits.items);
    fillCards("features-grid", t.features && t.features.items);
    fillCards("usecases-grid", t.usecases && t.usecases.items);
    fillList("pricing-free-list", t.pricing && t.pricing.freeItems);
    fillList("pricing-pro-list", t.pricing && t.pricing.proItems);
    if (t.meta) {
      document.title = t.meta.title || document.title;
      document.documentElement.lang = t.meta.lang || "ja";
      var desc = document.querySelector('meta[name="description"]');
      if (desc && t.meta.description) desc.setAttribute("content", t.meta.description);
    }
    var sel = document.getElementById("lang-select");
    if (sel && t.meta && t.meta.lang) sel.value = t.meta.lang;
  }
  function load(lang) {
    return fetch("i18n/" + lang + ".json").then(function (res) {
      if (!res.ok) throw new Error("Failed to load i18n/" + lang + ".json");
      return res.json();
    });
  }
  function setLang(lang) {
    var resolved = resolveLang(lang);
    return load(resolved).then(function (t) {
      apply(t);
      try { localStorage.setItem(STORAGE_KEY, resolved); } catch (e) {}
    }).catch(function (err) {
      console.error(err);
      if (resolved !== DEFAULT) return setLang(DEFAULT);
    });
  }
  document.addEventListener("DOMContentLoaded", function () {
    var saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    setLang(saved);
    var sel = document.getElementById("lang-select");
    if (sel) sel.addEventListener("change", function () { setLang(sel.value); });
  });
})();
