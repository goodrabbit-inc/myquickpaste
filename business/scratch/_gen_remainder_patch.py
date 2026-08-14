#!/usr/bin/env python3
"""Generate patch_homepage_remainder_i18n.py with embedded translations."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "patch_homepage_remainder_i18n.py"
LICENSE = Path(__file__).resolve().parent / "patch_license_i18n.py"

# Import license strings for cta_sub / hero trial consistency
exec(LICENSE.read_text(encoding="utf-8").split("# fmt: on", 1)[0] + "\nALL = ALL\n", globals())

HEADER = r'''#!/usr/bin/env python3
"""Patch homepage i18n JSON — remaining homepage keys for 19 non-English languages."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"
TARGET_LANGS = [
    "fr", "de", "zh", "zh_TW", "ko", "ru", "it", "es", "pt",
    "hi", "ar", "id", "th", "vi", "tr", "uk", "nl", "pl", "sv",
]
VERIFY_LANGS = ["en", "ja"]

_SKIP = object()


def deep_merge(target: dict[str, Any], patch: dict[str, Any]) -> int:
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


def build_patch(t: dict[str, str]) -> dict[str, Any]:
    return {
        "meta": {"title": t["meta_title"], "ogTitle": t["meta_ogTitle"]},
        "nav": {
            "home": t["nav_home"],
            "features": t["nav_features"],
            "how": t["nav_how"],
            "screens": t["nav_screens"],
            "pricing": t["nav_pricing"],
            "support": t["nav_support"],
            "releaseNotes": t["nav_releaseNotes"],
            "privacy": t["nav_privacy"],
            "cta": t["nav_cta"],
        },
        "brand": {"edition": t["brand_edition"]},
        "hero": {
            "eyebrow": t["hero_eyebrow"],
            "ctaPrimary": t["hero_ctaPrimary"],
            "ctaSecondary": t["hero_ctaSecondary"],
            "statusPlay": t["hero_statusPlay"],
            "statusApp": t["hero_statusApp"],
            "pill1": t["hero_pill1"],
            "pill2": t["hero_pill2"],
            "pill3": t["hero_pill3"],
            "pill4": t["hero_pill4"],
            "badge": t["hero_badge"],
            "catch": t["hero_catch"],
            "platformLine": t["hero_platformLine"],
            "trialTitle": t["hero_trialTitle"],
            "trialText": t["hero_trialText"],
            "trust": t["hero_trust"],
        },
        "stores": {
            "googlePlay": t["stores_googlePlay"],
            "appStore": t["stores_appStore"],
            "comingSoon": t["stores_comingSoon"],
            "inDevelopment": t["stores_inDevelopment"],
            "googlePlayBadgeAlt": t["stores_googlePlayBadgeAlt"],
            "appStoreBadgeAlt": t["stores_appStoreBadgeAlt"],
            "microsoftBadgeAlt": t["stores_microsoftBadgeAlt"],
        },
        "pain": {
            "resolveLine1": t["pain_resolveLine1"],
            "resolveLine2": t["pain_resolveLine2"],
            "flowOldLabel": t["pain_flowOldLabel"],
            "flowOld1": t["pain_flowOld1"],
            "flowOld2": t["pain_flowOld2"],
            "flowOld3": t["pain_flowOld3"],
            "flowNewLabel": t["pain_flowNewLabel"],
            "flowNew1": t["pain_flowNew1"],
            "flowNew2": t["pain_flowNew2"],
        },
        "steps": {
            "titleLine1": t["steps_titleLine1"],
            "titleLine2": t["steps_titleLine2"],
            "title": t["steps_title"],
            "subtitle": t["steps_subtitle"],
            "items": [
                {"title": t["steps_i0_title"]},
                {"title": t["steps_i1_title"], "text": t["steps_i1_text"]},
                {"title": t["steps_i2_title"], "text": t["steps_i2_text"]},
            ],
        },
        "sceneWork": {
            "points": [_SKIP, _SKIP, _SKIP, {"title": t["sw_p3_title"], "text": t["sw_p3_text"]}],
        },
        "sceneDaily": {
            "points": [
                {"title": t["sd_p0_title"], "text": t["sd_p0_text"]},
                {"title": t["sd_p1_title"], "text": t["sd_p1_text"]},
                {"title": t["sd_p2_title"], "text": t["sd_p2_text"]},
                {"title": t["sd_p3_title"], "text": t["sd_p3_text"]},
            ],
        },
        "sceneMore": {"titleLine1": t["sceneMore_titleLine1"]},
        "screenshots": {
            "titleLine1": t["ss_titleLine1"],
            "titleLine2": t["ss_titleLine2"],
            "title": t["ss_title"],
            "lead": t["ss_lead"],
            "subtitle": t["ss_subtitle"],
            "freetextAlt": t["ss_freetextAlt"],
            "snippetsAlt": t["ss_snippetsAlt"],
            "imagesAlt": t["ss_imagesAlt"],
            "profileAlt": t["ss_profileAlt"],
            "profileEditAlt": t["ss_profileEditAlt"],
            "freetextCap": t["ss_freetextCap"],
            "snippetsCap": t["ss_snippetsCap"],
            "imagesCap": t["ss_imagesCap"],
            "profileCap": t["ss_profileCap"],
            "profileEditCap": t["ss_profileEditCap"],
        },
        "features": {
            "titleLine1": t["feat_titleLine1"],
            "titleLine2": t["feat_titleLine2"],
            "title": t["feat_title"],
            "subtitle": t["feat_subtitle"],
            "items": [
                {"title": t["fi0_title"], "text": t["fi0_text"]},
                {"title": t["fi1_title"]},
                {"title": t["fi2_title"], "text": t["fi2_text"]},
                {"title": t["fi3_title"], "text": t["fi3_text"]},
                {"title": t["fi4_title"], "text": t["fi4_text"]},
                _SKIP,
                {"title": t["fi6_title"], "text": t["fi6_text"]},
                {"title": t["fi7_title"], "text": t["fi7_text"]},
            ],
        },
        "comparison": {
            "titleLine1": t["cmp_titleLine1"],
            "titleLine2": t["cmp_titleLine2"],
            "otherLabel": t["cmp_otherLabel"],
            "other1": t["cmp_other1"],
            "other2": t["cmp_other2"],
            "other3": t["cmp_other3"],
            "other4": t["cmp_other4"],
            "otherText": t["cmp_otherText"],
            "app1": t["cmp_app1"],
            "app2": t["cmp_app2"],
            "app3": t["cmp_app3"],
        },
        "themesSection": {
            "titleLine1": t["th_titleLine1"],
            "titleLine2": t["th_titleLine2"],
            "title": t["th_title"],
            "imageAlt": t["th_imageAlt"],
            "caption": t["th_caption"],
            "note": t["th_note"],
        },
        "privacySection": {
            "titleLine1": t["pv_titleLine1"],
            "titleLine2": t["pv_titleLine2"],
            "title": t["pv_title"],
            "text": t["pv_text"],
            "points": [t["pv_p0"], _SKIP, t["pv_p2"], t["pv_p3"]],
            "link": t["pv_link"],
        },
        "faq": {
            "title": t["faq_title"],
            "items": [
                {"q": t["faq_i0_q"], "a": t["faq_i0_a"]},
                {"q": t["faq_i1_q"], "a": t["faq_i1_a"]},
                {"q": t["faq_i2_q"], "a": t["faq_i2_a"]},
                {"q": t["faq_i3_q"], "a": t["faq_i3_a"]},
                {"q": t["faq_i4_q"], "a": t["faq_i4_a"]},
                {"q": t["faq_i5_q"]},
            ],
        },
        "windowsEdition": {
            "titleLine1": t["win_titleLine1"],
            "titleLine2": t["win_titleLine2"],
            "text": t["win_text"],
            "note": t["win_note"],
            "link": t["win_link"],
        },
        "footer": {
            "pcEdition": t["footer_pcEdition"],
            "contact": t["footer_contact"],
            "developer": t["footer_developer"],
        },
        "cta": {"sub": t["cta_sub"]},
    }


