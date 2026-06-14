# -*- coding: utf-8 -*-
import json
from pathlib import Path

CATCH = {
    "en": "Save frequently used text. Paste with one click.",
    "ja": "\u3088\u304f\u4f7f\u3046\u6587\u7ae0\u3092\u4fdd\u5b58\u3002\u30ef\u30f3\u30af\u30ea\u30c3\u30af\u3067\u8cbc\u308a\u4ed8\u3051\u3002",
    "fr": "Enregistrez vos textes fr\u00e9quents. Collez en un clic.",
    "de": "H\u00e4ufig genutzten Text speichern. Mit einem Klick einf\u00fcgen.",
    "zh-cn": "\u4fdd\u5b58\u5e38\u7528\u6587\u672c\u3002\u4e00\u952e\u7c98\u8d34\u3002",
    "zh-tw": "\u5132\u5b58\u5e38\u7528\u6587\u5b57\u3002\u4e00\u9375\u8cbc\u4e0a\u3002",
    "ko": "\uc790\uc8fc \uc4f0\ub294 \ud14d\uc2a4\ud2b8\ub97c \uc800\uc7a5\ud558\uc138\uc694. \uc6d0\ud074\ub9ad\uc73c\ub85c \ubd99\uc5ec\ub123\uae30.",
    "ru": "\u0421\u043e\u0445\u0440\u0430\u043d\u044f\u0439\u0442\u0435 \u0447\u0430\u0441\u0442\u044b\u0439 \u0442\u0435\u043a\u0441\u0442. \u0412\u0441\u0442\u0430\u0432\u043b\u044f\u0439\u0442\u0435 \u0432 \u043e\u0434\u0438\u043d \u043a\u043b\u0438\u043a.",
    "it": "Salva i testi che usi spesso. Incolla con un clic.",
    "es": "Guarda textos frecuentes. Pega con un clic.",
    "pt": "Guarde textos usados com frequ\u00eancia. Cole com um clique.",
    "hi": "\u092c\u093e\u0930-\u092c\u093e\u0930 \u0909\u092a\u092f\u094b\u0917 \u0939\u094b\u0928\u0947 \u0935\u093e\u0932\u093e \u091f\u0947\u0915\u094d\u0938\u094d\u091f \u0938\u0939\u0947\u091c\u0947\u0902\u0964 \u090f\u0915 \u0915\u094d\u0932\u093f\u0915 \u092e\u0947\u0902 \u092a\u0947\u0938\u094d\u091f \u0915\u0930\u0947\u0902\u0964",
    "ar": "\u0627\u062d\u0641\u0638 \u0627\u0644\u0646\u0635\u0648\u0635 \u0627\u0644\u062a\u064a \u062a\u0633\u062a\u062e\u062f\u0645\u0647\u0627 \u0643\u062b\u064a\u0631\u064b\u0627. \u0627\u0644\u0635\u0642 \u0628\u0646\u0642\u0631\u0629 \u0648\u0627\u062d\u062f\u0629.",
    "id": "Simpan teks yang sering digunakan. Tempel dengan satu klik.",
    "th": "\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01\u0e02\u0e49\u0e2d\u0e04\u0e27\u0e32\u0e21\u0e17\u0e35\u0e48\u0e43\u0e0a\u0e49\u0e1a\u0e48\u0eAD\u0e22 \u0e27\u0e32\u0e07\u0e14\u0e49\u0e27\u0e22\u0e04\u0e25\u0e34\u0e01\u0e40\u0e14\u0e35\u0e22\u0e27",
    "vi": "L\u01b0u v\u0103n b\u1ea3n hay d\u00f9ng. D\u00e1n ch\u1ec9 v\u1edbi m\u1ed9t c\u00fa nh\u1ea5p.",
    "tr": "S\u0131k kulland\u0131\u011f\u0131n\u0131z metni kaydedin. Tek t\u0131kla yap\u0131\u015ft\u0131r\u0131n.",
    "uk": "\u0417\u0431\u0435\u0440\u0456\u0433\u0430\u0439\u0442\u0435 \u0447\u0430\u0441\u0442\u043e \u0432\u0438\u043a\u043e\u0440\u0438\u0441\u0442\u043e\u0432\u0443\u0432\u0430\u043d\u0438\u0439 \u0442\u0435\u043a\u0441\u0442. \u0412\u0441\u0442\u0430\u0432\u043b\u044f\u0439\u0442\u0435 \u043e\u0434\u043d\u0438\u043c \u043a\u043b\u0456\u043a\u043e\u043c.",
    "nl": "Bewaar veelgebruikte tekst. Plak met \u00e9\u00e9n klik.",
    "sv": "Spara ofta anv\u00e4nd text. Klistra in med ett klick.",
    "pl": "Zapisuj cz\u0119sto u\u017cywany tekst. Wklejaj jednym klikni\u0119ciem.",
}

root = Path(__file__).resolve().parents[1] / "i18n"
for code, catch in CATCH.items():
    path = root / f"{code}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["hero"]["catch"] = catch
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated", code)
