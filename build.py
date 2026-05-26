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
from datetime import date, datetime, timezone
from email.utils import format_datetime

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
    # PNG 래스터(icons.py)와 동일한 4획 'M' 모노그램 (음각)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<defs><radialGradient id="g" cx="36%" cy="30%" r="80%">'
        '<stop offset="0%" stop-color="#f4d29c"/><stop offset="55%" stop-color="#e9b8a7"/>'
        '<stop offset="100%" stop-color="#c98a6b"/></radialGradient></defs>'
        '<rect width="64" height="64" rx="14" fill="#0b0b0e"/>'
        '<circle cx="32" cy="32" r="25.6" fill="url(#g)"/>'
        '<circle cx="23" cy="19" r="7" fill="#fff" opacity=".28"/>'
        '<polyline points="20.5,41.6 20.5,22.4 32,35.2 43.5,22.4 43.5,41.6" '
        'fill="none" stroke="#0b0b0e" stroke-width="6.7" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>'
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
    # 색인 봇별 허용 (구글·네이버 Yeti·다음·빙 + AI 크롤러) + 다중 사이트맵 + RSS
    host = C.DOMAIN.replace("https://", "").replace("http://", "")
    bots = ["*", "Googlebot", "Googlebot-Image", "Yeti", "NaverBot", "Daum", "Daumoa",
            "bingbot", "GPTBot", "ClaudeBot", "Google-Extended"]
    body = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    body = body.replace("User-agent: *\nAllow: /\n\n",
                        "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /api/\n\n")
    return (
        body
        + f"Sitemap: {C.DOMAIN}/sitemap.xml\n"
        + f"Sitemap: {C.DOMAIN}/sitemap1.xml\n"
        + f"Sitemap: {C.DOMAIN}/rss.xml\n"
        + f"Host: {host}\n"
    )


def _priority(p):
    depth = p.strip("/").count("/")
    if p == "/":
        return "1.0", "daily"
    if p.startswith("/locations/") and depth == 2:  # 행정구 리프
        return "0.75", "weekly"
    if p.startswith("/magazine/") and p != "/magazine/":
        return "0.7", "weekly"
    if p.startswith("/policy/"):
        return "0.3", "yearly"
    if depth >= 1:
        return "0.85", "weekly"
    return "0.9", "weekly"


def sitemap_urlset(paths):
    """전체 URL 사이트맵 (sitemap1.xml — 구글/네이버 제출용)."""
    today = date.today().isoformat()
    items = ""
    for p in paths:
        pr, freq = _priority(p)
        items += (f"<url><loc>{C.DOMAIN}{p}</loc><lastmod>{today}</lastmod>"
                  f"<changefreq>{freq}</changefreq><priority>{pr}</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</urlset>")


def sitemap_index():
    """사이트맵 인덱스 (sitemap.xml) — 하위 사이트맵을 가리킴."""
    today = date.today().isoformat()
    subs = [f"{C.DOMAIN}/sitemap1.xml"]
    items = "".join(f"<sitemap><loc>{u}</loc><lastmod>{today}</lastmod></sitemap>" for u in subs)
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</sitemapindex>")


def _rfc822(d):
    try:
        dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        dt = datetime.now(timezone.utc)
    return format_datetime(dt)


def _x(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rss_xml():
    """RSS 2.0 피드 — 네이버/구글 빠른 색인용. 매거진 + 핵심 페이지를 항목으로."""
    from src import data as D
    now = format_datetime(datetime.now(timezone.utc))
    items = []
    # 매거진 글 (콘텐츠 스트림)
    for m in D.MAGAZINE:
        url = f"{C.DOMAIN}/magazine/{m['slug']}/"
        items.append(
            f"<item><title>{_x(m['title'])}</title><link>{url}</link>"
            f"<guid isPermaLink=\"true\">{url}</guid>"
            f"<pubDate>{_rfc822(m['date'])}</pubDate>"
            f"<description>{_x(m['desc'])}</description></item>")
    # 주요 허브 페이지 (신규 색인 유도)
    hubs = [("/", f"{C.BRAND_FULL} — 서울·경기·인천·부산 24시간 출장 건강관리"),
            ("/pricing/", f"{C.BRAND} 출장마사지 요금 안내"),
            ("/locations/", f"{C.BRAND} 지역별 출장마사지")]
    for r in D.REGIONS:
        hubs.append((f"/locations/{r['slug']}/", f"{r['kr']} 출장마사지 — {C.BRAND}"))
    for path, title in hubs:
        url = C.DOMAIN + path
        items.append(
            f"<item><title>{_x(title)}</title><link>{url}</link>"
            f"<guid isPermaLink=\"true\">{url}</guid>"
            f"<pubDate>{now}</pubDate></item>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f"<title>{_x(C.BRAND_FULL)}</title>"
        f"<link>{C.DOMAIN}/</link>"
        f'<atom:link href="{C.DOMAIN}/rss.xml" rel="self" type="application/rss+xml"/>'
        f"<description>{_x('서울·경기·인천·부산 24시간 출장 건강관리 — 마톡 매거진과 지역 안내')}</description>"
        "<language>ko</language>"
        f"<lastBuildDate>{now}</lastBuildDate>"
        f"<pubDate>{now}</pubDate>"
        + "".join(items) +
        "</channel></rss>")


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
        "sitemap.xml": sitemap_index(),
        "sitemap1.xml": sitemap_urlset(sorted(set(written))),
        "rss.xml": rss_xml(),
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
    print("  · robots.txt / sitemap.xml(index) / sitemap1.xml / rss.xml / manifest / favicon 생성됨")
    return 0 if not (dup_t or dup_d or dup_c) else 1


if __name__ == "__main__":
    sys.exit(main())
