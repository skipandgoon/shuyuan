# -*- coding: utf-8 -*-
"""合并 xiangse/ 下明文 JSON 书源为 xiangse-all.xbs (香色合集) — GitHub Actions 用
依赖同目录 decode_xbs.py (纯 python XXTEA codec)"""
import json
import glob
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
XSE = os.path.join(BASE, "xiangse")
OUT_JSON = os.path.join(XSE, "xiangse-all.json")
OUT_XBS = os.path.join(XSE, "xiangse-all.xbs")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decode_xbs  # noqa: E402

merged = {}
for p in sorted(glob.glob(os.path.join(XSE, "*.json"))):
    base = os.path.basename(p)
    if base == "xiangse-all.json":  # 跳过合集自身
        continue
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"SKIP {base}: {e}")
        continue
    # 明文格式: {"书源名": {source...}} 或数组
    if isinstance(d, dict):
        for name, src in d.items():
            if isinstance(src, dict) and "sourceName" in src:
                merged[name] = src
    elif isinstance(d, list):
        for src in d:
            if isinstance(src, dict) and src.get("sourceName"):
                merged[src["sourceName"]] = src

# 明文合集 (方便人工查看/编辑)
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=1)

# 加密合集
buf = json.dumps(merged, ensure_ascii=False).encode("utf-8")
with open(OUT_XBS, "wb") as f:
    f.write(decode_xbs.json2xbs_bytes(buf))

print(f"merged {len(merged)} xiangse sources -> {OUT_XBS} ({os.path.getsize(OUT_XBS)}B)")
