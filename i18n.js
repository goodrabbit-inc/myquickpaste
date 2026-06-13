(function () {
  "use strict";
  var SUPPORTED = ["ja", "en"];
  var DEFAULT = "ja";
  var STORAGE_KEY = "mqp-lang";
  var LANG_NAMES = { ja: "\u65e5\u672c\u8a9e", en: "English" };

  function resolveLang(pref) {
    if (pref && SUPPORTED.indexOf(pref) !== -1) return pref;
    var nav = (navigator.language || "ja").slice(0, 2).toLowerCase();
    if (SUPPORTED.indexOf(nav) !== -1) return nav;
    return DEFAULT;
  }

  function getBasePath() {
    var path = location.pathname || "/";
    if (/\.html$/i.test(path)) {
      return path.slice(0, path.lastIndexOf("/") + 1);
    }
    if (!path.endsWith("/")) {
      return path + "/";
    }
    return path;
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

  var pickerBtn = null;
  var pickerMenu = null;
  var pickerRoot = null;
  var pickerLabel = null;

  function closeLangMenu() {
    if (!pickerBtn || !pickerMenu) return;
    pickerBtn.setAttribute("aria-expanded", "false");
    pickerMenu.hidden = true;
  }

  function openLangMenu() {
    if (!pickerBtn || !pickerMenu) return;
    pickerBtn.setAttribute("aria-expanded", "true");
    pickerMenu.hidden = false;
  }

  function toggleLangMenu() {
    if (!pickerMenu) return;
    if (pickerMenu.hidden) openLangMenu();
    else closeLangMenu();
  }

  function updateLangPicker(lang) {
    if (pickerLabel && LANG_NAMES[lang]) pickerLabel.textContent = LANG_NAMES[lang];
    if (!pickerMenu) return;
    pickerMenu.querySelectorAll("[data-lang]").forEach(function (item) {
      var selected = item.getAttribute("data-lang") === lang;
      item.setAttribute("aria-selected", selected ? "true" : "false");
    });
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
      updateLangPicker(t.meta.lang || DEFAULT);
    }
  }

  function load(lang) {
    var url = getBasePath() + "i18n/" + lang + ".json";
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error("Failed to load " + url);
      return res.json();
    });
  }

  function setLang(lang) {
    var resolved = resolveLang(lang);
    return load(resolved).then(function (t) {
      apply(t);
      closeLangMenu();
      try { localStorage.setItem(STORAGE_KEY, resolved); } catch (e) {}
    }).catch(function (err) {
      console.error(err);
      if (resolved !== DEFAULT) return setLang(DEFAULT);
    });
  }

  function initLangPicker() {
    pickerBtn = document.getElementById("lang-picker-btn");
    pickerMenu = document.getElementById("lang-picker-menu");
    pickerRoot = document.getElementById("lang-picker");
    pickerLabel = document.getElementById("lang-picker-label");
    if (!pickerBtn || !pickerMenu || !pickerRoot) return;

    pickerBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      toggleLangMenu();
    });

    pickerMenu.addEventListener("click", function (e) {
      e.stopPropagation();
      var item = e.target.closest("[data-lang]");
      if (!item) return;
      setLang(item.getAttribute("data-lang"));
    });

    document.addEventListener("click", function (e) {
      if (!pickerRoot.contains(e.target)) closeLangMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeLangMenu();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initLangPicker();
    var saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    setLang(saved);
  });
})();