# fmt: off
TRANSLATIONS: dict[str, dict[str, str]] = {
'''

FOOTER = r'''
}
# fmt: on

PATCHES: dict[str, dict[str, Any]] = {
    lang: build_patch(TRANSLATIONS[lang]) for lang in TARGET_LANGS
}


def main() -> None:
    expected = count_patch_leaves(PATCHES[TARGET_LANGS[0]])
    summary: list[tuple[str, int]] = []

    for lang in VERIFY_LANGS:
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        pricing = deepcopy(data.get("pricing"))
        if not pricing:
            print(f"ERROR: missing pricing in {lang}", file=sys.stderr)
            sys.exit(1)
        print(f"Verified {path.name}: pricing present ({len(pricing)} keys), no content changes")
        summary.append((lang, 0))

    for lang in TARGET_LANGS:
        if lang not in PATCHES:
            print(f"ERROR: missing patch for {lang}", file=sys.stderr)
            sys.exit(1)
        path = I18N_DIR / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        pricing_before = deepcopy(data.get("pricing"))
        n = deep_merge(data, PATCHES[lang])
        if deepcopy(data.get("pricing")) != pricing_before:
            print(f"ERROR: pricing was modified for {lang}", file=sys.stderr)
            sys.exit(1)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary.append((lang, n))
        print(f"Patched {path.name}: {n} keys")

    print()
    print("=== Summary ===")
    print(f"Expected leaf keys per target language: {expected}")
    for lang, n in summary:
        print(f"  {lang}: {n} keys patched")
    print(f"Pricing subtree: unchanged for all {len(TARGET_LANGS)} target languages")


