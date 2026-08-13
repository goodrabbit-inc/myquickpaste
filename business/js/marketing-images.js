(function () {
  "use strict";

  /**
   * Locale → marketing image set (single source of truth).
   * Feature: one PNG per i18n locale code.
   * Use cases: ja | en sets; all other locales fall back to en.
   */
  var CACHE_BUST = "20260813a";

  var FEATURE_LOCALE = {
    en: "en",
    ja: "ja",
    fr: "fr",
    de: "de",
    zh: "zh",
    zh_TW: "zh_TW",
    ko: "ko",
    ru: "ru",
    it: "it",
    es: "es",
    pt: "pt",
    hi: "hi",
    ar: "ar",
    id: "id",
    th: "th",
    vi: "vi",
    tr: "tr",
    uk: "uk",
    nl: "nl",
    pl: "pl",
    sv: "sv",
  };

  var USECASE_SET_BY_LOCALE = {
    ja: "ja",
    en: "en",
  };

  var USECASE_FALLBACK_SET = "en";

  var ALT = {
    feature: {
      en: "MyQuickPaste feature graphic",
      ja: "MyQuickPaste フィーチャーグラフィック",
      default: "MyQuickPaste feature graphic",
    },
    usecase: [
      { en: "MyQuickPaste travel use case", ja: "MyQuickPaste 旅行の利用シーン" },
      { en: "MyQuickPaste airport lounge use case", ja: "MyQuickPaste 空港ラウンジの利用シーン" },
      { en: "MyQuickPaste marketplace use case", ja: "MyQuickPaste フリマの利用シーン" },
      { en: "MyQuickPaste chat use case", ja: "MyQuickPaste チャットの利用シーン" },
      { en: "MyQuickPaste social media use case", ja: "MyQuickPaste SNSの利用シーン" },
      { en: "MyQuickPaste event organizer use case", ja: "MyQuickPaste 幹事の利用シーン" },
      { en: "MyQuickPaste usage guide", ja: "MyQuickPaste 使い方ガイド" },
    ],
  };

  function resolveFeatureLocale(lang) {
    return FEATURE_LOCALE[lang] || "en";
  }

  function resolveUsecaseSet(lang) {
    return USECASE_SET_BY_LOCALE[lang] || USECASE_FALLBACK_SET;
  }

  function featurePath(lang) {
    var loc = resolveFeatureLocale(lang);
    return (
      "images/marketing/feature-" +
      loc +
      ".png?v=" +
      encodeURIComponent(CACHE_BUST + "-" + loc)
    );
  }

  function usecasePath(lang, index) {
    var set = resolveUsecaseSet(lang);
    var n = String(index).padStart(2, "0");
    return (
      "images/marketing/usecase-" +
      set +
      "-" +
      n +
      ".png?v=" +
      encodeURIComponent(CACHE_BUST + "-" + set + "-" + n)
    );
  }

  function altForFeature(lang) {
    if (ALT.feature[lang]) {
      return ALT.feature[lang];
    }
    return ALT.feature.default;
  }

  function altForUsecase(lang, index) {
    var entry = ALT.usecase[index - 1];
    if (!entry) {
      return "MyQuickPaste use case";
    }
    if (entry[lang]) {
      return entry[lang];
    }
    return entry.en;
  }

  function applyMarketingImages(lang) {
    if (!lang) {
      lang = "ja";
    }

    document.querySelectorAll('[data-marketing-img="feature"]').forEach(function (img) {
      img.src = featurePath(lang);
      img.alt = altForFeature(lang);
    });

    document.querySelectorAll('[data-marketing-img="usecase"]').forEach(function (img) {
      var raw = img.getAttribute("data-usecase-index");
      var index = parseInt(raw, 10);
      if (!index || index < 1 || index > 7) {
        return;
      }
      img.src = usecasePath(lang, index);
      img.alt = altForUsecase(lang, index);
    });
  }

  window.mqpMarketingImages = {
    resolveFeatureLocale: resolveFeatureLocale,
    resolveUsecaseSet: resolveUsecaseSet,
    featurePath: featurePath,
    usecasePath: usecasePath,
    apply: applyMarketingImages,
  };

  window.mqpApplyMarketingImages = applyMarketingImages;

  document.addEventListener("mqp:i18n-ready", function (e) {
    var detail = e.detail || {};
    applyMarketingImages(detail.lang || "ja");
  });
})();
