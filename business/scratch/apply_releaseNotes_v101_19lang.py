import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
I18N = BASE / "i18n"
MASTER_PATH = BASE / "scratch/MyQuickPaste_releaseNotesPage_v1.0.1_19languages_master_20260814.json"

LOCALES = [
    "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt", "hi", "ar", "id",
    "th", "vi", "tr", "uk", "nl", "pl", "sv",
]
KEYS = [
    "entries[0].date",
    "entries[0].title",
    "entries[0].items[0]",
    "entries[0].items[1]",
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


def get_path_value(obj, path: str):
    cur = obj
    for part in path.replace("]", "").split("."):
        if "[" in part:
            name, idx = part.split("[")
            cur = cur[name][int(idx)]
        else:
            cur = cur[part]
    return cur


def set_path_value(obj, path: str, value: str):
    parts = path.replace("]", "").split(".")
    cur = obj
    for part in parts[:-1]:
        if "[" in part:
            name, idx = part.split("[")
            cur = cur[name][int(idx)]
        else:
            cur = cur[part]
    last = parts[-1]
    if "[" in last:
        name, idx = last.split("[")
        cur[name][int(idx)] = value
    else:
        cur[last] = value


def main():
    master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
    if set(master.keys()) != set(LOCALES):
        raise SystemExit("master locale set mismatch")

    all_files = sorted(I18N.glob("*.json"))
    pre_hashes = {f.name: sha256_file(f) for f in all_files}

    # snapshots for unchanged checks
    ja_data = json.loads((I18N / "ja.json").read_text(encoding="utf-8"))
    en_data = json.loads((I18N / "en.json").read_text(encoding="utf-8"))
    ja_rn_before = json.dumps(ja_data["releaseNotesPage"], ensure_ascii=False, sort_keys=True)
    en_rn_before = json.dumps(en_data["releaseNotesPage"], ensure_ascii=False, sort_keys=True)
    ja_pp_before = json.dumps(ja_data["privacyPage"], ensure_ascii=False, sort_keys=True)
    en_pp_before = json.dumps(en_data["privacyPage"], ensure_ascii=False, sort_keys=True)

    v100_snapshots = {}
    privacy_snapshots = {}
    other_file_snapshots = {}
    for loc in LOCALES:
        data = json.loads((I18N / f"{loc}.json").read_text(encoding="utf-8"))
        rn = data["releaseNotesPage"]
        v100_snapshots[loc] = json.dumps(rn["entries"][1], ensure_ascii=False, sort_keys=True)
        privacy_snapshots[loc] = json.dumps(data["privacyPage"], ensure_ascii=False, sort_keys=True)
        # snapshot everything except the 4 keys we're changing
        snap = json.loads(json.dumps(data, ensure_ascii=False))
        for key in KEYS:
            set_path_value(snap, f"releaseNotesPage.{key}", "__PLACEHOLDER__")
        other_file_snapshots[loc] = json.dumps(snap, ensure_ascii=False, sort_keys=True)

    applied = 0
    for loc in LOCALES:
        path = I18N / f"{loc}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in KEYS:
            set_path_value(data, f"releaseNotesPage.{key}", master[loc][key])
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        applied += 1

    errors = []
    match_count = 0
    for loc in LOCALES:
        data = json.loads((I18N / f"{loc}.json").read_text(encoding="utf-8"))
        rn = data["releaseNotesPage"]
        for key in KEYS:
            actual = get_path_value(rn, key)
            expected = master[loc][key]
            if actual != expected:
                errors.append(f"{loc} {key}: mismatch")
            else:
                match_count += 1
        if rn["entries"][0]["version"] != "1.0.1":
            errors.append(f"{loc} version not 1.0.1")
        if len(rn["entries"][0]["items"]) != 3:
            errors.append(f"{loc} v1.0.1 items != 3")
        if len(rn["entries"][1]["items"]) != 8:
            errors.append(f"{loc} v1.0.0 items != 8")
        if json.dumps(rn["entries"][1], ensure_ascii=False, sort_keys=True) != v100_snapshots[loc]:
            errors.append(f"{loc} v1.0.0 changed")
        if json.dumps(data["privacyPage"], ensure_ascii=False, sort_keys=True) != privacy_snapshots[loc]:
            errors.append(f"{loc} privacyPage changed")

    ja_after = json.loads((I18N / "ja.json").read_text(encoding="utf-8"))
    en_after = json.loads((I18N / "en.json").read_text(encoding="utf-8"))
    if json.dumps(ja_after["releaseNotesPage"], ensure_ascii=False, sort_keys=True) != ja_rn_before:
        errors.append("ja releaseNotesPage changed")
    if json.dumps(en_after["releaseNotesPage"], ensure_ascii=False, sort_keys=True) != en_rn_before:
        errors.append("en releaseNotesPage changed")
    if json.dumps(ja_after["privacyPage"], ensure_ascii=False, sort_keys=True) != ja_pp_before:
        errors.append("ja privacyPage changed")
    if json.dumps(en_after["privacyPage"], ensure_ascii=False, sort_keys=True) != en_pp_before:
        errors.append("en privacyPage changed")

    for loc in LOCALES:
        data = json.loads((I18N / f"{loc}.json").read_text(encoding="utf-8"))
        snap = json.loads(json.dumps(data, ensure_ascii=False))
        for key in KEYS:
            set_path_value(snap, f"releaseNotesPage.{key}", "__PLACEHOLDER__")
        if json.dumps(snap, ensure_ascii=False, sort_keys=True) != other_file_snapshots[loc]:
            errors.append(f"{loc} other i18n changed beyond 4 keys")

    # privacy all 21
    for p in all_files:
        data = json.loads(p.read_text(encoding="utf-8"))
        loc = p.stem
        if loc in LOCALES:
            continue
        if loc in ("ja", "en"):
            pp = json.dumps(data["privacyPage"], ensure_ascii=False, sort_keys=True)
            if loc == "ja" and pp != ja_pp_before:
                errors.append("ja privacyPage changed (recheck)")
            if loc == "en" and pp != en_pp_before:
                errors.append("en privacyPage changed (recheck)")

    ref = None
    for p in all_files:
        data = json.loads(p.read_text(encoding="utf-8"))
        keys = sorted(flatten_keys(data))
        if ref is None:
            ref = keys
        elif keys != ref:
            errors.append(f"key structure mismatch: {p.name}")

    post_hashes = {f.name: sha256_file(f) for f in all_files}
    expected_changed = {f"{loc}.json" for loc in LOCALES}
    actually_changed = {k for k in pre_hashes if pre_hashes[k] != post_hashes[k]}
    if actually_changed != expected_changed:
        errors.append(f"unexpected hash changes: {actually_changed - expected_changed} / missing: {expected_changed - actually_changed}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

    print("OK")
    print(f"applied: {applied}/19")
    print(f"master match: {match_count}/76")
    print(f"json files: {len(all_files)}/21")
    print(f"changed files: {sorted(actually_changed)}")


if __name__ == "__main__":
    main()
