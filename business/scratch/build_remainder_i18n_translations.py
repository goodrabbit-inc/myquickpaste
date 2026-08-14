#!/usr/bin/env python3
"""Build remainder_i18n_translations.json for 19 homepage i18n languages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "remainder_i18n_translations.json"
GEN_PATCH = Path(__file__).resolve().parent / "_gen_remainder_patch.py"
from remainder_i18n_langs_extra import EXTRA_LANGS
from remainder_i18n_langs_extra2 import EXTRA_LANGS2
from remainder_i18n_langs_extra3 import EXTRA_LANGS3

REQUIRED_KEYS = [
    "meta_title", "meta_ogTitle",
    "nav_home", "nav_features", "nav_how", "nav_screens", "nav_pricing", "nav_support",
    "nav_releaseNotes", "nav_privacy",
    "brand_edition",
    "hero_eyebrow", "hero_ctaPrimary", "hero_statusPlay", "hero_statusApp",
    "hero_pill2", "hero_pill3", "hero_pill4", "hero_badge", "hero_catch",
    "hero_platformLine", "hero_trust",
    "stores_googlePlay", "stores_appStore", "stores_comingSoon", "stores_inDevelopment",
    "stores_googlePlayBadgeAlt", "stores_appStoreBadgeAlt", "stores_microsoftBadgeAlt",
    "pain_resolveLine1", "pain_resolveLine2", "pain_flowOldLabel",
    "pain_flowOld1", "pain_flowOld2", "pain_flowOld3",
    "pain_flowNewLabel", "pain_flowNew1", "pain_flowNew2",
    "steps_titleLine1", "steps_titleLine2", "steps_title", "steps_subtitle",
    "steps_i0_title", "steps_i1_title", "steps_i1_text", "steps_i2_title", "steps_i2_text",
    "sw_p3_title", "sw_p3_text",
    "sd_p0_title", "sd_p0_text", "sd_p1_title", "sd_p1_text",
    "sd_p2_title", "sd_p2_text", "sd_p3_title", "sd_p3_text",
    "sceneMore_titleLine1",
    "ss_titleLine1", "ss_titleLine2", "ss_title", "ss_lead", "ss_subtitle",
    "ss_freetextAlt", "ss_snippetsAlt", "ss_imagesAlt", "ss_profileAlt", "ss_profileEditAlt",
    "ss_freetextCap", "ss_snippetsCap", "ss_imagesCap", "ss_profileCap", "ss_profileEditCap",
    "feat_titleLine1", "feat_titleLine2", "feat_title", "feat_subtitle",
    "fi0_title", "fi0_text", "fi1_title", "fi2_title", "fi2_text",
    "fi3_title", "fi3_text", "fi4_title", "fi4_text", "fi6_title", "fi6_text",
    "fi7_title", "fi7_text",
    "cmp_titleLine1", "cmp_titleLine2", "cmp_otherLabel",
    "cmp_other1", "cmp_other2", "cmp_other3", "cmp_other4", "cmp_otherText",
    "cmp_app1", "cmp_app2", "cmp_app3",
    "th_titleLine1", "th_titleLine2", "th_title", "th_imageAlt", "th_caption", "th_note",
    "pv_titleLine1", "pv_titleLine2", "pv_title", "pv_text",
    "pv_p0", "pv_p2", "pv_p3", "pv_link",
    "faq_title", "faq_i0_q", "faq_i0_a", "faq_i1_q", "faq_i1_a", "faq_i2_q",
    "faq_i3_q", "faq_i3_a", "faq_i4_q", "faq_i4_a", "faq_i5_q",
    "win_titleLine1", "win_titleLine2", "win_text", "win_note", "win_link",
    "footer_pcEdition", "footer_contact", "footer_developer",
]

# Load fr/de from _gen_remainder_patch.py
_patch_text = GEN_PATCH.read_text(encoding="utf-8")
_start = _patch_text.index("LANG_BASE: dict[str, dict[str, str]] = {")
_end = _patch_text.index("\n}\n\n\nif __name__", _start)
_ns: dict = {}
exec(_patch_text[_start:_end + 2], _ns)
TRANSLATIONS: dict[str, dict[str, str]] = {
    "fr": _ns["LANG_BASE"]["fr"],
    "de": _ns["LANG_BASE"]["de"],
}

# fmt: off
TRANSLATIONS.update({
    "zh": {
        "meta_title": "MyQuickPaste | 一键复制日常文字",
        "meta_ogTitle": "MyQuickPaste | 一键复制日常文字",
        "nav_home": "首页", "nav_features": "功能", "nav_how": "使用方法", "nav_screens": "界面",
        "nav_pricing": "价格", "nav_support": "支持", "nav_releaseNotes": "更新日志", "nav_privacy": "隐私政策",
        "brand_edition": "手机版",
        "hero_eyebrow": "MyQuickPaste 手机版", "hero_ctaPrimary": "了解使用方法",
        "hero_statusPlay": "Google Play 即将推出", "hero_statusApp": "App Store 开发中",
        "hero_pill2": "Pro 一次性购买", "hero_pill3": "保存在本机", "hero_pill4": "21 种语言",
        "hero_badge": "MyQuickPaste 手机版", "hero_catch": "常用文字，一键复制。",
        "hero_platformLine": "Google Play 即将推出 · App Store 开发中", "hero_trust": "21 种语言",
        "stores_googlePlay": "在 Google Play 上获取", "stores_appStore": "App Store",
        "stores_comingSoon": "即将推出", "stores_inDevelopment": "开发中",
        "stores_googlePlayBadgeAlt": "在 Google Play 上获取",
        "stores_appStoreBadgeAlt": "在 App Store 下载",
        "stores_microsoftBadgeAlt": "从 Microsoft 获取（Windows 版 MyQuickPaste）",
        "pain_resolveLine1": "使用 MyQuickPaste，", "pain_resolveLine2": "列表中一键复制。",
        "pain_flowOldLabel": "常规流程", "pain_flowOld1": "查找", "pain_flowOld2": "选择", "pain_flowOld3": "复制",
        "pain_flowNewLabel": "MyQuickPaste", "pain_flowNew1": "点击", "pain_flowNew2": "复制",
        "steps_titleLine1": "保存、点击，", "steps_titleLine2": "然后粘贴。",
        "steps_title": "使用方法", "steps_subtitle": "无需复杂设置，只需三步。",
        "steps_i0_title": "保存常用内容", "steps_i1_title": "点击需要的条目",
        "steps_i1_text": "点击一次即可复制到剪贴板。",
        "steps_i2_title": "在其他应用中粘贴", "steps_i2_text": "切换到邮件、社交、聊天、地图等应用后粘贴。",
        "sw_p3_title": "快速复制", "sw_p3_text": "一键完成",
        "sd_p0_title": "地址", "sd_p0_text": "减少重复输入",
        "sd_p1_title": "个人资料", "sd_p1_text": "保存自我介绍",
        "sd_p2_title": "常用语", "sd_p2_text": "随时重复使用",
        "sd_p3_title": "快速查找", "sd_p3_text": "清晰整理",
        "sceneMore_titleLine1": "这些场景也用得上。",
        "ss_titleLine1": "一目了然，", "ss_titleLine2": "马上就能用。",
        "ss_title": "应用界面", "ss_lead": "大条目、清晰分类、简洁编辑操作——为日常使用而设计。",
        "ss_subtitle": "MyQuickPaste 的实际界面。",
        "ss_freetextAlt": "自由文字列表界面", "ss_snippetsAlt": "常用语列表界面",
        "ss_imagesAlt": "图片分类界面", "ss_profileAlt": "个人资料卡片界面",
        "ss_profileEditAlt": "个人资料编辑界面",
        "ss_freetextCap": "在一个列表中管理可重复使用的文字",
        "ss_snippetsCap": "快速复制常用回复",
        "ss_imagesCap": "保存、复制并分享图片",
        "ss_profileCap": "逐字段复制地址或联系方式",
        "ss_profileEditCap": "一并注册所需信息",
        "feat_titleLine1": "简洁，", "feat_titleLine2": "但功能齐全。",
        "feat_title": "功能", "feat_subtitle": "减轻日常输入负担的工具。",
        "fi0_title": "一键复制", "fi0_text": "点击条目即可将内容复制到剪贴板。",
        "fi1_title": "按用途整理",
        "fi2_title": "重新排序收藏", "fi2_text": "将常用条目移到顶部，更容易找到。",
        "fi3_title": "逐字段复制", "fi3_text": "只复制需要的地址、姓名或电话号码。",
        "fi4_title": "图片随时可用", "fi4_text": "保存徽标或照片，然后复制、分享或预览。",
        "fi6_title": "选择外观", "fi6_text": "提供浅色、深色和高级配色主题。",
        "fi7_title": "保存在本机", "fi7_text": "文字和个人资料在手机上管理。",
        "cmp_titleLine1": "不只是临时复制——", "cmp_titleLine2": "常用信息的固定存放处。",
        "cmp_otherLabel": "备忘录或剪贴板历史",
        "cmp_other1": "打开", "cmp_other2": "查找", "cmp_other3": "选择所需部分", "cmp_other4": "复制",
        "cmp_otherText": "适合最近的历史记录。对于经常复用的信息，查找会变成负担。",
        "cmp_app1": "打开", "cmp_app2": "点击条目", "cmp_app3": "已复制",
        "th_titleLine1": "匹配外观", "th_titleLine2": "适应使用场景。",
        "th_title": "主题", "th_imageAlt": "MyQuickPaste 主题库",
        "th_caption": "浅色 / 深色 / 高级主题",
        "th_note": "高级主题需要购买 Pro，不包含在 30 天体验中。",
        "pv_titleLine1": "重要内容", "pv_titleLine2": "留在你的设备上。",
        "pv_title": "本机隐私", "pv_text": "在 MyQuickPaste 中保存的文字和个人资料在设备上管理。我们不会自动将内容发送到云端。",
        "pv_p0": "无自动云同步", "pv_p2": "数据在设备上管理",
        "pv_p3": "Pro 可导出自己的备份", "pv_link": "阅读隐私政策",
        "faq_title": "常见问题",
        "faq_i0_q": "点击后会自动粘贴到其他应用吗？",
        "faq_i0_a": "点击条目会复制到剪贴板。然后切换到邮件、社交或聊天应用后粘贴。",
        "faq_i1_q": "我的数据存储在哪里？",
        "faq_i1_a": "文字、个人资料和设置保存在智能手机上。",
        "faq_i2_q": "30 天体验结束后还能使用应用吗？",
        "faq_i3_q": "Pro 是按月订阅吗？",
        "faq_i3_a": "不是。Pro 为一次性购买，没有按月续费。",
        "faq_i4_q": "可以与 Windows 版共享数据吗？",
        "faq_i4_a": "手机版和 Windows 版是独立应用，购买记录和保存的数据不共享。",
        "faq_i5_q": "换手机时可以迁移数据吗？",
        "win_titleLine1": "MyQuickPaste", "win_titleLine2": "也有 Windows 版。",
        "win_text": "Windows 版常驻屏幕边缘，可一键粘贴已注册的文字——这是独立应用。",
        "win_note": "与手机版不是同一应用，购买记录和保存的数据不共享。",
        "win_link": "Windows 版主页",
        "footer_pcEdition": "Windows 版", "footer_contact": "联系我们",
        "footer_developer": "开发者：Kazuhiro Suda",
    },
    "zh_TW": {
        "meta_title": "MyQuickPaste | 一鍵複製日常文字",
        "meta_ogTitle": "MyQuickPaste | 一鍵複製日常文字",
        "nav_home": "首頁", "nav_features": "功能", "nav_how": "使用方法", "nav_screens": "畫面",
        "nav_pricing": "價格", "nav_support": "支援", "nav_releaseNotes": "更新日誌", "nav_privacy": "隱私權",
        "brand_edition": "智慧型手機版",
        "hero_eyebrow": "MyQuickPaste 智慧型手機版", "hero_ctaPrimary": "了解使用方法",
        "hero_statusPlay": "Google Play 即將推出", "hero_statusApp": "App Store 開發中",
        "hero_pill2": "Pro 買斷制", "hero_pill3": "儲存在裝置內", "hero_pill4": "21 種語言",
        "hero_badge": "MyQuickPaste 智慧型手機版", "hero_catch": "常用文字，一鍵複製。",
        "hero_platformLine": "Google Play 即將推出 · App Store 開發中", "hero_trust": "21 種語言",
        "stores_googlePlay": "在 Google Play 上取得", "stores_appStore": "App Store",
        "stores_comingSoon": "即將推出", "stores_inDevelopment": "開發中",
        "stores_googlePlayBadgeAlt": "在 Google Play 上取得",
        "stores_appStoreBadgeAlt": "在 App Store 下載",
        "stores_microsoftBadgeAlt": "從 Microsoft 取得（Windows 版 MyQuickPaste）",
        "pain_resolveLine1": "使用 MyQuickPaste，", "pain_resolveLine2": "從清單一鍵複製。",
        "pain_flowOldLabel": "一般流程", "pain_flowOld1": "搜尋", "pain_flowOld2": "選取", "pain_flowOld3": "複製",
        "pain_flowNewLabel": "MyQuickPaste", "pain_flowNew1": "點擊", "pain_flowNew2": "複製",
        "steps_titleLine1": "儲存、點擊，", "steps_titleLine2": "然後貼上。",
        "steps_title": "使用方法", "steps_subtitle": "無需複雜設定，只需三個步驟。",
        "steps_i0_title": "儲存常用內容", "steps_i1_title": "點擊需要的項目",
        "steps_i1_text": "點一下即可複製到剪貼簿。",
        "steps_i2_title": "在其他 App 中貼上", "steps_i2_text": "切換到郵件、社群、聊天、地圖等 App 後貼上。",
        "sw_p3_title": "快速複製", "sw_p3_text": "一鍵完成",
        "sd_p0_title": "地址", "sd_p0_text": "減少重複輸入",
        "sd_p1_title": "個人資料", "sd_p1_text": "儲存自我介紹",
        "sd_p2_title": "常用語", "sd_p2_text": "隨時重複使用",
        "sd_p3_title": "快速找到", "sd_p3_text": "清楚整理",
        "sceneMore_titleLine1": "這些場景也用得上。",
        "ss_titleLine1": "一看就懂，", "ss_titleLine2": "馬上就能用。",
        "ss_title": "App 畫面", "ss_lead": "大列、清楚分類、簡單編輯操作——為日常使用而設計。",
        "ss_subtitle": "MyQuickPaste 的實際畫面。",
        "ss_freetextAlt": "自由文字清單畫面", "ss_snippetsAlt": "常用語清單畫面",
        "ss_imagesAlt": "圖片分類畫面", "ss_profileAlt": "個人資料卡片畫面",
        "ss_profileEditAlt": "個人資料編輯畫面",
        "ss_freetextCap": "在一個清單中管理可重複使用的文字",
        "ss_snippetsCap": "快速複製常用回覆",
        "ss_imagesCap": "儲存、複製並分享圖片",
        "ss_profileCap": "逐欄位複製地址或聯絡方式",
        "ss_profileEditCap": "一併註冊所需資訊",
        "feat_titleLine1": "簡潔，", "feat_titleLine2": "但功能齊全。",
        "feat_title": "功能", "feat_subtitle": "減輕日常輸入負擔的工具。",
        "fi0_title": "一鍵複製", "fi0_text": "點擊列即可將內容複製到剪貼簿。",
        "fi1_title": "依用途整理",
        "fi2_title": "重新排序常用項目", "fi2_text": "將常用項目移到上方，更容易找到。",
        "fi3_title": "逐欄位複製", "fi3_text": "只複製需要的地址、姓名或電話號碼。",
        "fi4_title": "圖片隨時可用", "fi4_text": "儲存標誌或照片，然後複製、分享或預覽。",
        "fi6_title": "選擇外觀", "fi6_text": "提供淺色、深色和進階配色主題。",
        "fi7_title": "保存在裝置內", "fi7_text": "文字和個人資料在裝置內管理。",
        "cmp_titleLine1": "不只是暫時複製——", "cmp_titleLine2": "常用資訊的固定存放處。",
        "cmp_otherLabel": "備忘錄或剪貼簿歷史",
        "cmp_other1": "開啟", "cmp_other2": "搜尋", "cmp_other3": "選取所需部分", "cmp_other4": "複製",
        "cmp_otherText": "適合最近的歷史記錄。對於經常重複使用的資訊，搜尋會變成負擔。",
        "cmp_app1": "開啟", "cmp_app2": "點擊列", "cmp_app3": "已複製",
        "th_titleLine1": "配合外觀", "th_titleLine2": "適應使用場景。",
        "th_title": "主題", "th_imageAlt": "MyQuickPaste 主題庫",
        "th_caption": "淺色 / 深色 / 進階主題",
        "th_note": "進階主題需購買 Pro，不包含在 30 天體驗中。",
        "pv_titleLine1": "重要內容", "pv_titleLine2": "留在你的裝置上。",
        "pv_title": "裝置內隱私", "pv_text": "在 MyQuickPaste 中儲存的文字和個人資料在裝置上管理。我們不會自動將內容傳送到雲端。",
        "pv_p0": "無自動雲端同步", "pv_p2": "資料在裝置上管理",
        "pv_p3": "Pro 可匯出自己的備份", "pv_link": "閱讀隱私權政策",
        "faq_title": "常見問題",
        "faq_i0_q": "點擊後會自動貼到其他 App 嗎？",
        "faq_i0_a": "點擊列會複製到剪貼簿。然後切換到郵件、社群或聊天 App 後貼上。",
        "faq_i1_q": "我的資料儲存在哪裡？",
        "faq_i1_a": "文字、個人資料和設定儲存在智慧型手機上。",
        "faq_i2_q": "30 天體驗結束後還能使用 App 嗎？",
        "faq_i3_q": "Pro 是按月訂閱嗎？",
        "faq_i3_a": "不是。Pro 為買斷制，沒有按月續費。",
        "faq_i4_q": "可以與 Windows 版共享資料嗎？",
        "faq_i4_a": "智慧型手機版與 Windows 版是獨立 App，購買記錄和儲存的資料不共享。",
        "faq_i5_q": "換手機時可以移轉資料嗎？",
        "win_titleLine1": "MyQuickPaste", "win_titleLine2": "也有 Windows 版。",
        "win_text": "Windows 版常駐螢幕邊緣，可一鍵貼上已註冊的文字——這是獨立 App。",
        "win_note": "與智慧型手機版不是同一 App，購買記錄和儲存的資料不共享。",
        "win_link": "Windows 版首頁",
        "footer_pcEdition": "Windows 版", "footer_contact": "聯絡我們",
        "footer_developer": "開發者：Kazuhiro Suda",
    },
})
# fmt: on
TRANSLATIONS.update(EXTRA_LANGS)
TRANSLATIONS.update(EXTRA_LANGS2)
TRANSLATIONS.update(EXTRA_LANGS3)

TARGET_LANGS = [
    "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]


def main() -> None:
    missing_langs = [lang for lang in TARGET_LANGS if lang not in TRANSLATIONS]
    if missing_langs:
        print(f"ERROR: missing translations for: {', '.join(missing_langs)}", file=sys.stderr)
        sys.exit(1)

    for lang in TARGET_LANGS:
        keys = set(TRANSLATIONS[lang])
        req = set(REQUIRED_KEYS)
        if keys != req:
            extra = sorted(keys - req)
            missing = sorted(req - keys)
            print(f"ERROR {lang}: extra={extra[:5]} missing={missing[:5]}", file=sys.stderr)
            sys.exit(1)

    OUT.write_text(
        json.dumps(TRANSLATIONS, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")
    for lang in TARGET_LANGS:
        print(f"  {lang}: {len(TRANSLATIONS[lang])} keys")


if __name__ == "__main__":
    main()
