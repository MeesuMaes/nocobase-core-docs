#!/usr/bin/env python3
"""把 134 篇官方 Core 文档蒸馏成「按任务聚合」的 references 卡。

不是压缩原文，而是三件事：
  1. 去噪：删掉纯导航句（"详见 xx.md"）、章节自述（"本章介绍…"）、重复空行
  2. 裁样板：整文件式代码块只留骨架（>40 行时留头 12 行 + 尾 6 行）
  3. 归并：按「开发者任务」而非文档目录，把同主题多篇聚成一卡

产物：distilled/<topic>/<card>.md  —— 直接作为 skill 的 references/
      distilled/_index.md          —— 全量 134 篇索引，保证一篇不漏

用法：
  python3 scripts/distill.py           # 生成全部
  python3 scripts/distill.py --stat    # 只打印压缩比
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")
OUT = os.path.join(ROOT, "distilled")

# ── 噪声规则 ────────────────────────────────────────────────────────────────
RE_ONLY_LINK = re.compile(r"^\s*[-*]?\s*\[[^\]]+\]\([^)]*\)\s*[。.]?\s*$")
RE_NAV = re.compile(r"^\s*[^|]{0,40}?(?:详见|参见|见|阅读|查阅|了解)[^|]{0,20}?\[[^\]]+\]\([^)]*\.md[^)]*\)\s*。?\s*$")
RE_SELFREF = re.compile(r"^\s*(?:本章|本篇|本节|这一章|此章)(?:节)?(?:介绍|说明|讲解|讨论|涵盖)")
RE_FENCE = re.compile(r"^\s*```")
RE_HEAD = re.compile(r"^#{1,6} ")
RE_TABLE = re.compile(r"^\s*\|")
# 约束句：有否定/强制的具体动作
RE_HARD = re.compile(
    r"(不要|不应|不能|不可|禁止|务必|不得|避免|否则|只能|只有|取决于|"
    r"不自动|不会|并不|仍然|切勿|注意|陷阱|易错)"
)
# 含具体 API / 命令 / 标识符的行：留下来当"索引锚点"
RE_API = re.compile(
    r"(@nocobase/|pnpm |nb |app\.|ctx\.|use[A-Z]|define[A-Z]|Repository|repository\(|"
    r"container\.|Token|schema|migration|`[a-zA-Z][\w.-]*`)"
)

CODE_CLIP_AT = 30
CODE_KEEP_HEAD = 12
CODE_KEEP_TAIL = 5
# prompt 示例块（"在 Agent 中这样描述需求"）对开发者参考价值低，超长才丢
PROMPT_LANGS = {"text", "prompt"}
PROMPT_KEEP_MAX = 10


def split_blocks(text):
    out, buf, code, lang = [], [], [], None
    for line in text.split("\n"):
        if RE_FENCE.match(line):
            if lang is None:
                if buf:
                    out.append(("md", buf))
                    buf = []
                lang = line.strip().lstrip("`").strip()
                code = []
            else:
                out.append(("code", (lang, "\n".join(code))))
                lang, code = None, []
            continue
        (code if lang is not None else buf).append(line)
    if buf:
        out.append(("md", buf))
    if code:
        out.append(("code", (lang, "\n".join(code))))
    return out


def clip_code(lang, body):
    lines = body.rstrip("\n").split("\n")
    # prompt 示例块：短的保留（常是 Agent 指令模板），长的丢
    if lang in PROMPT_LANGS and len(lines) > PROMPT_KEEP_MAX:
        return lang, None, True
    if len(lines) <= CODE_CLIP_AT:
        return lang, body, False
    head, tail = lines[:CODE_KEEP_HEAD], lines[-CODE_KEEP_TAIL:]
    omitted = len(lines) - CODE_KEEP_HEAD - CODE_KEEP_TAIL
    marker = (
        f"# …（省略 {omitted} 行，完整见原文）"
        if lang in ("bash", "sh", "shell", "text", "yaml", "json", "dockerfile", "")
        else f"// …（省略 {omitted} 行样板，完整见原文）"
    )
    return lang, "\n".join(head + [marker] + tail), True


def distill_md(lines):
    """关键行提取：留下结构、判断和索引锚点，丢掉叙述性铺垫。

    保留：标题 / 表格 / 每条标题后的第一句导语 / 约束句 / 含 API 的命令句
    丢弃：纯导航句、章节自述、其余叙述、连续空行
    """
    kept, st = [], {"nav": 0, "selfref": 0, "dropped": 0}
    after_heading = False
    for ln in lines:
        s = ln.strip()
        if RE_HEAD.match(ln):
            kept.append(ln)
            after_heading = True
            continue
        if not s:
            continue
        if RE_TABLE.match(ln):
            kept.append(ln)
            after_heading = False
            continue
        if RE_ONLY_LINK.match(ln) and len(s) < 90:
            st["nav"] += 1
            continue
        if RE_NAV.match(ln) and len(s) < 120:
            st["nav"] += 1
            continue
        if RE_SELFREF.match(ln):
            st["selfref"] += 1
            continue
        hit = RE_HARD.search(s) or RE_API.search(s)
        if after_heading and not s.startswith((">", "-", "*", "1.", "|")):
            # 标题后的第一句是这一节的"要解决什么"，留着当上下文
            kept.append(ln)
            after_heading = False
            continue
        if hit:
            kept.append(ln)
            after_heading = False
        else:
            st["dropped"] += 1
    return kept, st


def code_fingerprint(lang, body):
    """代码去重指纹：语言 + 首个 import/声明行，避免同一模板在多篇里重复占篇幅。"""
    for ln in body.split("\n"):
        s = ln.strip()
        if s and not s.startswith(("//", "#", "*", "/*")):
            return (lang, re.sub(r"\s+", "", s)[:80])
    return (lang, body[:80])


def distill_page(path, seen_codes=None):
    """提取一篇文档的关键行。seen_codes 跨篇共享，用于剔除重复代码模板。"""
    if seen_codes is None:
        seen_codes = set()
    raw = open(os.path.join(SRC, path), encoding="utf-8").read()
    st = {"chars_in": len(raw), "nav": 0, "selfref": 0, "dropped": 0,
          "clipped": 0, "deduped": 0}
    rendered = []
    for kind, payload in split_blocks(raw):
        if kind == "code":
            lang, body, changed = clip_code(*payload)
            if body is None:            # 丢弃的 prompt 示例块
                st["clipped"] += 1
                continue
            fp = code_fingerprint(lang, body)
            if fp in seen_codes:        # 同一模板已出现
                st["deduped"] += 1
                continue
            seen_codes.add(fp)
            st["clipped"] += 1 if changed else 0
            rendered.append(f"```{lang}\n{body}\n```")
        else:
            kept, s = distill_md(payload)
            for k in ("nav", "selfref", "dropped"):
                st[k] += s[k]
            rendered.append("\n".join(kept))
    text = "\n\n".join(x for x in rendered if x.strip())
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    st["chars_out"] = len(text)
    return text, st


# ── 主题 → 子卡 → 源文档 ─────────────────────────────────────────────────────
D = "core/developing-apps/"
E = "core/extension-development/"
F = "core/framework/"
U = "core/using-plugins/"
A = "core/architecture/"

TOPICS = {
    "app-dev": {
        "01-frontend-pages": [D + "overview", D + "project-structure", D + "pages-routes-and-navigation",
                              D + "pages-and-interactions", D + "page-layouts", D + "data-requests-and-state",
                              D + "client-business-services"],
        "02-server-services": [D + "apis-and-services", D + "server-business-services",
                               D + "request-validation-and-errors", D + "authentication-and-permissions",
                               D + "business-workflows", D + "background-tasks"],
        "03-data-models": [D + "data-models-and-migrations", D + "querying-data",
                           D + "transactions-and-consistency", D + "multiple-databases", D + "existing-databases"],
        "04-commands-cli": [D + "application-commands", D + "plugin-commands", D + "cli-client"],
        "05-quality-and-settings": [D + "testing-and-acceptance", D + "configuration-and-settings",
                                    D + "localization", D + "themes-and-styles"],
        "06-plugin-config": [U + "overview", D + "manage-plugins",
                             U + "authentication/users", U + "authentication/sign-in", U + "authentication/api-keys",
                             U + "authorization/permissions", U + "authorization/default-access",
                             U + "authorization/sharing-rules", U + "authorization/restriction-rules",
                             U + "data-and-files/database-explorer", U + "data-and-files/file-management",
                             U + "notifications/notification", U + "notifications/providers",
                             U + "notifications/in-app", U + "notifications/web-push", U + "notifications/mail",
                             U + "agents-and-knowledge/agents", U + "agents-and-knowledge/knowledge",
                             U + "collaboration/approval", U + "automation/scheduler", U + "automation/template-print",
                             U + "application-support/i18n", U + "application-support/foundation"],
    },
    "plugin-dev": {
        "01-decide-and-scaffold": [E + "when-to-write-a-plugin", E + "create-plugin", E + "plugin-structure",
                                   E + "plugin-development-guidance"],
        "02-walkthrough": [E + "write-your-first-plugin"],
        "03-declarations": [E + "plugin-declarations", E + "service-provider"],
        "04-client-side": [E + "pages-and-menus", E + "frontend-components", E + "react-context-and-providers",
                           E + "client-services", E + "localization"],
        "05-server-side": [E + "server-apis", E + "server-services", E + "background-jobs", E + "server-localization"],
        "06-data-and-migrations": [E + "database-and-migrations"],
        "07-extend-cli-and-skills": [E + "extend-command-line", E + "write-plugin-skills"],
        "08-test-and-publish": [E + "testing-and-verification", E + "publish-plugin"],
    },
    "framework": {
        "01-runtime": [F + "overview", F + "runtime/client", F + "runtime/server", F + "runtime/cli",
                       F + "runtime/lifecycle", F + "runtime/plugins", F + "runtime/react-providers"],
        "02-services": [F + "services/container", F + "services/tokens", F + "services/integration"],
        "03-http": [F + "http/routes", F + "http/middleware", F + "http/validation",
                    F + "http/repository-routes", F + "http/api-client"],
        "04-database": [F + "database/overview", F + "database/connections", F + "database/schema",
                        F + "database/relations", F + "database/repositories", F + "database/filtering-pagination",
                        F + "database/association-queries", F + "database/aggregation", F + "database/transactions",
                        F + "database/migrations", F + "database/seeds", F + "database/query-inputs"],
        "05-background-and-realtime": [F + "background/jobs", F + "background/scheduling", F + "background/queues",
                                       F + "realtime/topics", F + "realtime/websocket"],
        "06-support": [F + "support/caching", F + "support/logging", F + "support/ids", F + "file-storage"],
    },
    "architecture": {
        "01-models": [A + "overview"],
        "02-multi-portal": [A + "multi-portal/create-app", A + "multi-portal/develop",
                            A + "multi-portal/access", A + "multi-portal/manage"],
        "03-multi-app": [A + "multi-app/overview", A + "multi-app/quickstart", A + "multi-app/development",
                         A + "multi-app/management", A + "multi-app/single-sign-on", A + "multi-app/external-apps",
                         A + "multi-app/migration", A + "multi-app/deployment"],
    },
    "deploy-ops": {
        "01-choose-and-publish": ["core/deployment/choose-a-deployment-method", "core/deployment/publish-app-release"],
        "02-docker": ["core/tutorials/deploy-with-docker"],
        "03-installer": ["core/tutorials/deploy-with-app-installer"],
        "04-upgrade": [D + "upgrade-nocobase-core"],
    },
    "reference": {
        "01-reference": [f"core/reference/{x}" for x in
                         ("api", "cli", "configuration", "packages", "plugins", "project-conventions",
                          "compatibility", "database-configuration", "faq")],
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stat", action="store_true")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    manifest = json.load(open(os.path.join(SRC, "manifest.json"), encoding="utf-8"))
    by_path = {x["path"][:-3] if x["path"].endswith(".md") else x["path"]: x for x in manifest}

    known = {p for cards in TOPICS.values() for pages in cards.values() for p in pages}
    missing = [p for p in known if p not in by_path]
    if missing:
        print("⚠️ 主题表里这些文档不存在：", missing, file=sys.stderr)
        return 1

    tot_in = tot_out = 0
    rows, cards_made = [], 0
    for topic, cards in TOPICS.items():
        d = os.path.join(args.out, topic)
        os.makedirs(d, exist_ok=True)
        seen = set()          # 去重按主题隔离：同一段代码在不同 skill 里可能都需要
        for card, pages in cards.items():
            parts, cin = [], 0
            for p in pages:
                if p not in by_path:
                    continue
                meta = by_path[p]
                text, st = distill_page(meta["path"], seen)
                tot_in += st["chars_in"]
                tot_out += st["chars_out"]
                cin += st["chars_out"]
                parts.append(f"<!-- src: {meta['path']} | {meta['href']} -->\n{text}")
            body = "\n\n---\n\n".join(parts)
            open(os.path.join(d, card + ".md"), "w", encoding="utf-8").write(body + "\n")
            cards_made += 1
            rows.append((topic, card, len(pages), cin))

    orphans = [x for x in manifest
               if (x["path"][:-3] if x["path"].endswith(".md") else x["path"]) not in known]

    # 全量索引：134 篇一篇不漏
    idx = ["# 全量文档索引", "",
           f"> 共 {len(manifest)} 篇。已精蒸 {len(known)} 篇进各卡；其余见下，需要细节时打开原文。", ""]
    for x in manifest:
        href = x["href"] if x["href"].startswith("http") else "https://docs.nocobase.com/zh-CN/" + x["href"].lstrip("/")
        idx.append(f"- **{x['title']}** — `{x['path']}` · {x['chars']:,} 字符 · {href}")
    open(os.path.join(args.out, "_index.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")

    lines = ["# 蒸馏压缩比", "", "| 主题 | 卡 | 篇 | 蒸馏后字符 |", "| --- | --- | ---: | ---: |"]
    for topic, card, n, c in rows:
        lines.append(f"| {topic} | {card} | {n} | {c:,} |")
    lines += ["", f"合计 {len(known)} 篇：{tot_in:,} → {tot_out:,} = **{tot_out / tot_in:.0%}**",
              f"卡数 {cards_made}；索引覆盖 {len(manifest)} 篇（孤儿 {len(orphans)} 篇）"]
    open(os.path.join(args.out, "_compression.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"卡数 {cards_made}，压缩 {tot_in:,} → {tot_out:,} = {tot_out / tot_in:.0%}，索引覆盖 {len(manifest)} 篇")
    if orphans:
        print("未入卡（靠索引指路）：", [x['path'] for x in orphans])
    return 0


if __name__ == "__main__":
    sys.exit(main())
