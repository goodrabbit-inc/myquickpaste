#!/usr/bin/env python3
"""Apply remainder homepage i18n translations from remainder_i18n_translations.json."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
I18N_DIR = SCRATCH.parent / "i18n"
TRANSLATIONS_JSON = SCRATCH / "remainder_i18n_translations.json"
GEN = SCRATCH / "_gen_remainder_patch.py"
LICENSE = SCRATCH / "patch_license_i18n.py"

TARGET_LANGS = [
    "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]
VERIFY_LANGS = ["en", "ja"]


def load_build_patch():
    import importlib.util

    spec = importlib.util.spec_from_file_location("patch_license_i18n", LICENSE)
    lic_mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(lic_mod)

    gen_text = GEN.read_text(encoding="utf-8")
    start = gen_text.index("def build_patch")
    end = gen_text.index("\n# fmt: off\nTRANSLATIONS", start)
    ns: dict = {"_SKIP": object()}
    exec(gen_text[start:end], ns)
    return ns["build_patch"], lic_mod.ALL, ns["_SKIP"]


def lic_keys(all_dict: dict, lang: str) -> dict[str, str]:
    L = all_dict[lang]
    return {
        "nav_cta": L["nav_cta"],
        "hero_ctaSecondary": L["hero_cta_secondary"],
        "hero_pill1": L["hero_pill1"],
        "hero_trialTitle": L["hero_trial_title"],
        "hero_trialText": L["hero_trial_text"],
        "cta_sub": L["cta_sub"],
        "faq_i2_a": L["faq_trial_a"],
    }


def deep_merge(target: dict, patch: dict, skip: object) -> int:
    count = 0
    for key, val in patch.items():
        if val is skip:
            continue
        if isinstance(val, dict):
            if key not in target or not isinstance(target[key], dict):
                target[key] = {}
            count += deep_merge(target[key], val, skip)
        elif isinstance(val, list):
            if key not in target or not isinstance(target[key], list):
                target[key] = []
            for i, item in enumerate(val):
                if item is skip:
                    continue
                if isinstance(item, dict):
                    while len(target[key]) <= i:
                        target[key].append({})
                    if not isinstance(target[key][i], dict):
                        target[key][i] = {}
                    count += deep_merge(target[key][i], item, skip)
                else:
                    while len(target[key]) <= i:
                        target[key].append(None)
                    if target[key][i] != item:
                        target[key][i] = item
                        count += 1
        else:
            if target.get(key) != val:
                target[key] = val
                count += 1
    return count


def main() -> None:
    build_patch, all_dict, skip = load_build_patch()
    translations = json.loads(TRANSLATIONS_JSON.read_text(encoding="utf-8"))

    for lang in VERIFY_LANGS:
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if not data.get("pricing"):
            print(f"ERROR: missing pricing in {lang}", file=sys.stderr)
            sys.exit(1)
        print(f"Verified {path.name}: pricing present")

    summary: list[tuple[str, int]] = []
    for lang in TARGET_LANGS:
        if lang not in translations:
            print(f"ERROR: missing translations for {lang}", file=sys.stderr)
            sys.exit(1)
        merged = dict(translations[lang])
        merged.update(lic_keys(all_dict, lang))
        patch = build_patch(merged)
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        pricing_before = deepcopy(data.get("pricing"))
        n = deep_merge(data, patch, skip)
        if deepcopy(data.get("pricing")) != pricing_before:
            print(f"ERROR: pricing modified for {lang}", file=sys.stderr)
            sys.exit(1)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary.append((lang, n))
        print(f"Patched {path.name}: {n} keys")

    print("\n=== Summary ===")
    for lang, n in summary:
        print(f"  {lang}: {n} keys patched")


if __name__ == "__main__":
    main()
