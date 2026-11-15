# WYDNS 博客

轻量 Jekyll 站点，目标域名 `https://blog.wydns.dpdns.org`。本目录仅完成本地准备；没有发布、创建远程仓库或修改 DNS。

## 本地运行

推荐 Ruby **3.3**（与 Actions 一致），Bundler 2.x。依赖固定在 `Gemfile`；`Gemfile.lock` 应随仓库提交。不要使用 macOS 自带旧 Ruby 作为长期开发环境。

```sh
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --host 127.0.0.1 --future
```

打开 `http://127.0.0.1:4000`。`--future` 仅供预览；正式构建不会提前发布未来文章。不要提交 `vendor/`、`.bundle/` 或 `_site/`。

生产构建和验证：

```sh
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 scripts/verify.py
```

验证脚本检查生成页面的本地链接、媒体和锚点、Markdown 文章生成与自动列表、共享导航、站点地图、教程 noindex、源文件排除和教程逐文件校验。

## 写文章

新增 `_posts/YYYY-MM-DD-slug.md`：

```markdown
---
title: "文章标题"
description: "一句简短介绍"
date: 2026-11-15 10:00:00 +0800
category: 手记
---

Markdown 正文。
```

文章会自动出现在首页「最近手记」和站点地图；默认地址为 `/notes/slug/`。图片放 `assets/images/`，引用绝对站内路径，如 `/assets/images/example.jpg`。可通过 `noindex: true` 排除站点地图并添加 robots meta。草稿可放 `_drafts/`，本地用 `--drafts` 预览。正式发布日期由 `Asia/Shanghai` 时区控制。

## 文件结构

- `_layouts/default.html`：站点外壳、SEO 基础信息及同标签页导航。
- `_layouts/post.html`：文章布局。
- `assets/css/style.css`：暖象牙白与陶土色、系统字体、响应式样式。
- `index.html`：精选教程和自动文章列表。
- `cook/index.html`：厨房目录。
- `cook/avocado-codfish-tutorial/`：原有独立教程及其 16 张截图、1 个视频；HTML 与媒体保留原样。
- `robots.txt`：允许抓取，以便搜索引擎读取教程自身的 `noindex,nofollow,noarchive`。
- `sitemap.xml`：显式列出首页、厨房目录及可索引文章，不包含教程。
- `.github/workflows/pages.yml`：构建、验证、上传 Pages artifact，然后使用官方 Pages Actions 部署。

教程来源目录：`/Users/tim/hermes-workspace/video-lab/牛油果香煎鳕鱼/教程/site`。没有复制 `.git`、源 README、原 `.nojekyll` 或原根级 `robots.txt`（其 `Disallow: /` 不适用于新博客），也没有复制任何原始研究材料。教程内保留来源与权利说明；公开发布前应确认截图及视频的使用授权。`noindex` 不是访问控制，链接仍可被任何人打开。

## 部署准备（需另行授权执行）

1. 将**本目录作为仓库根目录**提交到 GitHub，默认分支设为 `main`；若使用其他分支，调整 workflow 的 `push.branches`。
2. 在仓库 Settings → Pages 选择 **GitHub Actions**。工作流使用 Ruby 3.3、锁定依赖、构建验证及官方 artifact 上传/部署。
3. Pages 自定义域名设为 `blog.wydns.dpdns.org`，并由域名负责人配置 DNS、确认域名验证与 HTTPS。`CNAME` 仅是本地部署配置文件，不会修改 DNS。
4. 推送 main 或手动运行 workflow 后检查 Actions 与 Pages URL。`contents: read` 用于构建；仅部署任务获得 `pages: write` 和 `id-token: write`，使用 `github-pages` environment。

未配置 Pages 或未授权域名时，Actions 部署可能失败。这是部署准备，不代表远程 CI/Pages 已验证。导航的主站、博客、游戏、影视域名均使用同标签页链接；外部服务可用性由各站负责人维护。
