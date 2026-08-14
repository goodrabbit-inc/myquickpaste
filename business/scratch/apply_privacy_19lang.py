import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent
i18n = base / "i18n"
master_path = base / "scratch/MyQuickPaste_privacyPage_19languages_master_20260814.json"
master = json.loads(master_path.read_text(encoding="utf-8"))

locales = [
    "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt", "hi", "ar", "id",
    "th", "vi", "tr", "uk", "nl", "pl", "sv",
]

if set(master.keys()) != set(locales):
    missing = set(locales) - set(master.keys())
    extra = set(master.keys()) - set(locales)
    raise SystemExit(f"master locale mismatch missing={missing} extra={extra}")

ja_path = i18n / "ja.json"
en_path = i18n / "en.json"
ja_before = json.loads(ja_path.read_text(encoding="utf-8"))
en_before = json.loads(en_path.read_text(encoding="utf-8"))
ja_pp_before = json.dumps(ja_before["privacyPage"], ensure_ascii=False, sort_keys=True)
en_pp_before = json.dumps(en_before["privacyPage"], ensure_ascii=False, sort_keys=True)
ja_rn_before = json.dumps(ja_before["releaseNotesPage"], ensure_ascii=False, sort_keys=True)
en_rn_before = json.dumps(en_before["releaseNotesPage"], ensure_ascii=False, sort_keys=True)

for loc in locales:
    p = i18n / f"{loc}.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["privacyPage"] = master[loc]
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

errors = []
all_files = sorted(i18n.glob("*.json"))
if len(all_files) != 21:
    errors.append(f"lang count {len(all_files)} != 21")

ja_after = json.loads(ja_path.read_text(encoding="utf-8"))
en_after = json.loads(en_path.read_text(encoding="utf-8"))
if json.dumps(ja_after["privacyPage"], ensure_ascii=False, sort_keys=True) != ja_pp_before:
    errors.append("ja privacyPage changed")
if json.dumps(en_after["privacyPage"], ensure_ascii=False, sort_keys=True) != en_pp_before:
    errors.append("en privacyPage changed")
if json.dumps(ja_after["releaseNotesPage"], ensure_ascii=False, sort_keys=True) != ja_rn_before:
    errors.append("ja releaseNotesPage changed")
if json.dumps(en_after["releaseNotesPage"], ensure_ascii=False, sort_keys=True) != en_rn_before:
    errors.append("en releaseNotesPage changed")

for loc in locales:
    data = json.loads((i18n / f"{loc}.json").read_text(encoding="utf-8"))
    if data["privacyPage"] != master[loc]:
        errors.append(f"{loc} privacyPage != master")
    if len(data["privacyPage"].get("sections", [])) != 8:
        errors.append(f"{loc} sections != 8")

def flatten(obj, prefix=""):
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.extend(flatten(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            keys.extend(flatten(v, f"{prefix}[{i}]"))
    else:
        keys.append(prefix)
    return keys

ref = None
for p in all_files:
    data = json.loads(p.read_text(encoding="utf-8"))
    keys = sorted(flatten(data))
    if ref is None:
        ref = keys
    elif keys != ref:
        errors.append(f"key structure mismatch {p.name}")

for loc in locales:
    pp = master[loc]
    text = json.dumps(pp, ensure_ascii=False)
    if ".mqp" not in text:
        errors.append(f"{loc} missing .mqp")
    if "myquickpaste@hotmail.com" not in text:
        errors.append(f"{loc} missing email")
    if "Google Play Billing" not in text:
        errors.append(f"{loc} missing Google Play Billing")
    if "30" not in text:
        errors.append(f"{loc} missing 30-day reference")
    if len(pp.get("sections", [])) != 8:
        errors.append(f"{loc} master sections != 8")

for p in all_files:
    data = json.loads(p.read_text(encoding="utf-8"))
    if len(data["privacyPage"].get("sections", [])) != 8:
        errors.append(f"{p.name} all-lang sections != 8")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("ALL CHECKS PASSED")
print("19/19 applied and verified")
