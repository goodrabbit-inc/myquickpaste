#!/usr/bin/env python3
"""Patch homepage i18n JSON — brand copy refresh for all 21 languages."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"
LANGS = [
    "en", "ja", "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]

# Sentinel: skip merging this list slot
_SKIP = object()


def set_nested(root: dict[str, Any], path: str, value: Any) -> None:
    """Set a value at a dotted path; supports list indices like items[0].text."""
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
            nxt = parts[parts.index(part) + 1] if part in parts else None
            idx_in_parts = parts.index(part)
            nxt_part = parts[idx_in_parts + 1] if idx_in_parts + 1 < len(parts) else None
            if part not in cur or not isinstance(cur[part], (dict, list)):
                cur[part] = [] if isinstance(nxt_part, int) else {}
            cur = cur[part]

    last = parts[-1]
    if isinstance(last, int):
        while len(cur) <= last:
            cur.append(None)
        cur[last] = value
    else:
        cur[last] = value


def deep_merge(target: dict[str, Any], patch: dict[str, Any]) -> int:
    """Deep-merge patch into target; returns count of scalar values applied."""
    count = 0
    for key, val in patch.items():
        if val is _SKIP:
            continue
        if isinstance(val, dict):
            if key not in target or not isinstance(target[key], dict):
                target[key] = {}
            count += deep_merge(target[key], val)
        elif isinstance(val, list):
            if key not in target or not isinstance(target[key], list):
                target[key] = []
            for i, item in enumerate(val):
                if item is _SKIP:
                    continue
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


def count_patch_leaves(patch: dict[str, Any]) -> int:
    n = 0
    for val in patch.values():
        if val is _SKIP:
            continue
        if isinstance(val, dict):
            n += count_patch_leaves(val)
        elif isinstance(val, list):
            for item in val:
                if item is _SKIP:
                    continue
                if isinstance(item, dict):
                    n += count_patch_leaves(item)
                else:
                    n += 1
        else:
            n += 1
    return n


# fmt: off
PATCHES: dict[str, dict[str, Any]] = {
    "ja": {
        "meta": {
            "description": "定型文、住所、連絡先、URL、絵文字、ハッシュタグなど、よく使う内容を保存してタップひとつでコピー。あとはいつものアプリに貼り付けるだけ。MyQuickPasteはスマートフォンの入力をシンプルにします。",
            "ogDescription": "よく使う文字や情報を保存して、必要な時にタップひとつでコピー。あとはいつものアプリに貼り付けるだけ。",
        },
        "hero": {
            "catchLine1": "よく使う文字を、",
            "catchLine2": "タップひとつで。",
            "lead": "定型文、住所、連絡先、URL、絵文字、ハッシュタグ。何度も使う内容を保存して、必要なときに一覧からタップひとつでコピー。",
            "sub": "あとは、いつものアプリに切り替えて貼り付けるだけ。",
        },
        "trust": {
            "t1Title": "タップでコピー",
            "t1Text": "保存した行をタップするだけ。",
            "t2Title": "買い切りPro",
            "t2Text": "毎月の支払いはありません。",
            "t3Title": "端末内に保存",
            "t3Text": "登録した内容は端末内で管理。",
            "t4Title": "21言語UI",
            "t4Text": "21言語の画面表示に対応。",
        },
        "pain": {
            "titleLine1": "毎回「どこだっけ？」を、",
            "titleLine2": "なくそう。",
            "lead": "よく使う情報なのに、毎回メモを探したり、長押しで選び直したり、同じ文章を打ち直したり。小さな手間が、毎日積み重なります。",
            "p1Title": "探す",
            "p1Text": "住所や定型文が、どこにあるか分からない。",
            "p2Title": "選ぶ",
            "p2Text": "必要な部分だけ長押しして範囲選択。",
            "p3Title": "打ち直す",
            "p3Text": "返信文やプロフィールを何度も打ち直す。",
            "resolveSub": "探さない。打ち直さない。必要な行をタップするだけ。",
        },
        "steps": {"items": [{"text": "よく使う文章や連絡先などを登録します。"}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "SNSでも",
            "titleLine1": "絵文字も、ハッシュタグも。",
            "titleLine2": "必要な時にすぐコピー。",
            "lead": "お気に入りの絵文字やハッシュタグ、よく使う投稿文を保存。使いたい内容をタップしてコピーし、いつものSNSへ貼り付けるだけ。",
            "points": [
                {"title": "絵文字", "text": "お気に入りを保存"},
                {"title": "投稿文", "text": "よく使う文章を保存"},
                {"title": "ハッシュタグ", "text": "まとめてコピー"},
                {"title": "すぐコピー", "text": "必要な時に1タップ"},
            ],
        },
        "sceneWork": {
            "eyebrow": "仕事でも",
            "titleLine1": "定型文も、連絡先も。",
            "titleLine2": "必要な時にすぐコピー。",
            "lead": "定型文、メールアドレス、電話番号、URLなど、何度も使う情報をひとまとめに。必要な行をタップして、すぐコピーできます。",
            "points": [
                {"title": "定型文", "text": "いつもの返信文"},
                {"title": "メール", "text": "署名や案内文を保存"},
                {"title": "連絡先", "text": "電話番号をすぐコピー"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "毎日の中でも",
            "titleLine1": "住所も、プロフィールも。",
            "titleLine2": "必要な時にすぐコピー。",
            "lead": "自宅の住所、メールアドレス、プロフィール文、よく使う一言。必要なときにタップして、すぐコピーできます。",
        },
        "features": {
            "categoriesLabel": "カテゴリ：フリーワード、定型文、メール、電話、画像、プロフィール",
            "categories": ["フリーワード", "定型文", "メール", "電話", "画像", "プロフィール"],
            "items": [_SKIP, {"text": "フリーワード、定型文、メール、電話、画像、プロフィールに分けて管理できます。"}, _SKIP, _SKIP, _SKIP, {"text": "バックアップを書き出し、必要なときに読み込めます。30日間の無料体験とProで利用できます。"}],
        },
        "themesSection": {"subtitle": "ライト、ダークに加え、Proではプレミアム配色テーマを利用できます。"},
        "comparison": {"appText": "何度も使う文章や情報を、分かりやすく整理して保存できます。"},
        "privacySection": {"points": [_SKIP, "登録内容を外部サーバーへ自動送信しない", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "バックアップを書き出し、必要なときに読み込めます。30日間の無料体験とProで利用できます。"}]},
        "cta": {
            "titleLine1": "よく使う文字を、",
            "titleLine2": "タップひとつで。",
            "title": "よく使う文字を、タップひとつで。",
            "lead": "保存して、タップして、あとは貼り付けるだけ。",
            "button": "30日間の無料体験",
        },
        "sceneMore": {
            "lead": "旅行、フリマ、チャット、幹事まで。よく使う文字を、どんな場面でもタップひとつでコピー。",
            "cap3": "フリマの定型文もすぐコピー",
            "cap4": "チャットの返信もすぐコピー",
            "cap6": "幹事の案内文もすぐコピー",
        },
    },
    "en": {
        "meta": {
            "description": "Save snippets, addresses, contacts, URLs, emoji, hashtags, and more—then copy with one tap. Switch to your usual app and paste. MyQuickPaste makes smartphone typing simpler.",
            "ogDescription": "Save the text and info you reuse, then copy with one tap when you need it. Switch to your usual app and paste.",
        },
        "hero": {
            "catchLine1": "Everyday text,",
            "catchLine2": "one tap away.",
            "lead": "Snippets, addresses, contacts, URLs, emoji, hashtags. Save what you reuse, then copy with one tap from your list when you need it.",
            "sub": "Then switch to your usual app and paste.",
        },
        "trust": {
            "t1Title": "Tap to copy",
            "t1Text": "Just tap a saved row.",
            "t2Title": "One-time Pro",
            "t2Text": "No monthly payments.",
            "t3Title": "Stored on device",
            "t3Text": "Your saved content is managed on device.",
            "t4Title": "21-language UI",
            "t4Text": "App screens in 21 languages.",
        },
        "pain": {
            "titleLine1": "Stop asking yourself,",
            "titleLine2": "\"Where was that?\"",
            "lead": "You reuse the same info—yet every time you search notes, long-press to reselect, or retype the same text. Those small steps add up every day.",
            "p1Title": "Search",
            "p1Text": "You can't find which note holds the address or snippet.",
            "p2Title": "Select",
            "p2Text": "Long-press again to grab just the part you need.",
            "p3Title": "Type again",
            "p3Text": "You retype the same reply or profile over and over.",
            "resolveSub": "Don't search. Don't retype. Just tap the row you need.",
        },
        "steps": {"items": [{"text": "Register your go-to text, contacts, and more."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "For social too",
            "titleLine1": "Emoji and hashtags—",
            "titleLine2": "copy when you need them.",
            "lead": "Save favorite emoji, hashtags, and go-to posts. Tap to copy what you need, then paste into your usual social apps.",
            "points": [
                {"title": "Emoji", "text": "Save favorites"},
                {"title": "Posts", "text": "Save go-to captions"},
                {"title": "Hashtags", "text": "Copy as a set"},
                {"title": "Quick copy", "text": "One tap when needed"},
            ],
        },
        "sceneWork": {
            "eyebrow": "At work too",
            "titleLine1": "Snippets and contacts—",
            "titleLine2": "copy when you need them.",
            "lead": "Keep snippets, email addresses, phone numbers, URLs, and other info you reuse in one place. Tap a row to copy instantly.",
            "points": [
                {"title": "Snippets", "text": "Your usual replies"},
                {"title": "Email", "text": "Save signatures and notices"},
                {"title": "Contacts", "text": "Copy phone numbers fast"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "In daily life",
            "titleLine1": "Address and profile—",
            "titleLine2": "copy when you need them.",
            "lead": "Home address, email, profile bio, favorite lines. Tap when you need them and copy instantly.",
        },
        "features": {
            "categoriesLabel": "Categories: Free text, Snippets, Email, Phone, Images, Profile",
            "categories": ["Free text", "Snippets", "Email", "Phone", "Images", "Profile"],
            "items": [_SKIP, {"text": "Organize by free text, snippets, email, phone, images, and profile."}, _SKIP, _SKIP, _SKIP, {"text": "Export backups and import when needed. Available with the 30-day free trial and Pro."}],
        },
        "themesSection": {"subtitle": "Light and dark, plus premium color themes with Pro."},
        "comparison": {"appText": "Organize and save the text and info you reuse, clearly and easily."},
        "privacySection": {"points": [_SKIP, "Does not auto-send saved content to external servers", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Export backups and import when needed. Available with the 30-day free trial and Pro."}]},
        "cta": {
            "titleLine1": "Everyday text,",
            "titleLine2": "one tap away.",
            "title": "Everyday text, one tap away.",
            "lead": "Save, tap, then paste.",
            "button": "30-day free trial",
        },
        "sceneMore": {
            "lead": "Travel, resale apps, chat, event planning—copy your go-to text with one tap, anywhere.",
            "cap3": "Copy resale listing snippets instantly",
            "cap4": "Copy chat replies instantly",
            "cap6": "Copy organizer notices instantly",
        },
    },
    "fr": {
        "meta": {
            "description": "Enregistrez textes types, adresses, contacts, URL, emoji, hashtags et plus—puis copiez d'un tap. Basculez vers votre appli habituelle et collez. MyQuickPaste simplifie la saisie sur smartphone.",
            "ogDescription": "Enregistrez les textes et infos que vous réutilisez, puis copiez d'un tap quand vous en avez besoin. Basculez vers votre appli habituelle et collez.",
        },
        "hero": {
            "catchLine1": "Vos textes du quotidien,",
            "catchLine2": "en un tap.",
            "lead": "Textes types, adresses, contacts, URL, emoji, hashtags. Enregistrez ce que vous réutilisez, puis copiez d'un tap depuis la liste quand vous en avez besoin.",
            "sub": "Ensuite, basculez vers votre appli habituelle et collez.",
        },
        "trust": {
            "t1Title": "Toucher pour copier",
            "t1Text": "Il suffit de toucher une ligne enregistrée.",
            "t2Title": "Pro à l'achat",
            "t2Text": "Aucun paiement mensuel.",
            "t3Title": "Stocké sur l'appareil",
            "t3Text": "Vos contenus enregistrés sont gérés sur l'appareil.",
            "t4Title": "Interface en 21 langues",
            "t4Text": "Écrans disponibles en 21 langues.",
        },
        "pain": {
            "titleLine1": "Fini de vous demander",
            "titleLine2": "« Où c'était déjà ? »",
            "lead": "Vous réutilisez les mêmes infos—pourtant à chaque fois vous cherchez dans vos notes, refaites une sélection au long appui ou retapez le même texte. Ces petites étapes s'accumulent.",
            "p1Title": "Chercher",
            "p1Text": "Vous ne savez plus quelle note contient l'adresse ou le texte type.",
            "p2Title": "Sélectionner",
            "p2Text": "Un long appui pour ne prendre que la partie utile.",
            "p3Title": "Retaper",
            "p3Text": "Vous retapez la même réponse ou le même profil encore et encore.",
            "resolveSub": "Ne cherchez plus. Ne retapez plus. Touchez simplement la ligne dont vous avez besoin.",
        },
        "steps": {"items": [{"text": "Enregistrez vos textes habituels, contacts et plus encore."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Sur les réseaux aussi",
            "titleLine1": "Emoji et hashtags—",
            "titleLine2": "copiez quand vous en avez besoin.",
            "lead": "Enregistrez vos emoji, hashtags et textes de publication favoris. Touchez pour copier, puis collez dans vos applis sociales habituelles.",
            "points": [
                {"title": "Emoji", "text": "Enregistrez vos favoris"},
                {"title": "Publications", "text": "Enregistrez vos textes habituels"},
                {"title": "Hashtags", "text": "Copiez en bloc"},
                {"title": "Copie rapide", "text": "Un tap quand il le faut"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Au travail aussi",
            "titleLine1": "Textes types et contacts—",
            "titleLine2": "copiez quand vous en avez besoin.",
            "lead": "Textes types, adresses e-mail, numéros de téléphone, URL et autres infos réutilisées, réunis au même endroit. Touchez une ligne pour copier instantanément.",
            "points": [
                {"title": "Textes types", "text": "Vos réponses habituelles"},
                {"title": "E-mail", "text": "Enregistrez signatures et notices"},
                {"title": "Contacts", "text": "Copiez les numéros rapidement"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "Au quotidien",
            "titleLine1": "Adresse et profil—",
            "titleLine2": "copiez quand vous en avez besoin.",
            "lead": "Adresse du domicile, e-mail, bio de profil, phrases favorites. Touchez pour copier instantanément quand vous en avez besoin.",
        },
        "features": {
            "categoriesLabel": "Catégories : Texte libre, Textes types, E-mail, Téléphone, Images, Profil",
            "categories": ["Texte libre", "Textes types", "E-mail", "Téléphone", "Images", "Profil"],
            "items": [_SKIP, {"text": "Organisez par texte libre, textes types, e-mail, téléphone, images et profil."}, _SKIP, _SKIP, _SKIP, {"text": "Exportez des sauvegardes et importez-les au besoin. Disponible avec l'essai gratuit de 30 jours et Pro."}],
        },
        "themesSection": {"subtitle": "Clair et sombre, plus des thèmes premium avec Pro."},
        "comparison": {"appText": "Organisez et enregistrez clairement les textes et infos que vous réutilisez."},
        "privacySection": {"points": [_SKIP, "N'envoie pas automatiquement vos contenus enregistrés vers des serveurs externes", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Exportez des sauvegardes et importez-les au besoin. Disponible avec l'essai gratuit de 30 jours et Pro."}]},
        "cta": {
            "titleLine1": "Vos textes du quotidien,",
            "titleLine2": "en un tap.",
            "title": "Vos textes du quotidien, en un tap.",
            "lead": "Enregistrer, toucher, puis coller.",
            "button": "30 jours d'essai gratuit",
        },
        "sceneMore": {
            "lead": "Voyage, vente entre particuliers, chat, organisation d'événements—copiez vos textes favoris d'un tap, partout.",
            "cap3": "Copiez vite vos textes pour les annonces",
            "cap4": "Copiez vos réponses de chat instantanément",
            "cap6": "Copiez vos messages d'organisateur instantanément",
        },
    },
    "de": {
        "meta": {
            "description": "Speichern Sie Textbausteine, Adressen, Kontakte, URLs, Emoji, Hashtags und mehr—kopieren Sie mit einem Tipp. Wechseln Sie zur gewohnten App und fügen ein. MyQuickPaste macht Smartphone-Tippen einfacher.",
            "ogDescription": "Speichern Sie oft genutzte Texte und Infos und kopieren Sie sie bei Bedarf mit einem Tipp. Wechseln Sie zur gewohnten App und fügen ein.",
        },
        "hero": {
            "catchLine1": "Alltagstexte,",
            "catchLine2": "ein Tipp entfernt.",
            "lead": "Textbausteine, Adressen, Kontakte, URLs, Emoji, Hashtags. Speichern Sie Wiederholtes und kopieren Sie bei Bedarf mit einem Tipp aus der Liste.",
            "sub": "Dann wechseln Sie zur gewohnten App und fügen ein.",
        },
        "trust": {
            "t1Title": "Tippen zum Kopieren",
            "t1Text": "Einfach eine gespeicherte Zeile antippen.",
            "t2Title": "Pro einmalig",
            "t2Text": "Keine monatlichen Zahlungen.",
            "t3Title": "Auf dem Gerät gespeichert",
            "t3Text": "Gespeicherte Inhalte werden auf dem Gerät verwaltet.",
            "t4Title": "UI in 21 Sprachen",
            "t4Text": "App-Oberfläche in 21 Sprachen.",
        },
        "pain": {
            "titleLine1": "Schluss mit",
            "titleLine2": "„Wo war das noch?“",
            "lead": "Immer wieder dieselben Infos—doch jedes Mal suchen Sie in Notizen, wählen per Long-Press neu oder tippen denselben Text erneut. Kleine Schritte, die sich summieren.",
            "p1Title": "Suchen",
            "p1Text": "Adresse oder Textbaustein—Sie wissen nicht, in welcher Notiz sie stehen.",
            "p2Title": "Auswählen",
            "p2Text": "Long-Press, um genau den Teil zu markieren, den Sie brauchen.",
            "p3Title": "Nochmal tippen",
            "p3Text": "Dieselbe Antwort oder dasselbe Profil tippen Sie immer wieder neu.",
            "resolveSub": "Nicht suchen. Nicht neu tippen. Einfach die Zeile antippen, die Sie brauchen.",
        },
        "steps": {"items": [{"text": "Registrieren Sie häufig genutzte Texte, Kontakte und mehr."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Auch für Social Media",
            "titleLine1": "Emoji und Hashtags—",
            "titleLine2": "kopieren, wenn Sie sie brauchen.",
            "lead": "Speichern Sie Lieblings-Emoji, Hashtags und Beitragstexte. Antippen zum Kopieren, dann in Ihre Social Apps einfügen.",
            "points": [
                {"title": "Emoji", "text": "Favoriten speichern"},
                {"title": "Beiträge", "text": "Häufige Texte speichern"},
                {"title": "Hashtags", "text": "Als Set kopieren"},
                {"title": "Schnell kopieren", "text": "Ein Tipp bei Bedarf"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Auch bei der Arbeit",
            "titleLine1": "Textbausteine und Kontakte—",
            "titleLine2": "kopieren, wenn Sie sie brauchen.",
            "lead": "Textbausteine, E-Mail-Adressen, Telefonnummern, URLs und andere oft genutzte Infos an einem Ort. Zeile antippen und sofort kopieren.",
            "points": [
                {"title": "Textbausteine", "text": "Ihre üblichen Antworten"},
                {"title": "E-Mail", "text": "Signaturen und Hinweise speichern"},
                {"title": "Kontakte", "text": "Telefonnummern schnell kopieren"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "Im Alltag",
            "titleLine1": "Adresse und Profil—",
            "titleLine2": "kopieren, wenn Sie sie brauchen.",
            "lead": "Heimadresse, E-Mail, Profiltext, Lieblingszeilen. Antippen und sofort kopieren, wenn Sie sie brauchen.",
        },
        "features": {
            "categoriesLabel": "Kategorien: Freitext, Textbausteine, E-Mail, Telefon, Bilder, Profil",
            "categories": ["Freitext", "Textbausteine", "E-Mail", "Telefon", "Bilder", "Profil"],
            "items": [_SKIP, {"text": "Verwalten Sie nach Freitext, Textbausteinen, E-Mail, Telefon, Bildern und Profil."}, _SKIP, _SKIP, _SKIP, {"text": "Backups exportieren und bei Bedarf importieren. Verfügbar mit 30-tägiger Testphase und Pro."}],
        },
        "themesSection": {"subtitle": "Hell und dunkel, plus Premium-Farbthemen mit Pro."},
        "comparison": {"appText": "Speichern Sie oft genutzte Texte und Infos übersichtlich und klar organisiert."},
        "privacySection": {"points": [_SKIP, "Sendet gespeicherte Inhalte nicht automatisch an externe Server", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Backups exportieren und bei Bedarf importieren. Verfügbar mit 30-tägiger Testphase und Pro."}]},
        "cta": {
            "titleLine1": "Alltagstexte,",
            "titleLine2": "ein Tipp entfernt.",
            "title": "Alltagstexte, ein Tipp entfernt.",
            "lead": "Speichern, tippen, dann einfügen.",
            "button": "30 Tage kostenlos testen",
        },
        "sceneMore": {
            "lead": "Reise, Flohmarkt-Apps, Chat, Eventplanung—Ihre Standardtexte immer nur einen Tipp entfernt.",
            "cap3": "Anzeigentexte blitzschnell kopieren",
            "cap4": "Chat-Antworten sofort kopieren",
            "cap6": "Organisatortexte sofort kopieren",
        },
    },
    "zh": {
        "meta": {
            "description": "保存常用语、地址、联系人、URL、表情、话题标签等内容，一键复制。切换到常用应用粘贴即可。MyQuickPaste 让手机输入更简单。",
            "ogDescription": "保存常用文字和信息，需要时一键复制。切换到常用应用粘贴即可。",
        },
        "hero": {
            "catchLine1": "常用文字，",
            "catchLine2": "一键复制。",
            "lead": "常用语、地址、联系人、URL、表情、话题标签。保存反复使用的内容，需要时从列表一键复制。",
            "sub": "然后切换到常用应用，粘贴即可。",
        },
        "trust": {
            "t1Title": "点击复制",
            "t1Text": "只需点击已保存的行。",
            "t2Title": "Pro 一次性购买",
            "t2Text": "无需按月付费。",
            "t3Title": "保存在设备内",
            "t3Text": "注册内容在设备内管理。",
            "t4Title": "21 种语言界面",
            "t4Text": "支持 21 种语言的界面显示。",
        },
        "pain": {
            "titleLine1": "别再每次都想",
            "titleLine2": "「放哪了？」",
            "lead": "经常用的信息，却每次都要翻备忘录、长按重选、反复输入相同文字。这些小步骤每天都在累积。",
            "p1Title": "查找",
            "p1Text": "地址或常用语，不知道在哪个备忘录里。",
            "p2Title": "选择",
            "p2Text": "长按选取，只要需要的部分。",
            "p3Title": "再次输入",
            "p3Text": "回复语或个人简介，反复在键盘上重打。",
            "resolveSub": "不用找。不用重打。点击需要的行即可。",
        },
        "steps": {"items": [{"text": "注册常用文字、联系人等内容。"}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "社交媒体也适用",
            "titleLine1": "表情和话题标签—",
            "titleLine2": "需要时立刻复制。",
            "lead": "保存常用表情、话题标签和发帖文字。点击复制，粘贴到常用社交应用即可。",
            "points": [
                {"title": "表情", "text": "保存收藏"},
                {"title": "发帖", "text": "保存常用文字"},
                {"title": "话题标签", "text": "整组复制"},
                {"title": "快速复制", "text": "需要时一键完成"},
            ],
        },
        "sceneWork": {
            "eyebrow": "工作也适用",
            "titleLine1": "常用语和联系人—",
            "titleLine2": "需要时立刻复制。",
            "lead": "常用语、邮箱、电话号码、URL 等反复使用的信息集中管理。点击行即可立即复制。",
            "points": [
                {"title": "常用语", "text": "日常回复语"},
                {"title": "邮件", "text": "保存签名和说明"},
                {"title": "联系人", "text": "快速复制电话号码"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "日常生活中",
            "titleLine1": "地址和个人简介—",
            "titleLine2": "需要时立刻复制。",
            "lead": "家庭地址、邮箱、个人简介、常用短语。需要时点击即可立即复制。",
        },
        "features": {
            "categoriesLabel": "分类：自由文字、常用语、邮件、电话、图片、个人资料",
            "categories": ["自由文字", "常用语", "邮件", "电话", "图片", "个人资料"],
            "items": [_SKIP, {"text": "可按自由文字、常用语、邮件、电话、图片、个人资料分类管理。"}, _SKIP, _SKIP, _SKIP, {"text": "可导出备份并在需要时导入。30 天免费体验与 Pro 可用。"}],
        },
        "themesSection": {"subtitle": "浅色与深色，Pro 还可使用高级配色主题。"},
        "comparison": {"appText": "清晰整理并保存反复使用的文字和信息。"},
        "privacySection": {"points": [_SKIP, "不会自动将注册内容发送到外部服务器", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "可导出备份并在需要时导入。30 天免费体验与 Pro 可用。"}]},
        "cta": {
            "titleLine1": "常用文字，",
            "titleLine2": "一键复制。",
            "title": "常用文字，一键复制。",
            "lead": "保存、点击，然后粘贴。",
            "button": "30 天免费体验",
        },
        "sceneMore": {
            "lead": "旅行、二手交易、聊天、活动组织—任何场景都能一键复制常用文字。",
            "cap3": "二手平台常用语，立刻复制",
            "cap4": "聊天回复，立刻复制",
            "cap6": "活动通知，立刻复制",
        },
    },
    "zh_TW": {
        "meta": {
            "description": "儲存常用語、地址、聯絡人、URL、表情符號、主題標籤等內容，一鍵複製。切換到常用 App 貼上即可。MyQuickPaste 讓手機輸入更簡單。",
            "ogDescription": "儲存常用文字和資訊，需要時一鍵複製。切換到常用 App 貼上即可。",
        },
        "hero": {
            "catchLine1": "常用文字，",
            "catchLine2": "一鍵複製。",
            "lead": "常用語、地址、聯絡人、URL、表情符號、主題標籤。儲存反覆使用的內容，需要時從清單一鍵複製。",
            "sub": "然後切換到常用 App，貼上即可。",
        },
        "trust": {
            "t1Title": "點擊複製",
            "t1Text": "只需點擊已儲存的列。",
            "t2Title": "Pro 買斷",
            "t2Text": "無需按月付費。",
            "t3Title": "儲存在裝置內",
            "t3Text": "註冊內容在裝置內管理。",
            "t4Title": "21 種語言介面",
            "t4Text": "支援 21 種語言的畫面顯示。",
        },
        "pain": {
            "titleLine1": "別再每次都想",
            "titleLine2": "「放哪了？」",
            "lead": "經常用的資訊，卻每次都要翻備忘錄、長按重選、反覆輸入相同文字。這些小步驟每天都在累積。",
            "p1Title": "查找",
            "p1Text": "地址或常用語，不知道在哪則備忘錄裡。",
            "p2Title": "選取",
            "p2Text": "長按選取，只要需要的部分。",
            "p3Title": "再次輸入",
            "p3Text": "回覆語或個人簡介，反覆在鍵盤上重打。",
            "resolveSub": "不用找。不用重打。點擊需要的列即可。",
        },
        "steps": {"items": [{"text": "註冊常用文字、聯絡人等內容。"}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "社群媒體也適用",
            "titleLine1": "表情符號和主題標籤—",
            "titleLine2": "需要時立刻複製。",
            "lead": "儲存常用表情符號、主題標籤和貼文文字。點擊複製，貼到常用社群 App 即可。",
            "points": [
                {"title": "表情符號", "text": "儲存收藏"},
                {"title": "貼文", "text": "儲存常用文字"},
                {"title": "主題標籤", "text": "整組複製"},
                {"title": "快速複製", "text": "需要時一鍵完成"},
            ],
        },
        "sceneWork": {
            "eyebrow": "工作也適用",
            "titleLine1": "常用語和聯絡人—",
            "titleLine2": "需要時立刻複製。",
            "lead": "常用語、電子郵件、電話號碼、URL 等反覆使用的資訊集中管理。點擊列即可立即複製。",
            "points": [
                {"title": "常用語", "text": "日常回覆語"},
                {"title": "郵件", "text": "儲存簽名和說明"},
                {"title": "聯絡人", "text": "快速複製電話號碼"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "日常生活中",
            "titleLine1": "地址和個人簡介—",
            "titleLine2": "需要時立刻複製。",
            "lead": "住家地址、電子郵件、個人簡介、常用短語。需要時點擊即可立即複製。",
        },
        "features": {
            "categoriesLabel": "分類：自由文字、常用語、郵件、電話、圖片、個人資料",
            "categories": ["自由文字", "常用語", "郵件", "電話", "圖片", "個人資料"],
            "items": [_SKIP, {"text": "可按自由文字、常用語、郵件、電話、圖片、個人資料分類管理。"}, _SKIP, _SKIP, _SKIP, {"text": "可匯出備份並在需要時匯入。30 天免費體驗與 Pro 可用。"}],
        },
        "themesSection": {"subtitle": "淺色與深色，Pro 還可使用進階配色主題。"},
        "comparison": {"appText": "清晰整理並儲存反覆使用的文字和資訊。"},
        "privacySection": {"points": [_SKIP, "不會自動將註冊內容傳送到外部伺服器", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "可匯出備份並在需要時匯入。30 天免費體驗與 Pro 可用。"}]},
        "cta": {
            "titleLine1": "常用文字，",
            "titleLine2": "一鍵複製。",
            "title": "常用文字，一鍵複製。",
            "lead": "儲存、點擊，然後貼上。",
            "button": "30 天免費體驗",
        },
        "sceneMore": {
            "lead": "旅行、二手交易、聊天、活動組織—任何場景都能一鍵複製常用文字。",
            "cap3": "二手平台常用語，立刻複製",
            "cap4": "聊天回覆，立刻複製",
            "cap6": "活動通知，立刻複製",
        },
    },
    "ko": {
        "meta": {
            "description": "상용구, 주소, 연락처, URL, 이모지, 해시태그 등 자주 쓰는 내용을 저장하고 탭 한 번에 복사하세요. 평소 쓰는 앱으로 전환해 붙여넣기만 하면 됩니다. MyQuickPaste는 스마트폰 입력을 더 간단하게 만듭니다.",
            "ogDescription": "자주 쓰는 글과 정보를 저장하고, 필요할 때 탭 한 번에 복사하세요. 평소 쓰는 앱으로 전환해 붙여넣기만 하면 됩니다.",
        },
        "hero": {
            "catchLine1": "자주 쓰는 글을,",
            "catchLine2": "탭 한 번으로.",
            "lead": "상용구, 주소, 연락처, URL, 이모지, 해시태그. 자주 쓰는 내용을 저장하고, 필요할 때 목록에서 탭 한 번에 복사.",
            "sub": "그다음 평소 쓰는 앱으로 전환해 붙여넣기만 하면 됩니다.",
        },
        "trust": {
            "t1Title": "탭으로 복사",
            "t1Text": "저장한 행을 탭하기만 하면 됩니다.",
            "t2Title": "일회성 Pro",
            "t2Text": "월별 결제가 없습니다.",
            "t3Title": "기기 내 저장",
            "t3Text": "등록한 내용은 기기 내에서 관리됩니다.",
            "t4Title": "21개 언어 UI",
            "t4Text": "21개 언어 화면을 지원합니다.",
        },
        "pain": {
            "titleLine1": "매번 「어디 있더라?」",
            "titleLine2": "그만하세요.",
            "lead": "자주 쓰는 정보인데 매번 메모를 찾고, 길게 눌러 다시 선택하고, 같은 글을 다시 입력합니다. 작은 수고가 매일 쌓입니다.",
            "p1Title": "찾기",
            "p1Text": "주소나 상용구가 어디에 있는지 모릅니다.",
            "p2Title": "선택",
            "p2Text": "필요한 부분만 길게 눌러 범위 선택.",
            "p3Title": "다시 입력",
            "p3Text": "답장이나 프로필을 키보드로 반복 입력.",
            "resolveSub": "찾지 않습니다. 다시 입력하지 않습니다. 필요한 행을 탭하기만 하면 됩니다.",
        },
        "steps": {"items": [{"text": "자주 쓰는 글, 연락처 등을 등록합니다."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "SNS에서도",
            "titleLine1": "이모지와 해시태그—",
            "titleLine2": "필요할 때 바로 복사.",
            "lead": "즐겨찾는 이모지, 해시태그, 자주 쓰는 게시글을 저장하세요. 탭해서 복사하고 평소 쓰는 SNS에 붙여넣기만 하면 됩니다.",
            "points": [
                {"title": "이모지", "text": "즐겨찾기 저장"},
                {"title": "게시글", "text": "자주 쓰는 글 저장"},
                {"title": "해시태그", "text": "한꺼번에 복사"},
                {"title": "빠른 복사", "text": "필요할 때 탭 한 번"},
            ],
        },
        "sceneWork": {
            "eyebrow": "업무에서도",
            "titleLine1": "상용구와 연락처—",
            "titleLine2": "필요할 때 바로 복사.",
            "lead": "상용구, 이메일, 전화번호, URL 등 자주 쓰는 정보를 한곳에 모으세요. 행을 탭하면 바로 복사할 수 있습니다.",
            "points": [
                {"title": "상용구", "text": "평소 답장"},
                {"title": "이메일", "text": "서명과 안내문 저장"},
                {"title": "연락처", "text": "전화번호 빠르게 복사"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "일상에서도",
            "titleLine1": "주소와 프로필—",
            "titleLine2": "필요할 때 바로 복사.",
            "lead": "집 주소, 이메일, 프로필 문구, 자주 쓰는 한마디. 필요할 때 탭해서 바로 복사할 수 있습니다.",
        },
        "features": {
            "categoriesLabel": "카테고리: 자유 입력, 상용구, 이메일, 전화, 이미지, 프로필",
            "categories": ["자유 입력", "상용구", "이메일", "전화", "이미지", "프로필"],
            "items": [_SKIP, {"text": "자유 입력, 상용구, 이메일, 전화, 이미지, 프로필로 나눠 관리할 수 있습니다."}, _SKIP, _SKIP, _SKIP, {"text": "백업을 내보내고 필요할 때 불러올 수 있습니다. 30일 무료 체험과 Pro에서 이용 가능합니다."}],
        },
        "themesSection": {"subtitle": "라이트, 다크에 더해 Pro에서는 프리미엄 색상 테마를 이용할 수 있습니다."},
        "comparison": {"appText": "자주 쓰는 글과 정보를 알기 쉽게 정리해 저장할 수 있습니다."},
        "privacySection": {"points": [_SKIP, "등록 내용을 외부 서버로 자동 전송하지 않음", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "백업을 내보내고 필요할 때 불러올 수 있습니다. 30일 무료 체험과 Pro에서 이용 가능합니다."}]},
        "cta": {
            "titleLine1": "자주 쓰는 글을,",
            "titleLine2": "탭 한 번으로.",
            "title": "자주 쓰는 글을, 탭 한 번으로.",
            "lead": "저장하고, 탭하고, 붙여넣기만 하면 됩니다.",
            "button": "30일 무료 체험",
        },
        "sceneMore": {
            "lead": "여행, 중고 거래, 채팅, 행사 준비까지. 어떤 상황에서도 자주 쓰는 글을 탭 한 번에 복사.",
            "cap3": "중고 거래 상용구, 바로 복사",
            "cap4": "채팅 답장, 바로 복사",
            "cap6": "행사 안내문, 바로 복사",
        },
    },
    "ru": {
        "meta": {
            "description": "Сохраняйте шаблоны, адреса, контакты, URL, эмодзи, хештеги и другое—копируйте одним нажатием. Переключитесь в привычное приложение и вставьте. MyQuickPaste упрощает ввод на смартфоне.",
            "ogDescription": "Сохраняйте часто используемые тексты и данные, копируйте одним нажатием, когда нужно. Переключитесь в привычное приложение и вставьте.",
        },
        "hero": {
            "catchLine1": "Частые тексты—",
            "catchLine2": "одним нажатием.",
            "lead": "Шаблоны, адреса, контакты, URL, эмодзи, хештеги. Сохраните то, что часто используете, и копируйте одним нажатием из списка, когда нужно.",
            "sub": "Затем переключитесь в привычное приложение и вставьте.",
        },
        "trust": {
            "t1Title": "Нажмите, чтобы скопировать",
            "t1Text": "Просто нажмите на сохранённую строку.",
            "t2Title": "Pro разово",
            "t2Text": "Без ежемесячных платежей.",
            "t3Title": "Хранение на устройстве",
            "t3Text": "Сохранённое содержимое управляется на устройстве.",
            "t4Title": "Интерфейс на 21 языке",
            "t4Text": "Экраны приложения на 21 языке.",
        },
        "pain": {
            "titleLine1": "Хватит каждый раз думать:",
            "titleLine2": "«Где это было?»",
            "lead": "Одна и та же информация — а каждый раз вы ищете в заметках, заново выделяете долгим нажатием или перепечатываете тот же текст. Мелкие шаги копятся каждый день.",
            "p1Title": "Искать",
            "p1Text": "Адрес или шаблон — непонятно, в какой заметке.",
            "p2Title": "Выделять",
            "p2Text": "Долгое нажатие, чтобы взять только нужную часть.",
            "p3Title": "Вводить снова",
            "p3Text": "Один и тот же ответ или профиль набираете снова и снова.",
            "resolveSub": "Не ищите. Не перепечатывайте. Просто нажмите нужную строку.",
        },
        "steps": {"items": [{"text": "Зарегистрируйте часто используемые тексты, контакты и другое."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "И для соцсетей",
            "titleLine1": "Эмодзи и хештеги—",
            "titleLine2": "копируйте, когда нужно.",
            "lead": "Сохраняйте любимые эмодзи, хештеги и тексты постов. Нажмите, чтобы скопировать, и вставьте в привычные соцприложения.",
            "points": [
                {"title": "Эмодзи", "text": "Сохраняйте избранное"},
                {"title": "Посты", "text": "Сохраняйте частые тексты"},
                {"title": "Хештеги", "text": "Копируйте набором"},
                {"title": "Быстрое копирование", "text": "Одно нажатие, когда нужно"},
            ],
        },
        "sceneWork": {
            "eyebrow": "И на работе",
            "titleLine1": "Шаблоны и контакты—",
            "titleLine2": "копируйте, когда нужно.",
            "lead": "Шаблоны, адреса e-mail, телефоны, URL и другая часто используемая информация в одном месте. Нажмите строку — и сразу скопируйте.",
            "points": [
                {"title": "Шаблоны", "text": "Ваши обычные ответы"},
                {"title": "E-mail", "text": "Сохраняйте подписи и уведомления"},
                {"title": "Контакты", "text": "Быстро копируйте номера"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "В повседневной жизни",
            "titleLine1": "Адрес и профиль—",
            "titleLine2": "копируйте, когда нужно.",
            "lead": "Домашний адрес, e-mail, текст профиля, любимые фразы. Нажмите и сразу скопируйте, когда нужно.",
        },
        "features": {
            "categoriesLabel": "Категории: Свободный текст, Шаблоны, E-mail, Телефон, Изображения, Профиль",
            "categories": ["Свободный текст", "Шаблоны", "E-mail", "Телефон", "Изображения", "Профиль"],
            "items": [_SKIP, {"text": "Управляйте по категориям: свободный текст, шаблоны, e-mail, телефон, изображения, профиль."}, _SKIP, _SKIP, _SKIP, {"text": "Экспортируйте резервные копии и импортируйте при необходимости. Доступно в 30-дневной пробной версии и Pro."}],
        },
        "themesSection": {"subtitle": "Светлая и тёмная темы, а также премиальные цветовые темы в Pro."},
        "comparison": {"appText": "Удобно организуйте и сохраняйте часто используемые тексты и данные."},
        "privacySection": {"points": [_SKIP, "Не отправляет сохранённое содержимое автоматически на внешние серверы", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Экспортируйте резервные копии и импортируйте при необходимости. Доступно в 30-дневной пробной версии и Pro."}]},
        "cta": {
            "titleLine1": "Частые тексты—",
            "titleLine2": "одним нажатием.",
            "title": "Частые тексты—одним нажатием.",
            "lead": "Сохранить, нажать, затем вставить.",
            "button": "30 дней бесплатно",
        },
        "sceneMore": {
            "lead": "Путешествия, барахолки, чаты, организация мероприятий—копируйте нужный текст одним нажатием в любой ситуации.",
            "cap3": "Тексты объявлений — мгновенно",
            "cap4": "Ответы в чате — мгновенно",
            "cap6": "Тексты для организатора — мгновенно",
        },
    },
    "it": {
        "meta": {
            "description": "Salva testi standard, indirizzi, contatti, URL, emoji, hashtag e altro—poi copia con un tap. Passa all'app che usi di solito e incolla. MyQuickPaste semplifica la digitazione su smartphone.",
            "ogDescription": "Salva testi e informazioni che riusi, poi copia con un tap quando ti servono. Passa all'app che usi di solito e incolla.",
        },
        "hero": {
            "catchLine1": "I testi di ogni giorno,",
            "catchLine2": "a un tap di distanza.",
            "lead": "Testi standard, indirizzi, contatti, URL, emoji, hashtag. Salva ciò che riusi e copia con un tap dalla lista quando ti serve.",
            "sub": "Poi passa all'app che usi di solito e incolla.",
        },
        "trust": {
            "t1Title": "Tocca per copiare",
            "t1Text": "Basta toccare una riga salvata.",
            "t2Title": "Pro una tantum",
            "t2Text": "Nessun pagamento mensile.",
            "t3Title": "Salvato sul dispositivo",
            "t3Text": "I contenuti registrati sono gestiti sul dispositivo.",
            "t4Title": "Interfaccia in 21 lingue",
            "t4Text": "Schermate dell'app in 21 lingue.",
        },
        "pain": {
            "titleLine1": "Basta chiedersi",
            "titleLine2": "«Dov'era?» ogni volta.",
            "lead": "Le stesse informazioni—eppure ogni volta cerchi nelle note, riselezioni con pressione prolungata o riscrivi lo stesso testo. Piccoli passi che si accumulano ogni giorno.",
            "p1Title": "Cercare",
            "p1Text": "Indirizzo o testo standard: non sai in quale nota si trova.",
            "p2Title": "Selezionare",
            "p2Text": "Pressione prolungata per prendere solo la parte che ti serve.",
            "p3Title": "Riscrivere",
            "p3Text": "Riscrivi la stessa risposta o lo stesso profilo più volte.",
            "resolveSub": "Non cercare. Non riscrivere. Tocca semplicemente la riga che ti serve.",
        },
        "steps": {"items": [{"text": "Registra testi abituali, contatti e altro."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Anche sui social",
            "titleLine1": "Emoji e hashtag—",
            "titleLine2": "copia quando ti servono.",
            "lead": "Salva emoji, hashtag e testi di post preferiti. Tocca per copiare, poi incolla nelle tue app social abituali.",
            "points": [
                {"title": "Emoji", "text": "Salva i preferiti"},
                {"title": "Post", "text": "Salva testi abituali"},
                {"title": "Hashtag", "text": "Copia in blocco"},
                {"title": "Copia rapida", "text": "Un tap quando serve"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Anche al lavoro",
            "titleLine1": "Testi standard e contatti—",
            "titleLine2": "copia quando ti servono.",
            "lead": "Testi standard, e-mail, numeri di telefono, URL e altre info riutilizzate in un unico posto. Tocca una riga per copiare subito.",
            "points": [
                {"title": "Testi standard", "text": "Le tue risposte abituali"},
                {"title": "E-mail", "text": "Salva firme e avvisi"},
                {"title": "Contatti", "text": "Copia i numeri rapidamente"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "Nella vita quotidiana",
            "titleLine1": "Indirizzo e profilo—",
            "titleLine2": "copia quando ti servono.",
            "lead": "Indirizzo di casa, e-mail, bio del profilo, frasi preferite. Tocca e copia subito quando ti servono.",
        },
        "features": {
            "categoriesLabel": "Categorie: Testo libero, Testi standard, E-mail, Telefono, Immagini, Profilo",
            "categories": ["Testo libero", "Testi standard", "E-mail", "Telefono", "Immagini", "Profilo"],
            "items": [_SKIP, {"text": "Organizza per testo libero, testi standard, e-mail, telefono, immagini e profilo."}, _SKIP, _SKIP, _SKIP, {"text": "Esporta backup e importa quando serve. Disponibile con prova gratuita di 30 giorni e Pro."}],
        },
        "themesSection": {"subtitle": "Chiaro e scuro, più temi premium con Pro."},
        "comparison": {"appText": "Organizza e salva chiaramente testi e informazioni che riusi."},
        "privacySection": {"points": [_SKIP, "Non invia automaticamente i contenuti salvati a server esterni", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Esporta backup e importa quando serve. Disponibile con prova gratuita di 30 giorni e Pro."}]},
        "cta": {
            "titleLine1": "I testi di ogni giorno,",
            "titleLine2": "a un tap di distanza.",
            "title": "I testi di ogni giorno, a un tap di distanza.",
            "lead": "Salva, tocca, poi incolla.",
            "button": "30 giorni di prova gratuita",
        },
        "sceneMore": {
            "lead": "Viaggi, marketplace, chat, organizzazione eventi—copia i tuoi testi preferiti con un tap, ovunque.",
            "cap3": "Testi per annunci, subito copiati",
            "cap4": "Risposte in chat, subito copiate",
            "cap6": "Messaggi da organizzatore, subito copiati",
        },
    },
    "es": {
        "meta": {
            "description": "Guarda textos fijos, direcciones, contactos, URL, emoji, hashtags y más—copia con un toque. Cambia a tu app habitual y pega. MyQuickPaste simplifica la escritura en el móvil.",
            "ogDescription": "Guarda textos e información que repites y cópialos con un toque cuando los necesites. Cambia a tu app habitual y pega.",
        },
        "hero": {
            "catchLine1": "Tus textos del día a día,",
            "catchLine2": "a un toque.",
            "lead": "Textos fijos, direcciones, contactos, URL, emoji, hashtags. Guarda lo que repites y cópialo con un toque desde la lista cuando lo necesites.",
            "sub": "Luego cambia a tu app habitual y pega.",
        },
        "trust": {
            "t1Title": "Toca para copiar",
            "t1Text": "Solo toca una fila guardada.",
            "t2Title": "Pro de pago único",
            "t2Text": "Sin pagos mensuales.",
            "t3Title": "Guardado en el dispositivo",
            "t3Text": "El contenido registrado se gestiona en el dispositivo.",
            "t4Title": "Interfaz en 21 idiomas",
            "t4Text": "Pantallas de la app en 21 idiomas.",
        },
        "pain": {
            "titleLine1": "Deja de preguntarte",
            "titleLine2": "«¿Dónde estaba?»",
            "lead": "La misma información—pero cada vez buscas en notas, vuelves a seleccionar con pulsación larga o reescribes el mismo texto. Pequeños pasos que se acumulan cada día.",
            "p1Title": "Buscar",
            "p1Text": "Dirección o texto fijo: no sabes en qué nota está.",
            "p2Title": "Seleccionar",
            "p2Text": "Pulsación larga para coger solo la parte que necesitas.",
            "p3Title": "Escribir otra vez",
            "p3Text": "Reescribes la misma respuesta o el mismo perfil una y otra vez.",
            "resolveSub": "No busques. No reescribas. Solo toca la fila que necesitas.",
        },
        "steps": {"items": [{"text": "Registra textos habituales, contactos y más."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "También en redes",
            "titleLine1": "Emoji y hashtags—",
            "titleLine2": "copia cuando los necesites.",
            "lead": "Guarda emoji, hashtags y textos de publicaciones favoritos. Toca para copiar y pega en tus apps sociales habituales.",
            "points": [
                {"title": "Emoji", "text": "Guarda favoritos"},
                {"title": "Publicaciones", "text": "Guarda textos habituales"},
                {"title": "Hashtags", "text": "Copia en bloque"},
                {"title": "Copia rápida", "text": "Un toque cuando haga falta"},
            ],
        },
        "sceneWork": {
            "eyebrow": "También en el trabajo",
            "titleLine1": "Textos fijos y contactos—",
            "titleLine2": "copia cuando los necesites.",
            "lead": "Textos fijos, correos, teléfonos, URL y otra info que repites, en un solo lugar. Toca una fila para copiar al instante.",
            "points": [
                {"title": "Textos fijos", "text": "Tus respuestas habituales"},
                {"title": "Correo", "text": "Guarda firmas y avisos"},
                {"title": "Contactos", "text": "Copia números rápido"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "En la vida diaria",
            "titleLine1": "Dirección y perfil—",
            "titleLine2": "copia cuando los necesites.",
            "lead": "Dirección de casa, correo, bio del perfil, frases favoritas. Toca y copia al instante cuando los necesites.",
        },
        "features": {
            "categoriesLabel": "Categorías: Texto libre, Textos fijos, Correo, Teléfono, Imágenes, Perfil",
            "categories": ["Texto libre", "Textos fijos", "Correo", "Teléfono", "Imágenes", "Perfil"],
            "items": [_SKIP, {"text": "Organiza por texto libre, textos fijos, correo, teléfono, imágenes y perfil."}, _SKIP, _SKIP, _SKIP, {"text": "Exporta copias de seguridad e impórtalas cuando haga falta. Disponible con prueba gratuita de 30 días y Pro."}],
        },
        "themesSection": {"subtitle": "Claro y oscuro, más temas premium con Pro."},
        "comparison": {"appText": "Organiza y guarda con claridad los textos e información que repites."},
        "privacySection": {"points": [_SKIP, "No envía automáticamente el contenido guardado a servidores externos", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Exporta copias de seguridad e impórtalas cuando haga falta. Disponible con prueba gratuita de 30 días y Pro."}]},
        "cta": {
            "titleLine1": "Tus textos del día a día,",
            "titleLine2": "a un toque.",
            "title": "Tus textos del día a día, a un toque.",
            "lead": "Guarda, toca, luego pega.",
            "button": "30 días de prueba gratuita",
        },
        "sceneMore": {
            "lead": "Viajes, apps de segunda mano, chat, organización de eventos—copia tu texto habitual con un toque, en cualquier situación.",
            "cap3": "Textos de anuncios al instante",
            "cap4": "Respuestas de chat al instante",
            "cap6": "Mensajes de organizador al instante",
        },
    },
    "pt": {
        "meta": {
            "description": "Salve textos padrão, endereços, contatos, URLs, emoji, hashtags e mais—copie com um toque. Mude para o app de sempre e cole. MyQuickPaste simplifica a digitação no smartphone.",
            "ogDescription": "Salve textos e informações que reutiliza e copie com um toque quando precisar. Mude para o app de sempre e cole.",
        },
        "hero": {
            "catchLine1": "Textos do dia a dia,",
            "catchLine2": "a um toque.",
            "lead": "Textos padrão, endereços, contatos, URLs, emoji, hashtags. Salve o que reutiliza e copie com um toque da lista quando precisar.",
            "sub": "Depois mude para o app de sempre e cole.",
        },
        "trust": {
            "t1Title": "Toque para copiar",
            "t1Text": "Basta tocar uma linha salva.",
            "t2Title": "Pro pagamento único",
            "t2Text": "Sem pagamentos mensais.",
            "t3Title": "Salvo no dispositivo",
            "t3Text": "O conteúdo registrado é gerenciado no dispositivo.",
            "t4Title": "Interface em 21 idiomas",
            "t4Text": "Telas do app em 21 idiomas.",
        },
        "pain": {
            "titleLine1": "Chega de pensar",
            "titleLine2": "«Onde estava isso?»",
            "lead": "A mesma informação—mas toda vez você procura nas notas, seleciona de novo com toque longo ou redigita o mesmo texto. Pequenos passos que se acumulam todo dia.",
            "p1Title": "Procurar",
            "p1Text": "Endereço ou texto padrão: não sabe em qual nota está.",
            "p2Title": "Selecionar",
            "p2Text": "Toque longo para pegar só a parte que precisa.",
            "p3Title": "Digitar de novo",
            "p3Text": "Redigita a mesma resposta ou o mesmo perfil várias vezes.",
            "resolveSub": "Não procure. Não redigite. Basta tocar a linha que precisa.",
        },
        "steps": {"items": [{"text": "Registre textos habituais, contatos e mais."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Nas redes também",
            "titleLine1": "Emoji e hashtags—",
            "titleLine2": "copie quando precisar.",
            "lead": "Salve emoji, hashtags e textos de publicação favoritos. Toque para copiar e cole nos seus apps sociais de sempre.",
            "points": [
                {"title": "Emoji", "text": "Salve favoritos"},
                {"title": "Publicações", "text": "Salve textos habituais"},
                {"title": "Hashtags", "text": "Copie em bloco"},
                {"title": "Cópia rápida", "text": "Um toque quando precisar"},
            ],
        },
        "sceneWork": {
            "eyebrow": "No trabalho também",
            "titleLine1": "Textos padrão e contatos—",
            "titleLine2": "copie quando precisar.",
            "lead": "Textos padrão, e-mails, telefones, URLs e outras informações reutilizadas em um só lugar. Toque uma linha para copiar na hora.",
            "points": [
                {"title": "Textos padrão", "text": "Suas respostas habituais"},
                {"title": "E-mail", "text": "Salve assinaturas e avisos"},
                {"title": "Contatos", "text": "Copie números rapidamente"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "No dia a dia",
            "titleLine1": "Endereço e perfil—",
            "titleLine2": "copie quando precisar.",
            "lead": "Endereço de casa, e-mail, bio do perfil, frases favoritas. Toque e copie na hora quando precisar.",
        },
        "features": {
            "categoriesLabel": "Categorias: Texto livre, Textos padrão, E-mail, Telefone, Imagens, Perfil",
            "categories": ["Texto livre", "Textos padrão", "E-mail", "Telefone", "Imagens", "Perfil"],
            "items": [_SKIP, {"text": "Organize por texto livre, textos padrão, e-mail, telefone, imagens e perfil."}, _SKIP, _SKIP, _SKIP, {"text": "Exporte backups e importe quando precisar. Disponível com teste gratuito de 30 dias e Pro."}],
        },
        "themesSection": {"subtitle": "Claro e escuro, mais temas premium com Pro."},
        "comparison": {"appText": "Organize e salve com clareza textos e informações que reutiliza."},
        "privacySection": {"points": [_SKIP, "Não envia automaticamente o conteúdo salvo para servidores externos", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Exporte backups e importe quando precisar. Disponível com teste gratuito de 30 dias e Pro."}]},
        "cta": {
            "titleLine1": "Textos do dia a dia,",
            "titleLine2": "a um toque.",
            "title": "Textos do dia a dia, a um toque.",
            "lead": "Salvar, tocar, depois colar.",
            "button": "30 dias de teste gratuito",
        },
        "sceneMore": {
            "lead": "Viagem, apps de usados, chat, organização de eventos—copie seu texto favorito com um toque, em qualquer situação.",
            "cap3": "Textos de anúncios na hora",
            "cap4": "Respostas de chat na hora",
            "cap6": "Mensagens de organizador na hora",
        },
    },
    "hi": {
        "meta": {
            "description": "तैयार पाठ, पता, संपर्क, URL, इमोजी, हैशटैग आदि सेव करें और एक टैप में कॉपी करें। अपने सामान्य ऐप में जाकर पेस्ट करें। MyQuickPaste स्मार्टफ़ोन पर टाइपिंग को सरल बनाता है।",
            "ogDescription": "अक्सर इस्तेमाल होने वाले पाठ और जानकारी सेव करें, ज़रूरत पर एक टैप में कॉपी करें। अपने सामान्य ऐप में जाकर पेस्ट करें।",
        },
        "hero": {
            "catchLine1": "अक्सर इस्तेमाल होने वाला पाठ,",
            "catchLine2": "एक टैप दूर।",
            "lead": "तैयार पाठ, पता, संपर्क, URL, इमोजी, हैशटैग। बार-बार इस्तेमाल होने वाला सेव करें, ज़रूरत पर सूची से एक टैप में कॉपी करें।",
            "sub": "फिर अपने सामान्य ऐप में जाकर पेस्ट करें।",
        },
        "trust": {
            "t1Title": "टैप से कॉपी",
            "t1Text": "सेव की गई पंक्ति पर बस टैप करें।",
            "t2Title": "एक बार का Pro",
            "t2Text": "कोई मासिक भुगतान नहीं।",
            "t3Title": "डिवाइस में सेव",
            "t3Text": "रजिस्टर की गई सामग्री डिवाइस पर प्रबंधित होती है।",
            "t4Title": "21 भाषाओं में UI",
            "t4Text": "21 भाषाओं में ऐप स्क्रीन।",
        },
        "pain": {
            "titleLine1": "हर बार 「कहाँ था?」",
            "titleLine2": "सोचना बंद करें।",
            "lead": "वही जानकारी—फिर भी हर बार नोट्स खोजना, लंबा दबाकर फिर चुनना या वही पाठ दोबारा टाइप करना। छोटे-छोटे कदम रोज़ जुड़ते हैं।",
            "p1Title": "खोजना",
            "p1Text": "पता या तैयार पाठ—पता नहीं किस नोट में है।",
            "p2Title": "चुनना",
            "p2Text": "ज़रूरी हिस्सा लंबे दबाव से चुनना।",
            "p3Title": "फिर टाइप",
            "p3Text": "वही जवाब या प्रोफ़ाइल बार-बार टाइप करना।",
            "resolveSub": "खोजें नहीं। दोबारा टाइप न करें। बस ज़रूरी पंक्ति पर टैप करें।",
        },
        "steps": {"items": [{"text": "अक्सर इस्तेमाल होने वाले पाठ, संपर्क आदि रजिस्टर करें।"}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "सोशल के लिए भी",
            "titleLine1": "इमोजी और हैशटैग—",
            "titleLine2": "ज़रूरत पर तुरंत कॉपी।",
            "lead": "पसंदीदा इमोजी, हैशटैग और पोस्ट पाठ सेव करें। टैप करके कॉपी करें और अपने सामान्य सोशल ऐप में पेस्ट करें।",
            "points": [
                {"title": "इमोजी", "text": "पसंदीदा सेव करें"},
                {"title": "पोस्ट", "text": "अक्सर इस्तेमाल होने वाला पाठ सेव करें"},
                {"title": "हैशटैग", "text": "एक साथ कॉपी"},
                {"title": "तुरंत कॉपी", "text": "ज़रूरत पर एक टैप"},
            ],
        },
        "sceneWork": {
            "eyebrow": "काम पर भी",
            "titleLine1": "तैयार पाठ और संपर्क—",
            "titleLine2": "ज़रूरत पर तुरंत कॉपी।",
            "lead": "तैयार पाठ, ईमेल, फ़ोन नंबर, URL आदि बार-बार इस्तेमाल होने वाली जानकारी एक जगह। पंक्ति पर टैप करके तुरंत कॉपी करें।",
            "points": [
                {"title": "तैयार पाठ", "text": "आपके सामान्य जवाब"},
                {"title": "ईमेल", "text": "हस्ताक्षर और सूचना सेव करें"},
                {"title": "संपर्क", "text": "फ़ोन नंबर तुरंत कॉपी"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "रोज़मर्रा में",
            "titleLine1": "पता और प्रोफ़ाइल—",
            "titleLine2": "ज़रूरत पर तुरंत कॉपी।",
            "lead": "घर का पता, ईमेल, प्रोफ़ाइल विवरण, पसंदीदा वाक्य। ज़रूरत पर टैप करके तुरंत कॉपी करें।",
        },
        "features": {
            "categoriesLabel": "श्रेणियाँ: मुक्त पाठ, तैयार पाठ, ईमेल, फ़ोन, छवियाँ, प्रोफ़ाइल",
            "categories": ["मुक्त पाठ", "तैयार पाठ", "ईमेल", "फ़ोन", "छवियाँ", "प्रोफ़ाइल"],
            "items": [_SKIP, {"text": "मुक्त पाठ, तैयार पाठ, ईमेल, फ़ोन, छवियाँ और प्रोफ़ाइल के अनुसार प्रबंधित करें।"}, _SKIP, _SKIP, _SKIP, {"text": "बैकअप निर्यात करें और ज़रूरत पर आयात करें। 30 दिन के मुफ़्त परीक्षण और Pro में उपलब्ध।"}],
        },
        "themesSection": {"subtitle": "लाइट और डार्क, Pro के साथ प्रीमियम रंग थीम भी।"},
        "comparison": {"appText": "बार-बार इस्तेमाल होने वाले पाठ और जानकारी को स्पष्ट रूप से व्यवस्थित करके सेव करें।"},
        "privacySection": {"points": [_SKIP, "रजिस्टर की गई सामग्री बाहरी सर्वर पर स्वचालित रूप से नहीं भेजता", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "बैकअप निर्यात करें और ज़रूरत पर आयात करें। 30 दिन के मुफ़्त परीक्षण और Pro में उपलब्ध।"}]},
        "cta": {
            "titleLine1": "अक्सर इस्तेमाल होने वाला पाठ,",
            "titleLine2": "एक टैप दूर।",
            "title": "अक्सर इस्तेमाल होने वाला पाठ, एक टैप दूर।",
            "lead": "सेव करें, टैप करें, फिर पेस्ट करें।",
            "button": "30 दिन का मुफ़्त परीक्षण",
        },
        "sceneMore": {
            "lead": "यात्रा, सेकंड-हैंड ऐप, चैट, इवेंट—किसी भी स्थिति में पसंदीदा पाठ एक टैप में कॉपी करें।",
            "cap3": "मार्केटप्लेस पाठ तुरंत कॉपी",
            "cap4": "चैट जवाब तुरंत कॉपी",
            "cap6": "आयोजक संदेश तुरंत कॉपी",
        },
    },
    "ar": {
        "meta": {
            "description": "احفظ النصوص الجاهزة والعناوين وجهات الاتصال والروابط والرموز التعبيرية والوسوم—ثم انسخ بنقرة واحدة. انتقل إلى تطبيقك المعتاد والصق. MyQuickPaste يبسّط الكتابة على الهاتف.",
            "ogDescription": "احفظ النصوص والمعلومات التي تكررها، ثم انسخها بنقرة واحدة عند الحاجة. انتقل إلى تطبيقك المعتاد والصق.",
        },
        "hero": {
            "catchLine1": "نصوصك اليومية،",
            "catchLine2": "بنقرة واحدة.",
            "lead": "نصوص جاهزة، عناوين، جهات اتصال، روابط، رموز تعبيرية، وسوم. احفظ ما تكرره وانسخه بنقرة واحدة من القائمة عند الحاجة.",
            "sub": "ثم انتقل إلى تطبيقك المعتاد والصق.",
        },
        "trust": {
            "t1Title": "انقر للنسخ",
            "t1Text": "فقط انقر على الصف المحفوظ.",
            "t2Title": "Pro دفعة واحدة",
            "t2Text": "لا مدفوعات شهرية.",
            "t3Title": "محفوظ على الجهاز",
            "t3Text": "المحتوى المسجّل يُدار على الجهاز.",
            "t4Title": "واجهة بـ 21 لغة",
            "t4Text": "شاشات التطبيق بـ 21 لغة.",
        },
        "pain": {
            "titleLine1": "كف عن التساؤل",
            "titleLine2": "«أين كان؟» في كل مرة.",
            "lead": "نفس المعلومات—لكن في كل مرة تبحث في الملاحظات، أو تعيد التحديد بالضغط المطول، أو تعيد كتابة النفس النص. خطوات صغيرة تتراكم يومًا بعد يوم.",
            "p1Title": "البحث",
            "p1Text": "العنوان أو النص الجاهز—لا تعرف في أي ملاحظة.",
            "p2Title": "التحديد",
            "p2Text": "ضغطة مطولة لاختيار الجزء الذي تحتاجه فقط.",
            "p3Title": "الكتابة مجددًا",
            "p3Text": "تعيد كتابة نفس الرد أو الملف الشخصي مرارًا.",
            "resolveSub": "لا تبحث. لا تعِد الكتابة. فقط انقر الصف الذي تحتاجه.",
        },
        "steps": {"items": [{"text": "سجّل النصوص المعتادة وجهات الاتصال والمزيد."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "للتواصل الاجتماعي أيضًا",
            "titleLine1": "الرموز التعبيرية والوسوم—",
            "titleLine2": "انسخها عند الحاجة.",
            "lead": "احفظ الرموز التعبيرية والوسوم ونصوص المنشورات المفضلة. انقر للنسخ ثم الصق في تطبيقاتك الاجتماعية المعتادة.",
            "points": [
                {"title": "رموز تعبيرية", "text": "احفظ المفضلة"},
                {"title": "منشورات", "text": "احفظ النصوص المعتادة"},
                {"title": "وسوم", "text": "انسخ دفعة واحدة"},
                {"title": "نسخ سريع", "text": "نقرة واحدة عند الحاجة"},
            ],
        },
        "sceneWork": {
            "eyebrow": "في العمل أيضًا",
            "titleLine1": "النصوص الجاهزة وجهات الاتصال—",
            "titleLine2": "انسخها عند الحاجة.",
            "lead": "النصوص الجاهزة والبريد الإلكتروني وأرقام الهاتف والروابط ومعلومات أخرى متكررة في مكان واحد. انقر صفًا للنسخ فورًا.",
            "points": [
                {"title": "نصوص جاهزة", "text": "ردودك المعتادة"},
                {"title": "بريد", "text": "احفظ التوقيعات والإشعارات"},
                {"title": "جهات اتصال", "text": "انسخ الأرقام بسرعة"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "في الحياة اليومية",
            "titleLine1": "العنوان والملف الشخصي—",
            "titleLine2": "انسخهما عند الحاجة.",
            "lead": "عنوان المنزل، البريد، نبذة الملف الشخصي، العبارات المفضلة. انقر وانسخ فورًا عند الحاجة.",
        },
        "features": {
            "categoriesLabel": "الفئات: نص حر، نصوص جاهزة، بريد، هاتف، صور، ملف شخصي",
            "categories": ["نص حر", "نصوص جاهزة", "بريد", "هاتف", "صور", "ملف شخصي"],
            "items": [_SKIP, {"text": "نظّم حسب النص الحر والنصوص الجاهزة والبريد والهاتف والصور والملف الشخصي."}, _SKIP, _SKIP, _SKIP, {"text": "صدّر النسخ الاحتياطية واستوردها عند الحاجة. متاح مع التجربة المجانية 30 يومًا وPro."}],
        },
        "themesSection": {"subtitle": "فاتح وداكن، بالإضافة إلى سمات ألوان مميزة مع Pro."},
        "comparison": {"appText": "نظّم واحفظ بوضوح النصوص والمعلومات التي تكررها."},
        "privacySection": {"points": [_SKIP, "لا يرسل المحتوى المحفوظ تلقائيًا إلى خوادم خارجية", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "صدّر النسخ الاحتياطية واستوردها عند الحاجة. متاح مع التجربة المجانية 30 يومًا وPro."}]},
        "cta": {
            "titleLine1": "نصوصك اليومية،",
            "titleLine2": "بنقرة واحدة.",
            "title": "نصوصك اليومية، بنقرة واحدة.",
            "lead": "احفظ، انقر، ثم الصق.",
            "button": "تجربة مجانية 30 يومًا",
        },
        "sceneMore": {
            "lead": "السفر، تطبيقات البيع، الدردشة، تنظيم الفعاليات—انسخ نصك المفضل بنقرة واحدة في أي موقف.",
            "cap3": "نصوص الإعلانات فورًا",
            "cap4": "ردود الدردشة فورًا",
            "cap6": "رسائل المنظم فورًا",
        },
    },
    "id": {
        "meta": {
            "description": "Simpan teks baku, alamat, kontak, URL, emoji, hashtag, dan lainnya—lalu salin dengan satu ketuk. Beralih ke aplikasi biasa Anda dan tempel. MyQuickPaste menyederhanakan pengetikan di smartphone.",
            "ogDescription": "Simpan teks dan info yang sering dipakai, lalu salin dengan satu ketuk saat diperlukan. Beralih ke aplikasi biasa Anda dan tempel.",
        },
        "hero": {
            "catchLine1": "Teks sehari-hari,",
            "catchLine2": "satu ketuk saja.",
            "lead": "Teks baku, alamat, kontak, URL, emoji, hashtag. Simpan yang sering dipakai, lalu salin dengan satu ketuk dari daftar saat diperlukan.",
            "sub": "Lalu beralih ke aplikasi biasa Anda dan tempel.",
        },
        "trust": {
            "t1Title": "Ketuk untuk menyalin",
            "t1Text": "Cukup ketuk baris yang disimpan.",
            "t2Title": "Pro sekali bayar",
            "t2Text": "Tanpa pembayaran bulanan.",
            "t3Title": "Disimpan di perangkat",
            "t3Text": "Konten terdaftar dikelola di perangkat.",
            "t4Title": "UI 21 bahasa",
            "t4Text": "Layar aplikasi dalam 21 bahasa.",
        },
        "pain": {
            "titleLine1": "Berhenti bertanya",
            "titleLine2": "«Di mana tadi?»",
            "lead": "Info yang sama—tapi setiap kali Anda cari di catatan, pilih ulang dengan tekan lama, atau ketik ulang teks yang sama. Langkah kecil menumpuk setiap hari.",
            "p1Title": "Mencari",
            "p1Text": "Alamat atau teks baku—tidak tahu di catatan mana.",
            "p2Title": "Memilih",
            "p2Text": "Tekan lama untuk mengambil bagian yang Anda butuhkan.",
            "p3Title": "Mengetik lagi",
            "p3Text": "Mengetik ulang balasan atau profil yang sama berkali-kali.",
            "resolveSub": "Jangan cari. Jangan ketik ulang. Cukup ketuk baris yang Anda butuhkan.",
        },
        "steps": {"items": [{"text": "Daftarkan teks favorit, kontak, dan lainnya."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Untuk media sosial juga",
            "titleLine1": "Emoji dan hashtag—",
            "titleLine2": "salin saat diperlukan.",
            "lead": "Simpan emoji, hashtag, dan teks posting favorit. Ketuk untuk menyalin, lalu tempel ke aplikasi sosial biasa Anda.",
            "points": [
                {"title": "Emoji", "text": "Simpan favorit"},
                {"title": "Posting", "text": "Simpan teks favorit"},
                {"title": "Hashtag", "text": "Salin sekaligus"},
                {"title": "Salin cepat", "text": "Satu ketuk saat perlu"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Untuk pekerjaan juga",
            "titleLine1": "Teks baku dan kontak—",
            "titleLine2": "salin saat diperlukan.",
            "lead": "Teks baku, email, nomor telepon, URL, dan info lain yang sering dipakai dalam satu tempat. Ketuk baris untuk menyalin segera.",
            "points": [
                {"title": "Teks baku", "text": "Balasan biasa Anda"},
                {"title": "Email", "text": "Simpan tanda tangan dan pemberitahuan"},
                {"title": "Kontak", "text": "Salin nomor dengan cepat"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "Dalam kehidupan sehari-hari",
            "titleLine1": "Alamat dan profil—",
            "titleLine2": "salin saat diperlukan.",
            "lead": "Alamat rumah, email, bio profil, frasa favorit. Ketuk dan salin segera saat diperlukan.",
        },
        "features": {
            "categoriesLabel": "Kategori: Teks bebas, Teks baku, Email, Telepon, Gambar, Profil",
            "categories": ["Teks bebas", "Teks baku", "Email", "Telepon", "Gambar", "Profil"],
            "items": [_SKIP, {"text": "Kelola menurut teks bebas, teks baku, email, telepon, gambar, dan profil."}, _SKIP, _SKIP, _SKIP, {"text": "Ekspor cadangan dan impor saat diperlukan. Tersedia dengan uji coba gratis 30 hari dan Pro."}],
        },
        "themesSection": {"subtitle": "Terang dan gelap, plus tema warna premium dengan Pro."},
        "comparison": {"appText": "Atur dan simpan teks serta info yang sering dipakai dengan jelas."},
        "privacySection": {"points": [_SKIP, "Tidak mengirim konten tersimpan secara otomatis ke server eksternal", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Ekspor cadangan dan impor saat diperlukan. Tersedia dengan uji coba gratis 30 hari dan Pro."}]},
        "cta": {
            "titleLine1": "Teks sehari-hari,",
            "titleLine2": "satu ketuk saja.",
            "title": "Teks sehari-hari, satu ketuk saja.",
            "lead": "Simpan, ketuk, lalu tempel.",
            "button": "Uji coba gratis 30 hari",
        },
        "sceneMore": {
            "lead": "Perjalanan, marketplace, chat, acara—salin teks favorit dengan satu ketuk di situasi apa pun.",
            "cap3": "Teks iklan, langsung disalin",
            "cap4": "Balasan chat, langsung disalin",
            "cap6": "Pesan panitia, langsung disalin",
        },
    },
    "th": {
        "meta": {
            "description": "บันทึกข้อความสำเร็จรูป ที่อยู่ ติดต่อ URL อีโมจิ แฮชแท็ก และอื่นๆ แล้วคัดลอกด้วยแตะครั้งเดียว สลับไปแอปที่ใช้ประจำแล้ววาง MyQuickPaste ทำให้การพิมพ์บนสมาร์ทโฟนง่ายขึ้น",
            "ogDescription": "บันทึกข้อความและข้อมูลที่ใช้บ่อย แล้วคัดลอกด้วยแตะครั้งเดียวเมื่อต้องการ สลับไปแอปที่ใช้ประจำแล้ววาง",
        },
        "hero": {
            "catchLine1": "ข้อความที่ใช้บ่อย",
            "catchLine2": "แตะครั้งเดียว",
            "lead": "ข้อความสำเร็จรูป ที่อยู่ ติดต่อ URL อีโมจิ แฮชแท็ก บันทึกสิ่งที่ใช้ซ้ำ แล้วคัดลอกด้วยแตะครั้งเดียวจากรายการเมื่อต้องการ",
            "sub": "จากนั้นสลับไปแอปที่ใช้ประจำแล้ววาง",
        },
        "trust": {
            "t1Title": "แตะเพื่อคัดลอก",
            "t1Text": "แค่แตะแถวที่บันทึกไว้",
            "t2Title": "Pro จ่ายครั้งเดียว",
            "t2Text": "ไม่มีค่าใช้จ่ายรายเดือน",
            "t3Title": "เก็บในอุปกรณ์",
            "t3Text": "เนื้อหาที่ลงทะเบียนจัดการในอุปกรณ์",
            "t4Title": "UI 21 ภาษา",
            "t4Text": "หน้าจอแอป 21 ภาษา",
        },
        "pain": {
            "titleLine1": "เลิกถามตัวเองว่า",
            "titleLine2": "「อยู่ไหนนะ?」",
            "lead": "ข้อมูลเดิมๆ—แต่ทุกครั้งต้องค้นบันทึก กดค้างเลือกใหม่ หรือพิมพ์ข้อความเดิมซ้ำ ขั้นตอนเล็กๆ สะสมทุกวัน",
            "p1Title": "ค้นหา",
            "p1Text": "ที่อยู่หรือข้อความสำเร็จรูป—ไม่รู้ว่าอยู่บันทึกไหน",
            "p2Title": "เลือก",
            "p2Text": "กดค้างเพื่อเลือกเฉพาะส่วนที่ต้องการ",
            "p3Title": "พิมพ์ใหม่",
            "p3Text": "พิมพ์คำตอบหรือโปรไฟล์เดิมซ้ำๆ",
            "resolveSub": "ไม่ต้องค้น ไม่ต้องพิมพ์ใหม่ แค่แตะแถวที่ต้องการ",
        },
        "steps": {"items": [{"text": "ลงทะเบียนข้อความที่ใช้บ่อย ติดต่อ และอื่นๆ"}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "สำหรับโซเชียลด้วย",
            "titleLine1": "อีโมจิและแฮชแท็ก—",
            "titleLine2": "คัดลอกเมื่อต้องการ",
            "lead": "บันทึกอีโมจิ แฮชแท็ก และข้อความโพสต์ที่ชอบ แตะเพื่อคัดลอก แล้ววางในแอปโซเชียลที่ใช้ประจำ",
            "points": [
                {"title": "อีโมจิ", "text": "บันทึกรายการโปรด"},
                {"title": "โพสต์", "text": "บันทึกข้อความที่ใช้บ่อย"},
                {"title": "แฮชแท็ก", "text": "คัดลอกเป็นชุด"},
                {"title": "คัดลอกเร็ว", "text": "แตะครั้งเดียวเมื่อต้องการ"},
            ],
        },
        "sceneWork": {
            "eyebrow": "สำหรับงานด้วย",
            "titleLine1": "ข้อความสำเร็จรูปและติดต่อ—",
            "titleLine2": "คัดลอกเมื่อต้องการ",
            "lead": "ข้อความสำเร็จรูป อีเมล เบอร์โทร URL และข้อมูลที่ใช้ซ้ำอื่นๆ ในที่เดียว แตะแถวเพื่อคัดลอกทันที",
            "points": [
                {"title": "ข้อความสำเร็จรูป", "text": "คำตอบที่ใช้ประจำ"},
                {"title": "อีเมล", "text": "บันทึกลายเซ็นและข้อความแจ้ง"},
                {"title": "ติดต่อ", "text": "คัดลอกเบอร์โทรเร็ว"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "ในชีวิตประจำวัน",
            "titleLine1": "ที่อยู่และโปรไฟล์—",
            "titleLine2": "คัดลอกเมื่อต้องการ",
            "lead": "ที่อยู่บ้าน อีเมล ข้อความโปรไฟล์ ประโยคที่ชอบ แตะและคัดลอกทันทีเมื่อต้องการ",
        },
        "features": {
            "categoriesLabel": "หมวดหมู่: ข้อความอิสระ ข้อความสำเร็จรูป อีเมล โทรศัพท์ รูปภาพ โปรไฟล์",
            "categories": ["ข้อความอิสระ", "ข้อความสำเร็จรูป", "อีเมล", "โทรศัพท์", "รูปภาพ", "โปรไฟล์"],
            "items": [_SKIP, {"text": "จัดการตามข้อความอิสระ ข้อความสำเร็จรูป อีเมล โทรศัพท์ รูปภาพ และโปรไฟล์"}, _SKIP, _SKIP, _SKIP, {"text": "ส่งออกสำรองและนำเข้าเมื่อต้องการ ใช้ได้กับทดลองใช้ฟรี 30 วันและ Pro"}],
        },
        "themesSection": {"subtitle": "สว่างและมืด รวมถึงธีมสีพรีเมียมกับ Pro"},
        "comparison": {"appText": "จัดระเบียบและบันทึกข้อความและข้อมูลที่ใช้ซ้ำอย่างชัดเจน"},
        "privacySection": {"points": [_SKIP, "ไม่ส่งเนื้อหาที่บันทึกไปยังเซิร์ฟเวอร์ภายนอกโดยอัตโนมัติ", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "ส่งออกสำรองและนำเข้าเมื่อต้องการ ใช้ได้กับทดลองใช้ฟรี 30 วันและ Pro"}]},
        "cta": {
            "titleLine1": "ข้อความที่ใช้บ่อย",
            "titleLine2": "แตะครั้งเดียว",
            "title": "ข้อความที่ใช้บ่อย แตะครั้งเดียว",
            "lead": "บันทึก แตะ แล้ววาง",
            "button": "ทดลองใช้ฟรี 30 วัน",
        },
        "sceneMore": {
            "lead": "ท่องเที่ยว ตลาดมือสอง แชท จัดงาน—คัดลอกข้อความโปรดด้วยแตะครั้งเดียวทุกสถานการณ์",
            "cap3": "ข้อความลงขาย คัดลอกทันที",
            "cap4": "ตอบแชท คัดลอกทันที",
            "cap6": "ข้อความผู้จัดงาน คัดลอกทันที",
        },
    },
    "vi": {
        "meta": {
            "description": "Lưu văn bản mẫu, địa chỉ, liên hệ, URL, emoji, hashtag và hơn thế—sao chép một chạm. Chuyển sang app quen dùng và dán. MyQuickPaste giúp gõ trên điện thoại đơn giản hơn.",
            "ogDescription": "Lưu văn bản và thông tin hay dùng, sao chép một chạm khi cần. Chuyển sang app quen dùng và dán.",
        },
        "hero": {
            "catchLine1": "Văn bản hay dùng,",
            "catchLine2": "một chạm là xong.",
            "lead": "Văn bản mẫu, địa chỉ, liên hệ, URL, emoji, hashtag. Lưu nội dung hay dùng, sao chép một chạm từ danh sách khi cần.",
            "sub": "Rồi chuyển sang app quen dùng và dán.",
        },
        "trust": {
            "t1Title": "Chạm để sao chép",
            "t1Text": "Chỉ cần chạm vào dòng đã lưu.",
            "t2Title": "Pro trả một lần",
            "t2Text": "Không trả phí hàng tháng.",
            "t3Title": "Lưu trên thiết bị",
            "t3Text": "Nội dung đăng ký được quản lý trên thiết bị.",
            "t4Title": "Giao diện 21 ngôn ngữ",
            "t4Text": "Màn hình app bằng 21 ngôn ngữ.",
        },
        "pain": {
            "titleLine1": "Đừng cứ hỏi",
            "titleLine2": "「Ở đâu nhỉ?」 mỗi lần.",
            "lead": "Cùng thông tin—nhưng mỗi lần lại tìm ghi chú, chọn lại bằng nhấn giữ hoặc gõ lại cùng văn bản. Những bước nhỏ cộng dồn mỗi ngày.",
            "p1Title": "Tìm",
            "p1Text": "Địa chỉ hay văn bản mẫu—không biết ở ghi chú nào.",
            "p2Title": "Chọn",
            "p2Text": "Nhấn giữ để chọn đúng phần cần dùng.",
            "p3Title": "Gõ lại",
            "p3Text": "Gõ lại cùng câu trả lời hoặc hồ sơ nhiều lần.",
            "resolveSub": "Không tìm. Không gõ lại. Chỉ chạm dòng bạn cần.",
        },
        "steps": {"items": [{"text": "Đăng ký văn bản hay dùng, liên hệ và hơn thế."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Cả mạng xã hội",
            "titleLine1": "Emoji và hashtag—",
            "titleLine2": "sao chép khi cần.",
            "lead": "Lưu emoji, hashtag và văn bản đăng yêu thích. Chạm để sao chép, rồi dán vào app mạng xã hội quen dùng.",
            "points": [
                {"title": "Emoji", "text": "Lưu mục yêu thích"},
                {"title": "Bài đăng", "text": "Lưu văn bản hay dùng"},
                {"title": "Hashtag", "text": "Sao chép cả bộ"},
                {"title": "Sao chép nhanh", "text": "Một chạm khi cần"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Cả công việc",
            "titleLine1": "Văn bản mẫu và liên hệ—",
            "titleLine2": "sao chép khi cần.",
            "lead": "Văn bản mẫu, email, số điện thoại, URL và thông tin hay dùng khác ở một nơi. Chạm dòng để sao chép ngay.",
            "points": [
                {"title": "Văn bản mẫu", "text": "Câu trả lời thường dùng"},
                {"title": "Email", "text": "Lưu chữ ký và thông báo"},
                {"title": "Liên hệ", "text": "Sao chép số nhanh"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "Trong đời sống hàng ngày",
            "titleLine1": "Địa chỉ và hồ sơ—",
            "titleLine2": "sao chép khi cần.",
            "lead": "Địa chỉ nhà, email, tiểu sử hồ sơ, câu yêu thích. Chạm và sao chép ngay khi cần.",
        },
        "features": {
            "categoriesLabel": "Danh mục: Văn bản tự do, Văn bản mẫu, Email, Điện thoại, Hình ảnh, Hồ sơ",
            "categories": ["Văn bản tự do", "Văn bản mẫu", "Email", "Điện thoại", "Hình ảnh", "Hồ sơ"],
            "items": [_SKIP, {"text": "Quản lý theo văn bản tự do, văn bản mẫu, email, điện thoại, hình ảnh và hồ sơ."}, _SKIP, _SKIP, _SKIP, {"text": "Xuất sao lưu và nhập khi cần. Có trong dùng thử miễn phí 30 ngày và Pro."}],
        },
        "themesSection": {"subtitle": "Sáng và tối, cùng chủ đề màu cao cấp với Pro."},
        "comparison": {"appText": "Sắp xếp và lưu rõ ràng văn bản và thông tin hay dùng."},
        "privacySection": {"points": [_SKIP, "Không tự động gửi nội dung đã lưu lên máy chủ bên ngoài", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Xuất sao lưu và nhập khi cần. Có trong dùng thử miễn phí 30 ngày và Pro."}]},
        "cta": {
            "titleLine1": "Văn bản hay dùng,",
            "titleLine2": "một chạm là xong.",
            "title": "Văn bản hay dùng, một chạm là xong.",
            "lead": "Lưu, chạm, rồi dán.",
            "button": "Dùng thử miễn phí 30 ngày",
        },
        "sceneMore": {
            "lead": "Du lịch, chợ đồ cũ, chat, tổ chức sự kiện—sao chép văn bản quen một chạm ở mọi tình huống.",
            "cap3": "Văn bản đăng bán, sao chép ngay",
            "cap4": "Trả lời chat, sao chép ngay",
            "cap6": "Tin nhắn ban tổ chức, sao chép ngay",
        },
    },
    "tr": {
        "meta": {
            "description": "Hazır metinleri, adresleri, kişileri, URL'leri, emoji ve hashtag'leri kaydedin—tek dokunuşla kopyalayın. Alıştığınız uygulamaya geçip yapıştırın. MyQuickPaste akıllı telefonda yazmayı basitleştirir.",
            "ogDescription": "Sık kullandığınız metinleri ve bilgileri kaydedin, gerektiğinde tek dokunuşla kopyalayın. Alıştığınız uygulamaya geçip yapıştırın.",
        },
        "hero": {
            "catchLine1": "Sık kullandığınız metinler,",
            "catchLine2": "tek dokunuş uzağınızda.",
            "lead": "Hazır metinler, adresler, kişiler, URL'ler, emoji, hashtag. Sık kullandıklarınızı kaydedin, gerektiğinde listeden tek dokunuşla kopyalayın.",
            "sub": "Sonra alıştığınız uygulamaya geçip yapıştırın.",
        },
        "trust": {
            "t1Title": "Kopyalamak için dokunun",
            "t1Text": "Kayıtlı satıra dokunmanız yeterli.",
            "t2Title": "Tek seferlik Pro",
            "t2Text": "Aylık ödeme yok.",
            "t3Title": "Cihazda saklanır",
            "t3Text": "Kayıtlı içerik cihazda yönetilir.",
            "t4Title": "21 dilde arayüz",
            "t4Text": "Uygulama ekranları 21 dilde.",
        },
        "pain": {
            "titleLine1": "Her seferinde",
            "titleLine2": "«Neredeydi?» demeyin.",
            "lead": "Aynı bilgi—ama her seferinde notlarda aramak, uzun basarak yeniden seçmek veya aynı metni yeniden yazmak. Küçük adımlar her gün birikir.",
            "p1Title": "Aramak",
            "p1Text": "Adres veya hazır metin—hangi notta olduğu belli değil.",
            "p2Title": "Seçmek",
            "p2Text": "İhtiyacınız olan kısmı uzun basarak seçmek.",
            "p3Title": "Yeniden yazmak",
            "p3Text": "Aynı yanıtı veya profili tekrar tekrar yazmak.",
            "resolveSub": "Aramayın. Yeniden yazmayın. Sadece ihtiyacınız olan satıra dokunun.",
        },
        "steps": {"items": [{"text": "Sık kullandığınız metinleri, kişileri ve daha fazlasını kaydedin."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Sosyal medya için de",
            "titleLine1": "Emoji ve hashtag—",
            "titleLine2": "gerektiğinde hemen kopyalayın.",
            "lead": "Favori emoji, hashtag ve gönderi metinlerinizi kaydedin. Dokunarak kopyalayın, alıştığınız sosyal uygulamalara yapıştırın.",
            "points": [
                {"title": "Emoji", "text": "Favorileri kaydedin"},
                {"title": "Gönderiler", "text": "Sık metinleri kaydedin"},
                {"title": "Hashtag", "text": "Toplu kopyalayın"},
                {"title": "Hızlı kopya", "text": "Gerektiğinde tek dokunuş"},
            ],
        },
        "sceneWork": {
            "eyebrow": "İş için de",
            "titleLine1": "Hazır metinler ve kişiler—",
            "titleLine2": "gerektiğinde hemen kopyalayın.",
            "lead": "Hazır metinler, e-posta, telefon, URL ve diğer sık kullanılan bilgiler tek yerde. Satıra dokunarak anında kopyalayın.",
            "points": [
                {"title": "Hazır metinler", "text": "Alışık yanıtlarınız"},
                {"title": "E-posta", "text": "İmza ve bildirimleri kaydedin"},
                {"title": "Kişiler", "text": "Numaraları hızlı kopyalayın"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "Günlük hayatta",
            "titleLine1": "Adres ve profil—",
            "titleLine2": "gerektiğinde hemen kopyalayın.",
            "lead": "Ev adresi, e-posta, profil metni, favori ifadeler. Gerektiğinde dokunarak anında kopyalayın.",
        },
        "features": {
            "categoriesLabel": "Kategoriler: Serbest metin, Hazır metinler, E-posta, Telefon, Görseller, Profil",
            "categories": ["Serbest metin", "Hazır metinler", "E-posta", "Telefon", "Görseller", "Profil"],
            "items": [_SKIP, {"text": "Serbest metin, hazır metinler, e-posta, telefon, görseller ve profile göre yönetin."}, _SKIP, _SKIP, _SKIP, {"text": "Yedekleri dışa aktarın ve gerektiğinde içe aktarın. 30 günlük ücretsiz deneme ve Pro ile kullanılabilir."}],
        },
        "themesSection": {"subtitle": "Açık ve koyu, Pro ile premium renk temaları."},
        "comparison": {"appText": "Sık kullandığınız metinleri ve bilgileri anlaşılır şekilde düzenleyip kaydedin."},
        "privacySection": {"points": [_SKIP, "Kayıtlı içeriği harici sunuculara otomatik göndermez", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Yedekleri dışa aktarın ve gerektiğinde içe aktarın. 30 günlük ücretsiz deneme ve Pro ile kullanılabilir."}]},
        "cta": {
            "titleLine1": "Sık kullandığınız metinler,",
            "titleLine2": "tek dokunuş uzağınızda.",
            "title": "Sık kullandığınız metinler, tek dokunuş uzağınızda.",
            "lead": "Kaydedin, dokunun, sonra yapıştırın.",
            "button": "30 gün ücretsiz deneme",
        },
        "sceneMore": {
            "lead": "Seyahat, ikinci el uygulamalar, sohbet, etkinlik—her durumda favori metninizi tek dokunuşla kopyalayın.",
            "cap3": "İlan metinleri anında kopyalanır",
            "cap4": "Sohbet yanıtları anında kopyalanır",
            "cap6": "Organizatör mesajları anında kopyalanır",
        },
    },
    "uk": {
        "meta": {
            "description": "Зберігайте шаблони, адреси, контакти, URL, емодзі, хештеги та інше—копіюйте одним натисканням. Перейдіть до звичного застосунку та вставте. MyQuickPaste спрощує введення на смартфоні.",
            "ogDescription": "Зберігайте часто використовувані тексти та дані, копіюйте одним натисканням, коли потрібно. Перейдіть до звичного застосунку та вставте.",
        },
        "hero": {
            "catchLine1": "Часті тексти—",
            "catchLine2": "одним натисканням.",
            "lead": "Шаблони, адреси, контакти, URL, емодзі, хештеги. Збережіть те, що часто використовуєте, і копіюйте одним натисканням зі списку, коли потрібно.",
            "sub": "Потім перейдіть до звичного застосунку та вставте.",
        },
        "trust": {
            "t1Title": "Натисніть, щоб скопіювати",
            "t1Text": "Просто натисніть збережений рядок.",
            "t2Title": "Pro разово",
            "t2Text": "Без щомісячних платежів.",
            "t3Title": "Зберігання на пристрої",
            "t3Text": "Збережений вміст керується на пристрої.",
            "t4Title": "Інтерфейс 21 мовою",
            "t4Text": "Екрани застосунку 21 мовою.",
        },
        "pain": {
            "titleLine1": "Досить щоразу думати:",
            "titleLine2": "«Де це було?»",
            "lead": "Та сама інформація—але щоразу ви шукаєте в нотатках, знову виділяєте довгим натисканням або переписуєте той самий текст. Дрібні кроки накопичуються щодня.",
            "p1Title": "Шукати",
            "p1Text": "Адреса чи шаблон—невідомо, у якій нотатці.",
            "p2Title": "Виділяти",
            "p2Text": "Довге натискання, щоб взяти лише потрібну частину.",
            "p3Title": "Вводити знову",
            "p3Text": "Той самий відповідь чи профіль набираєте знову і знову.",
            "resolveSub": "Не шукайте. Не переписуйте. Просто натисніть потрібний рядок.",
        },
        "steps": {"items": [{"text": "Зареєструйте часто використовувані тексти, контакти та інше."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "І для соцмереж",
            "titleLine1": "Емодзі та хештеги—",
            "titleLine2": "копіюйте, коли потрібно.",
            "lead": "Зберігайте улюблені емодзі, хештеги та тексти дописів. Натисніть, щоб скопіювати, і вставте у звичні соцзастосунки.",
            "points": [
                {"title": "Емодзі", "text": "Зберігайте обране"},
                {"title": "Дописи", "text": "Зберігайте часті тексти"},
                {"title": "Хештеги", "text": "Копіюйте набором"},
                {"title": "Швидке копіювання", "text": "Одне натискання, коли потрібно"},
            ],
        },
        "sceneWork": {
            "eyebrow": "І на роботі",
            "titleLine1": "Шаблони та контакти—",
            "titleLine2": "копіюйте, коли потрібно.",
            "lead": "Шаблони, e-mail, телефони, URL та інша часто використовувана інформація в одному місці. Натисніть рядок—і одразу скопіюйте.",
            "points": [
                {"title": "Шаблони", "text": "Ваші звичні відповіді"},
                {"title": "E-mail", "text": "Зберігайте підписи та сповіщення"},
                {"title": "Контакти", "text": "Швидко копіюйте номери"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "У повсякденному житті",
            "titleLine1": "Адреса та профіль—",
            "titleLine2": "копіюйте, коли потрібно.",
            "lead": "Домашня адреса, e-mail, текст профілю, улюблені фрази. Натисніть і одразу скопіюйте, коли потрібно.",
        },
        "features": {
            "categoriesLabel": "Категорії: Вільний текст, Шаблони, E-mail, Телефон, Зображення, Профіль",
            "categories": ["Вільний текст", "Шаблони", "E-mail", "Телефон", "Зображення", "Профіль"],
            "items": [_SKIP, {"text": "Керуйте за категоріями: вільний текст, шаблони, e-mail, телефон, зображення, профіль."}, _SKIP, _SKIP, _SKIP, {"text": "Експортуйте резервні копії та імпортуйте за потреби. Доступно в 30-денній пробній версії та Pro."}],
        },
        "themesSection": {"subtitle": "Світла та темна теми, а також преміальні кольорові теми в Pro."},
        "comparison": {"appText": "Зручно організуйте та зберігайте часто використовувані тексти та дані."},
        "privacySection": {"points": [_SKIP, "Не надсилає збережений вміст автоматично на зовнішні сервери", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Експортуйте резервні копії та імпортуйте за потреби. Доступно в 30-денній пробній версії та Pro."}]},
        "cta": {
            "titleLine1": "Часті тексти—",
            "titleLine2": "одним натисканням.",
            "title": "Часті тексти—одним натисканням.",
            "lead": "Зберегти, натиснути, потім вставити.",
            "button": "30 днів безкоштовно",
        },
        "sceneMore": {
            "lead": "Подорожі, барахолки, чати, організація заходів—копіюйте потрібний текст одним натисканням у будь-якій ситуації.",
            "cap3": "Тексти оголошень—миттєво",
            "cap4": "Відповіді в чаті—миттєво",
            "cap6": "Повідомлення організатора—миттєво",
        },
    },
    "nl": {
        "meta": {
            "description": "Bewaar standaardteksten, adressen, contacten, URL's, emoji, hashtags en meer—kopieer met één tik. Schakel over naar je gebruikelijke app en plak. MyQuickPaste maakt typen op je smartphone eenvoudiger.",
            "ogDescription": "Bewaar teksten en info die je hergebruikt, kopieer met één tik wanneer nodig. Schakel over naar je gebruikelijke app en plak.",
        },
        "hero": {
            "catchLine1": "Dagelijkse teksten,",
            "catchLine2": "één tik verder.",
            "lead": "Standaardteksten, adressen, contacten, URL's, emoji, hashtags. Bewaar wat je hergebruikt en kopieer met één tik uit de lijst wanneer nodig.",
            "sub": "Schakel daarna over naar je gebruikelijke app en plak.",
        },
        "trust": {
            "t1Title": "Tik om te kopiëren",
            "t1Text": "Tik gewoon op een opgeslagen regel.",
            "t2Title": "Pro eenmalig",
            "t2Text": "Geen maandelijkse betalingen.",
            "t3Title": "Opgeslagen op apparaat",
            "t3Text": "Geregistreerde inhoud wordt op het apparaat beheerd.",
            "t4Title": "UI in 21 talen",
            "t4Text": "App-schermen in 21 talen.",
        },
        "pain": {
            "titleLine1": "Stop met jezelf afvragen:",
            "titleLine2": "«Waar stond dat?»",
            "lead": "Dezelfde info—maar elke keer zoek je in notities, selecteer je opnieuw met lang indrukken of typ je dezelfde tekst opnieuw. Kleine stappen stapelen zich op.",
            "p1Title": "Zoeken",
            "p1Text": "Adres of standaardtekst—je weet niet in welke notitie.",
            "p2Title": "Selecteren",
            "p2Text": "Lang indrukken om precies het stuk te pakken dat je nodig hebt.",
            "p3Title": "Opnieuw typen",
            "p3Text": "Hetzelfde antwoord of profiel steeds opnieuw typen.",
            "resolveSub": "Niet zoeken. Niet opnieuw typen. Tik gewoon de regel die je nodig hebt.",
        },
        "steps": {"items": [{"text": "Registreer vaste teksten, contacten en meer."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Ook voor social media",
            "titleLine1": "Emoji en hashtags—",
            "titleLine2": "kopieer wanneer je ze nodig hebt.",
            "lead": "Bewaar favoriete emoji, hashtags en postteksten. Tik om te kopiëren en plak in je gebruikelijke social apps.",
            "points": [
                {"title": "Emoji", "text": "Bewaar favorieten"},
                {"title": "Posts", "text": "Bewaar vaste teksten"},
                {"title": "Hashtags", "text": "Kopieer als set"},
                {"title": "Snel kopiëren", "text": "Één tik wanneer nodig"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Ook voor werk",
            "titleLine1": "Standaardteksten en contacten—",
            "titleLine2": "kopieer wanneer je ze nodig hebt.",
            "lead": "Standaardteksten, e-mail, telefoonnummers, URL's en andere hergebruikte info op één plek. Tik een regel om direct te kopiëren.",
            "points": [
                {"title": "Standaardteksten", "text": "Je gebruikelijke antwoorden"},
                {"title": "E-mail", "text": "Bewaar handtekeningen en mededelingen"},
                {"title": "Contacten", "text": "Kopieer nummers snel"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "In het dagelijks leven",
            "titleLine1": "Adres en profiel—",
            "titleLine2": "kopieer wanneer je ze nodig hebt.",
            "lead": "Thuisadres, e-mail, profieltekst, favoriete zinnen. Tik en kopieer direct wanneer nodig.",
        },
        "features": {
            "categoriesLabel": "Categorieën: Vrije tekst, Standaardteksten, E-mail, Telefoon, Afbeeldingen, Profiel",
            "categories": ["Vrije tekst", "Standaardteksten", "E-mail", "Telefoon", "Afbeeldingen", "Profiel"],
            "items": [_SKIP, {"text": "Beheer per vrije tekst, standaardteksten, e-mail, telefoon, afbeeldingen en profiel."}, _SKIP, _SKIP, _SKIP, {"text": "Exporteer back-ups en importeer wanneer nodig. Beschikbaar met 30 dagen gratis proberen en Pro."}],
        },
        "themesSection": {"subtitle": "Licht en donker, plus premium kleurthema's met Pro."},
        "comparison": {"appText": "Organiseer en bewaar hergebruikte teksten en info duidelijk en overzichtelijk."},
        "privacySection": {"points": [_SKIP, "Stuurt opgeslagen inhoud niet automatisch naar externe servers", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Exporteer back-ups en importeer wanneer nodig. Beschikbaar met 30 dagen gratis proberen en Pro."}]},
        "cta": {
            "titleLine1": "Dagelijkse teksten,",
            "titleLine2": "één tik verder.",
            "title": "Dagelijkse teksten, één tik verder.",
            "lead": "Opslaan, tikken, dan plakken.",
            "button": "30 dagen gratis proberen",
        },
        "sceneMore": {
            "lead": "Reizen, marktplaats-apps, chat, evenementen—kopieer je vaste tekst met één tik, overal.",
            "cap3": "Advertentieteksten direct kopiëren",
            "cap4": "Chatantwoorden direct kopiëren",
            "cap6": "Organisatorteksten direct kopiëren",
        },
    },
    "pl": {
        "meta": {
            "description": "Zapisuj szablony, adresy, kontakty, URL, emoji, hashtagi i więcej—kopiuj jednym dotknięciem. Przełącz się do zwykłej aplikacji i wklej. MyQuickPaste upraszcza pisanie na smartfonie.",
            "ogDescription": "Zapisuj często używane teksty i informacje, kopiuj jednym dotknięciem, gdy potrzebujesz. Przełącz się do zwykłej aplikacji i wklej.",
        },
        "hero": {
            "catchLine1": "Codzienne teksty,",
            "catchLine2": "jedno dotknięcie.",
            "lead": "Szablony, adresy, kontakty, URL, emoji, hashtagi. Zapisz to, co powtarzasz, i kopiuj jednym dotknięciem z listy, gdy potrzebujesz.",
            "sub": "Potem przełącz się do zwykłej aplikacji i wklej.",
        },
        "trust": {
            "t1Title": "Dotknij, aby skopiować",
            "t1Text": "Wystarczy dotknąć zapisanego wiersza.",
            "t2Title": "Pro jednorazowo",
            "t2Text": "Bez comiesięcznych płatności.",
            "t3Title": "Zapisane na urządzeniu",
            "t3Text": "Zarejestrowana treść jest zarządzana na urządzeniu.",
            "t4Title": "Interfejs w 21 językach",
            "t4Text": "Ekrany aplikacji w 21 językach.",
        },
        "pain": {
            "titleLine1": "Koniec z pytaniem",
            "titleLine2": "«Gdzie to było?»",
            "lead": "Te same informacje—a za każdym razem szukasz w notatkach, zaznaczasz ponownie długim naciśnięciem lub przepisujesz ten sam tekst. Małe kroki sumują się codziennie.",
            "p1Title": "Szukać",
            "p1Text": "Adres lub szablon—nie wiesz, w której notatce.",
            "p2Title": "Zaznaczać",
            "p2Text": "Długie naciśnięcie, by wziąć tylko potrzebną część.",
            "p3Title": "Pisać ponownie",
            "p3Text": "Piszesz tę samą odpowiedź lub profil w kółko.",
            "resolveSub": "Nie szukaj. Nie przepisuj. Po prostu dotknij potrzebnego wiersza.",
        },
        "steps": {"items": [{"text": "Zarejestruj często używane teksty, kontakty i więcej."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Także w social mediach",
            "titleLine1": "Emoji i hashtagi—",
            "titleLine2": "kopiuj, gdy potrzebujesz.",
            "lead": "Zapisuj ulubione emoji, hashtagi i teksty postów. Dotknij, aby skopiować, i wklej w zwykłych aplikacjach społecznościowych.",
            "points": [
                {"title": "Emoji", "text": "Zapisuj ulubione"},
                {"title": "Posty", "text": "Zapisuj częste teksty"},
                {"title": "Hashtagi", "text": "Kopiuj zestawem"},
                {"title": "Szybkie kopiowanie", "text": "Jedno dotknięcie, gdy trzeba"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Także w pracy",
            "titleLine1": "Szablony i kontakty—",
            "titleLine2": "kopiuj, gdy potrzebujesz.",
            "lead": "Szablony, e-mail, telefony, URL i inne często używane informacje w jednym miejscu. Dotknij wiersza, aby skopiować od razu.",
            "points": [
                {"title": "Szablony", "text": "Twoje zwykłe odpowiedzi"},
                {"title": "E-mail", "text": "Zapisuj podpisy i powiadomienia"},
                {"title": "Kontakty", "text": "Szybko kopiuj numery"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "W codziennym życiu",
            "titleLine1": "Adres i profil—",
            "titleLine2": "kopiuj, gdy potrzebujesz.",
            "lead": "Adres domowy, e-mail, opis profilu, ulubione zwroty. Dotknij i skopiuj od razu, gdy potrzebujesz.",
        },
        "features": {
            "categoriesLabel": "Kategorie: Wolny tekst, Szablony, E-mail, Telefon, Obrazy, Profil",
            "categories": ["Wolny tekst", "Szablony", "E-mail", "Telefon", "Obrazy", "Profil"],
            "items": [_SKIP, {"text": "Zarządzaj według wolnego tekstu, szablonów, e-mail, telefon, obrazów i profilu."}, _SKIP, _SKIP, _SKIP, {"text": "Eksportuj kopie zapasowe i importuj, gdy potrzebujesz. Dostępne w 30-dniowym bezpłatnym okresie próbnym i Pro."}],
        },
        "themesSection": {"subtitle": "Jasny i ciemny, plus premium motywy kolorystyczne z Pro."},
        "comparison": {"appText": "Uporządkuj i zapisuj często używane teksty i informacje w przejrzysty sposób."},
        "privacySection": {"points": [_SKIP, "Nie wysyła automatycznie zapisanej treści na zewnętrzne serwery", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Eksportuj kopie zapasowe i importuj, gdy potrzebujesz. Dostępne w 30-dniowym bezpłatnym okresie próbnym i Pro."}]},
        "cta": {
            "titleLine1": "Codzienne teksty,",
            "titleLine2": "jedno dotknięcie.",
            "title": "Codzienne teksty, jedno dotknięcie.",
            "lead": "Zapisz, dotknij, potem wklej.",
            "button": "30 dni bezpłatnego okresu próbnego",
        },
        "sceneMore": {
            "lead": "Podróże, marketplace, czat, organizacja wydarzeń—kopiuj ulubiony tekst jednym dotknięciem w każdej sytuacji.",
            "cap3": "Teksty ogłoszeń od razu",
            "cap4": "Odpowiedzi na czacie od razu",
            "cap6": "Wiadomości organizatora od razu",
        },
    },
    "sv": {
        "meta": {
            "description": "Spara standardsvar, adresser, kontakter, URL:er, emoji, hashtags och mer—kopiera med ett tryck. Byt till din vanliga app och klistra in. MyQuickPaste gör det enklare att skriva på mobilen.",
            "ogDescription": "Spara texter och info du återanvänder, kopiera med ett tryck när du behöver. Byt till din vanliga app och klistra in.",
        },
        "hero": {
            "catchLine1": "Vardagstexter,",
            "catchLine2": "ett tryck bort.",
            "lead": "Standardsvar, adresser, kontakter, URL:er, emoji, hashtags. Spara det du återanvänder och kopiera med ett tryck från listan när du behöver.",
            "sub": "Byt sedan till din vanliga app och klistra in.",
        },
        "trust": {
            "t1Title": "Tryck för att kopiera",
            "t1Text": "Tryck bara på en sparad rad.",
            "t2Title": "Pro engångsköp",
            "t2Text": "Inga månadsbetalningar.",
            "t3Title": "Sparas på enheten",
            "t3Text": "Registrerat innehåll hanteras på enheten.",
            "t4Title": "UI på 21 språk",
            "t4Text": "Appskärmar på 21 språk.",
        },
        "pain": {
            "titleLine1": "Sluta fråga dig",
            "titleLine2": "«Var var det?»",
            "lead": "Samma info—men varje gång letar du i anteckningar, markerar om med långtryck eller skriver samma text igen. Små steg som staplas varje dag.",
            "p1Title": "Söka",
            "p1Text": "Adress eller standardsvar—du vet inte i vilken anteckning.",
            "p2Title": "Markera",
            "p2Text": "Långtryck för att få just den del du behöver.",
            "p3Title": "Skriva igen",
            "p3Text": "Du skriver samma svar eller profil om och om igen.",
            "resolveSub": "Sök inte. Skriv inte om. Tryck bara på raden du behöver.",
        },
        "steps": {"items": [{"text": "Registrera vanliga texter, kontakter och mer."}, _SKIP, _SKIP]},
        "sceneSocial": {
            "eyebrow": "Även för sociala medier",
            "titleLine1": "Emoji och hashtags—",
            "titleLine2": "kopiera när du behöver dem.",
            "lead": "Spara favorit-emoji, hashtags och inläggstexter. Tryck för att kopiera och klistra in i dina vanliga sociala appar.",
            "points": [
                {"title": "Emoji", "text": "Spara favoriter"},
                {"title": "Inlägg", "text": "Spara vanliga texter"},
                {"title": "Hashtags", "text": "Kopiera som set"},
                {"title": "Snabbkopiera", "text": "Ett tryck när det behövs"},
            ],
        },
        "sceneWork": {
            "eyebrow": "Även på jobbet",
            "titleLine1": "Standardsvar och kontakter—",
            "titleLine2": "kopiera när du behöver dem.",
            "lead": "Standardsvar, e-post, telefonnummer, URL:er och annan återanvänd info på ett ställe. Tryck på en rad för att kopiera direkt.",
            "points": [
                {"title": "Standardsvar", "text": "Dina vanliga svar"},
                {"title": "E-post", "text": "Spara signaturer och meddelanden"},
                {"title": "Kontakter", "text": "Kopiera nummer snabbt"},
                _SKIP,
            ],
        },
        "sceneDaily": {
            "eyebrow": "I vardagen",
            "titleLine1": "Adress och profil—",
            "titleLine2": "kopiera när du behöver dem.",
            "lead": "Hemadress, e-post, profiltext, favoritfraser. Tryck och kopiera direkt när du behöver.",
        },
        "features": {
            "categoriesLabel": "Kategorier: Fri text, Standardsvar, E-post, Telefon, Bilder, Profil",
            "categories": ["Fri text", "Standardsvar", "E-post", "Telefon", "Bilder", "Profil"],
            "items": [_SKIP, {"text": "Hantera efter fri text, standardsvar, e-post, telefon, bilder och profil."}, _SKIP, _SKIP, _SKIP, {"text": "Exportera säkerhetskopior och importera vid behov. Tillgängligt med 30 dagars gratis provperiod och Pro."}],
        },
        "themesSection": {"subtitle": "Ljust och mörkt, plus premiumfärgade teman med Pro."},
        "comparison": {"appText": "Organisera och spara återanvänd text och info tydligt och enkelt."},
        "privacySection": {"points": [_SKIP, "Skickar inte sparat innehåll automatiskt till externa servrar", _SKIP, _SKIP]},
        "faq": {"items": [_SKIP, _SKIP, _SKIP, _SKIP, _SKIP, {"a": "Exportera säkerhetskopior och importera vid behov. Tillgängligt med 30 dagars gratis provperiod och Pro."}]},
        "cta": {
            "titleLine1": "Vardagstexter,",
            "titleLine2": "ett tryck bort.",
            "title": "Vardagstexter, ett tryck bort.",
            "lead": "Spara, tryck, sedan klistra in.",
            "button": "30 dagars gratis provperiod",
        },
        "sceneMore": {
            "lead": "Resor, second hand, chatt, event—kopiera din favorittext med ett tryck i alla situationer.",
            "cap3": "Annonsannonser kopieras direkt",
            "cap4": "Chattsvar kopieras direkt",
            "cap6": "Organisatormeddelanden kopieras direkt",
        },
    },
}
# fmt: on


def main() -> None:
    if len(PATCHES) != 21:
        print(f"ERROR: expected 21 languages, got {len(PATCHES)}", file=sys.stderr)
        sys.exit(1)

    expected_keys = count_patch_leaves(PATCHES["ja"])
    summary: list[tuple[str, int]] = []

    for lang in LANGS:
        if lang not in PATCHES:
            print(f"ERROR: missing translations for {lang}", file=sys.stderr)
            sys.exit(1)

        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))

        # Preserve pricing subtree untouched (sanity snapshot)
        pricing_before = deepcopy(data.get("pricing"))

        n = deep_merge(data, PATCHES[lang])

        if deepcopy(data.get("pricing")) != pricing_before:
            print(f"ERROR: pricing was modified for {lang}", file=sys.stderr)
            sys.exit(1)

        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary.append((lang, n))
        print(f"Patched {path.name}: {n} keys")

    print()
    print("=== Summary ===")
    print(f"Expected leaf keys per language: {expected_keys}")
    for lang, n in summary:
        print(f"  {lang}: {n} keys patched")
    print(f"Total files: {len(summary)}")


if __name__ == "__main__":
    main()

