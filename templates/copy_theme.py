#!/usr/bin/env python3
"""prepare_docs.py のあとに実行する。theme/ の中身(ja-docs-base の部品)を、ビルド用の .site-src/assets/ へコピーする。"""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
dst = root / ".site-src" / "assets"
dst.mkdir(parents=True, exist_ok=True)
for f in sorted((root / "theme").glob("*")):
    if f.is_file():
        shutil.copy2(f, dst / f.name)
print(f"copied theme -> {dst}")
