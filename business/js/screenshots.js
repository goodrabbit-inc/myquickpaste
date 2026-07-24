(function () {
  "use strict";

  var PHONE_TYPES = ["freetext", "snippets", "images", "profile", "profile-edit"];
  var FALLBACK_LANG = "en";
  var DEFAULT_CATE = "images/ss-cate.png";
  var CACHE_BUST = "20260725";

  function setImgSrc(img, candidates) {
    var idx = 0;
    function tryNext() {
      if (idx >= candidates.length) {
        return;
      }
      var path = candidates[idx];
      idx += 1;
      img.onerror = function () {
        img.onerror = null;
        tryNext();
      };
      img.src = path;
    }
    tryNext();
  }

  function phoneCandidates(type, lang) {
    var q = "?v=" + encodeURIComponent(CACHE_BUST + "-" + lang);
    return [
      "images/ss-" + type + "-" + lang + ".png" + q,
      "images/ss-" + type + "-" + FALLBACK_LANG + ".png" + q,
      "images/ss-" + type + ".png" + q
    ];
  }

  function cateCandidates(lang) {
    var q = "?v=" + encodeURIComponent(CACHE_BUST + "-" + lang);
    return [
      "images/ss-cate-" + lang + ".png" + q,
      "images/ss-cate-" + FALLBACK_LANG + ".png" + q,
      DEFAULT_CATE + q
    ];
  }

  function applyScreenshots(lang) {
    if (!lang) {
      lang = "ja";
    }
    document.querySelectorAll("[data-shot-img]").forEach(function (img) {
      var type = img.getAttribute("data-shot-img");
      if (PHONE_TYPES.indexOf(type) !== -1) {
        setImgSrc(img, phoneCandidates(type, lang));
      } else if (type === "cate") {
        setImgSrc(img, cateCandidates(lang));
      }
    });
  }

  window.mqpApplyScreenshots = applyScreenshots;

  document.addEventListener("mqp:i18n-ready", function (e) {
    var detail = e.detail || {};
    applyScreenshots(detail.lang || "ja");
  });
})();
