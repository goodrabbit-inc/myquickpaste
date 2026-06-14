# -*- coding: utf-8 -*-
"""Generate i18n/*.json for all Store listing languages."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "i18n"
STORE_URL = "https://apps.microsoft.com/detail/9N8WHWKDDSKK"

COMMON_FOOTER = {
    "copyright": "Copyright © 2025–2026 Good Rabbit inc., Japan. All rights reserved.",
    "developer": "Developed by Kazuhiro Suda",
}


def pack(meta_lang, title, description, lang_label, nav, hero, problem, benefits, features, usecases, pricing, cta):
    return {
        "meta": {"lang": meta_lang, "title": title, "description": description},
        "lang": {"label": lang_label},
        "nav": nav,
        "hero": hero,
        "problem": problem,
        "benefits": benefits,
        "features": features,
        "usecases": usecases,
        "pricing": pricing,
        "cta": cta,
        "footer": COMMON_FOOTER.copy(),
    }


LOCALES = {
    "ja": pack(
        "ja",
        "MyQuickPaste - ワンクリックで全文を貼り付け",
        "毎日同じ文章を何度もコピペしていませんか？MyQuickPasteは常に前面表示のWindows常駐型軽量ツール。Microsoft Storeで無料。",
        "言語",
        {"home": "ホーム", "support": "サポート", "releaseNotes": "リリースノート", "privacy": "プライバシー"},
        {
            "kicker": "MyQuickPaste",
            "catch": "毎日同じ文章を何度もコピペしていませんか？",
            "headline": "MyQuickPaste — 画面の隅に置いてワンクリックで素早く貼り付けできる、Windows用コピペ作業効率化・常駐型軽量ツール",
            "features": [
                {"label": "すぐ呼び出し", "text": "AIプロンプト、コードスニペット、メール定型文を素早く呼び出し。"},
                {"label": "かんたん登録", "text": "コピーした文章を即座に登録できるシンプルな仕組み。"},
                {"label": "100%ローカル保存", "text": "データ暗号化・完全プライバシー保護。クラウド送信なし。"},
                {"label": "すぐ使えるUI", "text": "初めてでも一瞬で分かる。横幅200px固定、常に最前面表示。"},
            ],
            "ctaPrimary": "Microsoft Store で無料ダウンロード",
            "ctaSecondary": "14日間、Pro全機能を無料でお試し",
            "trust": "Microsoft Store 認定 · データはPC内で暗号化保存",
            "screenshotAlt": "MyQuickPaste：一覧をクリックすると登録した全文が貼り付け。Editで一度だけ登録。",
        },
        {
            "title": "こんな経験、ありませんか？",
            "items": [
                "ChatGPTのプロンプトを毎回探し直している",
                "メールやチャットで同じ挨拶・返信文を何度も打っている",
                "Excelの数式やIDをメモ帳から探している",
            ],
            "solution": "MyQuickPasteなら、一度保存するだけ。常に前面に表示されるコンパクトなウィンドウから、いつでもどこでもペーストできます。",
        },
        {
            "title": "選ばれる3つの理由",
            "items": [
                {"title": "ワンクリックでペースト", "text": "保存した文字列を、作業の流れを止めずにすぐ貼り付け。"},
                {"title": "いつも手の届く場所に", "text": "コンパクトで常に前面表示。コピーのためにアプリを切り替える必要はありません。"},
                {"title": "プライバシー重視", "text": "データはPC内に暗号化して保存。クラウドには送信しません。"},
            ],
        },
        {
            "title": "主な機能",
            "items": [
                {"title": "テキストスロット", "text": "A〜Eの5タブで整理。無料版は10スロット、Proで拡張。"},
                {"title": "クリップボード履歴", "text": "直近20件を自動保存（Pro）。過去のコピーをすぐ呼び出せます。"},
                {"title": "クイック変換", "text": "日付・時刻の挿入や大文字/小文字変換をワンタップで。"},
                {"title": "21言語UI", "text": "日本語・英語を含む21言語のインターフェースに対応。"},
            ],
        },
        {
            "title": "こんな方におすすめ",
            "items": [
                {"title": "ビジネスパーソン", "text": "メール定型文、署名、よく使う返信文をワンクリックで。"},
                {"title": "クリエイター・開発者", "text": "AIプロンプト、コード片、テンプレートをすぐ貼り付け。"},
                {"title": "サポート・事務", "text": "FAQ回答や定型挨拶をチャットに即投入。"},
                {"title": "毎日PCで入力する方", "text": "同じ文字列の繰り返し入力を、今日からゼロに。"},
            ],
        },
        {
            "title": "料金",
            "freeTitle": "無料版",
            "freePrice": "¥0",
            "freeItems": ["テキストスロット最大10個", "ウィンドウサイズ変更", "21言語UI", "14日間Pro全機能試用"],
            "proTitle": "Pro版（買い切り）",
            "proPrice": "価格はStoreでご確認ください",
            "proItems": ["スロット数の拡張", "クリップボード履歴（20件）", "インポート / エクスポート", "買い切り・サブスクなし"],
            "note": "本体アプリは無料です。Pro版はMicrosoft Storeのアドオンとして購入できます。",
        },
        {
            "title": "繰り返し入力の時間を、もう無駄にしない",
            "lead": "数分でインストール。無料で始めて、14日間すべてのPro機能を体験できます。",
            "button": "Microsoft Store で無料ダウンロード",
        },
    ),
    "en": pack(
        "en",
        "MyQuickPaste - One Click. Paste the Full Text.",
        "Still copy-pasting the same text every day? MyQuickPaste is a slim, always-on-top Windows sidekick. Free on Microsoft Store.",
        "Language",
        {"home": "Home", "support": "Support", "releaseNotes": "Release Notes", "privacy": "Privacy"},
        {
            "kicker": "MyQuickPaste",
            "catch": "Still copying and pasting the same text over and over every day?",
            "headline": "MyQuickPaste — a slim, always-on-top Windows sidekick for faster copy-paste, ready in the corner of your screen with one-click paste",
            "features": [
                {"label": "Instant access", "text": "Pull up AI prompts, code snippets, and email templates in seconds."},
                {"label": "Simple setup", "text": "Register copied text instantly with a straightforward workflow."},
                {"label": "100% local storage", "text": "Encrypted on your PC. Complete privacy—nothing sent to the cloud."},
                {"label": "Ready in seconds", "text": "Easy from day one: ~200px wide, always on top, zero learning curve."},
            ],
            "ctaPrimary": "Download free on Microsoft Store",
            "ctaSecondary": "Try all Pro features free for 14 days",
            "trust": "Microsoft Store certified · Data encrypted locally on your PC",
            "screenshotAlt": "MyQuickPaste: click a slot to paste the full saved text. Setup once in Edit.",
        },
        {
            "title": "Sound familiar?",
            "items": [
                "Searching for the same ChatGPT prompt every time you need it",
                "Retyping the same greetings and replies in email and chat",
                "Hunting through Notepad for Excel formulas or IDs you use daily",
            ],
            "solution": "With MyQuickPaste, save it once. Paste from a compact always-on-top window anytime, anywhere.",
        },
        {
            "title": "Three reasons users love it",
            "items": [
                {"title": "One-click paste", "text": "Paste saved text into any app instantly without breaking your flow."},
                {"title": "Always within reach", "text": "Compact, always-on-top window. No more alt-tabbing just to copy and paste."},
                {"title": "Private by design", "text": "Your snippets stay on your PC, encrypted locally. Nothing sent to the cloud."},
            ],
        },
        {
            "title": "Key features",
            "items": [
                {"title": "Text slots", "text": "Organize across tabs A–E. Free: 10 slots. Pro unlocks more."},
                {"title": "Clipboard history", "text": "Auto-save your last 20 copies (Pro). Recall past clips in seconds."},
                {"title": "Quick transforms", "text": "Insert date, time, or change case before you paste with one tap."},
                {"title": "21-language UI", "text": "Interface available in 21 languages including English and Japanese."},
            ],
        },
        {
            "title": "Perfect for",
            "items": [
                {"title": "Business professionals", "text": "Email templates, signatures, and canned replies—one click away."},
                {"title": "Creators & developers", "text": "AI prompts, code snippets, and templates pasted instantly."},
                {"title": "Support & admin", "text": "Drop FAQ answers and standard greetings into chat in one click."},
                {"title": "Anyone who types daily", "text": "Eliminate repetitive typing starting today."},
            ],
        },
        {
            "title": "Pricing",
            "freeTitle": "Free",
            "freePrice": "$0",
            "freeItems": ["Up to 10 text slots", "Resizable window", "21-language UI", "14-day full Pro trial"],
            "proTitle": "Pro (one-time)",
            "proPrice": "See Store for price",
            "proItems": ["Expanded slot limit", "Clipboard history (20 items)", "Import / export", "One-time purchase, no subscription"],
            "note": "The base app is free. Pro is available as a Microsoft Store add-on.",
        },
        {
            "title": "Stop wasting time on repetitive typing",
            "lead": "Install in minutes. Start free and experience every Pro feature for 14 days.",
            "button": "Download free on Microsoft Store",
        },
    ),
}

# Additional locales: hero + meta fully localized; body sections follow native SaaS phrasing.
def hero_block(catch, headline, f1, f2, f3, f4, cta, cta2, trust, alt):
    return {
        "kicker": "MyQuickPaste",
        "catch": catch,
        "headline": headline,
        "features": [
            {"label": f1[0], "text": f1[1]},
            {"label": f2[0], "text": f2[1]},
            {"label": f3[0], "text": f3[1]},
            {"label": f4[0], "text": f4[1]},
        ],
        "ctaPrimary": cta,
        "ctaSecondary": cta2,
        "trust": trust,
        "screenshotAlt": alt,
    }


def add_locale(code, meta_lang, title, desc, lang_label, nav, hero, problem_title, problem_items, problem_solution,
               benefits_title, benefits, features_title, features, usecases_title, usecases,
               pricing, cta_title, cta_lead, cta_button):
    LOCALES[code] = pack(
        meta_lang, title, desc, lang_label, nav, hero,
        {"title": problem_title, "items": problem_items, "solution": problem_solution},
        {"title": benefits_title, "items": benefits},
        {"title": features_title, "items": features},
        {"title": usecases_title, "items": usecases},
        pricing,
        {"title": cta_title, "lead": cta_lead, "button": cta_button},
    )


add_locale(
    "fr", "fr",
    "MyQuickPaste - Collez tout le texte en un clic",
    "Vous copiez-collez les mêmes textes chaque jour ? MyQuickPaste, l'assistant Windows toujours au premier plan. Gratuit sur Microsoft Store.",
    "Langue",
    {"home": "Accueil", "support": "Assistance", "releaseNotes": "Notes de version", "privacy": "Confidentialité"},
    hero_block(
        "Vous copiez-collez encore les mêmes textes chaque jour ?",
        "MyQuickPaste — un outil Windows léger et toujours visible pour coller vos textes en un clic, depuis le coin de l'écran",
        ("Accès instantané", "Récupérez prompts IA, extraits de code et modèles d'e-mails en un instant."),
        ("Enregistrement simple", "Enregistrez un texte copié immédiatement, sans prise de tête."),
        ("100 % local", "Données chiffrées sur votre PC. Confidentialité totale, sans cloud."),
        ("Prêt en un clin d'œil", "Interface simple : ~200 px de large, toujours au premier plan."),
        "Télécharger gratuitement sur Microsoft Store",
        "Essai Pro gratuit pendant 14 jours",
        "Certifié Microsoft Store · Données chiffrées localement sur votre PC",
        "MyQuickPaste : cliquez sur un slot pour coller le texte complet. Configurez une fois dans Modifier.",
    ),
    "Ça vous parle ?", [
        "Retrouver le même prompt ChatGPT à chaque fois",
        "Retaper les mêmes salutations dans vos e-mails",
        "Chercher une formule Excel dans le Bloc-notes",
    ],
    "Avec MyQuickPaste, enregistrez une fois. Collez depuis une fenêtre compacte toujours visible.",
    "Trois raisons de l'adopter",
    [
        {"title": "Collage en un clic", "text": "Collez vos textes sans interrompre votre flux de travail."},
        {"title": "Toujours à portée de main", "text": "Fenêtre compacte et toujours au premier plan."},
        {"title": "Confidentialité", "text": "Vos données restent sur votre PC, chiffrées localement."},
    ],
    "Fonctionnalités clés",
    [
        {"title": "Slots de texte", "text": "Organisez par onglets A–E. Gratuit : 10 slots. Pro : plus."},
        {"title": "Historique du presse-papiers", "text": "20 derniers copies (Pro)."},
        {"title": "Transformations rapides", "text": "Date, heure, casse en un tap."},
        {"title": "Interface 21 langues", "text": "Disponible en 21 langues."},
    ],
    "Idéal pour",
    [
        {"title": "Professionnels", "text": "Modèles d'e-mails et réponses types en un clic."},
        {"title": "Créateurs & devs", "text": "Prompts IA, code et modèles instantanément."},
        {"title": "Support", "text": "FAQ et salutations prêtes à coller."},
        {"title": "Utilisateurs quotidiens", "text": "Fini la saisie répétitive."},
    ],
    {"title": "Tarifs", "freeTitle": "Gratuit", "freePrice": "0 €", "freeItems": ["10 slots", "Fenêtre redimensionnable", "21 langues", "Essai Pro 14 jours"],
     "proTitle": "Pro (achat unique)", "proPrice": "Voir le Store", "proItems": ["Plus de slots", "Historique (20)", "Import / export", "Sans abonnement"],
     "note": "L'application de base est gratuite. Pro disponible en add-on Store."},
    "Arrêtez de perdre du temps à retaper", "Installez en quelques minutes.", "Télécharger gratuitement sur Microsoft Store",
)

# Continue with de, zh-cn, zh-tw, ko, ru, it, es, pt, hi, ar, id, th, vi, tr, uk, nl, sv, pl
# Using similar pattern - I'll add remaining in the script file and run

# For brevity in this generator, load extended data from a second batch function
EXTENDED = []

def ext(code, meta_lang, title, desc, lang_label, nav, catch, headline, f1, f2, f3, f4, cta, cta2, trust, alt,
        pt, pi, ps, bt, bi, ft, fi, ut, ui, pr, ct, cl, cb):
    add_locale(code, meta_lang, title, desc, lang_label, nav,
               hero_block(catch, headline, f1, f2, f3, f4, cta, cta2, trust, alt),
               pt, pi, ps, bt, bi, ft, fi, ut, ui, pr, ct, cl, cb)

ext("de", "de", "MyQuickPaste – Mit einem Klick einfügen", "Kopieren Sie täglich denselben Text? Schlankes Windows-Tool, immer im Vordergrund. Kostenlos im Microsoft Store.", "Sprache",
    {"home": "Start", "support": "Support", "releaseNotes": "Versionshinweise", "privacy": "Datenschutz"},
    "Kopieren und einfügen Sie noch immer jeden Tag denselben Text?",
    "MyQuickPaste – schlankes, immer sichtbares Windows-Tool für schnelles Einfügen per Klick in der Bildschirmecke",
    ("Sofort abrufen", "KI-Prompts, Code-Snippets und E-Mail-Vorlagen blitzschnell nutzen."),
    ("Einfach speichern", "Kopierte Texte sofort registrieren – ganz unkompliziert."),
    ("100 % lokal", "Verschlüsselt auf dem PC. Volle Privatsphäre, kein Cloud-Upload."),
    ("Sofort verständlich", "Schmal (~200 px), immer im Vordergrund, sofort einsatzbereit."),
    "Kostenlos im Microsoft Store herunterladen", "14 Tage Pro kostenlos testen",
    "Microsoft Store-zertifiziert · Lokal verschlüsselt auf Ihrem PC",
    "MyQuickPaste: Slot anklicken, vollständigen Text einfügen. Einmal in Bearbeiten einrichten.",
    "Kommt Ihnen bekannt vor?", ["Immer wieder denselben ChatGPT-Prompt suchen", "Gleiche E-Mail-Grüße neu tippen", "Excel-Formeln im Editor suchen"],
    "Mit MyQuickPaste einmal speichern. Jederzeit aus dem kompakten Fenster einfügen.",
    "Drei Gründe für MyQuickPaste",
    [{"title": "Einfügen mit einem Klick", "text": "Ohne Workflow-Unterbrechung."}, {"title": "Immer griffbereit", "text": "Kompakt und immer im Vordergrund."}, {"title": "Privatsphäre", "text": "Verschlüsselt lokal auf dem PC."}],
    "Hauptfunktionen",
    [{"title": "Text-Slots", "text": "Tabs A–E. Gratis: 10 Slots."}, {"title": "Zwischenablage-Verlauf", "text": "20 Einträge (Pro)."}, {"title": "Schnellfunktionen", "text": "Datum, Uhrzeit, Groß/Klein."}, {"title": "21 Sprachen", "text": "Mehrsprachige Oberfläche."}],
    "Perfekt für",
    [{"title": "Business", "text": "E-Mail-Vorlagen per Klick."}, {"title": "Entwickler", "text": "Code und Prompts sofort einfügen."}, {"title": "Support", "text": "FAQ-Antworten bereithalten."}, {"title": "Tägliche PC-Nutzer", "text": "Wiederholtes Tippen eliminieren."}],
    {"title": "Preise", "freeTitle": "Kostenlos", "freePrice": "0 €", "freeItems": ["10 Slots", "Größe änderbar", "21 Sprachen", "14 Tage Pro-Test"],
     "proTitle": "Pro (Einmalkauf)", "proPrice": "Preis im Store", "proItems": ["Mehr Slots", "Verlauf (20)", "Import/Export", "Kein Abo"],
     "note": "Basis-App kostenlos. Pro als Store-Add-on."},
    "Schluss mit repetitivem Tippen", "In Minuten installiert.", "Kostenlos im Microsoft Store herunterladen")

# zh-cn
ext("zh-cn", "zh-CN", "MyQuickPaste - 一键粘贴全文", "还在每天重复复制粘贴相同文字？MyQuickPaste 是常驻屏幕角落的轻量 Windows 工具。Microsoft Store 免费下载。",
    "语言", {"home": "首页", "support": "支持", "releaseNotes": "发行说明", "privacy": "隐私"},
    "是否还在每天反复复制粘贴同样的文字？",
    "MyQuickPaste — 放在屏幕角落、一键快速粘贴的 Windows 复制粘贴效率常驻轻量工具",
    ("即时调用", "快速调出 AI 提示词、代码片段和邮件模板。"),
    ("简单注册", "复制的内容可立即保存，操作非常简单。"),
    ("100% 本地存储", "数据加密，完全保护隐私，不上传云端。"),
    ("上手即用", "新手也能秒懂：宽约 200px，始终置顶显示。"),
    "在 Microsoft Store 免费下载", "14 天免费试用 Pro 全部功能",
    "Microsoft Store 认证 · 数据在 PC 本地加密保存",
    "MyQuickPaste：点击槽位即可粘贴完整文本。在编辑中一次性设置。",
    "是否有同感？", ["每次都要找相同的 ChatGPT 提示词", "在邮件和聊天中重复输入相同问候语", "在记事本里找 Excel 公式或 ID"],
    "MyQuickPaste 一次保存，随时从置顶小窗粘贴。",
    "用户喜爱的三大理由",
    [{"title": "一键粘贴", "text": "不中断工作流程，立即粘贴。"}, {"title": "触手可及", "text": "小巧置顶，无需切换窗口。"}, {"title": "隐私优先", "text": "数据本地加密，不上传云端。"}],
    "主要功能",
    [{"title": "文本槽位", "text": "A–E 五个标签页整理。免费 10 个槽位。"}, {"title": "剪贴板历史", "text": "自动保存最近 20 条（Pro）。"}, {"title": "快速转换", "text": "插入日期、时间或更改大小写。"}, {"title": "21 种语言", "text": "界面支持 21 种语言。"}],
    "适合人群",
    [{"title": "商务人士", "text": "邮件模板和签名一键粘贴。"}, {"title": "创作者与开发者", "text": "AI 提示词和代码即时粘贴。"}, {"title": "客服支持", "text": "FAQ 和标准回复快速发送。"}, {"title": "日常 PC 用户", "text": "告别重复输入。"}],
    {"title": "价格", "freeTitle": "免费", "freePrice": "¥0", "freeItems": ["最多 10 个槽位", "可调窗口大小", "21 种语言", "14 天 Pro 试用"],
     "proTitle": "Pro（一次性购买）", "proPrice": "请在 Store 查看价格", "proItems": ["扩展槽位", "剪贴板历史（20 条）", "导入/导出", "一次性购买，无订阅"],
     "note": "基础应用免费。Pro 为 Microsoft Store 附加组件。"},
    "别再浪费时间重复输入", "几分钟即可安装。", "在 Microsoft Store 免费下载")

# zh-tw
ext("zh-tw", "zh-TW", "MyQuickPaste - 一鍵貼上全文", "還在每天重複複製貼上相同文字？MyQuickPaste 是常駐螢幕角落的輕量 Windows 工具。Microsoft Store 免費下載。",
    "語言", {"home": "首頁", "support": "支援", "releaseNotes": "版本資訊", "privacy": "隱私權"},
    "是否還在每天反覆複製貼上同樣的文字？",
    "MyQuickPaste — 放在螢幕角落、一鍵快速貼上的 Windows 複製貼上效率常駐輕量工具",
    ("即時呼叫", "快速叫出 AI 提示詞、程式碼片段和郵件範本。"),
    ("簡單註冊", "複製的內容可立即儲存，操作非常簡單。"),
    ("100% 本機儲存", "資料加密，完整保護隱私，不上傳雲端。"),
    ("立刻上手", "新手也能秒懂：寬約 200px，始終置頂顯示。"),
    "在 Microsoft Store 免費下載", "14 天免費試用 Pro 全部功能",
    "Microsoft Store 認證 · 資料在 PC 本機加密保存",
    "MyQuickPaste：點擊槽位即可貼上完整文字。在編輯中一次性設定。",
    "是否有同感？", ["每次都要找相同的 ChatGPT 提示詞", "在郵件和聊天中重複輸入相同問候語", "在記事本裡找 Excel 公式或 ID"],
    "MyQuickPaste 一次儲存，隨時從置頂小視窗貼上。",
    "使用者喜愛的三大理由",
    [{"title": "一鍵貼上", "text": "不中斷工作流程，立即貼上。"}, {"title": "触手可及", "text": "小巧置頂，無需切換視窗。"}, {"title": "隱私優先", "text": "資料本機加密，不上傳雲端。"}],
    "主要功能",
    [{"title": "文字槽位", "text": "A–E 五個標籤頁整理。免費 10 個槽位。"}, {"title": "剪貼簿歷史", "text": "自動保存最近 20 條（Pro）。"}, {"title": "快速轉換", "text": "插入日期、時間或變更大小寫。"}, {"title": "21 種語言", "text": "介面支援 21 種語言。"}],
    "適合對象",
    [{"title": "商務人士", "text": "郵件範本和簽名一鍵貼上。"}, {"title": "創作者與開發者", "text": "AI 提示詞和程式碼即時貼上。"}, {"title": "客服支援", "text": "FAQ 和標準回覆快速傳送。"}, {"title": "日常 PC 使用者", "text": "告別重複輸入。"}],
    {"title": "價格", "freeTitle": "免費", "freePrice": "NT$0", "freeItems": ["最多 10 個槽位", "可調視窗大小", "21 種語言", "14 天 Pro 試用"],
     "proTitle": "Pro（一次性購買）", "proPrice": "請在 Store 查看價格", "proItems": ["擴展槽位", "剪貼簿歷史（20 條）", "匯入/匯出", "一次性購買，無訂閱"],
     "note": "基本應用程式免費。Pro 為 Microsoft Store 附加元件。"},
    "別再浪費時間重複輸入", "幾分鐘即可安裝。", "在 Microsoft Store 免費下載")

from locales_remaining import register_remaining
register_remaining(ext)

if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    for code, data in LOCALES.items():
        path = ROOT / f"{code}.json"
        with path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path.name)

