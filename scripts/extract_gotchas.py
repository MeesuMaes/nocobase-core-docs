#!/usr/bin/env python3
"""从官方文档抽出「边界约束句」——skill 判断层最该保留的东西。

这类句子的特征是「有否定/强制的具体动作」，而不是"本章介绍…"这类铺垫。
抽出来后按 skill 主题分组，供 SKILL.md 的 Gotchas 章节取材。

用法：
  python3 scripts/extract_gotchas.py            # 输出 distilled/_gotchas.md
  python3 scripts/extract_gotchas.py --topic plugin-dev
"""
import argparse
import collections
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")
OUT = os.path.join(ROOT, "distilled")

# 强约束：出现即说明存在"做错的方式"
RE_HARD = re.compile(
    r"(不要|不应|不能|不可|禁止|务必|不得|避免|否则|只能|只有|取决于|"
    r"不自动|不会|并不|仍然|切勿|注意|陷阱|易错)"
)
# 弱信号：解释性，容易误伤，默认不收
RE_WEAK = re.compile(r"(必须|应(?:当)?|需要)")

RE_TABLE = re.compile(r"^\s*\|")
RE_HEAD = re.compile(r"^#{1,6} ")
RE_LINKONLY = re.compile(r"^\s*[-*]?\s*\[[^\]]+\]\([^)]*\)\s*[。.]?\s*$")


def topic_of(path):
    p = path.replace("core/", "")
    if p.startswith("extension-development/"):
        return "plugin-dev"
    if p.startswith("developing-apps/") or p.startswith("using-plugins/"):
        return "app-dev"
    if p.startswith("framework/"):
        return "framework"
    if p.startswith("architecture/"):
        return "architecture"
    if p.startswith("deployment/") or p.startswith("tutorials/"):
        return "deploy-ops"
    if p.startswith("reference/"):
        return "reference"
    return "other"


def collect():
    manifest = json.load(open(os.path.join(SRC, "manifest.json"), encoding="utf-8"))
    buckets = collections.defaultdict(list)
    for x in manifest:
        path = x["path"]
        text = open(os.path.join(SRC, path), encoding="utf-8").read()
        topic = topic_of(path)
        in_code = False
        heading = ""
        for raw in text.split("\n"):
            if raw.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if RE_HEAD.match(raw):
                heading = raw.lstrip("#").strip()
                continue
            s = raw.strip()
            if not s or RE_TABLE.match(raw) or RE_LINKONLY.match(raw):
                continue
            if len(s) < 12 or len(s) > 260:
                continue
            if s.startswith((">", "!", "- [", "* [")):
                # 引用块里的"一句话原则"很有价值，保留；列表链接丢弃
                if s.startswith((">",)):
                    pass
                else:
                    continue
            if not RE_HARD.search(s):
                continue
            # 去掉纯链接包裹，保留可读文本
            plain = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
            plain = re.sub(r"\s+", " ", plain).strip()
            buckets[topic].append((path, heading, plain))
    return buckets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic")
    args = ap.parse_args()
    buckets = collect()

    order = ["plugin-dev", "app-dev", "framework", "architecture", "deploy-ops", "reference", "other"]
    lines = ["# 边界约束句（Gotchas）总表", "",
             "> 由 scripts/extract_gotchas.py 从官方文档自动抽取。每条都带来源篇与所属小节。",
             "> 这些是「做错的方式」清单，不是概念解释。", ""]
    total = 0
    for topic in order:
        items = buckets.get(topic, [])
        if not items:
            continue
        if args.topic and topic != args.topic:
            continue
        total += len(items)
        lines.append(f"## {topic}（{len(items)} 条）")
        lines.append("")
        by_src = collections.OrderedDict()
        for path, heading, txt in items:
            by_src.setdefault(path, []).append((heading, txt))
        for path, rows in by_src.items():
            lines.append(f"### `{path}`")
            for heading, txt in rows:
                tag = f"〔{heading}〕" if heading else ""
                lines.append(f"- {txt} {tag}")
            lines.append("")
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, "_gotchas.md")
    open(dst, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"抽取 {total} 条 → {dst}")
    for topic in order:
        if buckets.get(topic):
            print(f"  {topic:14s} {len(buckets[topic]):4d} 条")


if __name__ == "__main__":
    main()
