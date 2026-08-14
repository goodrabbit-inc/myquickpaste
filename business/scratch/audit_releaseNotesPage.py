#!/usr/bin/env py -3
"""Audit releaseNotesPage across 21 i18n files. Read-only."""
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
I18N = BASE / "i18n"
SCRATCH = BASE / "scratch"

LOCALES_19 = [
    "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt", "hi", "ar", "id",
    "th", "vi", "tr", "uk", "nl", "pl", "sv",
]
ALL_LOCALES = ["ja", "en"] + LOCALES_19

# Tokens allowed to remain English in translations
ALLOWED_ENGLISH = {
    "myquickpaste", "pro", "android", "ios", "google play", "app store", "windows",
    "jpeg", "png", "webp", "gif", "json", "mqp", "url", "email", "phone",
}
ALLOWED_ENGLISH_PATTERNS = [
    re.compile(r"^\d+(\.\d+)*$"),  # version numbers
    re.compile(r"^\d{4}$"),  # year
    re.compile(r"^[\d\s/\-–—:.,]+$"),  # mostly numeric/punct
    re.compile(r"^https?://", re.I),
]

SPEC_CONTRADICTION_PATTERNS = [
    (r"for business|for Business|ビジネス版", "MyQuickPaste for Business 表記"),
    (r"Pro trial|pro trial|Pro トライアル", "Pro trial 表記"),
    (r"30-day Pro trial|30 day Pro trial", "30-day Pro trial 表記"),
    (r"JSON export|JSON エクスポート|JSON export/import", "JSON 形式エクスポート（現仕様は .mqp）"),
    (r"Clipee|clipee", "旧ブランド Clipee"),
    (r"Pastee|pastee", "旧ブランド Pastee"),
    (r"subscription|サブスクリプション|Subscription", "サブスクリプション表記"),
    (r"monthly|毎月", "月額表記"),
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten_keys(obj, prefix=""):
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.extend(flatten_keys(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            keys.extend(flatten_keys(v, f"{prefix}[{i}]"))
    else:
        keys.append(prefix)
    return keys


def collect_string_paths(obj, prefix=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(collect_string_paths(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(collect_string_paths(v, f"{prefix}[{i}]"))
    elif isinstance(obj, str):
        out.append((prefix, obj))
    return out


def is_mostly_english(text: str) -> bool:
    if not text or not text.strip():
        return False
    t = text.strip().lower()
    if t in ALLOWED_ENGLISH:
        return False
    for pat in ALLOWED_ENGLISH_PATTERNS:
        if pat.match(text.strip()):
            return False
    # Allow strings that are primarily non-Latin
    non_ascii = sum(1 for c in text if ord(c) > 127)
    if non_ascii >= max(1, len(text) // 4):
        return False
    # Count Latin letters
    latin = sum(1 for c in text if c.isalpha() and ord(c) < 128)
    if latin == 0:
        return False
    # Common English function words
    words = re.findall(r"[A-Za-z]+", text)
    if not words:
        return False
    common_en = {
        "the", "and", "for", "with", "added", "supports", "tap", "copy", "share",
        "preview", "images", "image", "category", "release", "initial", "public",
        "free", "plan", "trial", "day", "export", "import", "settings", "light",
        "dark", "themes", "premium", "reorder", "mode", "list", "profile", "cards",
        "field", "long", "press", "based", "lists", "snippets", "email", "phone",
        "updates", "delivered", "through", "when", "available", "version", "history",
        "latest", "business", "cards", "logos", "more", "save", "startup", "data",
        "backup", "feedback", "per", "and", "or",
    }
    en_hits = sum(1 for w in words if w.lower() in common_en or len(w) > 2)
    ratio = en_hits / len(words)
    return ratio >= 0.5 and latin >= 8


def is_allowed_english_residual(text: str, en_value: str) -> bool:
    if text != en_value:
        return False
    t = text.strip()
    tl = t.lower()
    if tl in ALLOWED_ENGLISH:
        return True
    for pat in ALLOWED_ENGLISH_PATTERNS:
        if pat.match(t):
            return True
    # version field identical is OK
    if re.fullmatch(r"\d+\.\d+\.\d+", t):
        return True
    if re.fullmatch(r"\d{4}", t):
        return True
    # Pro alone in item
    if tl == "pro":
        return True
    # Technical formats in items
    if "jpeg" in tl or "png" in tl or "webp" in tl or "gif" in tl:
        if text == en_value:
            return True
    return False


def compare_ja_en(ja_rn, en_rn):
    result = {
        "structure_match": True,
        "version_count_ja": len(ja_rn.get("entries", [])),
        "version_count_en": len(en_rn.get("entries", [])),
        "top_level_keys_ja": list(ja_rn.keys()),
        "top_level_keys_en": list(en_rn.keys()),
        "field_comparison": {},
        "entries_comparison": [],
        "issues": [],
    }

    for key in ["title", "lead", "latestPrefix", "storeNote"]:
        jv = ja_rn.get(key, "")
        ev = en_rn.get(key, "")
        result["field_comparison"][key] = {"ja": jv, "en": ev, "same_meaning_expected": True}

    ja_entries = ja_rn.get("entries", [])
    en_entries = en_rn.get("entries", [])
    if len(ja_entries) != len(en_entries):
        result["structure_match"] = False
        result["issues"].append(
            f"entry count mismatch: ja={len(ja_entries)} en={len(en_entries)}"
        )

    for i, (je, ee) in enumerate(zip(ja_entries, en_entries)):
        entry_cmp = {
            "index": i,
            "version_ja": je.get("version"),
            "version_en": ee.get("version"),
            "date_ja": je.get("date"),
            "date_en": ee.get("date"),
            "title_ja": je.get("title"),
            "title_en": ee.get("title"),
            "items_count_ja": len(je.get("items", [])),
            "items_count_en": len(ee.get("items", [])),
            "issues": [],
        }
        if je.get("version") != ee.get("version"):
            entry_cmp["issues"].append("version mismatch")
            result["issues"].append(f"entries[{i}] version: {je.get('version')} vs {ee.get('version')}")
        if len(je.get("items", [])) != len(ee.get("items", [])):
            entry_cmp["issues"].append("items count mismatch")
            result["issues"].append(
                f"entries[{i}] items count: {len(je.get('items', []))} vs {len(ee.get('items', []))}"
            )
        result["entries_comparison"].append(entry_cmp)

    # semantic notes (not auto-fix)
    if any("JSON" in x for e in ja_entries for x in e.get("items", [])):
        result["issues"].append("note: ja 1.0.0 mentions JSON export/import (historical wording)")
    if any("JSON" in x for e in en_entries for x in e.get("items", [])):
        result["issues"].append("note: en 1.0.0 mentions JSON export/import (historical wording)")

    return result


def classify_locale(loc: str, rn, en_rn, ja_rn):
    en_paths = {p: v for p, v in collect_string_paths(en_rn)}
    loc_paths = {p: v for p, v in collect_string_paths(rn)}

    missing_keys = sorted(set(en_paths) - set(loc_paths))
    extra_keys = sorted(set(loc_paths) - set(en_paths))

    identical_to_en = []
    needs_translation = []
    allowed_identical = []

    for path, en_val in en_paths.items():
        loc_val = loc_paths.get(path, "")
        if loc_val == en_val:
            if is_allowed_english_residual(loc_val, en_val):
                allowed_identical.append({"path": path, "value": loc_val})
            else:
                identical_to_en.append({"path": path, "value": loc_val})

    for path, loc_val in loc_paths.items():
        if path not in en_paths:
            continue
        if loc_val == en_paths[path]:
            continue
        if is_mostly_english(loc_val) and loc != "en":
            needs_translation.append({"path": path, "current": loc_val, "en_reference": en_paths[path]})

    total_strings = len(en_paths)
    untranslated_count = len(identical_to_en)
    translated_count = total_strings - untranslated_count - len(allowed_identical)

    if missing_keys:
        status = "欠落あり"
    elif untranslated_count == 0:
        status = "完全翻訳済み"
    elif untranslated_count >= total_strings * 0.7:
        status = "ほぼ英語"
    elif untranslated_count > 0:
        status = "一部英語残存"
    else:
        status = "完全翻訳済み"

    return {
        "locale": loc,
        "status": status,
        "total_string_keys": total_strings,
        "translated_or_localized_count": total_strings - untranslated_count,
        "identical_to_en_count": untranslated_count,
        "allowed_identical_to_en_count": len(allowed_identical),
        "missing_keys": missing_keys,
        "extra_keys": extra_keys,
        "identical_to_en": identical_to_en,
        "allowed_identical_to_en": allowed_identical,
        "mostly_english_non_identical": needs_translation,
    }


def find_spec_contradictions(all_data):
    candidates = []
    for loc in ALL_LOCALES:
        rn = all_data[loc]["releaseNotesPage"]
        for path, val in collect_string_paths(rn):
            for pattern, label in SPEC_CONTRADICTION_PATTERNS:
                if re.search(pattern, val, re.I):
                    candidates.append({
                        "locale": loc,
                        "path": path,
                        "value": val,
                        "candidate_reason": label,
                        "note": "過去履歴としてそのまま残すべき可能性がある項目",
                    })
    return candidates


def build_translation_source(ja_rn, en_rn, analyses_19):
    en_paths = dict(collect_string_paths(en_rn))
    ja_paths = dict(collect_string_paths(ja_rn))
    source = {
        "ja_full": ja_rn,
        "en_full": en_rn,
        "locales_needing_translation": {},
        "unique_paths_needing_translation": [],
    }
    all_paths = set()
    for a in analyses_19:
        loc = a["locale"]
        keys_needed = []
        for item in a["identical_to_en"]:
            path = item["path"]
            all_paths.add(path)
            keys_needed.append({
                "path": path,
                "current_value": item["value"],
                "en_reference": en_paths.get(path, ""),
                "ja_reference": ja_paths.get(path, ""),
            })
        for mk in a["missing_keys"]:
            all_paths.add(mk)
            keys_needed.append({
                "path": mk,
                "current_value": None,
                "en_reference": en_paths.get(mk, ""),
                "ja_reference": ja_paths.get(mk, ""),
                "note": "missing key",
            })
        source["locales_needing_translation"][loc] = keys_needed
    source["unique_paths_needing_translation"] = sorted(all_paths)
    return source


def main():
    # Pre hashes
    pre_hashes = {f.name: sha256_file(I18N / f.name) for f in sorted(I18N.glob("*.json"))}

    all_data = {}
    for loc in ALL_LOCALES:
        path = I18N / f"{loc}.json"
        all_data[loc] = json.loads(path.read_text(encoding="utf-8"))

    ja_rn = all_data["ja"]["releaseNotesPage"]
    en_rn = all_data["en"]["releaseNotesPage"]

    ja_en_cmp = compare_ja_en(ja_rn, en_rn)

    # Key structure across 21 langs for releaseNotesPage only
    ref_keys = None
    key_structure = {}
    for loc in ALL_LOCALES:
        keys = sorted(flatten_keys(all_data[loc]["releaseNotesPage"], "releaseNotesPage"))
        key_structure[loc] = keys
        if ref_keys is None:
            ref_keys = keys
        elif keys != ref_keys:
            key_structure["__mismatch__"] = True

    analyses_19 = [classify_locale(loc, all_data[loc]["releaseNotesPage"], en_rn, ja_rn) for loc in LOCALES_19]
    spec_candidates = find_spec_contradictions(all_data)

    total_needs_translation = sum(
        len(a["identical_to_en"]) + len(a["missing_keys"]) for a in analyses_19
    )
    unique_paths = sorted({
        item["path"]
        for a in analyses_19
        for item in a["identical_to_en"]
    } | {
        mk for a in analyses_19 for mk in a["missing_keys"]
    })
    langs_with_english = [a["locale"] for a in analyses_19 if a["identical_to_en_count"] > 0]

    audit = {
        "audit_meta": {
            "title": "MyQuickPaste releaseNotesPage 21言語 事前監査",
            "audited_at": "2026-08-14",
            "i18n_changed": False,
            "push_deploy": False,
        },
        "ja_en_comparison": ja_en_cmp,
        "key_structure": {
            "consistent_across_21": ref_keys is not None and not key_structure.get("__mismatch__"),
            "releaseNotesPage_key_count": len(ref_keys) if ref_keys else None,
            "per_locale_key_counts": {loc: len(key_structure[loc]) for loc in ALL_LOCALES if loc in key_structure and loc != "__mismatch__"},
        },
        "version_summary": {
            "versions_in_ja": [e.get("version") for e in ja_rn.get("entries", [])],
            "versions_in_en": [e.get("version") for e in en_rn.get("entries", [])],
            "entry_count": len(ja_rn.get("entries", [])),
        },
        "locales_19_status": {a["locale"]: {
            "status": a["status"],
            "identical_to_en_count": a["identical_to_en_count"],
            "allowed_identical_to_en_count": a["allowed_identical_to_en_count"],
            "missing_keys_count": len(a["missing_keys"]),
            "total_string_keys": a["total_string_keys"],
        } for a in analyses_19},
        "locales_19_detail": analyses_19,
        "english_residual_summary": {
            "total_key_locale_pairs_needing_translation": total_needs_translation,
            "unique_paths_needing_translation": unique_paths,
            "unique_path_count": len(unique_paths),
            "locales_with_untranslated_identical_to_en": langs_with_english,
        },
        "current_spec_contradiction_candidates": spec_candidates,
        "summary": {
            "ja_en_structure_match": ja_en_cmp["structure_match"],
            "ja_en_issue_count": len(ja_en_cmp["issues"]),
            "version_count": len(ja_rn.get("entries", [])),
            "fully_translated_locales": [a["locale"] for a in analyses_19 if a["status"] == "完全翻訳済み"],
            "partial_english_locales": [a["locale"] for a in analyses_19 if a["status"] == "一部英語残存"],
            "mostly_english_locales": [a["locale"] for a in analyses_19 if a["status"] == "ほぼ英語"],
            "missing_locales": [a["locale"] for a in analyses_19 if a["status"] == "欠落あり"],
        },
    }

    translation_source = build_translation_source(ja_rn, en_rn, analyses_19)
    translation_source["meta"] = {
        "note": "翻訳文は未作成。ja/en 全文と他19言語で en と同一の未翻訳キーのみ（許容英語残存は除外済み）。",
        "total_key_locale_pairs_needing_translation": total_needs_translation,
        "unique_path_count": len(unique_paths),
    }

    (SCRATCH / "releaseNotesPage_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (SCRATCH / "releaseNotesPage_translation_source.json").write_text(
        json.dumps(translation_source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Post hashes
    post_hashes = {f.name: sha256_file(I18N / f.name) for f in sorted(I18N.glob("*.json"))}
    unchanged = pre_hashes == post_hashes
    audit["audit_meta"]["i18n_sha256_unchanged"] = unchanged
    (SCRATCH / "releaseNotesPage_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("i18n unchanged:", unchanged)
    print("versions:", len(ja_rn.get("entries", [])))
    print("ja/en issues:", len(ja_en_cmp["issues"]))
    print("total keys needing translation (19 langs):", total_needs_translation)
    for a in analyses_19:
        print(f"  {a['locale']}: {a['status']} identical={a['identical_to_en_count']} missing={len(a['missing_keys'])}")
    print("spec contradiction candidates:", len(spec_candidates))
    if not unchanged:
        changed = [k for k in pre_hashes if pre_hashes[k] != post_hashes[k]]
        print("CHANGED FILES:", changed)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
