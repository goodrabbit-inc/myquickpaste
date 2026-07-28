(function () {
  "use strict";

  var SUPPORTED = [
    "ja", "en", "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es",
    "pt", "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv"
  ];
  var DEFAULT_LANG = "ja";
  var STORAGE_KEY = "mqp-business-lang";
  var MAIN_STORAGE_KEY = "mqp-lang";
  var RTL_LANGS = ["ar"];

  var LANG_NAMES = {
    ja: "\u65e5\u672c\u8a9e",
    en: "English",
    fr: "Fran\u00e7ais",
    de: "Deutsch",
    zh: "\u4e2d\u6587\uff08\u7b80\u4f53\uff09",
    zh_TW: "\u4e2d\u6587\uff08\u7e41\u9ad4\uff09",
    ko: "\ud55c\uad6d\uc5b4",
    ru: "\u0420\u0443\u0441\u0441\u043a\u0438\u0439",
    it: "Italiano",
    es: "Espa\u00f1ol",
    pt: "Portugu\u00eas",
    hi: "\u0939\u093f\u0928\u094d\u0926\u0940",
    ar: "\u0627\u0644\u0639\u0631\u0628\u064a\u0629",
    id: "Bahasa Indonesia",
    th: "\u0e44\u0e17\u0e22",
    vi: "Ti\u1ebfng Vi\u1ec7t",
    tr: "T\u00fcrk\u00e7e",
    uk: "\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430",
    nl: "Nederlands",
    pl: "Polski",
    sv: "Svenska"
  };

  var LANG_ALIASES = {
    "zh-cn": "zh",
    "zh-hans": "zh",
    "zh-sg": "zh",
    "zh-my": "zh",
    "zh-tw": "zh_TW",
    "zh-hant": "zh_TW",
    "zh-hk": "zh_TW",
    "zh-mo": "zh_TW",
    "pt-br": "pt",
    "pt-pt": "pt",
    "en-us": "en",
    "en-gb": "en"
  };

  function normalizeLangCode(raw) {
    if (!raw) {
      return "";
    }
    var normalized = String(raw).trim().toLowerCase().replace(/_/g, "-");
    if (LANG_ALIASES[normalized]) {
      return LANG_ALIASES[normalized];
    }
    if (normalized.indexOf("-") !== -1) {
      var base = normalized.split("-")[0];
      if (LANG_ALIASES[base]) {
        return LANG_ALIASES[base];
      }
      return base;
    }
    return normalized;
  }

  function resolveSupported(rawCode) {
    var normalized = normalizeLangCode(rawCode);
    if (SUPPORTED.indexOf(normalized) !== -1) {
      return normalized;
    }
    var lower = normalized.toLowerCase();
    for (var i = 0; i < SUPPORTED.length; i++) {
      if (SUPPORTED[i].toLowerCase() === lower) {
        return SUPPORTED[i];
      }
    }
    return null;
  }

  function mapMainSiteLang(raw) {
    if (!raw) {
      return null;
    }
    return resolveSupported(raw);
  }

  function getNested(obj, path) {
    return path.split(".").reduce(function (o, key) {
      return o && o[key] != null ? o[key] : undefined;
    }, obj);
  }

  function detectLang() {
    var params = new URLSearchParams(window.location.search);
    var fromQuery = resolveSupported(params.get("lang"));
    if (fromQuery) {
      return fromQuery;
    }
    try {
      var mainStored = localStorage.getItem(MAIN_STORAGE_KEY);
      var mappedMain = mapMainSiteLang(mainStored);
      if (mappedMain) {
        return mappedMain;
      }
      var stored = resolveSupported(localStorage.getItem(STORAGE_KEY));
      if (stored) {
        return stored;
      }
    } catch (e) {
      /* ignore */
    }
    var browser = resolveSupported(navigator.language || navigator.userLanguage || "");
    if (browser) {
      return browser;
    }
    return DEFAULT_LANG;
  }

  function setLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
      localStorage.setItem(MAIN_STORAGE_KEY, lang);
    } catch (e) {
      /* ignore */
    }
  }

  function loadMessages(lang) {
    return fetch("i18n/" + lang + ".json?v=19")
      .then(function (res) {
        if (!res.ok) {
          throw new Error("i18n load failed");
        }
        return res.json();
      });
  }

  function applyText(root, messages) {
    root.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var value = getNested(messages, key);
      if (value != null) {
        el.textContent = value;
      }
    });
  }

  function applyAttrs(root, messages) {
    root.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr")
        .split(";")
        .forEach(function (pair) {
          var parts = pair.split(":");
          if (parts.length < 2) {
            return;
          }
          var attr = parts[0].trim();
          var key = parts.slice(1).join(":").trim();
          var value = getNested(messages, key);
          if (value != null) {
            el.setAttribute(attr, value);
          }
        });
    });
  }

  function renderStringList(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item) {
        return "<li>" + escapeHtml(item) + "</li>";
      })
      .join("");
  }

  function padStep(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function stepIconSvg(index) {
    var icons = [
      '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
      '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
      '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>'
    ];
    return (
      '<svg class="step-icon" aria-hidden="true" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
      (icons[index] || icons[0]) +
      "</svg>"
    );
  }

  function renderSteps(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item, index) {
        return (
          '<article class="step-card step">' +
          '<div class="step-num" aria-hidden="true">' +
          padStep(index + 1) +
          "</div>" +
          stepIconSvg(index) +
          "<h3>" +
          escapeHtml(item.title) +
          "</h3>" +
          "<p>" +
          escapeHtml(item.text) +
          "</p>" +
          "</article>"
        );
      })
      .join("");
  }

  var SCENE_ICONS = {
    heart: '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>',
    camera: '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    tag: '<path d="M20.6 13.4 12.2 21.8a2 2 0 0 1-2.8 0L2 14.4V2h12.4z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    doc: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8M8 9h2"/>',
    mail: '<path d="M4 4h16v16H4z"/><path d="m22 6-10 7L2 6"/>',
    phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.6a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.5-1.1a2 2 0 0 1 2.1-.4c.9.3 1.8.5 2.7.6a2 2 0 0 1 1.6 2z"/>',
    zap: '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    home: '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    user: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    note: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>'
  };

  var FEATURE_ICONS = {
    tap: '<path d="M9 11V6a2 2 0 1 1 4 0v5"/><path d="M13 11V4a2 2 0 1 1 4 0v8"/><path d="M17 12v-1a2 2 0 1 1 4 0v5a8 8 0 0 1-8 8h-2a8 8 0 0 1-7.3-4.7L3 14a2 2 0 0 1 3.4-2L9 15"/>',
    folder: '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    sort: '<path d="m3 16 4 4 4-4M7 20V4M21 8l-4-4-4 4M17 4v16"/>',
    card: '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    image: '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/>',
    backup: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    theme: '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/>',
    lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
  };

  function iconSvg(map, key) {
    return (
      '<svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
      (map[key] || map.tap || "") +
      "</svg>"
    );
  }

  function renderScenePoints(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item) {
        return (
          '<article class="scene-point">' +
          '<div class="scene-point-icon" aria-hidden="true">' +
          iconSvg(SCENE_ICONS, item.icon) +
          "</div>" +
          "<h4>" +
          escapeHtml(item.title) +
          "</h4>" +
          "<p>" +
          escapeHtml(item.text) +
          "</p>" +
          "</article>"
        );
      })
      .join("");
  }

  function renderFeaturesBento(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item) {
        var large = item.large ? " is-large" : "";
        return (
          '<article class="feature-card' +
          large +
          '">' +
          '<div class="feature-icon" aria-hidden="true">' +
          iconSvg(FEATURE_ICONS, item.icon) +
          "</div>" +
          "<h3>" +
          escapeHtml(item.title) +
          "</h3>" +
          "<p>" +
          escapeHtml(item.text) +
          "</p>" +
          "</article>"
        );
      })
      .join("");
  }

  function renderFaqDetails(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item) {
        return (
          '<details class="faq-item">' +
          "<summary>" +
          escapeHtml(item.q) +
          "</summary>" +
          '<div class="faq-a"><p>' +
          escapeHtml(item.a) +
          "</p></div>" +
          "</details>"
        );
      })
      .join("");
  }

  function renderIconCards(container, items, extraClass) {
    if (!Array.isArray(items)) {
      return;
    }
    var cls = "cards" + (extraClass ? " " + extraClass : "");
    container.className = cls;
    container.innerHTML = items
      .map(function (item) {
        return (
          '<article class="card">' +
          '<div class="card-icon" aria-hidden="true">' +
          escapeHtml(item.icon || "") +
          "</div>" +
          "<h3>" +
          escapeHtml(item.title) +
          "</h3>" +
          "<p>" +
          escapeHtml(item.text) +
          "</p>" +
          "</article>"
        );
      })
      .join("");
  }

  function renderPlainCards(container, items, extraClass) {
    if (!Array.isArray(items)) {
      return;
    }
    var cls = "cards" + (extraClass ? " " + extraClass : "");
    container.className = cls;
    container.innerHTML = items
      .map(function (item) {
        return (
          '<article class="card">' +
          "<h3>" +
          escapeHtml(item.title) +
          "</h3>" +
          "<p>" +
          escapeHtml(item.text) +
          "</p>" +
          "</article>"
        );
      })
      .join("");
  }

  function renderChips(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item, index) {
        return (
          '<span class="chip chip-' +
          (index % 6) +
          '">' +
          escapeHtml(item) +
          "</span>"
        );
      })
      .join("");
  }

  function renderFaq(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item) {
        return (
          '<article class="faq-item">' +
          "<h3>" +
          escapeHtml(item.q) +
          "</h3>" +
          "<p>" +
          escapeHtml(item.a) +
          "</p>" +
          "</article>"
        );
      })
      .join("");
  }

  function renderSections(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item) {
        return (
          "<section>" +
          "<h2>" +
          escapeHtml(item.h) +
          "</h2>" +
          "<p>" +
          escapeHtml(item.p) +
          "</p>" +
          "</section>"
        );
      })
      .join("");
  }

  function renderReleases(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (entry) {
        var list = (entry.items || [])
          .map(function (line) {
            return "<li>" + escapeHtml(line) + "</li>";
          })
          .join("");
        return (
          '<article class="release-card">' +
          "<h2>v" +
          escapeHtml(entry.version) +
          " — " +
          escapeHtml(entry.title) +
          "</h2>" +
          '<p class="release-date">' +
          escapeHtml(entry.date) +
          "</p>" +
          "<ul>" +
          list +
          "</ul>" +
          "</article>"
        );
      })
      .join("");
  }

  function renderDynamicLists(root, messages) {
    root.querySelectorAll("[data-i18n-list]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-list");
      renderStringList(el, getNested(messages, key));
    });

    root.querySelectorAll("[data-i18n-steps]").forEach(function (el) {
      renderSteps(el, getNested(messages, el.getAttribute("data-i18n-steps")));
    });

    root.querySelectorAll("[data-i18n-benefits]").forEach(function (el) {
      renderIconCards(
        el,
        getNested(messages, el.getAttribute("data-i18n-benefits")),
        "cards-3"
      );
    });

    root.querySelectorAll("[data-i18n-features]").forEach(function (el) {
      renderIconCards(
        el,
        getNested(messages, el.getAttribute("data-i18n-features")),
        "cards-2"
      );
    });

    root.querySelectorAll("[data-i18n-usecases]").forEach(function (el) {
      renderPlainCards(
        el,
        getNested(messages, el.getAttribute("data-i18n-usecases")),
        "cards-3"
      );
    });

    root.querySelectorAll("[data-i18n-chips]").forEach(function (el) {
      renderChips(el, getNested(messages, el.getAttribute("data-i18n-chips")));
    });

    root.querySelectorAll("[data-i18n-faq]").forEach(function (el) {
      renderFaq(el, getNested(messages, el.getAttribute("data-i18n-faq")));
    });

    root.querySelectorAll("[data-i18n-faq-details]").forEach(function (el) {
      renderFaqDetails(
        el,
        getNested(messages, el.getAttribute("data-i18n-faq-details"))
      );
    });

    root.querySelectorAll("[data-i18n-scene-points]").forEach(function (el) {
      renderScenePoints(
        el,
        getNested(messages, el.getAttribute("data-i18n-scene-points"))
      );
    });

    root.querySelectorAll("[data-i18n-features-bento]").forEach(function (el) {
      renderFeaturesBento(
        el,
        getNested(messages, el.getAttribute("data-i18n-features-bento"))
      );
    });

    root.querySelectorAll("[data-i18n-sections]").forEach(function (el) {
      renderSections(el, getNested(messages, el.getAttribute("data-i18n-sections")));
    });

    root.querySelectorAll("[data-i18n-releases]").forEach(function (el) {
      renderReleases(el, getNested(messages, el.getAttribute("data-i18n-releases")));
    });

    root.querySelectorAll("[data-i18n-pricing-list]").forEach(function (el) {
      renderStringList(el, getNested(messages, el.getAttribute("data-i18n-pricing-list")));
    });
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function updateLangPicker(lang, messages) {
    var btn = document.getElementById("lang-picker-btn");
    var menu = document.getElementById("lang-picker-menu");
    if (!btn || !menu) {
      return;
    }
    var langLabel = getNested(messages, "lang.label") || "Language";
    var langName = LANG_NAMES[lang] || lang;
    btn.setAttribute("aria-label", langLabel + ": " + langName);
    btn.querySelector(".lang-current").textContent = langName;
    menu.querySelectorAll("li").forEach(function (li) {
      var liLang = li.getAttribute("data-lang");
      if (LANG_NAMES[liLang]) {
        li.textContent = LANG_NAMES[liLang];
      }
      li.setAttribute("aria-selected", liLang === lang ? "true" : "false");
    });
  }

  function initNavToggle() {
    var toggle = document.getElementById("nav-toggle");
    var panel = document.getElementById("nav-panel");
    if (!toggle || !panel || toggle.getAttribute("data-nav-ready") === "1") {
      return;
    }
    toggle.setAttribute("data-nav-ready", "1");

    function setOpen(open) {
      panel.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("nav-open", open);
    }

    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      setOpen(!panel.classList.contains("is-open"));
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });
    document.addEventListener("click", function (e) {
      if (!panel.contains(e.target) && !toggle.contains(e.target)) {
        setOpen(false);
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        setOpen(false);
        var menu = document.getElementById("lang-picker-menu");
        var btn = document.getElementById("lang-picker-btn");
        if (menu && !menu.hasAttribute("hidden")) {
          menu.setAttribute("hidden", "");
          if (btn) {
            btn.setAttribute("aria-expanded", "false");
          }
        }
      }
    });
  }

  function updateUrlLang(lang) {
    try {
      var url = new URL(window.location.href);
      url.searchParams.set("lang", lang);
      window.history.replaceState({}, "", url.pathname + url.search + url.hash);
    } catch (e) {
      /* ignore */
    }
  }

  function initLangPicker(langState, applyFn) {
    var btn = document.getElementById("lang-picker-btn");
    var menu = document.getElementById("lang-picker-menu");
    if (!btn || !menu) {
      return;
    }
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var hidden = menu.hasAttribute("hidden");
      if (hidden) {
        menu.removeAttribute("hidden");
        btn.setAttribute("aria-expanded", "true");
      } else {
        menu.setAttribute("hidden", "");
        btn.setAttribute("aria-expanded", "false");
      }
    });
    menu.querySelectorAll("li").forEach(function (li) {
      li.addEventListener("click", function (e) {
        e.stopPropagation();
        var lang = li.getAttribute("data-lang");
        if (lang && lang !== langState.lang) {
          langState.lang = lang;
          setLang(lang);
          updateUrlLang(lang);
          applyFn(lang);
        }
        menu.setAttribute("hidden", "");
        btn.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("click", function () {
      menu.setAttribute("hidden", "");
      btn.setAttribute("aria-expanded", "false");
    });
  }

  function markActiveNav() {
    var page = document.body.getAttribute("data-page");
    if (!page) {
      return;
    }
    document.querySelectorAll(".nav a[data-nav]").forEach(function (link) {
      link.classList.toggle("is-active", link.getAttribute("data-nav") === page);
    });
  }

  function applyMessages(lang) {
    return loadMessages(lang)
      .catch(function () {
        if (lang !== DEFAULT_LANG) {
          return loadMessages(DEFAULT_LANG);
        }
        throw new Error("No i18n fallback");
      })
      .then(function (messages) {
        document.documentElement.lang = messages.meta && messages.meta.lang ? messages.meta.lang : lang;
        document.documentElement.dir = RTL_LANGS.indexOf(lang) !== -1 ? "rtl" : "ltr";
        if (messages.meta && messages.meta.title) {
          document.title = messages.meta.title;
        }
        applyText(document, messages);
        applyAttrs(document, messages);
        renderDynamicLists(document, messages);
        updateLangPicker(lang, messages);
        markActiveNav();
        if (typeof window.mqpApplyStoreBadges === "function") {
          window.mqpApplyStoreBadges(lang, messages);
        }
        if (typeof window.mqpApplyScreenshots === "function") {
          window.mqpApplyScreenshots(lang, messages);
        }
        document.dispatchEvent(
          new CustomEvent("mqp:i18n-ready", { detail: { lang: lang, messages: messages } })
        );
        return messages;
      });
  }

  function initSite() {
    initNavToggle();
    markActiveNav();
    var langState = { lang: detectLang() };
    initLangPicker(langState, function (newLang) {
      applyMessages(newLang);
    });
    updateUrlLang(langState.lang);
    applyMessages(langState.lang);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSite);
  } else {
    initSite();
  }
})();
