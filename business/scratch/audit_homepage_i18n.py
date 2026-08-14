#!/usr/bin/env python3
"""Audit homepage i18n: JSON syntax, EN-identical keys, legacy refs, screenshots."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
I18N_DIR = ROOT / "i18n"
LANGS = [
    "en", "ja", "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]
LEGACY_KEYS = ["compare", "problem", "clipboardCompare", "benefits", "usecases"]
HOMEPAGE_FILES = [
    ROOT / "index.html",
    ROOT / "js" / "site.js",
    ROOT / "js" / "i18n.js",
    ROOT / "js" / "marketing-images.js",
    ROOT / "js" / "screenshots.js",
]


def flatten(obj, prefix="") -> dict[str, str]:
    out: dict[str, str] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            out.update(flatten(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, f"{prefix}[{i}]"))
    elif isinstance(obj, str):
        out[prefix] = obj
    return out


def homepage_keys() -> set[str]:
    keys: set[str] = set()
    for fp in HOMEPAGE_FILES:
        if not fp.exists():
            continue
        text = fp.read_text(encoding="utf-8")
        keys.update(re.findall(r'data-i18n="([^"]+)"', text))
        keys.update(re.findall(r'data-i18n-attr="[^:"]+:([^"]+)"', text))
        keys.update(re.findall(r'getNested\(messages,\s*"([^"]+)"\)', text))
        keys.update(re.findall(r'getNested\(messages,\s*\'([^\']+)\'\)', text))
    return keys


def legacy_refs() -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    search_files = list(ROOT.rglob("*"))
    for key in LEGACY_KEYS:
        hits: list[str] = []
        pat = re.compile(rf"\b{re.escape(key)}\b")
        for fp in search_files:
            if fp.suffix not in {".html", ".js", ".css", ".py"}:
                continue
            if "scratch" in fp.parts or "i18n" in fp.parts and fp.suffix == ".json":
                continue
            rel = str(fp.relative_to(ROOT))
            try:
                if pat.search(fp.read_text(encoding="utf-8", errors="ignore")):
                    hits.append(rel)
            except OSError:
                pass
        refs[key] = sorted(set(hits))
    return refs


def screenshot_usage() -> dict:
    ss_js = ROOT / "js" / "screenshots.js"
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    js_types = re.findall(r"type:\s*['\"]([\w-]+)['\"]", ss_js.read_text(encoding="utf-8"))
    html_cate = "cate" in html or "cateAlt" in html
    ja = json.loads((I18N_DIR / "ja.json").read_text(encoding="utf-8"))
    caps = len(ja.get("screenshots", {}).get("items", []))
    return {
        "js_types": js_types,
        "js_count": len(js_types),
        "html_cate": html_cate,
        "i18n_items": caps,
        "i18n_cateAlt": ja.get("screenshots", {}).get("cateAlt"),
    }


def main() -> None:
    en = json.loads((I18N_DIR / "en.json").read_text(encoding="utf-8"))
    en_flat = flatten(en)
    hp_keys = homepage_keys()

    print("Homepage i18n audit")
    print(f"HTML/JS static keys: {len(hp_keys)}")

    syntax_ok = 0
    for lang in LANGS:
        try:
            json.loads((I18N_DIR / f"{lang}.json").read_text(encoding="utf-8"))
            syntax_ok += 1
        except json.JSONDecodeError as e:
            print(f"JSON ERROR {lang}: {e}")

    print(f"JSON syntax OK: {syntax_ok}/21")

    total_en_identical = 0
    en_remaining: dict[str, list[str]] = {}
    for lang in LANGS:
        if lang == "en":
            continue
        data = json.loads((I18N_DIR / f"{lang}.json").read_text(encoding="utf-8"))
        flat = flatten(data)
        same = []
        for k in hp_keys:
            if k in en_flat and k in flat and flat[k] == en_flat[k]:
                same.append(k)
        en_remaining[lang] = same
        total_en_identical += len(same)
        print(f"  {lang}: {len(same)} EN-identical (homepage keys)")

    print(f"TOTAL EN-identical (homepage keys): {total_en_identical}")

    print("\nLegacy key references:")
    refs = legacy_refs()
    for key, files in refs.items():
        print(f"  {key}: {len(files)} files -> {files or 'NONE'}")

    ss = screenshot_usage()
    print(f"\nScreenshots: JS uses {ss['js_count']} types {ss['js_types']}")
    print(f"HTML cate shot: {'present' if ss['html_cate'] else 'not present'}")
    print(f"i18n items captions: {ss['i18n_items']}, cateAlt: {ss['i18n_cateAlt']!r}")

    # License sanity
    bad_license = [
        "Pro体験", "Try Pro for 30", "30-day Pro trial", "view-only", "Up to 5 free",
    ]
    print("\nLicense phrase check:")
    for lang in LANGS:
        text = (I18N_DIR / f"{lang}.json").read_text(encoding="utf-8")
        hits = [b for b in bad_license if b in text]
        if hits:
            print(f"  {lang}: {hits}")
    print("  (no output = clean)")

    # Write detailed EN remaining to file
    out = SCRATCH = Path(__file__).resolve().parent / "audit_homepage_report.txt"
    lines = [
        "Homepage i18n audit",
        f"JSON syntax OK: {syntax_ok}/21",
        f"TOTAL EN-identical: {total_en_identical}",
        "",
    ]
    for lang, keys in en_remaining.items():
        if keys:
            lines.append(f"\n{lang} ({len(keys)}):")
            for k in keys[:80]:
                lines.append(f"  {k}")
            if len(keys) > 80:
                lines.append(f"  ... +{len(keys) - 80} more")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
