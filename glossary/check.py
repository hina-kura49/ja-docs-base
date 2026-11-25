#!/usr/bin/env python3
"""用語集の検査: python3 glossary/check.py
必須の項目、同じ語の重複(団体をまたいでも)、説明の長さ(読み切れる 120 字以内)を調べる。"""
import json, sys, pathlib
d = pathlib.Path(__file__).parent
seen, bad = {}, 0
for f in sorted(d.glob('*.json')):
    for e in json.loads(f.read_text(encoding='utf-8')):
        for k in ('term', 'ja', 'desc'):
            if not e.get(k): print(f'{f.name}: {e.get("term")} に {k} がありません'); bad += 1
        names = [e['term'].lower()] + [a.lower() for a in e.get('aliases', [])]
        for n in names:
            if n in seen and seen[n] != f.name:
                print(f'重複: {n} が {seen[n]} と {f.name} にあります'); bad += 1
            seen[n] = f.name
        if len(e.get('desc', '')) > 120: print(f'長すぎる: {e["term"]}'); bad += 1
print('問題', bad, '件 / 用語', sum(1 for _ in seen), '語（別名を含む）')
sys.exit(1 if bad else 0)
