(function () {
  "use strict";

  var STORE_URL = "https://apps.microsoft.com/detail/9N8WHWKDDSKK";
  var STORAGE_KEY = "mqp-lang";
  var DEFAULT = "en";
  var FALLBACK = "en";

  var LANG_REGISTRY = [
    { code: "ja", file: "ja", label: "\u65e5\u672c\u8a9e", short: "JA", rtl: false },
    { code: "en", file: "en", label: "English", short: "EN", rtl: false },
    { code: "fr", file: "fr", label: "Fran\u00e7ais", short: "FR", rtl: false },
    { code: "de", file: "de", label: "Deutsch", short: "DE", rtl: false },
    { code: "zh-cn", file: "zh-cn", label: "\u4e2d\u6587 (\u7b80\u4f53)", short: "ZH", rtl: false },
    { code: "zh-tw", file: "zh-tw", label: "\u7e41\u9ad4\u4e2d\u6587", short: "TW", rtl: false },
    { code: "ko", file: "ko", label: "\ud55c\uad6d\uc5b4", short: "KO", rtl: false },
    { code: "ru", file: "ru", label: "\u0420\u0443\u0441\u0441\u043a\u0438\u0439", short: "RU", rtl: false },
    { code: "it", file: "it", label: "Italiano", short: "IT", rtl: false },
    { code: "es", file: "es", label: "Espa\u00f1ol", short: "ES", rtl: false },
    { code: "pt", file: "pt", label: "Portugu\u00eas", short: "PT", rtl: false },
    { code: "hi", file: "hi", label: "\u0939\u093f\u0928\u094d\u0926\u0940", short: "HI", rtl: false },
    { code: "ar", file: "ar", label: "\u0627\u0644\u0639\u0631\u0628\u064a\u0629", short: "AR", rtl: true },
    { code: "id", file: "id", label: "Bahasa Indonesia", short: "ID", rtl: false },
    { code: "th", file: "th", label: "\u0e44\u0e17\u0e22", short: "TH", rtl: false },
    { code: "vi", file: "vi", label: "Ti\u1ebfng Vi\u1ec7t", short: "VI", rtl: false },
    { code: "tr", file: "tr", label: "T\u00fcrk\u00e7e", short: "TR", rtl: false },
    { code: "uk", file: "uk", label: "\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430", short: "UK", rtl: false },
    { code: "nl", file: "nl", label: "Nederlands", short: "NL", rtl: false },
    { code: "sv", file: "sv", label: "Svenska", short: "SV", rtl: false },
    { code: "pl", file: "pl", label: "Polski", short: "PL", rtl: false }
  ];

  var SUPPORTED = LANG_REGISTRY.map(function (e) { return e.code; });

  var LANG_BY_CODE = {};
  LANG_REGISTRY.forEach(function (e) {
    LANG_BY_CODE[e.code] = e;
  });

  var ALIASES = {
    "en-us": "en",
    "en-gb": "en",
    "en_us": "en",
    "zh": "zh-cn",
    "zh-hans": "zh-cn",
    "zh_cn": "zh-cn",
    "zh-tw": "zh-tw",
    "zh-hant": "zh-tw",
    "zh_tw": "zh-tw"
  };

  function normalizeLangCode(raw) {
    if (!raw) return "";
    return String(raw).trim().toLowerCase().replace(/_/g, "-");
  }

  function resolveLang(pref) {
    var key = normalizeLangCode(pref);
    if (ALIASES[key]) return ALIASES[key];
    if (LANG_BY_CODE[key]) return key;
    if (key.indexOf("-") !== -1) {
      var base = key.split("-")[0];
      if (LANG_BY_CODE[base]) return base;
    }
    var nav = normalizeLangCode(navigator.language || navigator.userLanguage || "");
    if (ALIASES[nav]) return ALIASES[nav];
    if (LANG_BY_CODE[nav]) return nav;
    if (nav.indexOf("-") !== -1) {
      var navBase = nav.split("-")[0];
      if (LANG_BY_CODE[navBase]) return navBase;
    }
    return DEFAULT;
  }

  function getLangFromUrl() {
    try {
      return new URLSearchParams(window.location.search).get("lang");
    } catch (e) {
      return null;
    }
  }

  function getBasePath() {
    var path = location.pathname || "/";
    if (/\.html$/i.test(path)) {
      path = path.slice(0, path.lastIndexOf("/") + 1);
    } else if (!path.endsWith("/")) {
      path = path + "/";
    }
    if (/\/(privacy|support|release-notes)\/$/.test(path)) {
      return path.replace(/\/(privacy|support|release-notes)\/$/, "/");
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

  function fillHeroFeatures(id, items) {
    var ul = document.getElementById(id);
    if (!ul || !items) return;
    ul.innerHTML = items.map(function (item) {
      if (typeof item === "string") return "<li>" + escapeHtml(item) + "</li>";
      return "<li><strong>" + escapeHtml(item.label) + "</strong>: " + escapeHtml(item.text) + "</li>";
    }).join("");
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

  function applyStoreLinks() {
    document.querySelectorAll("[data-store='true']").forEach(function (a) {
      a.setAttribute("href", STORE_URL);
    });
  }

  function applyDocumentDirection(lang) {
    var entry = LANG_BY_CODE[lang];
    var rtl = entry && entry.rtl;
    document.documentElement.dir = rtl ? "rtl" : "ltr";
    document.documentElement.classList.toggle("is-rtl", !!rtl);
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

  function buildLangMenu() {
    if (!pickerMenu) return;
    pickerMenu.innerHTML = LANG_REGISTRY.map(function (entry) {
      return (
        '<li role="option" data-lang="' + escapeHtml(entry.code) + '" aria-selected="false">' +
        '<span class="lang-option-code">' + escapeHtml(entry.short) + "</span>" +
        '<span class="lang-option-name">' + escapeHtml(entry.label) + "</span>" +
        "</li>"
      );
    }).join("");
  }

  function updateLangPicker(lang) {
    var entry = LANG_BY_CODE[lang];
    if (pickerLabel && entry) pickerLabel.textContent = entry.label;
    if (!pickerMenu) return;
    pickerMenu.querySelectorAll("[data-lang]").forEach(function (item) {
      var selected = item.getAttribute("data-lang") === lang;
      item.setAttribute("aria-selected", selected ? "true" : "false");
    });
  }

  function getPageSectionKey() {
    var page = document.body && document.body.getAttribute("data-page");
    if (page === "support") return "supportPage";
    if (page === "release-notes") return "releaseNotesPage";
    if (page === "privacy") return "privacyPage";
    return null;
  }

  function updatePageSeo(langCode, t, historyMode) {
    if (t) {
      document.documentElement.lang = (t.meta && t.meta.lang) || langCode;
      var pageKey = getPageSectionKey();
      var pageSection = pageKey ? t[pageKey] : null;
      if (pageSection && pageSection.metaTitle) {
        document.title = pageSection.metaTitle;
      } else if (t.meta && t.meta.title) {
        document.title = t.meta.title;
      }
      var desc = document.querySelector('meta[name="description"]');
      if (desc && t.meta && t.meta.description && !pageKey) {
        desc.setAttribute("content", t.meta.description);
      }
    }

    if (!historyMode) return;

    var newUrl =
      window.location.protocol +
      "//" +
      window.location.host +
      window.location.pathname +
      "?lang=" +
      encodeURIComponent(langCode);

    if (historyMode === "replace") {
      window.history.replaceState({ path: newUrl, lang: langCode }, "", newUrl);
    } else if (historyMode === "push") {
      window.history.pushState({ path: newUrl, lang: langCode }, "", newUrl);
    }
  }

  function apply(t, lang, historyMode) {
    if (!t) return;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var val = get(t, key);
      if (val != null) el.textContent = val;
    });
    fillList("problem-list", t.problem && t.problem.items);
    fillHeroFeatures("hero-features", t.hero && t.hero.features);
    setText("problem-solution", t.problem && t.problem.solution);
    fillCards("benefits-grid", t.benefits && t.benefits.items);
    fillCards("features-grid", t.features && t.features.items);
    fillCards("usecases-grid", t.usecases && t.usecases.items);
    fillList("pricing-free-list", t.pricing && t.pricing.freeItems);
    fillList("pricing-pro-list", t.pricing && t.pricing.proItems);
    if (t.releaseNotesPage) {
      fillList("rn-3030-list", t.releaseNotesPage.v3030Items);
      fillList("rn-3029-list", t.releaseNotesPage.v3029Items);
    }
    var heroImg = document.getElementById("hero-screenshot");
    if (heroImg && t.hero && t.hero.screenshotAlt) heroImg.alt = t.hero.screenshotAlt;
    applyStoreLinks();
    applyDocumentDirection(lang);
    updateLangPicker(lang);
    updatePageSeo(lang, t, historyMode);
  }

  function load(lang) {
    var entry = LANG_BY_CODE[lang] || LANG_BY_CODE[FALLBACK];
    var url = getBasePath() + "i18n/" + entry.file + ".json";
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error("Failed to load " + url);
      return res.json();
    });
  }

  function setLang(lang, historyMode) {
    var resolved = resolveLang(lang);
    var history = historyMode !== undefined ? historyMode : "push";
    return load(resolved).then(function (t) {
      apply(t, resolved, history);
      closeLangMenu();
      try { localStorage.setItem(STORAGE_KEY, resolved); } catch (e) {}
    }).catch(function (err) {
      console.error(err);
      if (resolved !== FALLBACK) return setLang(FALLBACK, history);
    });
  }

  function initLangPicker() {
    pickerBtn = document.getElementById("lang-picker-btn");
    pickerMenu = document.getElementById("lang-picker-menu");
    pickerRoot = document.getElementById("lang-picker");
    pickerLabel = document.getElementById("lang-picker-label");
    if (!pickerBtn || !pickerMenu || !pickerRoot) return;

    buildLangMenu();

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

    window.addEventListener("popstate", function () {
      var urlLang = getLangFromUrl();
      if (urlLang) setLang(urlLang, null);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initLangPicker();
    applyStoreLinks();
    var urlLang = getLangFromUrl();
    var saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    setLang(urlLang || saved, "replace");
  });
})();
