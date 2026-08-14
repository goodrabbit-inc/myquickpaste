import json
from pathlib import Path

U = {
    "en": {
        "featureThemeText": "Choose light or dark in Settings.",
        "themesSubtitle": "Free includes light and dark. Pro unlocks premium palettes for business and everyday use.",
        "releaseThemeItem": "Light and dark themes; premium themes with Pro",
    },
    "ja": {
        "featureThemeText": "設定でライトまたはダークを選べます。",
        "themesSubtitle": "無料版はライト／ダーク。Pro版ではビジネス向けのプレミアムテーマを追加で選べます。",
        "releaseThemeItem": "ライト／ダーク、プレミアムテーマは Pro 購入限定",
    },
    "de": {
        "featureThemeText": "Wählen Sie in den Einstellungen zwischen Hell und Dunkel.",
        "themesSubtitle": "Kostenlos: Hell und Dunkel. Pro schaltet Premium-Paletten für Business und Alltag frei.",
        "releaseThemeItem": "Helle und dunkle Themes; Premium-Themes mit Pro",
    },
    "fr": {
        "featureThemeText": "Choisissez clair ou sombre dans les réglages.",
        "themesSubtitle": "Gratuit : clair et sombre. Pro débloque des palettes premium pour le travail et le quotidien.",
        "releaseThemeItem": "Thèmes clair et sombre ; thèmes premium avec Pro",
    },
    "es": {
        "featureThemeText": "Elige claro u oscuro en los ajustes.",
        "themesSubtitle": "Gratis incluye claro y oscuro. Pro desbloquea paletas premium para negocios y uso diario.",
        "releaseThemeItem": "Temas claro y oscuro; temas premium con Pro",
    },
    "it": {
        "featureThemeText": "Scegli chiaro o scuro nelle impostazioni.",
        "themesSubtitle": "Gratis: chiaro e scuro. Pro sblocca palette premium per lavoro e uso quotidiano.",
        "releaseThemeItem": "Temi chiaro e scuro; temi premium con Pro",
    },
    "pt": {
        "featureThemeText": "Escolha claro ou escuro nas configurações.",
        "themesSubtitle": "Grátis inclui claro e escuro. Pro desbloqueia paletas premium para negócios e uso diário.",
        "releaseThemeItem": "Temas claro e escuro; temas premium com Pro",
    },
    "nl": {
        "featureThemeText": "Kies licht of donker in de instellingen.",
        "themesSubtitle": "Gratis: licht en donker. Pro ontgrendelt premiumpaletten voor werk en dagelijks gebruik.",
        "releaseThemeItem": "Lichte en donkere thema's; premiumthema's met Pro",
    },
    "pl": {
        "featureThemeText": "Wybierz jasny lub ciemny motyw w ustawieniach.",
        "themesSubtitle": "W wersji darmowej: jasny i ciemny. Pro odblokowuje palety premium do pracy i codziennego użytku.",
        "releaseThemeItem": "Motywy jasny i ciemny; motywy premium z Pro",
    },
    "ru": {
        "featureThemeText": "Выберите светлую или тёмную тему в настройках.",
        "themesSubtitle": "Бесплатно: светлая и тёмная. Pro открывает премиальные палитры для работы и повседневного использования.",
        "releaseThemeItem": "Светлая и тёмная темы; премиальные темы с Pro",
    },
    "uk": {
        "featureThemeText": "Оберіть світлу або темну тему в налаштуваннях.",
        "themesSubtitle": "Безкоштовно: світла та темна. Pro відкриває преміальні палітри для роботи та щоденного використання.",
        "releaseThemeItem": "Світла та темна теми; преміальні теми з Pro",
    },
    "tr": {
        "featureThemeText": "Ayarlardan açık veya koyu temayı seçin.",
        "themesSubtitle": "Ücretsiz: açık ve koyu. Pro, iş ve günlük kullanım için premium paletlerin kilidini açar.",
        "releaseThemeItem": "Açık ve koyu temalar; premium temalar Pro ile",
    },
    "sv": {
        "featureThemeText": "Välj ljust eller mörkt i inställningarna.",
        "themesSubtitle": "Gratis inkluderar ljust och mörkt. Pro låser upp premiumpaletter för arbete och vardag.",
        "releaseThemeItem": "Ljusa och mörka teman; premiumteman med Pro",
    },
    "ar": {
        "featureThemeText": "اختر المظهر الفاتح أو الداكن من الإعدادات.",
        "themesSubtitle": "المجاني يتضمن الفاتح والداكن. Pro يفتح لوحات ألوان مميزة للعمل والاستخدام اليومي.",
        "releaseThemeItem": "سمات فاتحة وداكنة؛ سمات مميزة مع Pro",
    },
    "hi": {
        "featureThemeText": "सेटिंग्स में लाइट या डार्क थीम चुनें।",
        "themesSubtitle": "मुफ़्त में लाइट और डार्क शामिल। Pro व्यवसाय और दैनिक उपयोग के लिए प्रीमियम पैलेट खोलता है।",
        "releaseThemeItem": "लाइट और डार्क थीम; Pro के साथ प्रीमियम थीम",
    },
    "id": {
        "featureThemeText": "Pilih tema terang atau gelap di pengaturan.",
        "themesSubtitle": "Gratis mencakup terang dan gelap. Pro membuka palet premium untuk bisnis dan penggunaan harian.",
        "releaseThemeItem": "Tema terang dan gelap; tema premium dengan Pro",
    },
    "ko": {
        "featureThemeText": "설정에서 라이트 또는 다크 테마를 선택할 수 있습니다.",
        "themesSubtitle": "무료 버전은 라이트/다크. Pro 버전에서는 비즈니스용 프리미엄 테마를 추가로 선택할 수 있습니다.",
        "releaseThemeItem": "라이트/다크 테마, 프리미엄 테마는 Pro 구매 시",
    },
    "th": {
        "featureThemeText": "เลือกธีมสว่างหรือมืดได้ในการตั้งค่า",
        "themesSubtitle": "ฟรีมีโหมดสว่างและมืด Pro ปลดล็อกพาเลตพรีเมียมสำหรับธุรกิจและใช้งานประจำวัน",
        "releaseThemeItem": "ธีมสว่างและมืด ธีมพรีเมียมเมื่อซื้อ Pro",
    },
    "vi": {
        "featureThemeText": "Chọn chủ đề sáng hoặc tối trong Cài đặt.",
        "themesSubtitle": "Miễn phí gồm sáng và tối. Pro mở khóa bảng màu cao cấp cho công việc và dùng hàng ngày.",
        "releaseThemeItem": "Chủ đề sáng và tối; chủ đề cao cấp với Pro",
    },
    "zh": {
        "featureThemeText": "可在设置中选择浅色或深色主题。",
        "themesSubtitle": "免费版含浅色与深色。Pro 版可解锁适合商务与日常使用的 premium 主题。",
        "releaseThemeItem": "浅色/深色主题；高级主题需购买 Pro",
    },
    "zh_TW": {
        "featureThemeText": "可在設定中選擇淺色或深色主題。",
        "themesSubtitle": "免費版含淺色與深色。Pro 版可解鎖適合商務與日常使用的 premium 主題。",
        "releaseThemeItem": "淺色/深色主題；進階主題需購買 Pro",
    },
}

THEME_MARKERS = (
    "theme", "thema", "thème", "tema", "motyw", "тем", "ธีม", "主题", "主題", "テーマ", "tema", "thème", "سم", "थीम"
)

def is_theme_release_item(item: str) -> bool:
    low = item.lower()
    if "json" in low:
        return False
    if any(m in item for m in ("主题", "主題", "テーマ", "ธีม", "थीम", "سم")):
        return True
    return any(k in low for k in ("theme", "thema", "thème", "tema", "motyw", "тем"))

i18n_dir = Path(r"C:\Users\gacha\Desktop\myquickpaste-github\business\i18n")
for path in sorted(i18n_dir.glob("*.json")):
    lang = path.stem
    t = U.get(lang, U["en"])
    data = json.loads(path.read_text(encoding="utf-8"))

    for item in data["features"]["items"]:
        if item.get("icon") == "🌓":
            item["text"] = t["featureThemeText"]
            break

    data["themesSection"]["subtitle"] = t["themesSubtitle"]

    items = data["releaseNotesPage"]["entries"][0]["items"]
    for i, item in enumerate(items):
        if is_theme_release_item(item):
            items[i] = t["releaseThemeItem"]
            break

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated", lang)