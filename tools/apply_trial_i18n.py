import json
from pathlib import Path

U = json.loads(Path(r"C:\Users\gacha\Desktop\myquickpaste-github\tools\trial_i18n_updates.json").read_text(encoding="utf-8"))

def update_pro_items(items, theme_item):
    items = list(items)
    if theme_item not in items:
        items.insert(len(items) - 1, theme_item)
    return items

def update_release_items(items, trial_item, theme_item):
    out = []
    for item in items:
        low = item.lower()
        if any(k in low for k in ("30-day", "30 day", "30日", "30 d", "30 g", "30 j", "30 t", "30天", "30 天", "trial", "試用", "deneme", "proef", "essai", "prueba", "prova", "teste", "prob", "проб", "تجرب", "ट्राय", "체험", "ทดลอง", "dùng thử", "试用", "試用", "pro trial", "pro 試用", "pro 试用")):
            out.append(trial_item)
        elif any(k in low for k in ("light/dark", "light & dark", "light, dark", "ライト", "theme", "thème", "tema", "motyw", "тем", "ธีม", "主题", "主題", "thema")):
            out.append(theme_item)
        else:
            out.append(item)
    return out

i18n_dir = Path(r"C:\Users\gacha\Desktop\myquickpaste-github\business\i18n")
for path in sorted(i18n_dir.glob("*.json")):
    lang = path.stem
    t = U.get(lang, U["en"])
    data = json.loads(path.read_text(encoding="utf-8"))
    data["hero"]["trialTitle"] = t["trialTitle"]
    data["hero"]["trialText"] = t["trialText"]
    data["cta"]["lead"] = t["ctaLead"]
    data["pricing"]["freeItems"][-1] = t["freeTrialItem"]
    data["pricing"]["proItems"] = update_pro_items(data["pricing"]["proItems"], t["proThemeItem"])
    data["supportPage"]["items"][1]["a"] = t["faqDiffA"]
    data["supportPage"]["items"][2]["a"] = t["faqTrialA"]
    if data.get("releaseNotesPage", {}).get("entries"):
        data["releaseNotesPage"]["entries"][0]["items"] = update_release_items(
            data["releaseNotesPage"]["entries"][0]["items"], t["releaseTrialItem"], t["releaseThemeItem"]
        )
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated", lang)