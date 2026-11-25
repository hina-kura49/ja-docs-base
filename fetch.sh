#!/bin/sh
# 使い方: fetch.sh <版> <エンジン: mkdocs|jekyll> <保存先フォルダ> [ロゴ名: rustsecjp|minusone]
# 例:     fetch.sh v0.1.0 mkdocs theme minusone
# 取り込む版(タグ)を固定するので、基盤を直しても、版を上げるまで公開サイトは変わらない。
set -eu
VER="$1"; ENGINE="$2"; OUT="$3"; LOGO="${4:-}"
BASE="https://raw.githubusercontent.com/hina-kura49/ja-docs-base/$VER/dist"
mkdir -p "$OUT"
get() { curl -fsSL "$BASE/$1" -o "$OUT/$2"; }
get ja-docs.css ja-docs.css
get ja-docs.js ja-docs.js
case "$ENGINE" in
  mkdocs) get mkdocs.css mkdocs.css ;;
  jekyll) get jekyll.css jekyll.css; get jekyll.js jekyll.js ;;
  *) echo "エンジンは mkdocs か jekyll" >&2; exit 1 ;;
esac
if [ -n "$LOGO" ]; then get "logos/$LOGO.png" "logo.png"; fi
mkdir -p .github/ISSUE_TEMPLATE
curl -fsSL "$BASE/mistranslation.md" -o .github/ISSUE_TEMPLATE/mistranslation.md
