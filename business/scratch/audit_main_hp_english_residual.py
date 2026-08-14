#!/usr/bin/env python3
"""Audit English-like strings on main HP i18n keys only. Read-only — does not modify i18n."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BUSINESS = Path(__file__).resolve().parent.parent
I18N_DIR = BUSINESS / "i18n"
INDEX = BUSINESS / "index.html"
JS_FILES = [
    BUSINESS / "js" / "i18n.js",
    BUSINESS / "js" / "site.js",
    BUSINESS / "js" / "marketing-images.js",
    BUSINESS / "js" / "screenshots.js",
    BUSINESS / "js" / "stores.js",
]
OUT_AUDIT = Path(__file__).resolve().parent / "main_hp_english_residual_audit.json"
OUT_C = Path(__file__).resolve().parent / "main_hp_untranslated_candidates.json"

LANGS = [
    "en", "ja", "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]
NON_EN = [x for x in LANGS if x != "en"]

BRAND_SECTIONS = [
    "hero", "trust", "pain", "steps", "sceneSocial", "sceneWork", "sceneDaily",
    "sceneMore", "screenshots", "features", "comparison", "themesSection",
    "privacySection", "pricing", "faq", "windowsEdition", "cta", "footer",
]

# Exact string or entire-value whitelist → A
EXACT_A = {
    "MyQuickPaste", "Pro", "FAQ", "URL", "JSON", "SNS", "UI", "¥0", "$0", "0",
    "Copyright © 2025–2026 Good Rabbit inc., Japan. All rights reserved.",
    "Contact", "Support", "Privacy", "Home", "Features", "Pricing", "Screens",
}

# Token whitelist (product / service / tech) — presence alone does not force C
TOKEN_A = {
    "myquickpaste", "pro", "google", "play", "app", "store", "microsoft", "windows",
    "url", "faq", "json", "sns", "ui", "pc", "android", "ios", "iphone", "line",
    "good", "rabbit", "inc", "japan", "copyright", "kazuhiro", "suda", "hotmail",
    "com", "all", "rights", "reserved", "billing", "jpeg", "png", "webp", "gif",
}

# Internal icon ids — excluded from audit
ICON_IDS = {
    "tap", "folder", "sort", "card", "image", "backup", "theme", "lock",
    "heart", "camera", "tag", "clock", "doc", "mail", "phone", "zap", "home",
    "user", "note", "search",
}

# Ambiguous English loanwords → B when they dominate untranslated tokens
TOKEN_B = {
    "ui", "theme", "themes", "backup", "profile", "social", "chat", "smartphone",
    "premium", "store", "free", "trial", "simple", "features", "pricing", "screens",
    "support", "contact", "privacy", "home", "search", "reorder", "quick", "save",
    "copy", "paste", "clipboard", "cloud", "device", "data", "export", "import",
    "light", "dark", "one", "time", "purchase", "subscription", "monthly", "fee",
}


def file_hashes() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted(I18N_DIR.glob("*.json")):
        out[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def flatten(obj: Any, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            out.update(flatten(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, f"{prefix}[{i}]"))
    elif isinstance(obj, (str, int, float, bool)):
        out[prefix] = str(obj)
    return out


def collect_static_keys() -> set[str]:
    keys: set[str] = set()
    text = INDEX.read_text(encoding="utf-8")
    keys.update(re.findall(r'data-i18n="([^"]+)"', text))
    for m in re.finditer(r'data-i18n-attr="[^:"]+:([^"]+)"', text):
        keys.add(m.group(1))
    # Dynamic list roots on index.html
    for attr in (
        "data-i18n-steps", "data-i18n-scene-points", "data-i18n-features-bento",
        "data-i18n-faq-details", "data-i18n-list", "data-i18n-pricing-list",
    ):
        keys.update(re.findall(rf'{attr}="([^"]+)"', text))
    # JS-only keys used on main HP
    keys.add("meta.title")
    keys.add("lang.label")
    return keys


def expand_dynamic_keys(ja_flat: dict[str, str], roots: set[str]) -> set[str]:
    expanded: set[str] = set()
    for root in roots:
        if root in ja_flat:
            expanded.add(root)
            continue
        prefix = root + "."
        prefix_br = root + "["
        for k in ja_flat:
            if k == root or k.startswith(prefix) or k.startswith(prefix_br):
                if k.endswith(".icon") or re.search(r"\.icon$", k):
                    continue
                if k.endswith(".large"):
                    continue
                expanded.add(k)
    return expanded


def is_icon_key(key: str) -> bool:
    if key.endswith(".icon"):
        return True
    m = re.search(r"\.points\[\d+\]\.icon$|\.items\[\d+\]\.icon$", key)
    return bool(m)


def latin_tokens(s: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Za-z]{2,}", s)]


def non_whitelisted_tokens(s: str) -> list[str]:
    return [t for t in latin_tokens(s) if t not in TOKEN_A and t not in ICON_IDS]


def is_primarily_english(s: str) -> bool:
    tokens = non_whitelisted_tokens(s)
    if not tokens:
        return False
    # Mostly ASCII words
    ascii_chars = sum(1 for c in s if ord(c) < 128 and c.isalpha())
    non_ascii_alpha = sum(1 for c in s if ord(c) >= 128 and c.isalpha())
    if non_ascii_alpha == 0 and len(tokens) >= 1:
        return True
    if ascii_chars and non_ascii_alpha:
        return len(tokens) >= 2 and ascii_chars > non_ascii_alpha * 2
    return False


A_KEYS = {
    "brand.name", "pain.flowNewLabel", "comparison.appLabel",
    "pricing.proTitle", "pricing.freePrice", "footer.copyright", "lang.en",
}


def is_a_whitelist(key: str, value: str) -> tuple[bool, str]:
    if value in EXACT_A:
        return True, "固定の固有名詞・製品名・許容表記"
    if key in A_KEYS:
        return True, "製品名・価格表記・著作権・言語名（意図的）"
    if key == "windowsEdition.titleLine1" and value == "MyQuickPaste":
        return True, "製品名のみの見出し"
    if "Google Play" in value or "App Store" in value:
        rest = value.replace("Google Play", "").replace("App Store", "").strip(" ·/-")
        if not non_whitelisted_tokens(rest):
            return True, "ストア名を含む許容表記"
        if not is_primarily_english(rest):
            return True, "ストア名＋該当言語本文"
    if "MyQuickPaste" in value:
        rest = value.replace("MyQuickPaste", "").strip(" 、，,.")
        if not non_whitelisted_tokens(rest):
            return True, "MyQuickPaste を含む許容表記"
        if locale_ok_mixed(rest):
            return True, "MyQuickPaste＋該当言語本文"
    return False, ""


def locale_ok_mixed(rest: str) -> bool:
    """True if remainder is clearly non-English (has CJK, Arabic, Cyrillic, etc.)."""
    if re.search(r"[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af\u0600-\u06ff\u0400-\u04ff"
                 r"\u0900-\u097f\u0e00-\u0e7f\u0100-\u024f]", rest):
        return True
    if re.search(r"[àâäéèêëïîôùûüçœæ]", rest, re.I):
        return True
    return False


def classify(locale: str, key: str, value: str, en_value: str | None) -> tuple[str, str] | None:
    """Return (class, reason) or None if not English-like / not in scope."""
    if locale == "en":
        return None
    if is_icon_key(key):
        return None
    if value in ICON_IDS:
        return None

    ok, reason = is_a_whitelist(key, value)
    if ok:
        return "A", reason

    identical_en = en_value is not None and value == en_value
    tokens = non_whitelisted_tokens(value)
    if not tokens and not identical_en:
        return None

    # C: clearly untranslated — same as English master
    if identical_en:
        if len(tokens) == 0:
            return None
        short_loan = len(tokens) <= 2 and all(t in TOKEN_B or t in TOKEN_A for t in tokens)
        if short_loan:
            return "B", f"英語マスターと同一の短語（{', '.join(tokens)}）— 言語慣習要確認"
        return "C", "英語マスター（en.json）と同一の未翻訳文字列"

    # ja: English body embedded in otherwise Japanese UI
    if locale == "ja":
        if is_primarily_english(value):
            return "C", "日本語ページに英語本文が残存"
        if tokens and all(t in TOKEN_B for t in tokens):
            return "B", f"日本語文に英語借詞（{', '.join(tokens)}）"
        if tokens:
            return "B", f"日本語文に英語語句が混在（{', '.join(tokens[:5])}）"
        return None

    # Non-en, not identical to en: loanwords only → B (translated text is not C)
    if tokens and all(t in TOKEN_B for t in tokens):
        return "B", f"該当言語文に英語借詞（{', '.join(tokens)}）"
    if tokens:
        return "B", f"該当言語文に英語語句が混在（{', '.join(tokens[:5])}）"
    return None


def main() -> None:
    hashes_before = file_hashes()

    ja = json.loads((I18N_DIR / "ja.json").read_text(encoding="utf-8"))
    en = json.loads((I18N_DIR / "en.json").read_text(encoding="utf-8"))
    ja_flat = flatten(ja)
    en_flat = flatten(en)

    static = collect_static_keys()
    dynamic_roots = {
        k for k in static
        if any(k.endswith(s) for s in (
            ".items", ".points", "freeItems", "proItems",
        )) or k in (
            "steps.items", "sceneSocial.points", "sceneWork.points", "sceneDaily.points",
            "features.items", "faq.items", "privacySection.points",
            "pricing.freeItems", "pricing.proItems",
        )
    }
    static_only = static - dynamic_roots
    hp_keys = static_only | expand_dynamic_keys(ja_flat, dynamic_roots)

    # Exclude non-HP top-level sections if any key leaked
    excluded_prefixes = (
        "privacyPage.", "releaseNotesPage.", "supportPage.",
        "compare.", "problem.", "clipboardCompare.", "benefits.", "usecases.",
    )
    hp_keys = {k for k in hp_keys if not any(k.startswith(p) for p in excluded_prefixes)}
    hp_keys = {k for k in hp_keys if k in ja_flat}

    entries: list[dict[str, str]] = []
    summary: dict[str, dict[str, int]] = {
        lang: {"A": 0, "B": 0, "C": 0} for lang in LANGS
    }
    brand_checks: dict[str, list[str]] = {sec: [] for sec in BRAND_SECTIONS}

    total_english_like = 0

    for locale in LANGS:
        data = json.loads((I18N_DIR / f"{locale}.json").read_text(encoding="utf-8"))
        flat = flatten(data)
        for key in sorted(hp_keys):
            value = flat.get(key, "")
            if not isinstance(value, str) or not value.strip():
                continue
            en_val = en_flat.get(key, "")
            result = classify(locale, key, value, en_val)
            if not result:
                continue
            cls, reason = result
            total_english_like += 1
            summary[locale][cls] += 1
            entry = {
                "locale": locale,
                "key": key,
                "value": value,
                "classification": cls,
                "reason": reason,
            }
            if locale != "en" and value == en_val:
                entry["identical_to_en"] = True
            entries.append(entry)
            top = key.split("[")[0].split(".")[0]
            if top in brand_checks and cls == "C":
                brand_checks[top].append(f"{locale}:{key}")

    c_entries = [e for e in entries if e["classification"] == "C"]

    audit_doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "main_hp_i18n_key_count": len(hp_keys),
        "english_like_total": total_english_like,
        "summary_by_locale": summary,
        "totals": {
            "A": sum(s["A"] for s in summary.values()),
            "B": sum(s["B"] for s in summary.values()),
            "C": sum(s["C"] for s in summary.values()),
        },
        "brand_section_c_hits": {k: v for k, v in brand_checks.items() if v},
        "entries": entries,
    }

    OUT_AUDIT.write_text(json.dumps(audit_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_C.write_text(
        json.dumps(
            {
                "generated_at": audit_doc["generated_at"],
                "count": len(c_entries),
                "locales_with_c": sorted({e["locale"] for e in c_entries}),
                "entries": c_entries,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    hashes_after = file_hashes()
    i18n_unchanged = hashes_before == hashes_after

    # git diff check
    git_diff = subprocess.run(
        ["git", "diff", "--stat", "business/i18n/"],
        cwd=BUSINESS.parent,
        capture_output=True,
        text=True,
    )

    print("=== Main HP English Residual Audit ===")
    print(f"Main HP i18n keys: {len(hp_keys)}")
    print(f"English-like strings: {total_english_like}")
    print(f"A: {audit_doc['totals']['A']}")
    print(f"B: {audit_doc['totals']['B']}")
    print(f"C: {audit_doc['totals']['C']}")
    print(f"C locales: {sorted({e['locale'] for e in c_entries})}")
    print(f"i18n unchanged: {i18n_unchanged}")
    print(f"Wrote {OUT_AUDIT.name}")
    print(f"Wrote {OUT_C.name}")
    if git_diff.stdout.strip():
        print("GIT DIFF (unexpected):", git_diff.stdout[:200])
    else:
        print("git diff business/i18n/: clean")

    if not i18n_unchanged:
        print("ERROR: i18n files changed during audit", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
