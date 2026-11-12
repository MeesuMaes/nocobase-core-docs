#!/usr/bin/env python3
"""从 source/ 生成 docs/ 页面与 sidebar.json（Rspress）。用法：python3 scripts/generate.py"""
import json, os, re, shutil
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DOCS = os.path.join(ROOT, "source"), os.path.join(ROOT, "docs")
BASE = "https://docs.nocobase.com"


# Shiki 内置语言白名单；未命中的围栏语言降级为 text，避免构建报错
KNOWN_LANGS = {
    "ts", "tsx", "js", "jsx", "typescript", "javascript", "json", "jsonc", "yaml", "yml",
    "bash", "sh", "shell", "zsh", "text", "txt", "plaintext", "html", "css", "scss",
    "diff", "sql", "http", "python", "markdown", "md", "docker", "dockerfile", "nginx",
    "toml", "xml", "go", "rust", "java", "php", "graphql", "vue", "svelte", "",
}
FENCE = re.compile(r"^(\s*)```([A-Za-z0-9_+-]*)\s*$")


def normalize_fence(line):
    m = FENCE.match(line)
    if not m or not m.group(2):
        return line
    lang = m.group(2).lower()
    return line if lang in KNOWN_LANGS else f"{m.group(1)}```text"


def esc(t):
    """MDX 安全：代码块外的 { } < 转义；未知围栏语言降级"""
    out, code = [], False
    for line in t.split("\n"):
        if line.lstrip().startswith("```"):
            line = normalize_fence(line)
            code = not code
            out.append(line)
            continue
        if not code:
            parts = re.split(r"(`[^`]*`)", line)
            line = "".join(p if p.startswith("`") else
                           p.replace("{", "\\{").replace("}", "\\}").replace("<", "&lt;")
                           for p in parts)
        out.append(line)
    return "\n".join(out)


def route_of(path):
    """core/framework/database/overview.md -> framework/database/overview"""
    return path[len("core/"):-3]


def main():
    m = json.load(open(os.path.join(SRC, "manifest.json"), encoding="utf-8"))
    m = [i for i in m if "error" not in i]

    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)

    # 页面
    for it in m:
        rp = route_of(it["path"])
        body = open(os.path.join(SRC, it["path"]), encoding="utf-8").read().strip()
        dst = os.path.join(DOCS, rp + ".md")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        head = f"<!-- 来源：{BASE + it['href']} -->\n\n"
        open(dst, "w", encoding="utf-8").write(head + esc(body) + "\n")

    # 侧栏
    groups = OrderedDict()
    for it in m:
        groups.setdefault(it["group"] or "（根）", OrderedDict()).setdefault(
            " / ".join(it["folders"]) or "—", []).append(it)

    def link(it):
        r = route_of(it["path"])
        return "/" if r == "index" else "/" + r

    sb, root_items = [], []
    for g, subs in groups.items():
        if g == "（根）":
            root_items = [{"text": d["title"], "link": "/"} for d in subs.get("—", [])]
            continue
        items = []
        for sub, docs in subs.items():
            leaves = [{"text": d["title"], "link": link(d)} for d in docs]
            if sub == "—":
                items.extend(leaves)
            else:
                items.append({"text": sub, "collapsed": True, "items": leaves})
        sb.append({"text": g, "collapsed": False, "items": items})
    if root_items:
        sb.insert(0, {"text": "开始", "collapsed": False, "items": root_items})
    json.dump(sb, open(os.path.join(ROOT, "sidebar.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # 首页
    idx = next(i for i in m if i["path"] == "core/index.md")
    body = open(os.path.join(SRC, idx["path"]), encoding="utf-8").read().strip()
    body = body.split("\n", 1)[1].strip() if body.startswith("# ") else body
    lines = ["# NocoBase 3 Core 文档（简体中文）", "",
             "> NocoBase 3 官方文档 Core 章节的简体中文镜像，"
             f"共 {len(m)} 篇。原文：[{BASE}/zh-CN/core/]({BASE}/zh-CN/core/)", "",
             body, "", "## 章节导航", "", "| 分组 | 子分组 | 文档数 |", "| --- | --- | --- |"]
    for g, subs in groups.items():
        if g == "（根）":
            continue
        cnt = len([d for v in subs.values() for d in v])
        subn = "、".join(k for k in subs if k != "—") or "—"
        lines.append(f"| {g} | {subn} | {cnt} |")
    open(os.path.join(DOCS, "index.md"), "w", encoding="utf-8").write(esc("\n".join(lines)) + "\n")

    print(f"pages={len(m)} groups={len(sb)}")


if __name__ == "__main__":
    main()
