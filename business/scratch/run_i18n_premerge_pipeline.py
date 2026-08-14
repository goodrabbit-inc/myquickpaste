#!/usr/bin/env python3
"""Safe i18n merge: backup → remainder (19 langs) → premerge patch (21 langs) → validate."""
from __future__ import annotations

import json
import re
import shutil
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

SCRATCH = Path(__file__).resolve().parent
BUSINESS = SCRATCH.parent
I18N_DIR = BUSINESS / "i18n"
REMAINDER_JSON = SCRATCH / "remainder_i18n_translations.json"
PREMERGE_CANDIDATES = [
    SCRATCH / "MyQuickPaste_i18n_premerge_patch.json",
    BUSINESS / "MyQuickPaste_i18n_premerge_patch.json",
    Path(r"C:\Users\gacha\Desktop\MyQuickPaste_i18n_premerge_patch.json"),
]

LANGS = [
    "en", "ja", "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]
REMAINDER_LANGS = [x for x in LANGS if x not in ("en", "ja")]

HP_SECTIONS = [
    "meta", "nav", "brand", "hero", "stores", "trust", "pain", "steps",
    "sceneSocial", "sceneWork", "sceneDaily", "sceneMore", "screenshots",
    "features", "comparison", "themesSection", "privacySection", "pricing",
    "faq", "windowsEdition", "cta", "footer",
]

ALLOWED_EN_IDENTICAL = {
    "MyQuickPaste", "Pro", "Google Play", "App Store", "Microsoft", "Windows",
    "FAQ", "¥0", "$0", "0",
}

LICENSE_CORE_KEYS = [
    "subtitle", "trialTitle", "trialText", "trialNote", "freeLead",
    "freeItems", "proItems", "proTag", "proLead", "notSub",
]


def find_premerge_patch() -> Path:
    for p in PREMERGE_CANDIDATES:
        if p.is_file():
            return p
    raise FileNotFoundError(
        "MyQuickPaste_i18n_premerge_patch.json not found. Place it at:\n"
        + "\n".join(f"  - {p}" for p in PREMERGE_CANDIDATES)
    )


def deep_merge(target: dict[str, Any], patch: dict[str, Any]) -> int:
    count = 0
    for key, val in patch.items():
        if isinstance(val, dict):
            if key not in target or not isinstance(target[key], dict):
                target[key] = {}
            count += deep_merge(target[key], val)
        elif isinstance(val, list):
            if key not in target or not isinstance(target[key], list):
                target[key] = []
            for i, item in enumerate(val):
                if isinstance(item, dict):
                    while len(target[key]) <= i:
                        target[key].append({})
                    if not isinstance(target[key][i], dict):
                        target[key][i] = {}
                    count += deep_merge(target[key][i], item)
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


def flatten(obj: Any, prefix: str = "") -> dict[str, str]:
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


def backup_i18n() -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = SCRATCH / f"i18n_backup_premerge_{stamp}"
    shutil.copytree(I18N_DIR, dest)
    print(f"Backup: {dest}")
    return dest


def apply_remainder() -> dict[str, int]:
    import importlib.util

    apply_mod_path = SCRATCH / "apply_remainder_i18n.py"
    spec = importlib.util.spec_from_file_location("apply_remainder", apply_mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    build_patch, all_dict, skip = mod.load_build_patch()
    translations = json.loads(REMAINDER_JSON.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}

    for lang in REMAINDER_LANGS:
        merged = dict(translations[lang])
        merged.update(mod.lic_keys(all_dict, lang))
        patch = build_patch(merged)
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        pricing_before = deepcopy(data.get("pricing"))
        n = mod.deep_merge(data, patch, skip)
        if deepcopy(data.get("pricing")) != pricing_before:
            raise RuntimeError(f"remainder modified pricing for {lang}")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        counts[lang] = n
        print(f"Remainder merged {lang}.json: {n} keys")
    return counts


def set_by_path(root: dict[str, Any], path: str, value: Any) -> None:
    """Set value at dotted path with list indices, e.g. features.items[5].title."""
    parts: list[str | int] = []
    for segment in path.split("."):
        while segment:
            if "[" in segment:
                head, rest = segment.split("[", 1)
                if head:
                    parts.append(head)
                idx_str, segment = rest.split("]", 1)
                parts.append(int(idx_str))
                if segment.startswith("."):
                    segment = segment[1:]
            else:
                parts.append(segment)
                break

    cur: Any = root
    for part in parts[:-1]:
        if isinstance(part, int):
            while len(cur) <= part:
                cur.append({})
            cur = cur[part]
        else:
            nxt_idx = parts[parts.index(part) + 1]
            if part not in cur or not isinstance(cur[part], (dict, list)):
                cur[part] = [] if isinstance(nxt_idx, int) else {}
            cur = cur[part]

    last = parts[-1]
    if isinstance(last, int):
        while len(cur) <= last:
            cur.append(None)
        cur[last] = value
    else:
        cur[last] = value


def apply_flat_patch(data: dict[str, Any], flat_patch: dict[str, str]) -> int:
    count = 0
    for path, val in flat_patch.items():
        before = flatten(data).get(path)
        set_by_path(data, path, val)
        if before != val:
            count += 1
    return count


def apply_premerge(patch_path: Path) -> dict[str, int]:
    raw = json.loads(patch_path.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}

    if "patches" in raw and isinstance(raw["patches"], dict):
        patches = raw["patches"]
    elif all(lang in raw for lang in LANGS):
        patches = raw
    else:
        raise ValueError("premerge patch must be {lang: {...}} or {patches: {lang: {...}}}")

    for lang in LANGS:
        if lang not in patches:
            raise ValueError(f"premerge patch missing language: {lang}")
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        pricing_before = deepcopy(data.get("pricing"))
        lang_patch = patches[lang]
        if lang_patch and all(isinstance(v, str) for v in lang_patch.values()):
            n = apply_flat_patch(data, lang_patch)
        else:
            n = deep_merge(data, lang_patch)
        if deepcopy(data.get("pricing")) != pricing_before:
            raise RuntimeError(f"premerge modified pricing for {lang}")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        counts[lang] = n
        print(f"Premerge applied {lang}.json: {n} keys")
    return counts


def validate_json_syntax() -> int:
    ok = 0
    for lang in LANGS:
        json.loads((I18N_DIR / f"{lang}.json").read_text(encoding="utf-8"))
        ok += 1
    return ok


def validate_key_structure() -> bool:
    ref = set(flatten(json.loads((I18N_DIR / "ja.json").read_text(encoding="utf-8"))).keys())
    ok = True
    for lang in LANGS:
        keys = set(flatten(json.loads((I18N_DIR / f"{lang}.json").read_text(encoding="utf-8"))).keys())
        if keys != ref:
            missing = sorted(ref - keys)[:5]
            extra = sorted(keys - ref)[:5]
            print(f"KEY MISMATCH {lang}: missing={missing} extra={extra}")
            ok = False
    return ok


def is_probably_english(s: str) -> bool:
    if s in ALLOWED_EN_IDENTICAL:
        return False
    if re.fullmatch(r"[\W\d_]+", s):
        return False
    if "MyQuickPaste" in s or "Google Play" in s or "App Store" in s:
        return False
    ascii_words = re.findall(r"[A-Za-z]{3,}", s)
    if not ascii_words:
        return False
    return True


def count_hp_english(lang: str, en_flat: dict[str, str]) -> list[str]:
    if lang == "en":
        return []
    data = json.loads((I18N_DIR / f"{lang}.json").read_text(encoding="utf-8"))
    hits: list[str] = []
    for sec in HP_SECTIONS:
        if sec not in data:
            continue
        for k, v in flatten(data[sec], sec).items():
            if v == en_flat.get(k) and is_probably_english(v):
                hits.append(k)
    return hits


def validate_license(backup_dir: Path) -> bool:
    ok = True
    for lang in LANGS:
        before = json.loads((backup_dir / f"{lang}.json").read_text(encoding="utf-8")).get("pricing", {})
        after = json.loads((I18N_DIR / f"{lang}.json").read_text(encoding="utf-8")).get("pricing", {})
        for k in LICENSE_CORE_KEYS:
            if before.get(k) != after.get(k):
                print(f"LICENSE DIFF {lang}.{k}")
                ok = False
    return ok


def validate_brand_ja() -> bool:
    data = json.loads((I18N_DIR / "ja.json").read_text(encoding="utf-8"))
    checks = {
        "hero.catchLine1": "よく使う文字を、",
        "hero.catchLine2": "タップひとつで。",
        "steps.titleLine1": "保存して、タップして、",
        "steps.titleLine2": "あとは貼り付けるだけ。",
        "cta.titleLine1": "よく使う文字を、",
        "cta.titleLine2": "タップひとつで。",
    }
    flat = flatten(data)
    ok = True
    for k, expected in checks.items():
        if flat.get(k) != expected:
            print(f"BRAND BROKEN ja {k}: {flat.get(k)!r}")
            ok = False
    return ok


def check_three_fixes(patch_path: Path) -> dict[str, Any]:
    patch_raw = json.loads(patch_path.read_text(encoding="utf-8"))
    en_export = "Export and import"
    result: dict[str, Any] = {
        "items5_title_not_english": {},
        "items6_has_pro": {},
        "points3_trial_pro": {},
        "patch_exact_match": {},
    }
    for lang in LANGS:
        d = json.loads((I18N_DIR / f"{lang}.json").read_text(encoding="utf-8"))
        flat = flatten(d)
        expected = patch_raw[lang]
        t5 = d["features"]["items"][5]["title"]
        t6 = d["features"]["items"][6]["text"]
        p3 = d["privacySection"]["points"][3]
        if lang in REMAINDER_LANGS:
            result["items5_title_not_english"][lang] = t5 != en_export
        result["items6_has_pro"][lang] = "Pro" in t6 or "pro" in t6.lower()
        result["points3_trial_pro"][lang] = flat.get("privacySection.points[3]") == expected["privacySection.points[3]"]
        result["patch_exact_match"][lang] = (
            t5 == expected["features.items[5].title"]
            and t6 == expected["features.items[6].text"]
            and p3 == expected["privacySection.points[3]"]
        )
    return result


def main() -> None:
    if not REMAINDER_JSON.is_file():
        print(f"ERROR: missing {REMAINDER_JSON}", file=sys.stderr)
        sys.exit(1)

    patch_path = find_premerge_patch()
    print(f"Premerge patch: {patch_path}")

    backup_dir = backup_i18n()
    remainder_counts = apply_remainder()
    premerge_counts = apply_premerge(patch_path)

    syntax_ok = validate_json_syntax()
    structure_ok = validate_key_structure()
    license_ok = validate_license(backup_dir)
    brand_ok = validate_brand_ja()
    en_flat = flatten(json.loads((I18N_DIR / "en.json").read_text(encoding="utf-8")))
    hp_en: dict[str, int] = {}
    total_hp_en = 0
    for lang in LANGS:
        if lang == "en":
            continue
        hits = count_hp_english(lang, en_flat)
        hp_en[lang] = len(hits)
        total_hp_en += len(hits)

    fixes = check_three_fixes(patch_path)

    print("\n=== REPORT ===")
    print(f"remainder 19 langs merged: {len(remainder_counts) == 19}")
    for lang, n in sorted(remainder_counts.items()):
        print(f"  remainder {lang}: {n} keys")
    print(f"premerge 21 langs applied: {len(premerge_counts) == 21}")
    for lang, n in sorted(premerge_counts.items()):
        print(f"  premerge {lang}: {n} keys")
    print(f"JSON syntax: {syntax_ok}/21")
    print(f"Key structure match: {structure_ok}")
    print(f"HP unnecessary EN total: {total_hp_en}")
    for lang, n in sorted(hp_en.items()):
        if n:
            print(f"  HP EN {lang}: {n}")
    print(f"features.items[5].title translated (19 langs): {all(fixes['items5_title_not_english'].values())}")
    print(f"features.items[6].text Pro-limited (21 langs): {all(fixes['items6_has_pro'].values())}")
    print(f"privacySection.points[3] trial+Pro exact (21 langs): {all(fixes['points3_trial_pro'].values())}")
    print(f"premerge patch exact match (21 langs): {all(fixes['patch_exact_match'].values())}")
    print(f"License unchanged: {license_ok}")
    print(f"Brand ja intact: {brand_ok}")

    if not all([
        len(remainder_counts) == 19,
        len(premerge_counts) == 21,
        syntax_ok == 21,
        structure_ok,
        license_ok,
        brand_ok,
        all(fixes["items5_title_not_english"].values()),
        all(fixes["items6_has_pro"].values()),
        all(fixes["points3_trial_pro"].values()),
        all(fixes["patch_exact_match"].values()),
    ]):
        sys.exit(1)


if __name__ == "__main__":
    main()
