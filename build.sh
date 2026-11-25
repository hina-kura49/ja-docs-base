#!/bin/sh
# core と各エンジン用の部品を、配る形(dist/)にまとめる。
set -eu
cd "$(dirname "$0")"
rm -rf dist && mkdir -p dist/logos

# 共通(コードの窓・誤訳ボタン)
cp core/ja-docs.css dist/ja-docs.css
cp core/ja-docs.js  dist/ja-docs.js

# MkDocs(Material): 共通 + 白黒の配色
cat mkdocs/theme.css > dist/mkdocs.css

# Jekyll: 白黒のサイト一式の CSS と、目次の JS
cp jekyll/site.css dist/jekyll.css
cp jekyll/site.js  dist/jekyll.js

cp logos/*.png dist/logos/
cp templates/mistranslation.md dist/mistranslation.md
echo "built: $(ls dist | tr '\n' ' ')"
