(function () {
  "use strict";

  var GOOGLE_PLAY_URL =
    "https://play.google.com/store/apps/details?id=com.goodrabbit.clipee";
  var MICROSOFT_STORE_URL =
    "https://apps.microsoft.com/detail/9N8WHWKDDSKK";

  var BADGES = {
    "google-play": {
      ja: "images/badges/google-play-ja.png",
      en: "images/badges/google-play-en.png",
      width: 155,
      height: 60,
      soon: true,
    },
    "app-store": {
      ja: "images/badges/app-store-ja.svg",
      en: "images/badges/app-store-en.svg",
      width: 120,
      height: 40,
      soon: true,
    },
    microsoft: {
      ja: "images/badges/ms-store-ja.svg",
      en: "images/badges/ms-store-en.svg",
      width: 161,
      height: 44,
      url: MICROSOFT_STORE_URL,
    },
  };

  function assetRoot() {
    var icon = document.querySelector('link[rel="icon"][href*="images/"]');
    if (icon && icon.href) {
      return icon.href.replace(/images\/[^/]*$/, "");
    }
    var path = window.location.pathname.replace(/[^/]*$/, "");
    return window.location.origin + path;
  }

  function resolveAsset(relativePath) {
    return assetRoot() + relativePath.replace(/^\//, "");
  }

  function badgeLang(lang) {
    return lang === "ja" ? "ja" : "en";
  }

  function getMessage(messages, path) {
    return path.split(".").reduce(function (o, key) {
      return o && o[key] != null ? o[key] : undefined;
    }, messages);
  }

  function applyBadges(lang, messages) {
    var bl = badgeLang(lang);
    document.querySelectorAll("[data-badge-img]").forEach(function (img) {
      var key = img.getAttribute("data-badge-img");
      var spec = BADGES[key];
      if (!spec) {
        return;
      }
      img.src = resolveAsset(spec[bl]);
      img.width = spec.width;
      img.height = spec.height;
      var altKeys = {
        "google-play": "stores.googlePlayBadgeAlt",
        "app-store": "stores.appStoreBadgeAlt",
        microsoft: "stores.microsoftBadgeAlt",
      };
      var alt = getMessage(messages, altKeys[key]);
      if (alt) {
        img.alt = alt;
      }
    });

    document.querySelectorAll("[data-badge-link]").forEach(function (el) {
      var key = el.getAttribute("data-badge-link");
      var spec = BADGES[key];
      if (!spec || spec.soon) {
        return;
      }
      if (spec.url) {
        el.href = spec.url;
      }
    });
  }

  window.mqpApplyStoreBadges = applyBadges;

  document.addEventListener("mqp:i18n-ready", function (e) {
    var detail = e.detail || {};
    applyBadges(detail.lang || "ja", detail.messages || {});
  });

  applyBadges(document.documentElement.lang || "ja", {});
})();
