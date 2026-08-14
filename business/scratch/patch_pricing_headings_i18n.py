#!/usr/bin/env python3
"""Patch pricing section headings (titleLine1/2, trialLabel, proTag, proLead, notSub) for 19 langs."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"
TARGET = [
    "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]

# Faithful to ja/en pricing heading semantics
PATCHES: dict[str, dict[str, str]] = {
    "fr": {
        "titleLine1": "Commencez par 30 jours,",
        "titleLine2": "et testez l'expérience.",
        "trialLabel": "Première installation uniquement",
        "proTag": "Achat unique",
        "proLead": "Pas de frais mensuels.",
        "notSub": "Ce n'est pas un abonnement",
        "faq_title": "Questions fréquentes",
    },
    "de": {
        "titleLine1": "Testen Sie 30 Tage,",
        "titleLine2": "und spüren Sie den Unterschied.",
        "trialLabel": "Nur bei Erstinstallation",
        "proTag": "Einmaliger Kauf",
        "proLead": "Keine monatliche Gebühr.",
        "notSub": "Kein Abonnement",
        "faq_title": "Häufige Fragen",
    },
    "zh": {
        "titleLine1": "先体验 30 天，",
        "titleLine2": "感受使用体验。",
        "trialLabel": "仅限首次安装",
        "proTag": "一次性购买",
        "proLead": "无月费。",
        "notSub": "不是订阅制",
        "faq_title": "常见问题",
    },
    "zh_TW": {
        "titleLine1": "先體驗 30 天，",
        "titleLine2": "感受使用體驗。",
        "trialLabel": "僅限首次安裝",
        "proTag": "一次性購買",
        "proLead": "無月費。",
        "notSub": "不是訂閱制",
        "faq_title": "常見問題",
    },
    "ko": {
        "titleLine1": "먼저 30일,",
        "titleLine2": "사용감을 체험해 보세요.",
        "trialLabel": "최초 설치 한정",
        "proTag": "일회성 구매",
        "proLead": "월 요금 없음.",
        "notSub": "구독이 아닙니다",
        "faq_title": "자주 묻는 질문",
    },
    "ru": {
        "titleLine1": "Попробуйте 30 дней,",
        "titleLine2": "и оцените удобство.",
        "trialLabel": "Только при первой установке",
        "proTag": "Разовая покупка",
        "proLead": "Без ежемесячной платы.",
        "notSub": "Это не подписка",
        "faq_title": "Частые вопросы",
    },
    "it": {
        "titleLine1": "Prova per 30 giorni,",
        "titleLine2": "e senti la differenza.",
        "trialLabel": "Solo al primo install",
        "proTag": "Acquisto una tantum",
        "proLead": "Nessun costo mensile.",
        "notSub": "Non è un abbonamento",
        "faq_title": "Domande frequenti",
    },
    "es": {
        "titleLine1": "Pruébalo 30 días,",
        "titleLine2": "y nota la diferencia.",
        "trialLabel": "Solo en la primera instalación",
        "proTag": "Compra única",
        "proLead": "Sin cuota mensual.",
        "notSub": "No es una suscripción",
        "faq_title": "Preguntas frecuentes",
    },
    "pt": {
        "titleLine1": "Experimente por 30 dias,",
        "titleLine2": "e sinta a diferença.",
        "trialLabel": "Apenas na primeira instalação",
        "proTag": "Compra única",
        "proLead": "Sem taxa mensal.",
        "notSub": "Não é uma assinatura",
        "faq_title": "Perguntas frequentes",
    },
    "hi": {
        "titleLine1": "पहले 30 दिन,",
        "titleLine2": "उपयोग का अनुभव करें।",
        "trialLabel": "केवल पहली इंस्टॉल पर",
        "proTag": "एक बार की खरीद",
        "proLead": "कोई मासिक शुल्क नहीं।",
        "notSub": "सब्सक्रिप्शन नहीं",
        "faq_title": "अक्सर पूछे जाने वाले प्रश्न",
    },
    "ar": {
        "titleLine1": "جرّب لمدة 30 يومًا،",
        "titleLine2": "وانعم بتجربة الاستخدام.",
        "trialLabel": "التثبيت الأول فقط",
        "proTag": "شراء لمرة واحدة",
        "proLead": "بدون رسوم شهرية.",
        "notSub": "ليس اشتراكًا",
        "faq_title": "الأسئلة الشائعة",
    },
    "id": {
        "titleLine1": "Coba selama 30 hari,",
        "titleLine2": "dan rasakan pengalamannya.",
        "trialLabel": "Hanya instal pertama",
        "proTag": "Beli sekali",
        "proLead": "Tanpa biaya bulanan.",
        "notSub": "Bukan langganan",
        "faq_title": "Pertanyaan umum",
    },
    "th": {
        "titleLine1": "ลองใช้ 30 วัน",
        "titleLine2": "แล้วสัมผัสประสบการณ์",
        "trialLabel": "ติดตั้งครั้งแรกเท่านั้น",
        "proTag": "ซื้อครั้งเดียว",
        "proLead": "ไม่มีค่ารายเดือน",
        "notSub": "ไม่ใช่การสมัครสมาชิก",
        "faq_title": "คำถามที่พบบ่อย",
    },
    "vi": {
        "titleLine1": "Dùng thử 30 ngày,",
        "titleLine2": "và cảm nhận sự khác biệt.",
        "trialLabel": "Chỉ lần cài đặt đầu",
        "proTag": "Mua một lần",
        "proLead": "Không phí hàng tháng.",
        "notSub": "Không phải đăng ký",
        "faq_title": "Câu hỏi thường gặp",
    },
    "tr": {
        "titleLine1": "30 gün deneyin,",
        "titleLine2": "farkı hissedin.",
        "trialLabel": "Yalnızca ilk kurulum",
        "proTag": "Tek seferlik satın alma",
        "proLead": "Aylık ücret yok.",
        "notSub": "Abonelik değil",
        "faq_title": "Sık sorulan sorular",
    },
    "uk": {
        "titleLine1": "Спробуйте 30 днів,",
        "titleLine2": "і відчуйте зручність.",
        "trialLabel": "Лише при першому встановленні",
        "proTag": "Разова покупка",
        "proLead": "Без щомісячної плати.",
        "notSub": "Це не підписка",
        "faq_title": "Поширені запитання",
    },
    "nl": {
        "titleLine1": "Probeer 30 dagen,",
        "titleLine2": "en voel het verschil.",
        "trialLabel": "Alleen bij eerste installatie",
        "proTag": "Eenmalige aankoop",
        "proLead": "Geen maandelijks bedrag.",
        "notSub": "Geen abonnement",
        "faq_title": "Veelgestelde vragen",
    },
    "pl": {
        "titleLine1": "Wypróbuj przez 30 dni,",
        "titleLine2": "i poczuj różnicę.",
        "trialLabel": "Tylko przy pierwszej instalacji",
        "proTag": "Jednorazowy zakup",
        "proLead": "Bez miesięcznej opłaty.",
        "notSub": "To nie subskrypcja",
        "faq_title": "Często zadawane pytania",
    },
    "sv": {
        "titleLine1": "Prova i 30 dagar,",
        "titleLine2": "och känn skillnaden.",
        "trialLabel": "Endast vid första installation",
        "proTag": "Engångsköp",
        "proLead": "Ingen månadsavgift.",
        "notSub": "Inte en prenumeration",
        "faq_title": "Vanliga frågor",
    },
}


def main() -> None:
    for lang in TARGET:
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        pricing_before = deepcopy(data.get("pricing"))
        p = PATCHES[lang]
        pricing = data.setdefault("pricing", {})
        for k in ("titleLine1", "titleLine2", "trialLabel", "proTag", "proLead", "notSub"):
            pricing[k] = p[k]
        data.setdefault("faq", {})["title"] = p["faq_title"]
        if deepcopy(data.get("pricing")) == pricing_before and data["faq"]["title"] == p["faq_title"]:
            pass
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Patched {path.name}")


if __name__ == "__main__":
    main()
