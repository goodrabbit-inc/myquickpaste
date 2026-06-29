(function () {
  "use strict";

  var SUPPORTED = ["ja", "en"];
  var DEFAULT_LANG = "ja";
  var STORAGE_KEY = "mqp-business-lang";

  function getNested(obj, path) {
    return path.split(".").reduce(function (o, key) {
      return o && o[key] != null ? o[key] : undefined;
    }, obj);
  }

  function detectLang() {
    var params = new URLSearchParams(window.location.search);
    var fromQuery = params.get("lang");
    if (fromQuery && SUPPORTED.indexOf(fromQuery) !== -1) {
      return fromQuery;
    }
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored && SUPPORTED.indexOf(stored) !== -1) {
        return stored;
      }
    } catch (e) {
      /* ignore */
    }
    var browser = (navigator.language || navigator.userLanguage || "").slice(0, 2).toLowerCase();
    if (SUPPORTED.indexOf(browser) !== -1) {
      return browser;
    }
    return DEFAULT_LANG;
  }

  function setLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* ignore */
    }
  }

  function loadMessages(lang) {
    return fetch("i18n/" + lang + ".json")
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
    var labels = { ja: "日本語", en: "English" };
    btn.setAttribute("aria-label", getNested(messages, "lang.label") || "Language");
    btn.querySelector(".lang-current").textContent = labels[lang] || lang;
    menu.querySelectorAll("li").forEach(function (li) {
      var liLang = li.getAttribute("data-lang");
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
        if (messages.meta && messages.meta.title) {
          document.title = messages.meta.title;
        }
        applyText(document, messages);
        applyAttrs(document, messages);
        renderDynamicLists(document, messages);
        updateLangPicker(lang, messages);
        markActiveNav();
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
