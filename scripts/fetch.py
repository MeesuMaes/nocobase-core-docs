#!/usr/bin/env python3
"""
抓取 NocoBase 3 官方文档 Core 章节的原始 markdown，写入 source/。

用法：
    python3 scripts/fetch.py                # 默认简体中文，输出到 ./source
    python3 scripts/fetch.py --lang en --out ./source_en

产物：source/core/**/*.md（原文，保留官方层级）、manifest.json、INDEX.md、core-docs.csv
仅依赖 Python 3 标准库。
"""
import argparse, csv, json, os, posixpath, re, time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.request import Request, urlopen

BASE = "https://docs.nocobase.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")


def fetch(url, retries=4):
    for i in range(retries):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(1.5 * (i + 1))


class Sidebar(HTMLParser):
    """解析官方侧栏 doc-nav：doc-group > doc-folder > a"""

    def __init__(self, prefix):
        super().__init__()
        self.prefix, self.group, self.folders = prefix, "", []
        self.pending, self.capture, self.items, self.in_nav = None, None, [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        if tag == "nav" and "doc-nav" in cls:
            self.in_nav += 1
            return
        if not self.in_nav:
            return
        if tag == "div" and "doc-group" in cls:
            self.group = ""
        elif tag == "p" and "doc-group-title" in cls:
            self.capture = "group"
        elif tag == "details" and "doc-folder" in cls:
            self.pending = a.get("data-doc-folder") or ""
        elif tag == "span" and "doc-folder-link" in cls:
            self.capture = "folder"
        elif tag == "a" and (a.get("href") or "").startswith(self.prefix + "/core"):
            self.items.append({"group": self.group,
                               "folders": [f for f in self.folders if f],
                               "title": "", "href": a["href"]})
            self.capture = "link"

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_nav:
            self.in_nav -= 1
        elif tag == "details" and self.folders:
            self.folders.pop()
        if self.capture and tag in ("p", "span", "a"):
            self.capture = None

    def handle_data(self, data):
        d = data.strip()
        if not d or not self.capture:
            return
        if self.capture == "group":
            self.group = d
        elif self.capture == "folder":
            if self.pending is not None:
                self.folders.append(d)
                self.pending = None
            elif self.folders:
                self.folders[-1] = d
        elif self.capture == "link" and self.items:
            self.items[-1]["title"] += d


MD_LINK = re.compile(r"\]\(([^)\s]+?\.md)(#[^)\s]*)?\)")


def clean(text, rel_path, prefix, pages_dir):
    """图片/站外链接绝对化；Core 内部相对链接保留"""
    s = re.sub(r"\]\((/assets/[^)\s]+)", rf"]({BASE}\1)", text)
    s = re.sub(rf"\]\(({prefix}/[^)\s]+)", rf"]({BASE}\1)", s)
    cur_dir = posixpath.dirname(rel_path)
    cur_url = prefix + "/" + cur_dir

    def repl(mo):
        t, anc = mo.group(1), mo.group(2) or ""
        if t.startswith(("http", "/")):
            return mo.group(0)
        if os.path.exists(os.path.join(pages_dir, posixpath.normpath(posixpath.join(cur_dir, t)))):
            return mo.group(0)
        site = posixpath.normpath(posixpath.join(cur_url, t))[:-3]
        return f"]({BASE}{site}/{anc})"

    return MD_LINK.sub(repl, s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="zh-CN")
    ap.add_argument("--out", default="source")
    args = ap.parse_args()
    ZH, OUT = "/" + args.lang, os.path.abspath(args.out)
    PAGES = os.path.join(OUT, "core")
    os.makedirs(PAGES, exist_ok=True)

    sb = Sidebar(ZH)
    sb.feed(fetch(f"{BASE}{ZH}/core/"))
    seen, items = set(), []
    for it in sb.items:
        if it["href"] not in seen:
            seen.add(it["href"])
            items.append(it)

    def work(it):
        p = it["href"].rstrip("/")
        if p.endswith("/core"):
            p += "/index"
        rp = "core/" + p[len(ZH) + 1 + len("core/"):]
        rp = p[len(ZH) + 1:] + ".md"          # core/xxx.md
        url = f"{BASE}{p}.md"
        try:
            txt = fetch(url)
        except Exception as e:
            return {**it, "md_url": url, "path": rp, "error": str(e)}
        txt = clean(txt, rp, ZH, PAGES)
        fp = os.path.join(OUT, rp)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(txt)
        return {**it, "md_url": url, "path": rp, "chars": len(txt), "lines": txt.count("\n"),
                "bytes": len(txt.encode()),
                "h1": next((l[2:].strip() for l in txt.splitlines() if l.startswith("# ")), "")}

    with ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(work, items))
    bad = [r for r in res if "error" in r]
    ok = [r for r in res if "error" not in r]
    json.dump(res, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    groups = OrderedDict()
    for it in ok:
        groups.setdefault(it["group"] or "（根）", OrderedDict()).setdefault(
            " / ".join(it["folders"]) or "—", []).append(it)
    total = sum(i["chars"] for i in ok)

    L = ["# NocoBase 3 · Core 文档结构化索引", "",
         f"- 来源：{BASE}{ZH}/core/",
         f"- 文档数：{len(ok)} 篇 | 总字数：约 {total:,} 字符", "",
         "| # | 分组 | 子分组 | 文档数 | 字符数 |", "| --- | --- | --- | --- | --- |"]
    for gi, (g, subs) in enumerate(groups.items(), 1):
        docs = [d for v in subs.values() for d in v]
        L.append(f"| {gi} | {g} | {len([k for k in subs if k != '—']) or '—'} | {len(docs)} | {sum(d['chars'] for d in docs):,} |")
    L.append("")
    n = 0
    for g, subs in groups.items():
        L += [f"## {g}", ""]
        for sub, docs in subs.items():
            if sub != "—":
                L += [f"### {sub}", ""]
            L += ["| # | 文档 | 本地路径 | 源页面 | 字符 |", "| --- | --- | --- | --- | --- |"]
            for d in docs:
                n += 1
                L.append(f"| {n} | {d['title']} | `{d['path']}` | {BASE + d['href']} | {d['chars']:,} |")
            L.append("")
    open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8").write("\n".join(L))

    with open(os.path.join(OUT, "core-docs.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["序号", "分组", "子分组", "标题", "本地路径", "源页面", "markdown源", "字符数", "行数"])
        for i, d in enumerate(ok, 1):
            w.writerow([i, d["group"] or "（根）", " / ".join(d["folders"]) or "—", d["title"],
                        d["path"], BASE + d["href"], d["md_url"], d["chars"], d["lines"]])

    print(f"docs={len(ok)} fail={len(bad)} chars={total}")
    for r in bad:
        print("FAIL", r["href"], r["error"])


if __name__ == "__main__":
    main()
