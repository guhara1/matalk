#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""마톡 출장마사지 정적 사이트 빌더.

사용법:
    python3 build.py            # dist/ 에 전체 사이트 생성
    python3 build.py --minify   # 미니파이까지 적용

의존성 0개 — 순수 표준 라이브러리만 사용합니다.
"""
import os
import re
import sys
import json
import shutil
from datetime import date

from src import config as C
from src import data as D
from src import pages, pages2, icons

OUT = os.path.join(os.path.dirname(__file__), "dist")


# ─────────────────────────────────────────────
# 미니파이 (옵션)
# ─────────────────────────────────────────────
def minify_jsonld(m):
    try:
        obj = json.loads(m.group(2))
    except Exception:
        return m.group(0)
    return f'{m.group(1)}{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}{m.group(3)}'


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    css = re.sub(r"\s+", " ", css)
    return re.sub(r";}", "}", css).strip()


def minify_html(html):
    html = re.sub(r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', minify_jsonld, html, flags=re.S)
    html = re.sub(r"<style[^>]*>(.*?)</style>", lambda m: f"<style>{minify_css(m.group(1))}</style>", html, flags=re.S)
    # 태그 사이 공백 제거 (pre/script 외)
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"  +", " ", html)
    return html


# ─────────────────────────────────────────────
# 정적 자산
# ─────────────────────────────────────────────
def favicon_svg():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<defs><radialGradient id="g" cx="35%" cy="30%" r="80%">'
        '<stop offset="0%" stop-color="#f4d29c"/><stop offset="55%" stop-color="#e9b8a7"/>'
        '<stop offset="100%" stop-color="#c98a6b"/></radialGradient></defs>'
        '<rect width="64" height="64" rx="14" fill="#0b0b0e"/>'
        '<circle cx="32" cy="32" r="20" fill="url(#g)"/>'
        '<circle cx="26" cy="25" r="6" fill="#fff" opacity=".35"/>'
        '<text x="32" y="41" font-family="Georgia,serif" font-size="22" font-style="italic" '
        'text-anchor="middle" fill="#0b0b0e" font-weight="700">M</text></svg>'
    )


def webmanifest():
    return json.dumps({
        "name": C.BRAND_FULL, "short_name": C.BRAND,
        "description": "서울·경기·인천·부산 24시간 출장 건강관리",
        "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#0b0b0e", "theme_color": "#0b0b0e",
        "lang": "ko-KR", "orientation": "portrait",
        "icons": [
            {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }, ensure_ascii=False)


def robots_txt():
    return (
        "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /api/\n\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {C.DOMAIN}/sitemap.xml\n"
        f"Host: {C.DOMAIN.replace('https://', '')}\n"
    )


def sitemap_xml(paths):
    today = date.today().isoformat()
    prio = []
    for p in paths:
        url = p if p == "/" else p
        depth = p.strip("/").count("/")
        if p == "/":
            pr, freq = "1.0", "daily"
        elif p.startswith("/locations/") and depth == 2:  # district leaf
            pr, freq = "0.75", "weekly"
        elif p.startswith("/magazine/") and p != "/magazine/":
            pr, freq = "0.7", "monthly"
        elif p.startswith("/policy/"):
            pr, freq = "0.3", "yearly"
        elif depth >= 1:
            pr, freq = "0.85", "weekly"
        else:
            pr, freq = "0.9", "weekly"
        prio.append((C.DOMAIN + p, pr, freq))
    items = "".join(
        f"<url><loc>{u}</loc><lastmod>{today}</lastmod>"
        f"<changefreq>{f}</changefreq><priority>{pr}</priority></url>"
        for u, pr, f in prio)
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.w3.org/2000/sitemaps/0.9">' + items + "</urlset>")


# ─────────────────────────────────────────────
# 빌드
# ─────────────────────────────────────────────
def url_of(file_path):
    """/service/index.html -> /service/ ; /index.html -> /"""
    p = file_path[:-len("index.html")] if file_path.endswith("index.html") else file_path
    return p if p else "/"


def main():
    do_minify = "--minify" in sys.argv
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    builders = [
        pages.build_index, pages.build_services, pages.build_therapists, pages.build_pricing,
        pages2.build_locations_hub, pages2.build_region_hubs, pages2.build_districts,
        pages2.build_magazine, pages2.build_reviews, pages2.build_about, pages2.build_policies,
    ]
    written = []
    titles = {}
    descs = {}
    canons = {}
    for b in builders:
        for file_path, html in b():
            if do_minify:
                html = minify_html(html)
            dest = os.path.join(OUT, file_path.lstrip("/"))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(html)
            written.append(url_of(file_path))
            # 고유성 검증용 수집
            t = re.search(r"<title>(.*?)</title>", html, re.S)
            de = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
            cn = re.search(r'<link rel="canonical" href="(.*?)">', html)
            if t: titles.setdefault(t.group(1), []).append(file_path)
            if de: descs.setdefault(de.group(1), []).append(file_path)
            if cn: canons.setdefault(cn.group(1), []).append(file_path)

    # 정적 파일
    extra = {
        "robots.txt": robots_txt(),
        "sitemap.xml": sitemap_xml(sorted(set(written))),
        "site.webmanifest": webmanifest(),
        "favicon.svg": favicon_svg(),
    }
    for name, content in extra.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)

    # 아이콘 (PNG/ICO — 순수 파이썬 생성)
    icon_files = {
        "favicon.ico": icons.ico_bytes(32),
        "apple-touch-icon.png": icons.png_bytes(180),
        "icon-192.png": icons.png_bytes(192),
        "icon-512.png": icons.png_bytes(512),
        "icon-maskable-512.png": icons.png_bytes(512, maskable=True),
    }
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    icon_files["assets/logo.png"] = icons.png_bytes(512)
    icon_files["assets/og-cover.jpg"] = None  # placeholder note below
    for name, content in icon_files.items():
        if content is None:
            continue
        with open(os.path.join(OUT, name), "wb") as f:
            f.write(content)
    # OG 커버는 1200x630 전용 이미지가 권장됩니다(플레이스홀더로 512 PNG 복사).
    with open(os.path.join(OUT, "assets/og-cover.jpg"), "wb") as f:
        f.write(icons.png_bytes(512))

    # ── 검증 리포트 ──
    print(f"✓ 생성 완료: {len(written)} 페이지 → {OUT}")
    dup_t = {k: v for k, v in titles.items() if len(v) > 1}
    dup_d = {k: v for k, v in descs.items() if len(v) > 1}
    dup_c = {k: v for k, v in canons.items() if len(v) > 1}
    print(f"  · 고유 title: {len(titles)} / {len(written)}  (중복 {len(dup_t)})")
    print(f"  · 고유 description: {len(descs)} / {len(written)}  (중복 {len(dup_d)})")
    print(f"  · 고유 canonical: {len(canons)} / {len(written)}  (중복 {len(dup_c)})")
    for label, dup in (("TITLE", dup_t), ("DESC", dup_d), ("CANONICAL", dup_c)):
        for val, files in list(dup.items())[:10]:
            print(f"    ! {label} 중복: {val[:60]!r} → {files}")
    # 내부 링크 점검 (간단)
    print("  · robots.txt / sitemap.xml / site.webmanifest / favicon.svg 생성됨")
    return 0 if not (dup_t or dup_d or dup_c) else 1


if __name__ == "__main__":
    sys.exit(main())
