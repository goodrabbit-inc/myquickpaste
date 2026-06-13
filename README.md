# MyQuickPaste — GitHub Pages サイト

公開 URL: https://gacha0124-sketch.github.io/myquickpaste/

## 構成

| ファイル | 説明 |
|---------|------|
| `index.html` | セールス向けランディング（多言語対応） |
| `i18n.js` | 言語切替・JSON 読み込み |
| `i18n/ja.json`, `i18n/en.json` | 翻訳文案（第1段階: 日英） |
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

1. `i18n/xx.json` を追加（`ja.json` をコピーして翻訳）
2. `i18n.js` の `SUPPORTED` 配列にコードを追加
3. `index.html` の `<select>` に `<option>` を追加
