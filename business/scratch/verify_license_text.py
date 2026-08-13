import json
from pathlib import Path

I18N = Path(__file__).resolve().parent.parent / "i18n"
BAD = [
    "Pro体験", "Pro機能を体験", "Proの主要", "全カテゴリ",
    "Try Pro for 30", "Try Pro features", "30-day Pro trial",
    "Pro feature trial", "view-only", "Up to 5 free", "フリーワード最大5", "閲覧のみ",
    "all categories, and backup", "expanded capacity, all categories",
]
for p in sorted(I18N.glob("*.json")):
    text = p.read_text(encoding="utf-8")
    hits = [b for b in BAD if b in text]
    if hits:
        print(f"{p.name}: {hits}")
print("done")
