# MyQuickPaste — GitHub Pages サイト

公開 URL: https://goodrabbit-inc.github.io/myquickpaste/

## 構成

| ファイル | 説明 |
|---------|------|
| `index.html` | セールス向けランディング（21言語） |
| `i18n.js` | 言語切替・JSON 読み込み・RTL |
| `i18n/*.json` | 各言語の翻訳文案（Store listingData 準拠） |
| `support.html` 他 | サブページ（現状は日本語のみ） |

ブラウザ言語または `localStorage` で表示言語を保持します。

## ローカルで編集

```powershell
cd C:\Users\gacha\Desktop\myquickpaste-github
# 簡易プレビュー（Python があれば）
py -3 -m http.server 8080
# → http://localhost:8080

git add .
git commit -m "Update site"
git push
```

数分後に GitHub Pages に反映されます。

## 言語を追加する場合

1. `i18n/xx.json` を追加（`en.json` をコピーして翻訳）
2. `i18n.js` の `LANG_REGISTRY` にエントリを追加
3. `tools/generate_i18n.py` で一括生成する場合は `locales_remaining.py` 等を参照
