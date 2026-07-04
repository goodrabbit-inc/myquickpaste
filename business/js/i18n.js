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
    return fetch("i18n/" + lang + ".json?v=13")
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

  function renderSteps(container, items) {
    if (!Array.isArray(items)) {
      return;
    }
    container.innerHTML = items
      .map(function (item, index) {
        return (
          '<article class="step">' +
          '<div class="step-num" aria-hidden="true">' +
          (index + 1) +
          "</div>" +
          "<div>" +
          "<h3>" +
          escapeHtml(item.title) +
          "</h3>" +
          "<p>" +
          escapeHtml(item.text) +
          "</p>" +
          "</div>" +
          "</article>"
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
    if (!toggle || !panel) {
      return;
    }
    toggle.addEventListener("click", function () {
      var open = panel.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        panel.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("click", function (e) {
      if (!panel.contains(e.target) && !toggle.contains(e.target)) {
        panel.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
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
