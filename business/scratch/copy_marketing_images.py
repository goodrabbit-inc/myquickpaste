#!/usr/bin/env python3
"""Copy HP marketing assets into business/images/marketing/ with ASCII filenames."""
import shutil
from pathlib import Path

SRC = Path(r"C:\Users\gacha\Desktop\clipeeマーケティング\HP用")
DST = Path(__file__).resolve().parent.parent / "images" / "marketing"
ICON_DST = Path(__file__).resolve().parent.parent / "images" / "icon.png"

FEATURE_MAP = {
    "en": "en-フィーチャー.png",
    "ja": "ja-フィーチャー.png",
    "fr": "fr-フィーチャー.png",
    "de": "de-フィーチャー.png",
    "zh": "zh-cn-フィーチャー.png",
    "zh_TW": "zh-TW-フィーチャー.png",
    "ko": "ko-フィーチャー.png",
    "ru": "ru-フィーチャー.png",
    "it": "it-フィーチャー.png",
    "es": "es-フィーチャー.png",
    "pt": "pt-フィーチャー.png",
    "hi": "hi-フィーチャー.png",
    "ar": "ar-フィーチャー.png",
    "id": "id-フィーチャー.png",
    "th": "th-フィーチャー.png",
    "vi": "vi-フィーチャー.png",
    "tr": "tr-フィーチャー.png",
    "uk": "uk-フィーチャー.png",
    "nl": "nl-フィーチャー.png",
    "pl": "pl-フィーチャー.png",
    "sv": "sv-フィーチャー.png",
}

JA_USECASE = [
    "ja-旅1枚目.png",
    "ja-空港ラウンジ2枚目.png",
    "ja-フリマ3枚目.png",
    "ja-LINE4枚目.png",
    "ja-SNS5枚目.png",
    "ja-幹事6枚目.png",
    "ja-説明7枚目.png",
]

EN_USECASE = [f"en-{i}枚目.png" for i in range(1, 8)]

SKIP = {"ja-フィーチャーグラフィック.png", "zh-TW-フィーチャー.zip"}


def main():
    DST.mkdir(parents=True, exist_ok=True)
    copied = []

    icon_src = SRC / "icon.png"
    if icon_src.exists():
        shutil.copy2(icon_src, ICON_DST)
        copied.append(f"icon.png -> images/icon.png")

    for lang, name in FEATURE_MAP.items():
        src = SRC / name
        if not src.exists():
            raise FileNotFoundError(f"Missing feature: {name}")
        out = DST / f"feature-{lang}.png"
        shutil.copy2(src, out)
        copied.append(f"{name} -> marketing/feature-{lang}.png")

    for i, name in enumerate(JA_USECASE, 1):
        src = SRC / name
        if not src.exists():
            raise FileNotFoundError(f"Missing ja usecase: {name}")
        out = DST / f"usecase-ja-{i:02d}.png"
        shutil.copy2(src, out)
        copied.append(f"{name} -> marketing/usecase-ja-{i:02d}.png")

    for i, name in enumerate(EN_USECASE, 1):
        src = SRC / name
        if not src.exists():
            raise FileNotFoundError(f"Missing en usecase: {name}")
        out = DST / f"usecase-en-{i:02d}.png"
        shutil.copy2(src, out)
        copied.append(f"{name} -> marketing/usecase-en-{i:02d}.png")

    print(f"Copied {len(copied)} files")
    for line in copied:
        print(f"  {line}")


if __name__ == "__main__":
    main()
