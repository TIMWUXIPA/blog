#!/usr/bin/env python3
"""Dependency-free checks of the real Jekyll output; run after building."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
TUTORIAL = 'cook/avocado-codfish-tutorial'
assert SITE.is_dir(), 'Run bundle exec jekyll build first'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.metas, self.anchors = [], [], set()
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.anchors.add(a['id'])
        if tag == 'meta':
            self.metas.append(a)
        for key in ('href', 'src', 'poster'):
            if key in a:
                self.links.append((tag, key, a[key], a))

pages = list(SITE.rglob('*.html'))
checked = 0
for path in pages:
    text = path.read_text()
    assert '{{' not in text and '{%' not in text, f'Unrendered Liquid: {path}'
    page = Page(text)
    for tag, key, url, attrs in page.links:
        split = urlsplit(url)
        assert attrs.get('target') != '_blank', f'New-tab link: {path}: {url}'
        if split.scheme or split.netloc or url.startswith(('mailto:', 'tel:', 'data:')):
            continue
        if not split.path:
            target = path
        elif split.path.startswith('/'):
            target = SITE / unquote(split.path).lstrip('/')
        else:
            target = path.parent / unquote(split.path)
        if target.is_dir():
            target = target / 'index.html'
        assert target.is_file(), f'Missing local resource: {path}: {url}'
        if split.fragment and target.suffix == '.html':
            assert unquote(split.fragment) in Page(target.read_text()).anchors, f'Missing anchor: {path}: {url}'
        checked += 1

for relative in ('index.html', 'cook/index.html'):
    text = (SITE / relative).read_text()
    assert f'/{TUTORIAL}/' in text, f'Tutorial missing in {relative}'
    for url in ('https://wydns.dpdns.org', 'https://blog.wydns.dpdns.org', 'https://game.wydns.dpdns.org', 'https://tv.wydns.dpdns.org'):
        assert url in text, f'Nav missing {url}'
assert (SITE / 'notes/kitchen-notes/index.html').is_file(), 'Markdown post was not generated'
assert '厨房笔记，从记录过程开始' in (SITE / 'index.html').read_text(), 'Post not automatically listed'
text = (SITE / TUTORIAL / 'index.html').read_text()
assert any(m.get('name') == 'robots' and 'noindex' in m.get('content', '') for m in Page(text).metas), 'Tutorial lost noindex'
urls = [e.text for e in ET.parse(SITE / 'sitemap.xml').iter() if e.tag.endswith('}loc')]
assert len(urls) >= 3, f'Expected homepage, kitchen and at least one article: {urls}'
assert all(TUTORIAL not in u for u in urls), 'Tutorial indexed in sitemap'
assert all(u.startswith('https://blog.wydns.dpdns.org/') for u in urls)
assert 'Disallow:' not in (SITE / 'robots.txt').read_text(), 'Robots blocks crawl/noindex discovery'
assert not (SITE / TUTORIAL / 'robots.txt').exists()
for relative in ('README.md', 'Gemfile', 'Gemfile.lock', 'scripts/verify.py', '.github/workflows/pages.yml'):
    assert not (SITE / relative).exists(), f'Private build source leaked: {relative}'
source = ROOT / TUTORIAL
for p in source.rglob('*'):
    if p.is_file():
        out = SITE / p.relative_to(ROOT)
        assert out.is_file(), f'Missing migrated file {out}'
        assert hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(out.read_bytes()).digest(), f'Tutorial altered during build: {out}'
print(f'PASS: {len(pages)} generated HTML pages; {checked} local references/anchors; {len(urls)} sitemap URLs; post listing, navigation, noindex, output exclusions and all 18 tutorial files verified.')
