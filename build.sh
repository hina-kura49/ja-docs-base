#!/bin/sh
# core と各エンジン用の部品を、配る形(dist/)にまとめる。
set -eu
cd "$(dirname "$0")"
rm -rf dist && mkdir -p dist/logos

# 共通(コードの窓・誤訳ボタン)
cp core/ja-docs.css dist/ja-docs.css
cp core/ja-docs.js  dist/ja-docs.js
cp core/glossary.js dist/glossary.js

# 用語集: 共通 + 団体ごとのデータを、window.JA_GLOSSARY に入れる JS にする
python3 glossary/check.py
for org in minusone rustsecjp; do
  python3 - "$org" > "dist/glossary-$org.js" <<'PY'
import json, sys
org = sys.argv[1]
data = []
for name in ("common", org):
    data += json.load(open(f"glossary/{name}.json", encoding="utf-8"))
print("window.JA_GLOSSARY=" + json.dumps(data, ensure_ascii=False) + ";")
PY
done

# MkDocs(Material): 共通 + 白黒の配色
cat mkdocs/theme.css > dist/mkdocs.css

# MkDocs + MinusOne: 0xFF-MinusOne デザインシステム(mkdocs.css のあとに読み込む)
cp mkdocs/minusone.css dist/minusone.css

# Jekyll: 白黒のサイト一式の CSS と、目次の JS
cp jekyll/site.css dist/jekyll.css
cp jekyll/site.js  dist/jekyll.js
cp jekyll/layout-default.html dist/jekyll-layout.html

cp logos/* dist/logos/
cp templates/mistranslation.md dist/mistranslation.md
echo "built: $(ls dist | tr '\n' ' ')"
