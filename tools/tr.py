#!/usr/bin/env python3
"""翻訳のハーネス(Sphinx の .po 用)。訳のリポジトリのルートで実行する。使い方:
  python3 <ja-docs-base>/tools/tr.py ...
  python3 tr.py status                 ファイルごとの進み具合
  python3 tr.py next <名前> [件数]      次に訳す文を番号つきで出す
  python3 tr.py apply <名前> <JSON>     訳を入れる(記法が欠けた訳は却下)
  python3 tr.py lint [名前]             用語集と照合して、訳語がずれた文を出す"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools_po import parse
import apply_po

PO = 'locale/ja/LC_MESSAGES/{}.po'
GLOSSARY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'glossary')

def entries(name):
    return [e for e in parse(PO.format(name)) if e['msgid']]

def code_only(s):
    t = s.strip()
    return t.startswith(('>>>', '#')) or '->' in t or bool(re.fullmatch(r'[\w.:`\-\s,()]+', t) and (' ' not in t or re.fullmatch(r'[\w, ()]+', t)))

def alias_rule(s):
    return bool(apply_po.ALIAS.match(s) or apply_po.SAME_STR.match(s) or apply_po.SAME_BA.match(s))

def status():
    rows = []
    for f in sorted(glob.glob(PO.format('*'))):
        name = os.path.basename(f)[:-3]
        es = entries(name)
        target = [e for e in es if not code_only(e['msgid'])]
        done = sum(1 for e in target if e['msgstr'])
        if done: rows.append((name, done, len(target)))
    for n, d, t in rows: print(f'{n:12} {d:5} / {t:5}  ({d * 100 // t}%)')
    print(f'--- 着手済み {len(rows)} ファイル / 全 {len(glob.glob(PO.format("*")))} ファイル')

def next_(name, n=60):
    es = entries(name)
    todo = [(i, e['msgid']) for i, e in enumerate(es) if not e['msgstr'] and not code_only(e['msgid']) and not alias_rule(e['msgid'])]
    print(f'未訳 {len(todo)} 件(うち {n} 件を表示)')
    for i, s in todo[:n]: print(f'[{i}] {s}')

def load_glossary():
    data = []
    for f in ('common', 'minusone'):
        data += json.load(open(os.path.join(GLOSSARY_DIR, f + '.json'), encoding='utf-8'))
    return data

def lint(names):
    g = load_glossary()
    bad = 0
    for name in names:
        for i, e in enumerate(entries(name)):
            if not e['msgstr']: continue
            for t in g:
                head = re.sub(r'[（(].*$', '', t['ja']).strip()
                pat = r'(?<![A-Za-z0-9_])' + re.escape(t['term']) + r'(?![A-Za-z0-9_])'
                # `x`, ``x``, :role:`x` の中は、コードなので除く
                src = re.sub(r'``[^`]*``|`[^`]*`', '', e['msgid'])
                if re.search(pat, src, re.I) and head.lower() not in e['msgstr'].lower() and t['term'].lower() not in e['msgstr'].lower():
                    bad += 1
                    print(f'{name}[{i}] 「{t["term"]}」→「{head}」になっていない: {e["msgstr"][:60]}')
    print(f'ずれ {bad} 件')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    if a[0] == 'status': status()
    elif a[0] == 'next': next_(a[1], int(a[2]) if len(a) > 2 else 60)
    elif a[0] == 'apply': apply_po.apply(a[1], {k: v for f in a[2:] for k, v in json.load(open(f, encoding='utf-8')).items()})
    elif a[0] == 'lint': lint(a[1:] or ['tubes', 'util'])
    else: print(__doc__); sys.exit(1)
