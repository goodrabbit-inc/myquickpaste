(function () {
  "use strict";

  function prefersReducedMotion() {
    return (
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  }

  function initStickyHeader() {
    var header = document.getElementById("site-header");
    if (!header) {
      return;
    }
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function initReveal() {
    var nodes = document.querySelectorAll(".reveal");
    if (!nodes.length) {
      return;
    }
    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
      nodes.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    nodes.forEach(function (el) {
      io.observe(el);
    });
  }

  function initCarousel(root) {
    if (root.getAttribute("data-carousel-ready") === "1") {
      return;
    }
    root.setAttribute("data-carousel-ready", "1");
    var track = root.querySelector("[data-carousel-track]");
    var slides = Array.prototype.slice.call(
      root.querySelectorAll("[data-carousel-slide]")
    );
    var prev = root.querySelector("[data-carousel-prev]");
    var next = root.querySelector("[data-carousel-next]");
    var dotsWrap = root.querySelector("[data-carousel-dots]");
    if (!track || slides.length === 0) {
      return;
    }

    var index = Math.max(
      0,
      slides.findIndex(function (s) {
        return s.classList.contains("is-active");
      })
    );

    function syncDots() {
      if (!dotsWrap) {
        return;
      }
      dotsWrap.innerHTML = "";
      slides.forEach(function (_, i) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "shots-dot" + (i === index ? " is-active" : "");
        btn.setAttribute("role", "tab");
        btn.setAttribute("aria-selected", i === index ? "true" : "false");
        btn.setAttribute("aria-label", "Screenshot " + (i + 1));
        btn.addEventListener("click", function () {
          go(i);
        });
        dotsWrap.appendChild(btn);
      });
    }

    function go(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (slide, si) {
        slide.classList.toggle("is-active", si === index);
      });
      var target = slides[index];
      if (target && typeof target.scrollIntoView === "function") {
        target.scrollIntoView({
          behavior: prefersReducedMotion() ? "auto" : "smooth",
          inline: "center",
          block: "nearest",
        });
      }
      syncDots();
    }

    if (prev) {
      prev.addEventListener("click", function () {
        go(index - 1);
      });
    }
    if (next) {
      next.addEventListener("click", function () {
        go(index + 1);
      });
    }

    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(index - 1);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        go(index + 1);
      }
    });

    var scrollTimer = null;
    track.addEventListener(
      "scroll",
      function () {
        if (scrollTimer) {
          clearTimeout(scrollTimer);
        }
        scrollTimer = setTimeout(function () {
          var center = track.scrollLeft + track.clientWidth / 2;
          var best = 0;
          var bestDist = Infinity;
          slides.forEach(function (slide, i) {
            var mid = slide.offsetLeft + slide.offsetWidth / 2;
            var dist = Math.abs(mid - center);
            if (dist < bestDist) {
              bestDist = dist;
              best = i;
            }
          });
          if (best !== index) {
            index = best;
            slides.forEach(function (slide, si) {
              slide.classList.toggle("is-active", si === index);
            });
            syncDots();
          }
        }, 80);
      },
      { passive: true }
    );

    syncDots();
  }

  function initCarousels() {
    document.querySelectorAll("[data-carousel]").forEach(initCarousel);
  }

  function init() {
    initStickyHeader();
    initReveal();
    initCarousels();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  document.addEventListener("mqp:i18n-ready", function () {
    initReveal();
    initCarousels();
  });
})();
