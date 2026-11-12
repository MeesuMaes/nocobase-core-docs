# NocoBase 3 Core 文档（简体中文）

NocoBase 3 官方文档 **Core 章节** 的简体中文镜像，已清洗成可检索、可构建的文档集，基于 [Rspress](https://rspress.dev/) 构建。

- 原文：https://docs.nocobase.com/zh-CN/core/
- 规模：**134 篇 / 约 67.5 万字符**，7 大分组
- 在线：https://meesumaes.github.io/nocobase-core-docs/

## 给 LLM 用

| 入口 | 说明 |
| --- | --- |
| [`/llms.txt`](https://meesumaes.github.io/nocobase-core-docs/llms.txt) | 文档地图：按「分组 → 子分组 → 文档」列出全部 134 篇，每条含一句话摘要 + 该页 `.md` 直链 |
| [`/llms-full.txt`](https://meesumaes.github.io/nocobase-core-docs/llms-full.txt) | 全量正文单文件 |
| [`/map`](https://meesumaes.github.io/nocobase-core-docs/map) | 站内可浏览的文档地图页 |
| `/{route}.md` | 任一页面追加 `.md` 即为该页纯 markdown |

## 为什么单独建仓

这批内容是 NocoBase 3 的**开发手册**（应用开发 / 插件开发 / 框架 / 参考），属于 docs 范畴，不适合塞进官网 blog 内容库。独立成仓便于版本追踪、全文检索与喂给 AI。

## 目录结构

```
source/            原始抓取底稿（保留 core/ 层级，可追溯）
  core/**/*.md     每篇的官方 markdown 原文
  manifest.json    机读元数据：分组 / 标题 / 源 URL / 字符数
  INDEX.md         结构化索引（分组 → 子分组 → 文档）
  core-docs.csv    同一份清单的表格版
docs/              Rspress 页面（由 source 生成，勿手改）
sidebar.json       侧边栏（按官方分组层级生成）
scripts/           生成脚本
```

## 本地运行

```bash
npm install
npm run dev      # 本地预览
npm run build    # 产物在 doc_build/
```

## 更新文档

官方更新后重新抓取，再重新生成页面与侧栏：

```bash
python3 scripts/fetch.py --out ./source_raw   # 抓取官方 md 源
python3 scripts/generate.py                   # 生成 docs/ 与 sidebar.json
npm run build
```

依赖：Python 3（仅标准库）、Node 20+。

## 清洗口径

- 正文取自官网「Copy Markdown」对应的原始 `.md` 源，非 HTML 解析，无导航/侧栏/页脚噪声
- 图片相对路径补全为绝对 URL（108 处）
- 指向 Core 之外的相对链接转网页 URL（37 处）；Core 内部链接保留相对形态，目录层级与官方一致
- 代码块原样保留（736 处：ts 276、bash 236、tsx 65、yaml 21、json 20、prompt 16）
- 生成 Rspress 页面时对正文做 MDX 转义（代码块外 `{}` `<`），避免编译错误

## 说明

文档内容版权归 NocoBase 所有（上游 [nocobase/docs](https://github.com/nocobase/docs) 为 MIT 许可）。本仓库仅做抓取、清洗与排版，代码部分同样以 MIT 发布，详见 [LICENSE](./LICENSE)。
