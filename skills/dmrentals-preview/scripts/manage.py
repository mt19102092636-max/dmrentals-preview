#!/usr/bin/env python3
"""Manage one static preview and rebuild the existing catalog. Python 3.9+."""
import argparse
import html
import json
import re
import shutil
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', required=True, type=Path)
    p.add_argument('action', choices=['add', 'update', 'delete'])
    p.add_argument('--slug', required=True)
    p.add_argument('--name')
    p.add_argument('--summary')
    p.add_argument('--source', type=Path)
    a = p.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', a.slug):
        p.error('slug 必须为英文 kebab-case')
    root = a.repo.resolve()
    catalog = root / 'sites.json'
    data = json.loads(catalog.read_text(encoding='utf-8'))
    entries = data['sites']
    old = next((s for s in entries if s['slug'] == a.slug), None)
    target = root / 'previews' / a.slug
    if (root / 'previews').is_symlink() or target.is_symlink():
        p.error('拒绝通过符号链接修改页面')
    if a.action == 'add' and (old or target.exists()):
        p.error('名称已存在，请使用新的 slug')
    if a.action != 'add' and not old:
        p.error('目标页面不存在')
    index = root / 'index.html'
    template = index.read_text(encoding='utf-8')
    if not re.search(r'<main class="grid">.*?</main>', template, re.S):
        p.error('首页结构已变化，请先适配目录渲染器')
    now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')
    if a.action != 'delete':
        if not a.source or not a.name or not a.summary:
            p.error('新增、更新需要 source、name、summary')
        source = a.source.resolve()
        if not source.exists() or (source.is_dir() and not (source / 'index.html').is_file()):
            p.error('source 必须为 HTML 文件或包含 index.html 的文件夹')
        if source.is_file() and source.suffix.lower() not in ('.html', '.htm'):
            p.error('source 文件必须为 HTML')
        if source.is_dir() and (source == root or root in source.parents or source in root.parents):
            p.error('请从仓库以外的独立素材文件夹输入')
        files = list(source.rglob('*')) if source.is_dir() else [source]
        if any(f.is_symlink() for f in files):
            p.error('素材不可包含符号链接')
        for f in files:
            if f.is_file() and f.suffix.lower() in ('.html', '.htm', '.css', '.js'):
                content = f.read_text(encoding='utf-8')
                if re.search(r'file://|https?://(?:localhost|127\.0\.0\.1)|["\x27]/(?:Users|home)/', content):
                    p.error('发现本机路径或本地服务依赖：' + str(f))
        with tempfile.TemporaryDirectory() as tmp:
            staged = Path(tmp) / 'page'
            if source.is_dir():
                shutil.copytree(source, staged)
            else:
                staged.mkdir()
                shutil.copy2(source, staged / 'index.html')
            target.parent.mkdir(exist_ok=True)
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(staged, target)
        item = dict(old or {}, slug=a.slug, name=a.name, summary=a.summary,
                    path=f'previews/{a.slug}/', updatedAt=now)
        item.setdefault('createdAt', now)
        entries = [item if s['slug'] == a.slug else s for s in entries] if old else entries + [item]
    else:
        if target.exists():
            shutil.rmtree(target)
        entries = [s for s in entries if s['slug'] != a.slug]
    cards = []
    esc = html.escape
    for s in entries:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', s['slug']):
            raise ValueError('目录含非法 slug')
        cards.append(f'<article class="card"><div class="card-top"><span class="tag">{esc(s["slug"])}</span>'
                     f'<span class="time">更新于 {esc(s["updatedAt"][:16].replace("T", " "))}</span></div>'
                     f'<h2>{esc(s["name"])}</h2><p>{esc(s["summary"])}</p>'
                     f'<a href="./previews/{esc(s["slug"])}/">打开原型 <span>→</span></a></article>')
    body = '\n'.join(cards) or '<div class="empty"><h2>暂无原型</h2><p>新增 HTML 后将在这里展示。</p></div>'
    template = re.sub(r'<main class="grid">.*?</main>', lambda _: '<main class="grid">' + body + '</main>', template, flags=re.S)
    template = re.sub(r'共 \d+ 个原型', f'共 {len(entries)} 个原型', template)
    template = re.sub(r'目录更新：[^<]+', '目录更新：' + now[:16].replace('T', ' '), template)
    data.update(sites=entries, updatedAt=now)
    catalog.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    index.write_text(template, encoding='utf-8')
    print(f'{a.action}: {a.slug}，本地修改完成，尚未提交或部署')


if __name__ == '__main__':
    main()