if __name__ == "__main__":
    main()
'''

# Translation templates keyed by language
T: dict[str, dict[str, str]] = {}

def lic(lang: str) -> dict[str, str]:
    L = ALL[lang]
    return {
        "nav_cta": L["nav_cta"],
        "hero_ctaSecondary": L["hero_cta_secondary"],
        "hero_pill1": L["hero_pill1"],
        "hero_trialTitle": L["hero_trial_title"],
        "hero_trialText": L["hero_trial_text"],
        "cta_sub": L["cta_sub"],
        "faq_i2_a": L["faq_trial_a"],
    }


def merge(base: dict[str, str], lang: str) -> dict[str, str]:
    out = dict(base)
    out.update(lic(lang))
    return out


# Shared structural keys per language (faithful to en.json / ja.json semantics)
LANG_BASE: dict[str, dict[str, str]] = {
    "fr": {
        "meta_title": "MyQuickPaste | Copiez vos textes du quotidien d'un tap",
        "meta_ogTitle": "MyQuickPaste | Copiez vos textes du quotidien d'un tap",
        "nav_home": "Accueil", "nav_features": "Fonctionnalités", "nav_how": "Comment ça marche",
        "nav_screens": "Écrans", "nav_pricing": "Tarifs", "nav_support": "Assistance",
        "nav_releaseNotes": "Notes de version", "nav_privacy": "Confidentialité",
        "brand_edition": "Édition smartphone",
        "hero_eyebrow": "MyQuickPaste pour smartphones", "hero_ctaPrimary": "Voir comment ça marche",
        "hero_statusPlay": "Google Play bientôt disponible", "hero_statusApp": "App Store en développement",
        "hero_pill2": "Pro à l'achat unique", "hero_pill3": "Stocké sur l'appareil", "hero_pill4": "21 langues",
        "hero_badge": "MyQuickPaste pour smartphones", "hero_catch": "Vos textes du quotidien, en un tap.",
        "hero_platformLine": "Google Play bientôt disponible · App Store en développement", "hero_trust": "21 langues",
        "stores_googlePlay": "Disponible sur Google Play", "stores_appStore": "App Store",
        "stores_comingSoon": "Bientôt disponible", "stores_inDevelopment": "En développement",
        "stores_googlePlayBadgeAlt": "Disponible sur Google Play",
        "stores_appStoreBadgeAlt": "Télécharger sur l'App Store",
        "stores_microsoftBadgeAlt": "Obtenir sur Microsoft (MyQuickPaste pour Windows)",
        "pain_resolveLine1": "Avec MyQuickPaste,", "pain_resolveLine2": "un tap depuis la liste.",
        "pain_flowOldLabel": "Parcours habituel", "pain_flowOld1": "Chercher", "pain_flowOld2": "Sélectionner", "pain_flowOld3": "Copier",
        "pain_flowNewLabel": "MyQuickPaste", "pain_flowNew1": "Toucher", "pain_flowNew2": "Copier",
        "steps_titleLine1": "Enregistrer, toucher,", "steps_titleLine2": "puis coller.",
        "steps_title": "Comment ça marche", "steps_subtitle": "Pas de configuration complexe. Trois étapes suffisent.",
        "steps_i0_title": "Enregistrez ce que vous réutilisez",
        "steps_i1_title": "Touchez la ligne dont vous avez besoin",
        "steps_i1_text": "Un tap copie le contenu dans le presse-papiers.",
        "steps_i2_title": "Collez dans une autre appli",
        "steps_i2_text": "Basculez vers mail, réseaux, chat, cartes et collez.",
        "sw_p3_title": "Copie rapide", "sw_p3_text": "Terminé en un tap",
        "sd_p0_title": "Adresse", "sd_p0_text": "Moins de retouches",
        "sd_p1_title": "Profil", "sd_p1_text": "Enregistrez votre intro",
        "sd_p2_title": "Phrases favorites", "sd_p2_text": "Réutilisez à tout moment",
        "sd_p3_title": "Trouvez vite", "sd_p3_text": "Restez organisé",
        "sceneMore_titleLine1": "Utile dans ces situations aussi.",
        "ss_titleLine1": "Assez clair", "ss_titleLine2": "pour l'utiliser tout de suite.",
        "ss_title": "Écrans de l'appli",
        "ss_lead": "Grandes lignes, catégories claires et actions d'édition simples—conçu pour un usage quotidien.",
        "ss_subtitle": "Écrans réels de MyQuickPaste.",
        "ss_freetextAlt": "Écran liste texte libre", "ss_snippetsAlt": "Écran liste textes types",
        "ss_imagesAlt": "Écran catégorie Images", "ss_profileAlt": "Écran carte profil",
        "ss_profileEditAlt": "Écran édition profil",
        "ss_freetextCap": "Gérez les textes réutilisables dans une liste",
        "ss_snippetsCap": "Copiez vite vos réponses habituelles",
        "ss_imagesCap": "Enregistrez, copiez et partagez des images",
        "ss_profileCap": "Copiez adresse ou contacts champ par champ",
        "ss_profileEditCap": "Enregistrez les infos dont vous avez besoin ensemble",
        "feat_titleLine1": "Simple,", "feat_titleLine2": "avec l'essentiel.",
        "feat_title": "Fonctionnalités", "feat_subtitle": "Des outils qui allègent la saisie au quotidien.",
        "fi0_title": "Copier en un tap", "fi0_text": "Touchez une ligne pour copier son contenu dans le presse-papiers.",
        "fi1_title": "Organiser par usage",
        "fi2_title": "Réorganiser les favoris", "fi2_text": "Placez les éléments fréquents en haut pour les retrouver plus vite.",
        "fi3_title": "Copier champ par champ", "fi3_text": "Copiez uniquement l'adresse, le nom ou le numéro dont vous avez besoin.",
        "fi4_title": "Images prêtes à l'emploi", "fi4_text": "Enregistrez logos ou photos, puis copiez, partagez ou prévisualisez.",
        "fi6_title": "Choisir un style", "fi6_text": "Thèmes clair, sombre et premium disponibles.",
        "fi7_title": "Reste sur l'appareil", "fi7_text": "Vos textes et profils sont gérés sur le téléphone.",
        "cmp_titleLine1": "Pas seulement des copies temporaires—", "cmp_titleLine2": "un lieu pour ce que vous réutilisez.",
        "cmp_otherLabel": "Notes ou historique du presse-papiers",
        "cmp_other1": "Ouvrir", "cmp_other2": "Chercher", "cmp_other3": "Sélectionner ce qu'il faut", "cmp_other4": "Copier",
        "cmp_otherText": "Pratique pour l'historique récent. Pour les infos réutilisées souvent, la recherche devient une friction.",
        "cmp_app1": "Ouvrir", "cmp_app2": "Toucher une ligne", "cmp_app3": "Copié",
        "th_titleLine1": "Adaptez le style", "th_titleLine2": "à l'endroit où vous l'utilisez.",
        "th_title": "Thèmes", "th_imageAlt": "Galerie de thèmes MyQuickPaste",
        "th_caption": "Thèmes clair / sombre / premium",
        "th_note": "Les thèmes premium nécessitent l'achat Pro. Ils ne sont pas inclus dans l'essai de 30 jours.",
        "pv_titleLine1": "L'essentiel reste", "pv_titleLine2": "sur votre appareil.",
        "pv_title": "Confidentialité sur l'appareil",
        "pv_text": "Les textes et profils enregistrés dans MyQuickPaste sont gérés sur l'appareil. Nous n'envoyons pas automatiquement vos contenus vers le cloud.",
        "pv_p0": "Pas de synchronisation cloud automatique", "pv_p2": "Les données restent gérées sur l'appareil",
        "pv_p3": "Pro permet d'exporter votre propre sauvegarde", "pv_link": "Lire la politique de confidentialité",
        "faq_title": "FAQ",
        "faq_i0_q": "Un tap colle-t-il automatiquement dans une autre appli ?",
        "faq_i0_a": "Toucher une ligne la copie dans le presse-papiers. Basculez ensuite vers mail, réseaux ou chat et collez.",
        "faq_i1_q": "Où mes données sont-elles stockées ?",
        "faq_i1_a": "Textes, profils et réglages sont stockés sur votre smartphone.",
        "faq_i2_q": "Perds-je l'appli après l'essai de 30 jours ?",
        "faq_i3_q": "Pro est-il un abonnement mensuel ?",
        "faq_i3_a": "Non. Pro est un achat unique sans frais mensuels récurrents.",
        "faq_i4_q": "Puis-je partager des données avec l'édition Windows ?",
        "faq_i4_a": "Non. Les éditions smartphone et Windows sont des applis distinctes. Achats et données ne sont pas partagés.",
        "faq_i5_q": "Puis-je déplacer mes données en changeant de téléphone ?",
        "win_titleLine1": "MyQuickPaste", "win_titleLine2": "sur Windows aussi.",
        "win_text": "L'édition Windows reste en bordure d'écran et peut coller le texte enregistré en un clic—c'est une appli distincte.",
        "win_note": "Ce n'est pas la même appli que l'édition smartphone. Achats et données enregistrées ne sont pas partagés.",
        "win_link": "Site de l'édition Windows",
        "footer_pcEdition": "Édition Windows", "footer_contact": "Contact",
        "footer_developer": "Développeur : Kazuhiro Suda",
    },
    "de": {
        "meta_title": "MyQuickPaste | Alltagstexte mit einem Tipp kopieren",
        "meta_ogTitle": "MyQuickPaste | Alltagstexte mit einem Tipp kopieren",
        "nav_home": "Start", "nav_features": "Funktionen", "nav_how": "So funktioniert's",
        "nav_screens": "Bildschirme", "nav_pricing": "Preise", "nav_support": "Support",
        "nav_releaseNotes": "Versionshinweise", "nav_privacy": "Datenschutz",
        "brand_edition": "Smartphone-Edition",
        "hero_eyebrow": "MyQuickPaste für Smartphones", "hero_ctaPrimary": "So funktioniert's",
        "hero_statusPlay": "Google Play demnächst", "hero_statusApp": "App Store in Entwicklung",
        "hero_pill2": "Pro einmalig kaufen", "hero_pill3": "Auf dem Gerät gespeichert", "hero_pill4": "21 Sprachen",
        "hero_badge": "MyQuickPaste für Smartphones", "hero_catch": "Alltagstexte, ein Tipp entfernt.",
        "hero_platformLine": "Google Play demnächst · App Store in Entwicklung", "hero_trust": "21 Sprachen",
        "stores_googlePlay": "Bei Google Play", "stores_appStore": "App Store",
        "stores_comingSoon": "Demnächst", "stores_inDevelopment": "In Entwicklung",
        "stores_googlePlayBadgeAlt": "Jetzt bei Google Play",
        "stores_appStoreBadgeAlt": "Laden im App Store",
        "stores_microsoftBadgeAlt": "Im Microsoft Store laden (MyQuickPaste für Windows)",
        "pain_resolveLine1": "Mit MyQuickPaste", "pain_resolveLine2": "ein Tipp aus der Liste.",
        "pain_flowOldLabel": "Üblicher Ablauf", "pain_flowOld1": "Suchen", "pain_flowOld2": "Auswählen", "pain_flowOld3": "Kopieren",
        "pain_flowNewLabel": "MyQuickPaste", "pain_flowNew1": "Tippen", "pain_flowNew2": "Kopieren",
        "steps_titleLine1": "Speichern, tippen,", "steps_titleLine2": "dann einfügen.",
        "steps_title": "So funktioniert's", "steps_subtitle": "Keine komplexe Einrichtung. Nur drei Schritte.",
        "steps_i0_title": "Speichern Sie Wiederholtes",
        "steps_i1_title": "Tippen Sie die Zeile, die Sie brauchen",
        "steps_i1_text": "Ein Tipp kopiert den Inhalt in die Zwischenablage.",
        "steps_i2_title": "In einer anderen App einfügen",
        "steps_i2_text": "Wechseln Sie zu Mail, Social, Chat, Karten und fügen ein.",
        "sw_p3_title": "Schnell kopieren", "sw_p3_text": "Mit einem Tipp erledigt",
        "sd_p0_title": "Adresse", "sd_p0_text": "Weniger erneut tippen",
        "sd_p1_title": "Profil", "sd_p1_text": "Intro speichern",
        "sd_p2_title": "Lieblingsphrasen", "sd_p2_text": "Jederzeit wiederverwenden",
        "sd_p3_title": "Schnell finden", "sd_p3_text": "Übersichtlich organisiert",
        "sceneMore_titleLine1": "Auch in diesen Momenten praktisch.",
        "ss_titleLine1": "Klar genug,", "ss_titleLine2": "sofort nutzbar.",
        "ss_title": "App-Bildschirme",
        "ss_lead": "Große Zeilen, klare Kategorien und einfache Bearbeitung—für den Alltag gemacht.",
        "ss_subtitle": "Echte Bildschirme aus MyQuickPaste.",
        "ss_freetextAlt": "Freitext-Listenbildschirm", "ss_snippetsAlt": "Textbausteine-Listenbildschirm",
        "ss_imagesAlt": "Bilder-Kategoriebildschirm", "ss_profileAlt": "Profilkarten-Bildschirm",
        "ss_profileEditAlt": "Profil bearbeiten",
        "ss_freetextCap": "Wiederverwendbare Texte in einer Liste verwalten",
        "ss_snippetsCap": "Übliche Antworten schnell kopieren",
        "ss_imagesCap": "Bilder speichern, kopieren und teilen",
        "ss_profileCap": "Adresse oder Kontaktfelder einzeln kopieren",
        "ss_profileEditCap": "Benötigte Details gemeinsam registrieren",
        "feat_titleLine1": "Einfach,", "feat_titleLine2": "mit dem Wesentlichen.",
        "feat_title": "Funktionen", "feat_subtitle": "Werkzeuge, die tägliches Tippen erleichtern.",
        "fi0_title": "Mit einem Tipp kopieren", "fi0_text": "Tippen Sie eine Zeile, um den Inhalt in die Zwischenablage zu kopieren.",
        "fi1_title": "Nach Verwendung organisieren",
        "fi2_title": "Favoriten sortieren", "fi2_text": "Häufig genutzte Einträge nach oben verschieben, damit Sie sie leichter finden.",
        "fi3_title": "Feld für Feld kopieren", "fi3_text": "Kopieren Sie nur die Adresse, den Namen oder die Nummer, die Sie brauchen.",
        "fi4_title": "Bilder sofort griffbereit", "fi4_text": "Logos oder Fotos speichern, dann kopieren, teilen oder ansehen.",
        "fi6_title": "Look wählen", "fi6_text": "Helle, dunkle und Premium-Farbthemen verfügbar.",
        "fi7_title": "Bleibt auf dem Gerät", "fi7_text": "Texte und Profile werden auf dem Telefon verwaltet.",
        "cmp_titleLine1": "Nicht nur temporäre Kopien—", "cmp_titleLine2": "ein Zuhause für Wiederholtes.",
        "cmp_otherLabel": "Notizen oder Zwischenablage-Verlauf",
        "cmp_other1": "Öffnen", "cmp_other2": "Suchen", "cmp_other3": "Auswählen, was Sie brauchen", "cmp_other4": "Kopieren",
        "cmp_otherText": "Gut für kürzliche Historie. Für oft genutzte Infos wird Suchen zur Hürde.",
        "cmp_app1": "Öffnen", "cmp_app2": "Zeile antippen", "cmp_app3": "Kopiert",
        "th_titleLine1": "Passen Sie das Design", "th_titleLine2": "an den Einsatzort an.",
        "th_title": "Themes", "th_imageAlt": "MyQuickPaste Theme-Galerie",
        "th_caption": "Hell / dunkel / Premium-Themes",
        "th_note": "Premium-Themes erfordern Pro-Kauf. Sie sind nicht in der 30-Tage-Testphase enthalten.",
        "pv_titleLine1": "Wichtiges bleibt", "pv_titleLine2": "auf Ihrem Gerät.",
        "pv_title": "Datenschutz auf dem Gerät",
        "pv_text": "In MyQuickPaste gespeicherte Texte und Profile werden auf dem Gerät verwaltet. Wir senden Ihre Inhalte nicht automatisch in die Cloud.",
        "pv_p0": "Keine automatische Cloud-Synchronisierung", "pv_p2": "Daten bleiben auf dem Gerät verwaltet",
        "pv_p3": "Pro ermöglicht Export Ihrer eigenen Sicherung", "pv_link": "Datenschutzrichtlinie lesen",
        "faq_title": "FAQ",
        "faq_i0_q": "Fügt ein Tipp automatisch in eine andere App ein?",
        "faq_i0_a": "Ein Tipp auf eine Zeile kopiert sie in die Zwischenablage. Wechseln Sie dann zu Mail, Social oder Chat und fügen ein.",
        "faq_i1_q": "Wo werden meine Daten gespeichert?",
        "faq_i1_a": "Texte, Profile und Einstellungen werden auf Ihrem Smartphone gespeichert.",
        "faq_i2_q": "Verliere ich die App nach der 30-Tage-Testphase?",
        "faq_i3_q": "Ist Pro ein monatliches Abo?",
        "faq_i3_a": "Nein. Pro ist ein einmaliger Kauf ohne monatliche Gebühr.",
        "faq_i4_q": "Kann ich Daten mit der Windows-Edition teilen?",
        "faq_i4_a": "Nein. Smartphone- und Windows-Edition sind getrennte Apps. Käufe und Daten werden nicht geteilt.",
        "faq_i5_q": "Kann ich Daten beim Telefonwechsel übertragen?",
        "win_titleLine1": "MyQuickPaste", "win_titleLine2": "auch unter Windows.",
        "win_text": "Die Windows-Edition bleibt am Bildschirmrand und kann registrierten Text mit einem Klick einfügen—eine separate App.",
        "win_note": "Nicht dieselbe App wie die Smartphone-Edition. Käufe und gespeicherte Daten werden nicht geteilt.",
        "win_link": "Windows-Edition Homepage",
        "footer_pcEdition": "Windows-Edition", "footer_contact": "Kontakt",
        "footer_developer": "Entwickler: Kazuhiro Suda",
    },
}


if __name__ == "__main__":
    # Append remaining languages in separate update - run generator
    for lang in TARGET_LANGS if 'TARGET_LANGS' in dir() else []:
        pass
