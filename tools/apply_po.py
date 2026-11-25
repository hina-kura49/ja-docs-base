#!/usr/bin/env python3
"""使い方: python3 apply_po.py <対応表の名前(例: tubes)> <訳の JSON(index -> 日本語)> [...]
JSON のキーは、parse() が返す msgid ありの entry の番号。reST の記法(:meth:`x`、``x``、`x`)が、原文と同じだけ訳に残っているかを検査し、
欠けている訳は、適用しないで一覧する。"""
import json, re, sys
sys.path.insert(0, '.')
from tools_po import parse, render_entry

TOKEN = re.compile(r'(:[a-zA-Z_:]+:`[^`]+`|``[^`]+``|`[^`]+`)')
ALIAS = re.compile(r'^Alias for (:(?:meth|func|class|data|attr):`[^`]+`)\.?$')
SAME_STR = re.compile(r'^Same as (:(?:meth|func):`[^`]+`), but returns a str, decoding the result using `context\.encoding`\. \(note that the binary versions are way faster\)$')
SAME_BA = re.compile(r'^Same as (:(?:meth|func):`[^`]+`), but returns a bytearray$')

def tokens(s):
    return sorted(TOKEN.findall(s))

def check(src, ja):
    a, b = tokens(src), tokens(ja)
    missing = list(a)
    for t in b:
        if t in missing: missing.remove(t)
    return missing

def apply(name, mapping):
    path = f'locale/ja/LC_MESSAGES/{name}.po'
    entries = parse(path)
    idx = [k for k, e in enumerate(entries) if e['msgid']]
    done = rejected = rules = 0
    out = []
    for k, e in enumerate(entries):
        ja = None
        if e['msgid']:
            n = idx.index(k)
            m = ALIAS.match(e['msgid']); m2 = SAME_STR.match(e['msgid']); m3 = SAME_BA.match(e['msgid'])
            if m and not e['msgstr']:
                ja = f'{m.group(1)} の別名です。'; rules += 1
            elif m2 and not e['msgstr']:
                ja = f'{m2.group(1)} と同じですが、`context.encoding` で結果をデコードして、str で返します（バイト列版のほうが、ずっと速いです）。'; rules += 1
            elif m3 and not e['msgstr']:
                ja = f'{m3.group(1)} と同じですが、bytearray で返します。'; rules += 1
            elif str(n) in mapping:
                cand = mapping[str(n)]
                miss = check(e['msgid'], cand)
                if miss:
                    rejected += 1; print(f'  [却下 {n}] 記法が欠けている: {miss[:3]}')
                else:
                    ja = cand; done += 1
        out.append(render_entry(e, ja) if ja else e['raw'])
    open(path, 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    print(f'{name}: 適用 {done} 件 / 規則 {rules} 件 / 却下 {rejected} 件')

if __name__ == '__main__':
    name = sys.argv[1]
    mapping = {}
    for f in sys.argv[2:]:
        mapping.update(json.load(open(f, encoding='utf-8')))
    apply(name, mapping)
