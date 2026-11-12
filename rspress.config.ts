import * as path from 'node:path';
import { defineConfig } from '@rspress/core';
import { pluginLlms } from '@rspress/plugin-llms';
import sidebar from './sidebar.json';

export default defineConfig({
  root: path.join(__dirname, 'docs'),
  base: '/nocobase-core-docs/',
  lang: 'zh',
  llms: false,
  plugins: [pluginLlms()],
  title: 'NocoBase 3 Core 文档',
  themeConfig: {
    llmsUI: true,
    nav: [
      { text: '首页', link: '/' },
      { text: '开发应用', link: '/developing-apps/overview' },
      { text: '框架', link: '/framework/overview' },
      { text: '参考', link: '/reference/configuration' },
      { text: '官方原文', link: 'https://docs.nocobase.com/zh-CN/core/' },
    ],
    sidebar: { '/': sidebar as any },
    socialLinks: [
      { icon: 'github', mode: 'link', content: 'https://github.com/MeesuMaes/nocobase-core-docs' },
    ],
    lastUpdated: false,
  },
});
