import * as path from 'node:path';
import * as fs from 'node:fs';
import { defineConfig } from '@rspress/core';
import { pluginLlms } from '@rspress/plugin-llms';
import sidebar from './sidebar.json';

const SITE = 'https://meesumaes.github.io/nocobase-core-docs';
const BASE_PATH = '/nocobase-core-docs';
const maptree = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'maptree.json'), 'utf-8'),
) as Array<{
  group: string;
  sections: Array<{
    name: string | null;
    docs: Array<{ title: string; route: string; brief: string }>;
  }>;
}>;

/** 按「分组 > 子分组 > 文档」生成 llms.txt，作为给 LLM 的文档地图 */
function buildLlmsTxt(): string {
  const total = maptree.reduce(
    (n, g) => n + g.sections.reduce((k, s) => k + s.docs.length, 0),
    0,
  );
  const L: string[] = [
    '# NocoBase 3 Core 文档（简体中文）',
    '',
    `> NocoBase 3 官方文档 Core 章节的中文镜像，共 ${total} 篇，按官方分组层级整理。` +
      '内容涵盖应用开发、插件开发、框架机制、应用架构、部署运维与 API 参考。' +
      '原文：https://docs.nocobase.com/zh-CN/core/',
    '',
    `- 文档地图（可浏览）：${SITE}/map`,
    `- 全量正文（单文件）：${SITE}/llms-full.txt`,
    `- 每篇 markdown：本清单每条链接指向该页的 .md 源，可直接抓取`,
    '',
  ];
  const root = maptree.find((g) => g.group === '（根）');
  if (root) {
    L.push('## 开始', '');
    for (const sec of root.sections) {
      for (const d of sec.docs) L.push(`- [${d.title}](${SITE}/index.md): ${d.brief}`);
    }
    L.push('');
  }
  for (const node of maptree) {
    if (node.group === '（根）') continue;
    const cnt = node.sections.reduce((k, s) => k + s.docs.length, 0);
    L.push(`## ${node.group}（${cnt} 篇）`, '');
    for (const sec of node.sections) {
      if (sec.name) L.push(`### ${sec.name}`, '');
      for (const d of sec.docs) {
        const url = d.route === '/' ? `${SITE}/index.md` : `${SITE}${d.route}.md`;
        L.push(`- [${d.title}](${url}): ${d.brief}`);
      }
      L.push('');
    }
  }
  return L.join('\n');
}

export default defineConfig({
  root: path.join(__dirname, 'docs'),
  base: `${BASE_PATH}/`,
  lang: 'zh',
  llms: false,
  plugins: [
    pluginLlms({
      llmsTxt: {
        name: 'llms.txt',
        onAfterLlmsTxtGenerate: () => buildLlmsTxt(),
      },
    }),
  ],
  title: 'NocoBase 3 Core 文档',
  themeConfig: {
    llmsUI: true,
    nav: [
      { text: '首页', link: '/' },
      { text: '文档地图', link: '/map' },
      { text: 'llms.txt', link: `${SITE}/llms.txt` },
      { text: '官方原文', link: 'https://docs.nocobase.com/zh-CN/core/' },
    ],
    sidebar: { '/': sidebar as any },
    socialLinks: [
      { icon: 'github', mode: 'link', content: 'https://github.com/MeesuMaes/nocobase-core-docs' },
    ],
    lastUpdated: false,
  },
});
