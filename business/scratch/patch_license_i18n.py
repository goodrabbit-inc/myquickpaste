#!/usr/bin/env python3
"""Patch homepage i18n JSON — license/pricing/trial strings for all 21 languages."""
import json
import sys
from pathlib import Path

I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"
LANGS = [
    "en", "ja", "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]

# fmt: off
ALL = {
    "ja": {
        "nav_cta": "30日間の無料体験",
        "hero_cta_secondary": "30日間の無料体験",
        "hero_pill1": "30日間の無料体験",
        "hero_trial_title": "30日間の無料体験",
        "hero_trial_text": "初回インストール後30日間は、保存件数の上限アップとバックアップ機能を無料で体験できます。",
        "pricing_subtitle": "初回インストール後30日間は、保存件数の上限アップとバックアップ機能を無料で体験できます。期間後も無料版として使い続けられます。",
        "pricing_trial_title": "30日間の無料体験",
        "pricing_trial_text": "文字カテゴリ：各最大200件／画像：最大50件／プロフィール：最大30件／バックアップの書き出し・読み込み",
        "pricing_trial_note": "プレミアムテーマとカテゴリ名・アイコンの変更は、Pro購入後に利用できます。30日間の体験終了後も、登録したデータは削除されません。無料版の保存上限を超えたデータも保持され、Pro購入後に再び利用できます。",
        "pricing_free_lead": "基本機能は無料で使い続けられます。",
        "pricing_free_items": ["文字カテゴリ：各10件", "画像：10件", "プロフィール：1件", "検索", "並び替え", "クイック登録"],
        "pricing_pro_items": ["文字カテゴリ：各最大200件", "画像：最大50件", "プロフィール：最大30件", "バックアップの書き出し・読み込み", "プレミアムテーマ", "カテゴリ名・アイコンのカスタマイズ"],
        "cta_sub": "初回インストール後30日間、保存件数の上限アップとバックアップ機能を無料で体験できます。",
        "faq_trial_a": "いいえ。体験期間終了後は無料版として利用できます。登録したデータは削除されません。無料版の保存上限を超えたデータも保持され、Proを購入すると再び利用できます。",
        "support_free_pro_a": "無料版では、文字カテゴリ各10件、画像10件、プロフィール1件まで保存できます。コピー、データ登録、検索、並び替え、クイック登録も利用できます。Pro版では保存上限の拡大、バックアップの書き出し・読み込み、プレミアムテーマ、カテゴリ名・アイコンのカスタマイズが利用できます。初回インストール時は30日間、保存上限アップとバックアップを無料で体験できます（プレミアムテーマとカテゴリ名・アイコンの変更は Pro 購入後）。",
        "support_trial_a": "初回起動から30日間、文字カテゴリ各最大200件、画像最大50件、プロフィール最大30件、およびバックアップの書き出し・読み込みを無料で体験できます。プレミアムテーマとカテゴリ名・アイコンの変更は Pro 購入後のみ利用可能です。期間終了後も登録データは削除されません。無料版のまま使い続けるか、ストアで Pro を購入できます。",
        "release_trial_item": "無料版＋30日間の無料体験（保存上限アップ・バックアップ）",
    },
    "en": {
        "nav_cta": "30-day free trial",
        "hero_cta_secondary": "30-day free trial",
        "hero_pill1": "30-day free trial",
        "hero_trial_title": "30-day free trial",
        "hero_trial_text": "For 30 days after first install, try higher save limits and backup free of charge.",
        "pricing_subtitle": "For 30 days after first install, try higher save limits and backup free of charge. After that, keep using the free plan.",
        "pricing_trial_title": "30-day free trial",
        "pricing_trial_text": "Text categories: up to 200 items each · Images: up to 50 · Profiles: up to 30 · Backup export and import",
        "pricing_trial_note": "Premium themes and custom category names/icons are available after Pro purchase. After the 30-day trial, your saved data is not deleted. Data above free limits stays on your device and becomes usable again when you buy Pro.",
        "pricing_free_lead": "Core features stay free to use.",
        "pricing_free_items": ["Text categories: 10 items each", "Images: 10", "Profiles: 1", "Search", "Reorder", "Quick save"],
        "pricing_pro_items": ["Text categories: up to 200 items each", "Images: up to 50", "Profiles: up to 30", "Backup export and import", "Premium themes", "Custom category names and icons"],
        "cta_sub": "For 30 days after first install, try higher save limits and backup free of charge.",
        "faq_trial_a": "No. After the trial you can keep using the free plan. Your saved data is not deleted. Data above free limits stays on your device and becomes usable again when you buy Pro.",
        "support_free_pro_a": "The free plan includes up to 10 items per text category, 10 images, and 1 profile. Copy, add data, search, reorder, and quick save are available. Pro adds higher limits, backup export/import, premium themes, and custom category names/icons. New installs get 30 days to try higher limits and backup free (premium themes and category customization require Pro purchase).",
        "support_trial_a": "For 30 days from first launch, you can try up to 200 items per text category, 50 images, 30 profiles, and backup export/import free. Premium themes and category name/icon changes require Pro purchase. Your data is not deleted after the trial—you can stay on the free plan or buy Pro in the store.",
        "release_trial_item": "Free plan + 30-day free trial (higher limits and backup)",
    },
    "fr": {
        "nav_cta": "30 jours d'essai gratuit",
        "hero_cta_secondary": "30 jours d'essai gratuit",
        "hero_pill1": "30 jours d'essai gratuit",
        "hero_trial_title": "30 jours d'essai gratuit",
        "hero_trial_text": "Pendant 30 jours après la première installation, essayez gratuitement des limites plus élevées et la sauvegarde.",
        "pricing_subtitle": "Pendant 30 jours après la première installation, limites plus élevées et sauvegarde gratuites. Ensuite, continuez avec le forfait gratuit.",
        "pricing_trial_title": "30 jours d'essai gratuit",
        "pricing_trial_text": "Catégories texte : jusqu'à 200 chacune · Images : 50 · Profils : 30 · Export/import de sauvegarde",
        "pricing_trial_note": "Les thèmes premium et la personnalisation des catégories nécessitent l'achat Pro. Après l'essai, vos données ne sont pas supprimées. Les données au-delà des limites gratuites restent et redeviennent utilisables avec Pro.",
        "pricing_free_lead": "Les fonctions de base restent gratuites.",
        "pricing_free_items": ["Catégories texte : 10 chacune", "Images : 10", "Profils : 1", "Recherche", "Réorganisation", "Enregistrement rapide"],
        "pricing_pro_items": ["Catégories texte : jusqu'à 200 chacune", "Images : 50", "Profils : 30", "Export/import de sauvegarde", "Thèmes premium", "Noms et icônes de catégories personnalisés"],
        "cta_sub": "Pendant 30 jours après la première installation, essayez gratuitement des limites plus élevées et la sauvegarde.",
        "faq_trial_a": "Non. Après l'essai, vous pouvez continuer avec le forfait gratuit. Vos données ne sont pas supprimées. Les données au-delà des limites gratuites restent et redeviennent utilisables avec Pro.",
        "support_free_pro_a": "Le forfait gratuit inclut 10 éléments par catégorie texte, 10 images et 1 profil. Copie, ajout, recherche, réorganisation et enregistrement rapide sont inclus. Pro ajoute limites plus élevées, sauvegarde, thèmes premium et personnalisation des catégories. Nouvelle installation : 30 jours d'essai gratuit des limites et sauvegarde (thèmes premium et personnalisation Pro).",
        "support_trial_a": "Pendant 30 jours après le premier lancement : jusqu'à 200 éléments par catégorie texte, 50 images, 30 profils et sauvegarde gratuits. Thèmes premium et personnalisation Pro uniquement. Les données ne sont pas supprimées après l'essai.",
        "release_trial_item": "Forfait gratuit + 30 jours d'essai gratuit (limites et sauvegarde)",
    },
    "de": {
        "nav_cta": "30 Tage kostenlos testen",
        "hero_cta_secondary": "30 Tage kostenlos testen",
        "hero_pill1": "30 Tage kostenlos testen",
        "hero_trial_title": "30 Tage kostenlose Testphase",
        "hero_trial_text": "30 Tage nach der Erstinstallation können Sie höhere Speichergrenzen und Backup kostenlos testen.",
        "pricing_subtitle": "30 Tage nach der Erstinstallation: höhere Speichergrenzen und Backup kostenlos testen. Danach weiter mit dem kostenlosen Plan.",
        "pricing_trial_title": "30 Tage kostenlose Testphase",
        "pricing_trial_text": "Textkategorien: je bis zu 200 · Bilder: bis zu 50 · Profile: bis zu 30 · Backup exportieren/importieren",
        "pricing_trial_note": "Premium-Themes und angepasste Kategorienamen/-symbole sind nach Pro-Kauf verfügbar. Nach der Testphase werden Ihre Daten nicht gelöscht. Daten über den Gratis-Grenzen bleiben erhalten und sind nach Pro-Kauf wieder nutzbar.",
        "pricing_free_lead": "Grundfunktionen bleiben kostenlos nutzbar.",
        "pricing_free_items": ["Textkategorien: je 10 Einträge", "Bilder: 10", "Profile: 1", "Suche", "Sortieren", "Schnellspeichern"],
        "pricing_pro_items": ["Textkategorien: je bis zu 200", "Bilder: bis zu 50", "Profile: bis zu 30", "Backup exportieren/importieren", "Premium-Themes", "Kategorienamen und -symbole anpassen"],
        "cta_sub": "30 Tage nach der Erstinstallation: höhere Speichergrenzen und Backup kostenlos testen.",
        "faq_trial_a": "Nein. Nach der Testphase können Sie den kostenlosen Plan weiter nutzen. Ihre Daten werden nicht gelöscht. Daten über den Gratis-Grenzen bleiben erhalten und sind nach Pro-Kauf wieder nutzbar.",
        "support_free_pro_a": "Der kostenlose Plan umfasst je 10 Einträge pro Textkategorie, 10 Bilder und 1 Profil. Kopieren, Speichern, Suche, Sortieren und Schnellspeichern sind enthalten. Pro bietet höhere Limits, Backup, Premium-Themes und Kategorie-Anpassung. Neue Installationen: 30 Tage höhere Limits und Backup kostenlos (Premium-Themes und Kategorie-Anpassung erfordern Pro).",
        "support_trial_a": "30 Tage ab erstem Start: bis zu 200 Einträge pro Textkategorie, 50 Bilder, 30 Profile und Backup kostenlos testen. Premium-Themes und Kategorie-Anpassung erfordern Pro. Daten werden nach der Testphase nicht gelöscht.",
        "release_trial_item": "Kostenloser Plan + 30 Tage kostenlose Testphase (höhere Limits und Backup)",
    },
    "zh": {
        "nav_cta": "30 天免费体验",
        "hero_cta_secondary": "30 天免费体验",
        "hero_pill1": "30 天免费体验",
        "hero_trial_title": "30 天免费体验",
        "hero_trial_text": "首次安装后 30 天内，可免费体验更高的保存上限和备份功能。",
        "pricing_subtitle": "首次安装后 30 天内，可免费体验更高的保存上限和备份功能。之后仍可继续使用免费版。",
        "pricing_trial_title": "30 天免费体验",
        "pricing_trial_text": "文字分类：各类最多 200 条 · 图片：最多 50 · 资料：最多 30 · 备份导出/导入",
        "pricing_trial_note": "高级主题以及分类名称/图标更改需购买 Pro 后使用。30 天体验结束后，已注册的数据不会删除。超出免费上限的数据也会保留，购买 Pro 后可再次使用。",
        "pricing_free_lead": "基本功能可永久免费使用。",
        "pricing_free_items": ["文字分类：各类 10 条", "图片：10 张", "资料：1 个", "搜索", "排序", "快速注册"],
        "pricing_pro_items": ["文字分类：各类最多 200 条", "图片：最多 50 张", "资料：最多 30 个", "备份导出/导入", "高级主题", "分类名称与图标自定义"],
        "cta_sub": "首次安装后 30 天内，可免费体验更高的保存上限和备份功能。",
        "faq_trial_a": "不会。体验结束后仍可继续使用免费版。已注册的数据不会删除。超出免费上限的数据也会保留，购买 Pro 后可再次使用。",
        "support_free_pro_a": "免费版每类文字最多 10 条、图片 10 张、资料 1 个。复制、注册、搜索、排序、快速注册均可使用。Pro 提供更高上限、备份、高级主题和分类自定义。新安装可 30 天免费体验更高上限和备份（高级主题与分类更改需购买 Pro）。",
        "support_trial_a": "首次启动后 30 天内，可免费体验每类文字最多 200 条、图片 50 张、资料 30 个及备份导出/导入。高级主题与分类更改需购买 Pro。体验结束后数据不会删除。",
        "release_trial_item": "免费版 + 30 天免费体验（更高上限与备份）",
    },
    "zh_TW": {
        "nav_cta": "30 天免費體驗",
        "hero_cta_secondary": "30 天免費體驗",
        "hero_pill1": "30 天免費體驗",
        "hero_trial_title": "30 天免費體驗",
        "hero_trial_text": "首次安裝後 30 天內，可免費體驗更高的保存上限和備份功能。",
        "pricing_subtitle": "首次安裝後 30 天內，可免費體驗更高的保存上限和備份功能。之後仍可繼續使用免費版。",
        "pricing_trial_title": "30 天免費體驗",
        "pricing_trial_text": "文字分類：各類最多 200 則 · 圖片：最多 50 · 個人資料：最多 30 · 備份匯出/匯入",
        "pricing_trial_note": "進階主題以及分類名稱/圖示變更需購買 Pro 後使用。30 天體驗結束後，已註冊的資料不會刪除。超出免費上限的資料也會保留，購買 Pro 後可再次使用。",
        "pricing_free_lead": "基本功能可永久免費使用。",
        "pricing_free_items": ["文字分類：各類 10 則", "圖片：10 張", "個人資料：1 個", "搜尋", "排序", "快速註冊"],
        "pricing_pro_items": ["文字分類：各類最多 200 則", "圖片：最多 50 張", "個人資料：最多 30 個", "備份匯出/匯入", "進階主題", "分類名稱與圖示自訂"],
        "cta_sub": "首次安裝後 30 天內，可免費體驗更高的保存上限和備份功能。",
        "faq_trial_a": "不會。體驗結束後仍可繼續使用免費版。已註冊的資料不會刪除。超出免費上限的資料也會保留，購買 Pro 後可再次使用。",
        "support_free_pro_a": "免費版每類文字最多 10 則、圖片 10 張、個人資料 1 個。複製、註冊、搜尋、排序、快速註冊均可使用。Pro 提供更高上限、備份、進階主題和分類自訂。新安裝可 30 天免費體驗更高上限和備份（進階主題與分類更改需購買 Pro）。",
        "support_trial_a": "首次啟動後 30 天內，可免費體驗每類文字最多 200 則、圖片 50 張、個人資料 30 個及備份匯出/匯入。進階主題與分類更改需購買 Pro。體驗結束後資料不會刪除。",
        "release_trial_item": "免費版 + 30 天免費體驗（更高上限與備份）",
    },
    "ko": {
        "nav_cta": "30일 무료 체험",
        "hero_cta_secondary": "30일 무료 체험",
        "hero_pill1": "30일 무료 체험",
        "hero_trial_title": "30일 무료 체험",
        "hero_trial_text": "첫 설치 후 30일 동안 저장 한도 확대와 백업 기능을 무료로 체험할 수 있습니다.",
        "pricing_subtitle": "첫 설치 후 30일 동안 저장 한도 확대와 백업을 무료로 체험할 수 있습니다. 이후에도 무료 플랜으로 계속 사용할 수 있습니다.",
        "pricing_trial_title": "30일 무료 체험",
        "pricing_trial_text": "텍스트 카테고리: 각 최대 200개 · 이미지: 최대 50 · 프로필: 최대 30 · 백업 내보내기/가져오기",
        "pricing_trial_note": "프리미엄 테마와 카테고리 이름/아이콘 변경은 Pro 구매 후 이용 가능합니다. 30일 체험 종료 후에도 등록 데이터는 삭제되지 않습니다. 무료 한도를 초과한 데이터도 보관되며 Pro 구매 후 다시 이용할 수 있습니다.",
        "pricing_free_lead": "기본 기능은 무료로 계속 사용할 수 있습니다.",
        "pricing_free_items": ["텍스트 카테고리: 각 10개", "이미지: 10개", "프로필: 1개", "검색", "정렬", "빠른 등록"],
        "pricing_pro_items": ["텍스트 카테고리: 각 최대 200개", "이미지: 최대 50개", "프로필: 최대 30개", "백업 내보내기/가져오기", "프리미엄 테마", "카테고리 이름·아이콘 사용자 지정"],
        "cta_sub": "첫 설치 후 30일 동안 저장 한도 확대와 백업 기능을 무료로 체험할 수 있습니다.",
        "faq_trial_a": "아니요. 체험 종료 후에도 무료 플랜으로 계속 사용할 수 있습니다. 등록 데이터는 삭제되지 않습니다. 무료 한도를 초과한 데이터도 보관되며 Pro 구매 후 다시 이용할 수 있습니다.",
        "support_free_pro_a": "무료 플랜은 텍스트 카테고리 각 10개, 이미지 10개, 프로필 1개까지 저장할 수 있습니다. 복사, 등록, 검색, 정렬, 빠른 등록도 이용 가능합니다. Pro는 한도 확대, 백업, 프리미엄 테마, 카테고리 사용자 지정을 제공합니다. 신규 설치 시 30일간 한도 확대와 백업을 무료 체험(프리미엄 테마·카테고리 변경은 Pro 구매 후).",
        "support_trial_a": "첫 실행 후 30일 동안 텍스트 카테고리 각 최대 200개, 이미지 50개, 프로필 30개, 백업 내보내기/가져오기를 무료 체험할 수 있습니다. 프리미엄 테마와 카테고리 변경은 Pro 구매 후만 가능합니다. 체험 종료 후에도 데이터는 삭제되지 않습니다.",
        "release_trial_item": "무료 플랜 + 30일 무료 체험(저장 한도 확대·백업)",
    },
    "ru": {
        "nav_cta": "30 дней бесплатного пробного периода",
        "hero_cta_secondary": "30 дней бесплатного пробного периода",
        "hero_pill1": "30 дней бесплатного пробного периода",
        "hero_trial_title": "30 дней бесплатного пробного периода",
        "hero_trial_text": "В течение 30 дней после первой установки вы можете бесплатно попробовать повышенные лимиты сохранения и резервное копирование.",
        "pricing_subtitle": "В течение 30 дней после первой установки — повышенные лимиты и резервное копирование бесплатно. Затем можно продолжить пользоваться бесплатным планом.",
        "pricing_trial_title": "30 дней бесплатного пробного периода",
        "pricing_trial_text": "Текстовые категории: до 200 в каждой · Изображения: до 50 · Профили: до 30 · Экспорт/импорт резервной копии",
        "pricing_trial_note": "Премиум-темы и настройка названий/значков категорий доступны после покупки Pro. После пробного периода ваши данные не удаляются. Данные сверх бесплатных лимитов сохраняются и снова становятся доступны после покупки Pro.",
        "pricing_free_lead": "Основные функции остаются бесплатными.",
        "pricing_free_items": ["Текстовые категории: по 10", "Изображения: 10", "Профили: 1", "Поиск", "Сортировка", "Быстрое сохранение"],
        "pricing_pro_items": ["Текстовые категории: до 200 в каждой", "Изображения: до 50", "Профили: до 30", "Экспорт/импорт резервной копии", "Премиум-темы", "Свои названия и значки категорий"],
        "cta_sub": "В течение 30 дней после первой установки попробуйте повышенные лимиты и резервное копирование бесплатно.",
        "faq_trial_a": "Нет. После пробного периода можно продолжить пользоваться бесплатным планом. Сохранённые данные не удаляются. Данные сверх бесплатных лимитов сохраняются и снова становятся доступны после покупки Pro.",
        "support_free_pro_a": "Бесплатный план включает до 10 элементов в каждой текстовой категории, 10 изображений и 1 профиль. Доступны копирование, добавление, поиск, сортировка и быстрое сохранение. Pro добавляет повышенные лимиты, резервное копирование, премиум-темы и настройку категорий. При новой установке — 30 дней бесплатного пробного периода лимитов и резервного копирования (премиум-темы и настройка категорий — после покупки Pro).",
        "support_trial_a": "В течение 30 дней с первого запуска: до 200 элементов в каждой текстовой категории, 50 изображений, 30 профилей и резервное копирование бесплатно. Премиум-темы и настройка категорий требуют покупки Pro. Данные после пробного периода не удаляются.",
        "release_trial_item": "Бесплатный план + 30 дней бесплатного пробного периода (повышенные лимиты и резервное копирование)",
    },
    "it": {
        "nav_cta": "30 giorni di prova gratuita",
        "hero_cta_secondary": "30 giorni di prova gratuita",
        "hero_pill1": "30 giorni di prova gratuita",
        "hero_trial_title": "30 giorni di prova gratuita",
        "hero_trial_text": "Per 30 giorni dopo la prima installazione, prova gratis limiti più alti e backup.",
        "pricing_subtitle": "Per 30 giorni dopo la prima installazione, prova gratis limiti più alti e backup. Poi continua con il piano gratuito.",
        "pricing_trial_title": "30 giorni di prova gratuita",
        "pricing_trial_text": "Categorie testo: fino a 200 ciascuna · Immagini: 50 · Profili: 30 · Esportazione/importazione backup",
        "pricing_trial_note": "Temi premium e personalizzazione categorie richiedono l'acquisto Pro. Dopo i 30 giorni i dati non vengono eliminati. I dati oltre i limiti gratuiti restano e tornano utilizzabili con Pro.",
        "pricing_free_lead": "Le funzioni base restano gratuite.",
        "pricing_free_items": ["Categorie testo: 10 ciascuna", "Immagini: 10", "Profili: 1", "Ricerca", "Riordino", "Salvataggio rapido"],
        "pricing_pro_items": ["Categorie testo: fino a 200 ciascuna", "Immagini: 50", "Profili: 30", "Esportazione/importazione backup", "Temi premium", "Nomi e icone categorie personalizzati"],
        "cta_sub": "Per 30 giorni dopo la prima installazione, prova gratis limiti più alti e backup.",
        "faq_trial_a": "No. Dopo la prova puoi continuare con il piano gratuito. I dati salvati non vengono eliminati. I dati oltre i limiti gratuiti restano e tornano utilizzabili con Pro.",
        "support_free_pro_a": "Il piano gratuito include 10 elementi per categoria testo, 10 immagini e 1 profilo. Copia, registrazione, ricerca, riordino e salvataggio rapido sono disponibili. Pro aggiunge limiti più alti, backup, temi premium e personalizzazione categorie. Nuova installazione: 30 giorni di prova gratuita di limiti e backup (temi premium e personalizzazione richiedono Pro).",
        "support_trial_a": "Per 30 giorni dal primo avvio: fino a 200 elementi per categoria testo, 50 immagini, 30 profili e backup gratis. Temi premium e personalizzazione richiedono Pro. I dati non vengono eliminati dopo la prova.",
        "release_trial_item": "Piano gratuito + 30 giorni di prova gratuita (limiti e backup)",
    },
    "es": {
        "nav_cta": "30 días de prueba gratis",
        "hero_cta_secondary": "30 días de prueba gratis",
        "hero_pill1": "30 días de prueba gratis",
        "hero_trial_title": "30 días de prueba gratis",
        "hero_trial_text": "Durante 30 días tras la primera instalación, prueba gratis límites más altos y copia de seguridad.",
        "pricing_subtitle": "Durante 30 días tras la primera instalación, prueba gratis límites más altos y copia de seguridad. Después, sigue con el plan gratuito.",
        "pricing_trial_title": "30 días de prueba gratis",
        "pricing_trial_text": "Categorías de texto: hasta 200 cada una · Imágenes: 50 · Perfiles: 30 · Exportar/importar copia de seguridad",
        "pricing_trial_note": "Los temas premium y la personalización de categorías requieren comprar Pro. Tras los 30 días, tus datos no se eliminan. Los datos por encima del límite gratuito se conservan y vuelven a estar disponibles con Pro.",
        "pricing_free_lead": "Las funciones básicas siguen siendo gratuitas.",
        "pricing_free_items": ["Categorías de texto: 10 cada una", "Imágenes: 10", "Perfiles: 1", "Búsqueda", "Reordenar", "Registro rápido"],
        "pricing_pro_items": ["Categorías de texto: hasta 200 cada una", "Imágenes: 50", "Perfiles: 30", "Exportar/importar copia de seguridad", "Temas premium", "Nombres e iconos de categoría personalizados"],
        "cta_sub": "Durante 30 días tras la primera instalación, prueba gratis límites más altos y copia de seguridad.",
        "faq_trial_a": "No. Tras la prueba puedes seguir con el plan gratuito. Tus datos no se eliminan. Los datos por encima del límite gratuito se conservan y vuelven a estar disponibles con Pro.",
        "support_free_pro_a": "El plan gratuito incluye 10 elementos por categoría de texto, 10 imágenes y 1 perfil. Copiar, registrar, buscar, reordenar y registro rápido están disponibles. Pro añade límites más altos, copia de seguridad, temas premium y personalización de categorías. Instalación nueva: 30 días de prueba gratis de límites y copia de seguridad (temas premium y personalización requieren Pro).",
        "support_trial_a": "Durante 30 días desde el primer inicio: hasta 200 elementos por categoría de texto, 50 imágenes, 30 perfiles y copia de seguridad gratis. Temas premium y personalización requieren Pro. Los datos no se eliminan tras la prueba.",
        "release_trial_item": "Plan gratuito + 30 días de prueba gratis (límites y copia de seguridad)",
    },
    "pt": {
        "nav_cta": "30 dias de teste grátis",
        "hero_cta_secondary": "30 dias de teste grátis",
        "hero_pill1": "30 dias de teste grátis",
        "hero_trial_title": "30 dias de teste grátis",
        "hero_trial_text": "Por 30 dias após a primeira instalação, experimente gratuitamente limites maiores e backup.",
        "pricing_subtitle": "Por 30 dias após a primeira instalação, experimente gratuitamente limites maiores e backup. Depois, continue no plano gratuito.",
        "pricing_trial_title": "30 dias de teste grátis",
        "pricing_trial_text": "Categorias de texto: até 200 cada · Imagens: 50 · Perfis: 30 · Exportar/importar backup",
        "pricing_trial_note": "Temas premium e personalização de categorias exigem compra do Pro. Após os 30 dias, seus dados não são excluídos. Dados acima do limite gratuito permanecem e voltam a ficar disponíveis com Pro.",
        "pricing_free_lead": "Os recursos básicos continuam gratuitos.",
        "pricing_free_items": ["Categorias de texto: 10 cada", "Imagens: 10", "Perfis: 1", "Pesquisa", "Reordenar", "Registro rápido"],
        "pricing_pro_items": ["Categorias de texto: até 200 cada", "Imagens: 50", "Perfis: 30", "Exportar/importar backup", "Temas premium", "Nomes e ícones de categoria personalizados"],
        "cta_sub": "Por 30 dias após a primeira instalação, experimente gratuitamente limites maiores e backup.",
        "faq_trial_a": "Não. Após o teste você pode continuar no plano gratuito. Seus dados não são excluídos. Dados acima do limite gratuito permanecem e voltam a ficar disponíveis com Pro.",
        "support_free_pro_a": "O plano gratuito inclui 10 itens por categoria de texto, 10 imagens e 1 perfil. Copiar, registrar, pesquisar, reordenar e registro rápido estão disponíveis. Pro adiciona limites maiores, backup, temas premium e personalização de categorias. Nova instalação: 30 dias de teste grátis de limites e backup (temas premium e personalização exigem Pro).",
        "support_trial_a": "Por 30 dias desde o primeiro início: até 200 itens por categoria de texto, 50 imagens, 30 perfis e backup grátis. Temas premium e personalização exigem Pro. Os dados não são excluídos após o teste.",
        "release_trial_item": "Plano gratuito + 30 dias de teste grátis (limites e backup)",
    },
    "hi": {
        "nav_cta": "30 दिन का निःशुल्क परीक्षण",
        "hero_cta_secondary": "30 दिन का निःशुल्क परीक्षण",
        "hero_pill1": "30 दिन का निःशुल्क परीक्षण",
        "hero_trial_title": "30 दिन का निःशुल्क परीक्षण",
        "hero_trial_text": "पहली इंस्टॉल के बाद 30 दिनों तक उच्च सहेज सीमा और बैकअप निःशुल्क आज़माएँ।",
        "pricing_subtitle": "पहली इंस्टॉल के बाद 30 दिनों तक उच्च सहेज सीमा और बैकअप निःशुल्क। उसके बाद भी मुफ़्त प्लान जारी रखें।",
        "pricing_trial_title": "30 दिन का निःशुल्क परीक्षण",
        "pricing_trial_text": "टेक्स्ट श्रेणियाँ: प्रत्येक में अधिकतम 200 · छवियाँ: 50 · प्रोफ़ाइल: 30 · बैकअप निर्यात/आयात",
        "pricing_trial_note": "प्रीमियम थीम और श्रेणी नाम/आइकन बदलाव Pro खरीद के बाद उपलब्ध। 30 दिन बाद आपका डेटा हटाया नहीं जाता। मुफ़्त सीमा से अधिक डेटा रखा जाता है और Pro खरीदने पर फिर उपयोग हो सकता है।",
        "pricing_free_lead": "मुख्य सुविधाएँ मुफ़्त में बनी रहती हैं।",
        "pricing_free_items": ["टेक्स्ट श्रेणियाँ: प्रत्येक में 10", "छवियाँ: 10", "प्रोफ़ाइल: 1", "खोज", "क्रम बदलना", "त्वरित सहेज"],
        "pricing_pro_items": ["टेक्स्ट श्रेणियाँ: प्रत्येक में अधिकतम 200", "छवियाँ: 50", "प्रोफ़ाइल: 30", "बैकअप निर्यात/आयात", "प्रीमियम थीम", "श्रेणी नाम और आइकन अनुकूलन"],
        "cta_sub": "पहली इंस्टॉल के बाद 30 दिनों तक उच्च सहेज सीमा और बैकअप निःशुल्क आज़माएँ।",
        "faq_trial_a": "नहीं। परीक्षण के बाद आप मुफ़्त प्लान पर जारी रख सकते हैं। आपका सहेजा डेटा हटाया नहीं जाता। मुफ़्त सीमा से अधिक डेटा रखा जाता है और Pro खरीदने पर फिर उपयोग हो सकता है।",
        "support_free_pro_a": "मुफ़्त प्लान में प्रत्येक टेक्स्ट श्रेणी में 10 आइटम, 10 छवियाँ और 1 प्रोफ़ाइल शामिल हैं। कॉपी, जोड़ना, खोज, क्रम बदलना और त्वरित सहेज उपलब्ध हैं। Pro उच्च सीमा, बैकअप, प्रीमियम थीम और श्रेणी अनुकूलन देता है। नई इंस्टॉल: 30 दिन निःशुल्क सीमा और बैकअप (प्रीमियम थीम और अनुकूलन Pro खरीद के बाद)।",
        "support_trial_a": "पहले लॉन्च से 30 दिन: प्रत्येक टेक्स्ट श्रेणी में 200, 50 छवियाँ, 30 प्रोफ़ाइल और बैकअप निःशुल्क। प्रीमियम थीम और अनुकूलन Pro खरीद चाहते। परीक्षण के बाद डेटा हटाया नहीं जाता।",
        "release_trial_item": "मुफ़्त प्लान + 30 दिन निःशुल्क परीक्षण (उच्च सीमा और बैकअप)",
    },
    "ar": {
        "nav_cta": "تجربة مجانية لمدة 30 يومًا",
        "hero_cta_secondary": "تجربة مجانية لمدة 30 يومًا",
        "hero_pill1": "تجربة مجانية لمدة 30 يومًا",
        "hero_trial_title": "تجربة مجانية لمدة 30 يومًا",
        "hero_trial_text": "لمدة 30 يومًا بعد التثبيت الأول، جرّب حدود حفظ أعلى والنسخ الاحتياطي مجانًا.",
        "pricing_subtitle": "لمدة 30 يومًا بعد التثبيت الأول، جرّب حدود حفظ أعلى والنسخ الاحتياطي مجانًا. بعد ذلك استمر في الخطة المجانية.",
        "pricing_trial_title": "تجربة مجانية لمدة 30 يومًا",
        "pricing_trial_text": "فئات النص: حتى 200 لكل فئة · الصور: 50 · الملفات الشخصية: 30 · تصدير/استيراد النسخ الاحتياطي",
        "pricing_trial_note": "السمات المميزة وتخصيص أسماء/أيقونات الفئات متاح بعد شراء Pro. بعد التجربة لا تُحذف بياناتك. البيانات فوق حدود الخطة المجانية تبقى وتصبح قابلة للاستخدام مجددًا عند شراء Pro.",
        "pricing_free_lead": "الميزات الأساسية تبقى مجانية.",
        "pricing_free_items": ["فئات النص: 10 لكل فئة", "الصور: 10", "الملفات الشخصية: 1", "البحث", "إعادة الترتيب", "الحفظ السريع"],
        "pricing_pro_items": ["فئات النص: حتى 200 لكل فئة", "الصور: 50", "الملفات الشخصية: 30", "تصدير/استيراد النسخ الاحتياطي", "السمات المميزة", "أسماء وأيقونات فئات مخصّصة"],
        "cta_sub": "لمدة 30 يومًا بعد التثبيت الأول، جرّب حدود حفظ أعلى والنسخ الاحتياطي مجانًا.",
        "faq_trial_a": "لا. بعد التجربة يمكنك الاستمرار في الخطة المجانية. بياناتك المحفوظة لا تُحذف. البيانات فوق حدود الخطة المجانية تبقى وتصبح قابلة للاستخدام مجددًا عند شراء Pro.",
        "support_free_pro_a": "تتضمن الخطة المجانية 10 عناصر لكل فئة نص، و10 صور، وملفًا شخصيًا واحدًا. النسخ والإضافة والبحث وإعادة الترتيب والحفظ السريع متاحة. يضيف Pro حدودًا أعلى والنسخ الاحتياطي والسمات المميزة وتخصيص الفئات. التثبيت الجديد: 30 يومًا تجربة مجانية للحدود والنسخ الاحتياطي (السمات المميزة والتخصيص يتطلبان شراء Pro).",
        "support_trial_a": "لمدة 30 يومًا من أول تشغيل: حتى 200 عنصر لكل فئة نص، و50 صورة، و30 ملفًا شخصيًا، والنسخ الاحتياطي مجانًا. السمات المميزة والتخصيص يتطلبان Pro. لا تُحذف البيانات بعد التجربة.",
        "release_trial_item": "الخطة المجانية + تجربة مجانية 30 يومًا (حدود أعلى ونسخ احتياطي)",
    },
    "id": {
        "nav_cta": "Uji coba gratis 30 hari",
        "hero_cta_secondary": "Uji coba gratis 30 hari",
        "hero_pill1": "Uji coba gratis 30 hari",
        "hero_trial_title": "Uji coba gratis 30 hari",
        "hero_trial_text": "Selama 30 hari setelah instalasi pertama, coba batas simpan lebih tinggi dan cadangan secara gratis.",
        "pricing_subtitle": "Selama 30 hari setelah instalasi pertama, coba batas simpan lebih tinggi dan cadangan gratis. Setelah itu, lanjutkan paket gratis.",
        "pricing_trial_title": "Uji coba gratis 30 hari",
        "pricing_trial_text": "Kategori teks: hingga 200 masing-masing · Gambar: 50 · Profil: 30 · Ekspor/impor cadangan",
        "pricing_trial_note": "Tema premium dan kustomisasi nama/ikon kategori tersedia setelah membeli Pro. Setelah uji coba, data Anda tidak dihapus. Data di atas batas gratis tetap tersimpan dan bisa digunakan lagi setelah membeli Pro.",
        "pricing_free_lead": "Fitur inti tetap gratis digunakan.",
        "pricing_free_items": ["Kategori teks: 10 masing-masing", "Gambar: 10", "Profil: 1", "Pencarian", "Urut ulang", "Simpan cepat"],
        "pricing_pro_items": ["Kategori teks: hingga 200 masing-masing", "Gambar: 50", "Profil: 30", "Ekspor/impor cadangan", "Tema premium", "Nama dan ikon kategori kustom"],
        "cta_sub": "Selama 30 hari setelah instalasi pertama, coba batas simpan lebih tinggi dan cadangan secara gratis.",
        "faq_trial_a": "Tidak. Setelah uji coba Anda bisa lanjut paket gratis. Data tersimpan tidak dihapus. Data di atas batas gratis tetap tersimpan dan bisa digunakan lagi setelah membeli Pro.",
        "support_free_pro_a": "Paket gratis mencakup 10 item per kategori teks, 10 gambar, dan 1 profil. Salin, tambah, cari, urut ulang, dan simpan cepat tersedia. Pro menambah batas lebih tinggi, cadangan, tema premium, dan kustomisasi kategori. Instal baru: uji coba gratis 30 hari batas dan cadangan (tema premium dan kustomisasi memerlukan Pro).",
        "support_trial_a": "Selama 30 hari dari peluncuran pertama: hingga 200 item per kategori teks, 50 gambar, 30 profil, dan cadangan gratis. Tema premium dan kustomisasi memerlukan Pro. Data tidak dihapus setelah uji coba.",
        "release_trial_item": "Paket gratis + uji coba gratis 30 hari (batas lebih tinggi dan cadangan)",
    },
    "th": {
        "nav_cta": "ทดลองใช้ฟรี 30 วัน",
        "hero_cta_secondary": "ทดลองใช้ฟรี 30 วัน",
        "hero_pill1": "ทดลองใช้ฟรี 30 วัน",
        "hero_trial_title": "ทดลองใช้ฟรี 30 วัน",
        "hero_trial_text": "ภายใน 30 วันหลังติดตั้งครั้งแรก ลองใช้ขีดจำกัดการบันทึกที่สูงขึ้นและการสำรองข้อมูลได้ฟรี",
        "pricing_subtitle": "ภายใน 30 วันหลังติดตั้งครั้งแรก ลองใช้ขีดจำกัดที่สูงขึ้นและการสำรองข้อมูลได้ฟรี หลังจากนั้นยังใช้แผนฟรีต่อได้",
        "pricing_trial_title": "ทดลองใช้ฟรี 30 วัน",
        "pricing_trial_text": "หมวดข้อความ: สูงสุด 200 ต่อหมวด · รูปภาพ: 50 · โปรไฟล์: 30 · ส่งออก/นำเข้าข้อมูลสำรอง",
        "pricing_trial_note": "ธีมพรีเมียมและการเปลี่ยนชื่อ/ไอคอนหมวดหมู่ใช้ได้หลังซื้อ Pro หลังครบ 30 วัน ข้อมูลที่บันทึกจะไม่ถูกลบ ข้อมูลที่เกินขีดจำกัดฟรียังคงอยู่และใช้ได้อีกครั้งเมื่อซื้อ Pro",
        "pricing_free_lead": "ฟีเจอร์หลักใช้ฟรีได้ต่อเนื่อง",
        "pricing_free_items": ["หมวดข้อความ: 10 ต่อหมวด", "รูปภาพ: 10", "โปรไฟล์: 1", "ค้นหา", "จัดเรียง", "บันทึกด่วน"],
        "pricing_pro_items": ["หมวดข้อความ: สูงสุด 200 ต่อหมวด", "รูปภาพ: 50", "โปรไฟล์: 30", "ส่งออก/นำเข้าข้อมูลสำรอง", "ธีมพรีเมียม", "ชื่อและไอคอนหมวดหมู่ที่กำหนดเอง"],
        "cta_sub": "ภายใน 30 วันหลังติดตั้งครั้งแรก ลองใช้ขีดจำกัดที่สูงขึ้นและการสำรองข้อมูลได้ฟรี",
        "faq_trial_a": "ไม่ หลังทดลองใช้คุณยังใช้แผนฟรีต่อได้ ข้อมูลที่บันทึกจะไม่ถูกลบ ข้อมูลที่เกินขีดจำกัดฟรียังคงอยู่และใช้ได้อีกครั้งเมื่อซื้อ Pro",
        "support_free_pro_a": "แผนฟรีรวม 10 รายการต่อหมวดข้อความ รูปภาพ 10 และโปรไฟล์ 1 คัดลอก เพิ่มข้อมูล ค้นหา จัดเรียง และบันทึกด่วนใช้ได้ Pro เพิ่มขีดจำกัด การสำรองข้อมูล ธีมพรีเมียม และการปรับหมวดหมู่ ติดตั้งใหม่: ทดลองใช้ฟรี 30 วันสำหรับขีดจำกัดและสำรอง (ธีมพรีเมียมและการปรับแต่งต้องซื้อ Pro)",
        "support_trial_a": "ภายใน 30 วันจากการเปิดครั้งแรก: สูงสุด 200 รายการต่อหมวดข้อความ รูปภาพ 50 โปรไฟล์ 30 และสำรองข้อมูลฟรี ธีมพรีเมียมและการปรับแต่งต้องซื้อ Pro ข้อมูลไม่ถูกลบหลังทดลองใช้",
        "release_trial_item": "แผนฟรี + ทดลองใช้ฟรี 30 วัน (ขีดจำกัดสูงขึ้นและสำรองข้อมูล)",
    },
    "vi": {
        "nav_cta": "Dùng thử miễn phí 30 ngày",
        "hero_cta_secondary": "Dùng thử miễn phí 30 ngày",
        "hero_pill1": "Dùng thử miễn phí 30 ngày",
        "hero_trial_title": "Dùng thử miễn phí 30 ngày",
        "hero_trial_text": "Trong 30 ngày sau khi cài đặt lần đầu, hãy dùng thử miễn phí giới hạn lưu cao hơn và sao lưu.",
        "pricing_subtitle": "Trong 30 ngày sau khi cài đặt lần đầu, dùng thử miễn phí giới hạn cao hơn và sao lưu. Sau đó vẫn tiếp tục gói miễn phí.",
        "pricing_trial_title": "Dùng thử miễn phí 30 ngày",
        "pricing_trial_text": "Danh mục văn bản: tối đa 200 mỗi loại · Hình ảnh: 50 · Hồ sơ: 30 · Xuất/nhập sao lưu",
        "pricing_trial_note": "Chủ đề cao cấp và tùy chỉnh tên/biểu tượng danh mục có sau khi mua Pro. Sau 30 ngày dữ liệu không bị xóa. Dữ liệu vượt giới hạn miễn phí vẫn được giữ và dùng lại được khi mua Pro.",
        "pricing_free_lead": "Các tính năng cốt lõi vẫn miễn phí.",
        "pricing_free_items": ["Danh mục văn bản: 10 mỗi loại", "Hình ảnh: 10", "Hồ sơ: 1", "Tìm kiếm", "Sắp xếp", "Lưu nhanh"],
        "pricing_pro_items": ["Danh mục văn bản: tối đa 200 mỗi loại", "Hình ảnh: 50", "Hồ sơ: 30", "Xuất/nhập sao lưu", "Chủ đề cao cấp", "Tên và biểu tượng danh mục tùy chỉnh"],
        "cta_sub": "Trong 30 ngày sau khi cài đặt lần đầu, dùng thử miễn phí giới hạn cao hơn và sao lưu.",
        "faq_trial_a": "Không. Sau thời gian dùng thử bạn vẫn tiếp tục gói miễn phí. Dữ liệu đã lưu không bị xóa. Dữ liệu vượt giới hạn miễn phí vẫn được giữ và dùng lại được khi mua Pro.",
        "support_free_pro_a": "Gói miễn phí gồm 10 mục mỗi danh mục văn bản, 10 hình ảnh và 1 hồ sơ. Sao chép, thêm, tìm kiếm, sắp xếp và lưu nhanh đều có. Pro thêm giới hạn cao hơn, sao lưu, chủ đề cao cấp và tùy chỉnh danh mục. Cài mới: dùng thử miễn phí 30 ngày giới hạn và sao lưu (chủ đề cao cấp và tùy chỉnh cần mua Pro).",
        "support_trial_a": "Trong 30 ngày từ lần mở đầu: tối đa 200 mục mỗi danh mục văn bản, 50 hình, 30 hồ sơ và sao lưu miễn phí. Chủ đề cao cấp và tùy chỉnh cần mua Pro. Dữ liệu không bị xóa sau dùng thử.",
        "release_trial_item": "Gói miễn phí + dùng thử miễn phí 30 ngày (giới hạn cao hơn và sao lưu)",
    },
    "tr": {
        "nav_cta": "30 gün ücretsiz deneme",
        "hero_cta_secondary": "30 gün ücretsiz deneme",
        "hero_pill1": "30 gün ücretsiz deneme",
        "hero_trial_title": "30 gün ücretsiz deneme",
        "hero_trial_text": "İlk kurulumdan sonra 30 gün boyunca daha yüksek kayıt limitlerini ve yedeklemeyi ücretsiz deneyin.",
        "pricing_subtitle": "İlk kurulumdan sonra 30 gün boyunca daha yüksek limitler ve yedekleme ücretsiz. Sonrasında ücretsiz planda devam edin.",
        "pricing_trial_title": "30 gün ücretsiz deneme",
        "pricing_trial_text": "Metin kategorileri: her biri en fazla 200 · Görseller: 50 · Profiller: 30 · Yedekleme dışa/içe aktarma",
        "pricing_trial_note": "Premium temalar ve kategori adı/simge özelleştirme Pro satın alımından sonra kullanılabilir. 30 gün sonrasında verileriniz silinmez. Ücretsiz limitin üzerindeki veriler saklanır ve Pro satın alındığında yeniden kullanılabilir.",
        "pricing_free_lead": "Temel özellikler ücretsiz kullanılmaya devam eder.",
        "pricing_free_items": ["Metin kategorileri: her biri 10", "Görseller: 10", "Profiller: 1", "Arama", "Sıralama", "Hızlı kaydet"],
        "pricing_pro_items": ["Metin kategorileri: her biri en fazla 200", "Görseller: 50", "Profiller: 30", "Yedekleme dışa/içe aktarma", "Premium temalar", "Özel kategori adları ve simgeler"],
        "cta_sub": "İlk kurulumdan sonra 30 gün boyunca daha yüksek limitler ve yedeklemeyi ücretsiz deneyin.",
        "faq_trial_a": "Hayır. Deneme sonrasında ücretsiz planda devam edebilirsiniz. Kaydedilen veriler silinmez. Ücretsiz limitin üzerindeki veriler saklanır ve Pro satın alındığında yeniden kullanılabilir.",
        "support_free_pro_a": "Ücretsiz plan metin kategorisi başına 10 öğe, 10 görsel ve 1 profil içerir. Kopyalama, ekleme, arama, sıralama ve hızlı kaydet kullanılabilir. Pro daha yüksek limitler, yedekleme, premium temalar ve kategori özelleştirme ekler. Yeni kurulum: 30 gün ücretsiz limit ve yedekleme denemesi (premium temalar ve özelleştirme Pro gerektirir).",
        "support_trial_a": "İlk açılıştan itibaren 30 gün: metin kategorisi başına 200 öğe, 50 görsel, 30 profil ve yedekleme ücretsiz. Premium temalar ve özelleştirme Pro gerektirir. Deneme sonrası veriler silinmez.",
        "release_trial_item": "Ücretsiz plan + 30 gün ücretsiz deneme (daha yüksek limitler ve yedekleme)",
    },
    "uk": {
        "nav_cta": "30 днів безкоштовного пробного періоду",
        "hero_cta_secondary": "30 днів безкоштовного пробного періоду",
        "hero_pill1": "30 днів безкоштовного пробного періоду",
        "hero_trial_title": "30 днів безкоштовного пробного періоду",
        "hero_trial_text": "Протягом 30 днів після першого встановлення безкоштовно спробуйте підвищені ліміти збереження та резервне копіювання.",
        "pricing_subtitle": "Протягом 30 днів після першого встановлення — підвищені ліміти та резервне копіювання безкоштовно. Потім продовжуйте безкоштовний план.",
        "pricing_trial_title": "30 днів безкоштовного пробного періоду",
        "pricing_trial_text": "Текстові категорії: до 200 у кожній · Зображення: 50 · Профілі: 30 · Експорт/імпорт резервної копії",
        "pricing_trial_note": "Преміум-теми та налаштування назв/значків категорій доступні після покупки Pro. Після пробного періоду ваші дані не видаляються. Дані понад безкоштовні ліміти зберігаються і знову стають доступними після покупки Pro.",
        "pricing_free_lead": "Основні функції залишаються безкоштовними.",
        "pricing_free_items": ["Текстові категорії: по 10", "Зображення: 10", "Профілі: 1", "Пошук", "Сортування", "Швидке збереження"],
        "pricing_pro_items": ["Текстові категорії: до 200 у кожній", "Зображення: 50", "Профілі: 30", "Експорт/імпорт резервної копії", "Преміум-теми", "Власні назви та значки категорій"],
        "cta_sub": "Протягом 30 днів після першого встановлення безкоштовно спробуйте підвищені ліміти та резервне копіювання.",
        "faq_trial_a": "Ні. Після пробного періоду можна продовжити безкоштовний план. Збережені дані не видаляються. Дані понад безкоштовні ліміти зберігаються і знову стають доступними після покупки Pro.",
        "support_free_pro_a": "Безкоштовний план включає до 10 елементів у кожній текстовій категорії, 10 зображень і 1 профіль. Доступні копіювання, додавання, пошук, сортування та швидке збереження. Pro додає підвищені ліміти, резервне копіювання, преміум-теми та налаштування категорій. Нова установка: 30 днів безкоштовного пробного періоду лімітів і резервного копіювання (преміум-теми та налаштування — після покупки Pro).",
        "support_trial_a": "Протягом 30 днів від першого запуску: до 200 елементів у кожній текстовій категорії, 50 зображень, 30 профілів і резервне копіювання безкоштовно. Преміум-теми та налаштування потребують Pro. Дані після пробного періоду не видаляються.",
        "release_trial_item": "Безкоштовний план + 30 днів безкоштовного пробного періоду (підвищені ліміти та резервне копіювання)",
    },
    "nl": {
        "nav_cta": "30 dagen gratis proefperiode",
        "hero_cta_secondary": "30 dagen gratis proefperiode",
        "hero_pill1": "30 dagen gratis proefperiode",
        "hero_trial_title": "30 dagen gratis proefperiode",
        "hero_trial_text": "Gedurende 30 dagen na de eerste installatie kunt u gratis hogere opslaglimieten en back-up proberen.",
        "pricing_subtitle": "Gedurende 30 dagen na de eerste installatie: hogere limieten en back-up gratis. Daarna blijft u het gratis abonnement gebruiken.",
        "pricing_trial_title": "30 dagen gratis proefperiode",
        "pricing_trial_text": "Tekstcategorieën: tot 200 per categorie · Afbeeldingen: 50 · Profielen: 30 · Back-up exporteren/importeren",
        "pricing_trial_note": "Premiumthema's en aangepaste categorienamen/pictogrammen zijn beschikbaar na Pro-aankoop. Na de proefperiode worden uw gegevens niet verwijderd. Gegevens boven de gratis limiet blijven bewaard en worden weer bruikbaar na Pro-aankoop.",
        "pricing_free_lead": "Basisfuncties blijven gratis te gebruiken.",
        "pricing_free_items": ["Tekstcategorieën: 10 per categorie", "Afbeeldingen: 10", "Profielen: 1", "Zoeken", "Herschikken", "Snel opslaan"],
        "pricing_pro_items": ["Tekstcategorieën: tot 200 per categorie", "Afbeeldingen: 50", "Profielen: 30", "Back-up exporteren/importeren", "Premiumthema's", "Aangepaste categorienamen en pictogrammen"],
        "cta_sub": "Gedurende 30 dagen na de eerste installatie kunt u gratis hogere opslaglimieten en back-up proberen.",
        "faq_trial_a": "Nee. Na de proefperiode kunt u het gratis abonnement blijven gebruiken. Uw opgeslagen gegevens worden niet verwijderd. Gegevens boven de gratis limiet blijven bewaard en worden weer bruikbaar na Pro-aankoop.",
        "support_free_pro_a": "Het gratis abonnement omvat 10 items per tekstcategorie, 10 afbeeldingen en 1 profiel. Kopiëren, toevoegen, zoeken, herschikken en snel opslaan zijn beschikbaar. Pro voegt hogere limieten, back-up, premiumthema's en categorie-aanpassing toe. Nieuwe installatie: 30 dagen gratis proefperiode voor limieten en back-up (premiumthema's en aanpassing vereisen Pro).",
        "support_trial_a": "Gedurende 30 dagen vanaf de eerste start: tot 200 items per tekstcategorie, 50 afbeeldingen, 30 profielen en back-up gratis. Premiumthema's en aanpassing vereisen Pro. Gegevens worden na de proefperiode niet verwijderd.",
        "release_trial_item": "Gratis abonnement + 30 dagen gratis proefperiode (hogere limieten en back-up)",
    },
    "pl": {
        "nav_cta": "30 dni bezpłatnego okresu próbnego",
        "hero_cta_secondary": "30 dni bezpłatnego okresu próbnego",
        "hero_pill1": "30 dni bezpłatnego okresu próbnego",
        "hero_trial_title": "30 dni bezpłatnego okresu próbnego",
        "hero_trial_text": "Przez 30 dni po pierwszej instalacji wypróbuj bezpłatnie wyższe limity zapisu i kopię zapasową.",
        "pricing_subtitle": "Przez 30 dni po pierwszej instalacji — wyższe limity i kopia zapasowa bezpłatnie. Potem kontynuuj plan darmowy.",
        "pricing_trial_title": "30 dni bezpłatnego okresu próbnego",
        "pricing_trial_text": "Kategorie tekstu: do 200 w każdej · Obrazy: 50 · Profile: 30 · Eksport/import kopii zapasowej",
        "pricing_trial_note": "Motywy premium i dostosowanie nazw/ikon kategorii dostępne po zakupie Pro. Po okresie próbnym dane nie są usuwane. Dane powyżej limitu darmowego pozostają i znów stają się dostępne po zakupie Pro.",
        "pricing_free_lead": "Podstawowe funkcje pozostają bezpłatne.",
        "pricing_free_items": ["Kategorie tekstu: po 10", "Obrazy: 10", "Profile: 1", "Wyszukiwanie", "Zmiana kolejności", "Szybkie zapisywanie"],
        "pricing_pro_items": ["Kategorie tekstu: do 200 w każdej", "Obrazy: 50", "Profile: 30", "Eksport/import kopii zapasowej", "Motywy premium", "Własne nazwy i ikony kategorii"],
        "cta_sub": "Przez 30 dni po pierwszej instalacji wypróbuj bezpłatnie wyższe limity i kopię zapasową.",
        "faq_trial_a": "Nie. Po okresie próbnym możesz kontynuować plan darmowy. Zapisane dane nie są usuwane. Dane powyżej limitu darmowego pozostają i znów stają się dostępne po zakupie Pro.",
        "support_free_pro_a": "Plan darmowy obejmuje 10 elementów na kategorię tekstu, 10 obrazów i 1 profil. Kopiowanie, dodawanie, wyszukiwanie, zmiana kolejności i szybkie zapisywanie są dostępne. Pro dodaje wyższe limity, kopię zapasową, motywy premium i dostosowanie kategorii. Nowa instalacja: 30 dni bezpłatnego okresu próbnego limitów i kopii (motywy premium i dostosowanie wymagają Pro).",
        "support_trial_a": "Przez 30 dni od pierwszego uruchomienia: do 200 elementów na kategorię tekstu, 50 obrazów, 30 profili i kopia zapasowa bezpłatnie. Motywy premium i dostosowanie wymagają Pro. Dane nie są usuwane po okresie próbnym.",
        "release_trial_item": "Plan darmowy + 30 dni bezpłatnego okresu próbnego (wyższe limity i kopia zapasowa)",
    },
    "sv": {
        "nav_cta": "30 dagars gratis provperiod",
        "hero_cta_secondary": "30 dagars gratis provperiod",
        "hero_pill1": "30 dagars gratis provperiod",
        "hero_trial_title": "30 dagars gratis provperiod",
        "hero_trial_text": "I 30 dagar efter första installationen kan du prova högre spargränser och säkerhetskopiering gratis.",
        "pricing_subtitle": "I 30 dagar efter första installationen: högre gränser och säkerhetskopiering gratis. Fortsätt sedan med gratisplanen.",
        "pricing_trial_title": "30 dagars gratis provperiod",
        "pricing_trial_text": "Textkategorier: upp till 200 vardera · Bilder: 50 · Profiler: 30 · Exportera/importera säkerhetskopia",
        "pricing_trial_note": "Premiumteman och anpassade kategorinamn/ikoner finns efter Pro-köp. Efter provperioden raderas inte dina data. Data över gratisgränsen sparas och blir åter användbara när du köper Pro.",
        "pricing_free_lead": "Grundfunktionerna fortsätter vara gratis.",
        "pricing_free_items": ["Textkategorier: 10 vardera", "Bilder: 10", "Profiler: 1", "Sök", "Ordna om", "Snabbspara"],
        "pricing_pro_items": ["Textkategorier: upp till 200 vardera", "Bilder: 50", "Profiler: 30", "Exportera/importera säkerhetskopia", "Premiumteman", "Anpassade kategorinamn och ikoner"],
        "cta_sub": "I 30 dagar efter första installationen kan du prova högre spargränser och säkerhetskopiering gratis.",
        "faq_trial_a": "Nej. Efter provperioden kan du fortsätta med gratisplanen. Sparade data raderas inte. Data över gratisgränsen sparas och blir åter användbara när du köper Pro.",
        "support_free_pro_a": "Gratisplanen inkluderar 10 objekt per textkategori, 10 bilder och 1 profil. Kopiera, lägg till, sök, ordna om och snabbspara ingår. Pro lägger till högre gränser, säkerhetskopiering, premiumteman och kategorianpassning. Ny installation: 30 dagars gratis provperiod för gränser och säkerhetskopiering (premiumteman och anpassning kräver Pro).",
        "support_trial_a": "I 30 dagar från första start: upp till 200 objekt per textkategori, 50 bilder, 30 profiler och säkerhetskopiering gratis. Premiumteman och anpassning kräver Pro. Data raderas inte efter provperioden.",
        "release_trial_item": "Gratisplan + 30 dagars gratis provperiod (högre gränser och säkerhetskopiering)",
    },
}
# fmt: on

LICENSE_KEYS = [
    "nav.cta",
    "hero.ctaSecondary", "hero.pill1", "hero.trialTitle", "hero.trialText",
    "pricing.subtitle", "pricing.trialTitle", "pricing.trialText", "pricing.trialNote",
    "pricing.freeLead", "pricing.freeItems", "pricing.proItems",
    "cta.sub",
]


def apply_patch(data: dict, p: dict) -> None:
    data.setdefault("nav", {})["cta"] = p["nav_cta"]
    hero = data.setdefault("hero", {})
    hero["ctaSecondary"] = p["hero_cta_secondary"]
    hero["pill1"] = p["hero_pill1"]
    hero["trialTitle"] = p["hero_trial_title"]
    hero["trialText"] = p["hero_trial_text"]

    pricing = data.setdefault("pricing", {})
    pricing["subtitle"] = p["pricing_subtitle"]
    pricing["trialTitle"] = p["pricing_trial_title"]
    pricing["trialText"] = p["pricing_trial_text"]
    pricing["trialNote"] = p["pricing_trial_note"]
    pricing["freeLead"] = p["pricing_free_lead"]
    pricing["freeItems"] = list(p["pricing_free_items"])
    pricing["proItems"] = list(p["pricing_pro_items"])

    data.setdefault("cta", {})["sub"] = p["cta_sub"]

    for item in data.get("faq", {}).get("items", []):
        q = item.get("q", "")
        if "30" in q and ("?" in q or "？" in q or "吗" in q or "嗎" in q or "か" in q):
            item["a"] = p["faq_trial_a"]
            break

    support_items = data.get("supportPage", {}).get("items", [])
    if len(support_items) >= 2:
        support_items[1]["a"] = p["support_free_pro_a"]
    if len(support_items) >= 3:
        support_items[2]["a"] = p["support_trial_a"]

    for entry in data.get("releaseNotesPage", {}).get("entries", []):
        if entry.get("version") == "1.0.0":
            for i, line in enumerate(entry.get("items", [])):
                if "30" in line:
                    entry["items"][i] = p["release_trial_item"]
                    break


def main() -> None:
    if len(ALL) != 21:
        print(f"ERROR: expected 21 languages, got {len(ALL)}", file=sys.stderr)
        sys.exit(1)
    for lang in LANGS:
        if lang not in ALL:
            print(f"ERROR: missing translations for {lang}", file=sys.stderr)
            sys.exit(1)
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        apply_patch(data, ALL[lang])
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Patched {path.name}")


if __name__ == "__main__":
    main()
