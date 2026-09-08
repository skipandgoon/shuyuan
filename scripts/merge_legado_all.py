# -*- coding: utf-8 -*-
"""合并 legado/ 下全部书源(排除自身)为 legado-all.json — GitHub Actions 用"""
import json
import glob
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
LEGADO = os.path.join(BASE, "legado")
OUT = os.path.join(LEGADO, "legado-all.json")

all_sources = []
for p in sorted(glob.glob(os.path.join(LEGADO, "*.json"))):
    if os.path.abspath(p) == os.path.abspath(OUT):
        continue
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"SKIP {os.path.basename(p)}: {e}")
        continue
    if isinstance(d, list):
        all_sources.extend(d)
    elif isinstance(d, dict):
        # 兼容 {name: {bookSourceName...}} 包装
        for k, v in d.items():
            if isinstance(v, dict) and "bookSourceName" in v:
                all_sources.append(v)
            elif isinstance(v, dict):
                all_sources.append(v)

# 去重 (bookSourceName + bookSourceUrl)
seen = set()
uniq = []
for s in all_sources:
    if not isinstance(s, dict):
        continue
    key = (str(s.get("bookSourceName", "")), str(s.get("bookSourceUrl", "")))
    if key not in seen:
        seen.add(key)
        uniq.append(s)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(uniq, f, ensure_ascii=False)

print(f"merged {len(uniq)} sources -> legado-all.json ({os.path.getsize(OUT)}B)")
