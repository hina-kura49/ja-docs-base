# ja-docs-base

日本語訳サイトを、同じ見た目で作るための共通の部品です。RustSecJP と MinusOne の翻訳サイトで使います。

- 白黒の配色（OS のライト／ダーク設定に自動で合わせる）
- コードの「窓」（上の帯に 3 つの丸・言語名・コピーのボタン）
- 各ページの末尾の「誤訳を知らせる」ボタン（題名と URL を入れた issue の作成画面を開く）
- ページ下部の前後ボタン、検索、目次（MkDocs Material の標準機能を使う）

## 使い方

サイトのリポジトリで、使う版（タグ）を決めて取り込みます。

```sh
# MkDocs（Material）の場合。ロゴは minusone か rustsecjp
curl -fsSL https://raw.githubusercontent.com/hina-kura49/ja-docs-base/v0.1.0/fetch.sh | sh -s -- v0.1.0 mkdocs theme minusone
```

取り込む版を固定するので、この基盤を直しても、サイト側が版を上げるまで公開サイトは変わりません。

### MkDocs の設定

`mkdocs.yml` に次を足します。

```yaml
theme:
  name: material
  logo: assets/logo.png
  favicon: assets/logo.png
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
  features:
    - navigation.top
    - navigation.footer
extra_css:
  - assets/ja-docs.css
  - assets/mkdocs.css
extra_javascript:
  - assets/ja-docs.js
markdown_extensions:
  - pymdownx.highlight:
      pygments_lang_class: true
```

### Jekyll の場合

`jekyll.css`、`ja-docs.css`、`jekyll.js`、`ja-docs.js` を `assets/` に置いて読み込みます。誤訳ボタンのリポジトリは `window.JaDocs = { repo: "https://github.com/<組織>/<リポジトリ>" }` で指定します（MkDocs では自動で取れます）。

## 中身

| 場所 | 中身 |
|---|---|
| `core/` | コードの窓と誤訳ボタン（どのエンジンでも共通） |
| `mkdocs/` | Material の白黒の配色 |
| `jekyll/` | Jekyll 用のサイト一式の CSS と目次の JS |
| `logos/` | RustSecJP と MinusOne のロゴ |
| `templates/` | issue のひな形（誤訳・訳語の指摘） |
| `dist/` | 配る形（`build.sh` で作る。サイトが取り込むのはここ） |

直したあとは `./build.sh` で `dist/` を作り直し、タグを付けます。

## 翻訳するときのこと

原著のライセンスを守ってください。帰属表示は必須です。ShareAlike（CC BY-SA など）、GPL・AGPL では、訳したものも同じライセンスにします。NC（非営利）の原著では、広告や有料化はできません。ライセンスの記載がない原著は公開しません。公式のものではないことを、サイトに明記します。

## ライセンス

MIT（`LICENSE`）。ロゴは各組織のものです。MkDocs Material、Material Design Icons、Lucide のアイコンは、それぞれのライセンスに従います。
