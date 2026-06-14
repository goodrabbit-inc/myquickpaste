# -*- coding: utf-8 -*-
import json
from pathlib import Path

SPLITS = {
    "ja": ("画面の隅に置いてワンクリックで素早く貼り付けできる", "Windows用コピペ作業効率化・常駐型軽量ツール"),
    "en": ("A slim, always-on-top Windows sidekick for faster copy-paste", "Ready in the corner of your screen with one-click paste"),
    "fr": ("Un outil Windows léger et toujours visible pour coller vos textes en un clic", "Depuis le coin de l'écran"),
    "de": ("Schlankes, immer sichtbares Windows-Tool für schnelles Einfügen per Klick", "In der Bildschirmecke"),
    "zh-cn": ("放在屏幕角落、一键快速粘贴", "Windows 复制粘贴效率常驻轻量工具"),
    "zh-tw": ("放在螢幕角落、一鍵快速貼上", "Windows 複製貼上效率常駐輕量工具"),
    "ko": ("화면 구석에 두고 원클릭으로 빠르게 붙여넣는", "Windows 복사·붙여넣기 효율화 상주형 경량 도구"),
    "ru": ("Компактный Windows-помощник, всегда поверх окон", "Для быстрой вставки текста в один клик из угла экрана"),
    "it": ("Assistente Windows leggero e sempre in primo piano", "Per incollare più velocemente con un clic dall'angolo dello schermo"),
    "es": ("Asistente Windows ligero y siempre visible", "Para pegar más rápido con un clic desde la esquina de la pantalla"),
    "pt": ("Assistente Windows leve e sempre visível", "Para colar mais rápido com um clique no canto da tela"),
    "hi": ("स्क्रीन के कोने में रहने वाला पतला, हमेशा ऊपर Windows सहायक", "एक क्लिक में तेज़ पेस्ट के लिए"),
    "ar": ("مساعد Windows خفيف ودائم الظهور", "للصق أسرع بنقرة واحدة من زاوية الشاشة"),
    "id": ("Asisten Windows ringan dan selalu di atas", "Untuk menempel lebih cepat dengan satu klik dari sudut layar"),
    "th": ("ผู้ช่วย Windows บางเบา อยู่บนสุดเสมอ", "วางข้อความเร็วขึ้นด้วยคลิกเดียวจากมุมหน้าจอ"),
    "vi": ("Trợ lý Windows mỏng, luôn hiển thị trên cùng", "Dán nhanh hơn bằng một cú nhấp từ góc màn hình"),
    "tr": ("Ekran köşesinde tek tıkla hızlı yapıştırma için", "İnce, her zaman üstte Windows yardımcısı"),
    "uk": ("Компактний Windows-помічник, завжди поверх вікон", "Для швидкої вставки тексту в один клік з кута екрана"),
    "nl": ("Een slank, altijd-bovenop Windows-hulpje", "Voor sneller plakken met een klik vanuit de hoek van je scherm"),
    "sv": ("En smal, alltid-ovanpå Windows-assistent", "För snabbare inklistring med ett klick från skärmens hörn"),
    "pl": ("Smukły, zawsze na wierzchu asystent Windows", "Do szybszego wklejania jednym kliknięciem z rogu ekranu"),
}

root = Path("i18n")
for code, (line1, line2) in SPLITS.items():
    path = root / f"{code}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    hero = data["hero"]
    hero.pop("headline", None)
    hero["headline1"] = line1
    hero["headline2"] = line2
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated", code)
