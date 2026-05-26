# -*- coding: utf-8 -*-
"""공통 컴포넌트: <head>, 헤더, 푸터, 카드, JSON-LD 등 모든 페이지 공용 빌딩블록."""
import json
import html as _html
from . import config as C
from . import data as D

# ─────────────────────────────────────────────
# 전역 CSS (인라인 — 외부 요청 0)
# ─────────────────────────────────────────────
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0b0b0e;--surface:#13131a;--surface-2:#1a1a23;--line:rgba(255,255,255,.08);
  --text:#f3f3f5;--muted:#9a9aa3;--dim:#6c6c75;
  --gold:#d6b274;--rose:#e9b8a7;--copper:#c98a6b;
  --grad:linear-gradient(135deg,#f4d29c 0%,#e9b8a7 45%,#c98a6b 100%);
  --grad-soft:linear-gradient(135deg,rgba(244,210,156,.14),rgba(201,138,107,.06));
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);line-height:1.65;letter-spacing:-.01em;
  font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  -webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.serif,.note-num,.step .n{font-family:"Cormorant Garamond","Noto Serif KR",Georgia,serif;font-weight:300;font-style:italic}
.grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.wrap{max-width:1240px;margin:0 auto;padding:120px 24px}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:18px}
.pulse{width:7px;height:7px;border-radius:50%;background:var(--rose);box-shadow:0 0 0 0 rgba(233,184,167,.6);animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(233,184,167,.5)}70%{box-shadow:0 0 0 9px rgba(233,184,167,0)}100%{box-shadow:0 0 0 0 rgba(233,184,167,0)}}
h1{font-size:clamp(40px,6.5vw,76px);font-weight:800;letter-spacing:-.038em;line-height:1.05}
h2{font-size:clamp(28px,4vw,46px);letter-spacing:-.03em;font-weight:800;line-height:1.1}
.lead{color:var(--muted);font-size:clamp(15px,1.6vw,18px);max-width:560px;margin-top:18px;line-height:1.7}
.section-head{max-width:660px;margin-bottom:48px}
.section-head p{color:var(--muted);margin-top:14px;font-size:15px}

/* HEADER */
header{position:sticky;top:0;z-index:90;background:rgba(11,11,14,.82);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav{max-width:1240px;margin:0 auto;display:flex;align-items:center;gap:20px;padding:14px 24px}
.brand{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:30px;font-weight:600;letter-spacing:-.02em}
.brand b{font-style:normal;font-family:"Pretendard",sans-serif;font-weight:800;font-size:24px}
.menu{display:flex;align-items:center;gap:4px;margin-left:auto;list-style:none}
.menu>li{position:relative}
.menu>li>a{display:block;padding:10px 14px;font-size:14.5px;color:var(--text);border-radius:10px;transition:.2s}
.menu>li>a:hover{background:rgba(255,255,255,.05);color:var(--rose)}
.submenu{position:absolute;top:calc(100% + 6px);left:0;min-width:180px;background:var(--surface);
  border:1px solid var(--line);border-radius:14px;padding:8px;list-style:none;
  opacity:0;visibility:hidden;transform:translateY(8px);transition:.22s;box-shadow:0 18px 44px rgba(0,0,0,.4)}
.menu>li:hover>.submenu,.submenu.open{opacity:1;visibility:visible;transform:none}
.submenu a{display:block;padding:9px 12px;border-radius:9px;font-size:14px;color:var(--muted);transition:.18s}
.submenu a:hover{background:var(--grad-soft);color:var(--text)}
.cta-pill{background:var(--grad);color:#1a1108!important;font-weight:800;border-radius:999px;padding:11px 20px!important}
.cta-pill:hover{filter:brightness(1.05);transform:translateY(-1px)}
.toggle{display:none;margin-left:auto;background:none;border:1px solid var(--line);color:var(--text);
  font-size:20px;width:44px;height:44px;border-radius:11px;cursor:pointer}

/* HERO */
.hero{position:relative;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;
  background:radial-gradient(800px 500px at 80% -10%,rgba(244,210,156,.14),transparent 60%),
  radial-gradient(700px 500px at 10% 20%,rgba(201,138,107,.12),transparent 55%),
  radial-gradient(900px 700px at 50% 120%,rgba(233,184,167,.08),transparent 60%)}
.hero-inner{max-width:1240px;margin:0 auto;padding:96px 24px 110px;display:grid;grid-template-columns:1.15fr .85fr;gap:60px;align-items:center}
.hero h1 span.serif{display:inline-block}
.actions{display:flex;gap:14px;margin-top:30px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:8px;padding:14px 26px;border-radius:999px;font-weight:700;font-size:15px;transition:.22s}
.btn-primary{background:var(--grad);color:#1a1108}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 16px 36px rgba(201,138,107,.32)}
.btn-ghost{border:1px solid var(--line);color:var(--text)}
.btn-ghost:hover{border-color:rgba(244,210,156,.4);background:rgba(255,255,255,.03)}
.trust{margin-top:30px;display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--muted);font-size:13.5px;align-items:center}
.trust .stars{color:var(--gold);letter-spacing:2px}
.hero-visual{position:relative}
.glass{background:rgba(26,26,35,.55);backdrop-filter:blur(20px);border:1px solid;
  border-image:var(--grad) 1;border-radius:22px;padding:26px;transform:rotate(2deg);box-shadow:0 30px 70px rgba(0,0,0,.45)}
.glass h3{font-size:21px;font-weight:800;margin-bottom:16px}
.glass h3 small{display:block;font-size:11px;letter-spacing:.2em;color:var(--gold);font-weight:700;text-transform:uppercase;margin-bottom:6px}
.book-row{display:flex;justify-content:space-between;padding:11px 0;border-top:1px solid var(--line);font-size:14px}
.book-row span:first-child{color:var(--muted)}
.bk{display:block;text-align:center;margin-top:16px;background:var(--grad);color:#1a1108;font-weight:800;padding:13px;border-radius:13px}
.floating{position:absolute;background:var(--surface);border:1px solid var(--line);border-radius:14px;
  padding:11px 15px;font-size:12px;box-shadow:0 16px 40px rgba(0,0,0,.4);display:flex;align-items:center;gap:8px}
.floating b{font-weight:800}
.fl-1{top:-22px;left:-26px;transform:rotate(-4deg)}
.fl-2{bottom:-20px;right:-18px;transform:rotate(3deg)}
.fl-label{font-size:9px;letter-spacing:.18em;color:var(--gold);text-transform:uppercase;display:block}

/* compact hero (sub pages) */
.hero-compact{padding:72px 24px 64px}
.hero-compact h1{font-size:clamp(32px,5vw,56px)}
.breadcrumb{font-size:12.5px;color:var(--dim);margin-bottom:18px}
.breadcrumb a:hover{color:var(--rose)}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.chip{display:inline-flex;flex-direction:column;gap:2px;background:var(--surface);border:1px solid var(--line);
  border-radius:13px;padding:12px 18px}
.chip small{font-size:10px;letter-spacing:.16em;color:var(--gold);text-transform:uppercase;font-weight:700}
.chip b{font-size:16px;font-weight:800}

/* MARQUEE */
.marquee{overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:16px 0;background:var(--surface)}
.marquee-track{display:flex;gap:38px;width:max-content;animation:scroll 38s linear infinite}
.marquee-track span{color:var(--muted);font-size:13px;letter-spacing:.08em;white-space:nowrap}
.marquee-track span::before{content:"◆";color:var(--copper);margin-right:38px;font-size:8px;vertical-align:middle}
@keyframes scroll{to{transform:translateX(-50%)}}

/* GRID CARDS */
.grid{display:grid;gap:18px}
.g4{grid-template-columns:repeat(4,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
.card{background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);
  border-radius:18px;padding:24px;transition:.3s;position:relative;overflow:hidden}
.card:hover{transform:translateY(-4px);border-color:rgba(244,210,156,.28);box-shadow:0 18px 44px rgba(0,0,0,.32)}
.card .k{font-size:10.5px;letter-spacing:.18em;color:var(--gold);text-transform:uppercase;font-weight:700}
.card h3{font-size:19px;font-weight:800;margin:10px 0 8px}
.card p{color:var(--muted);font-size:14px;line-height:1.7}
.card .arrow{margin-top:14px;font-size:13px;color:var(--rose);font-weight:700}

/* NOTE CARD */
.notes{display:flex;flex-direction:column;gap:16px}
.note-card{display:flex;gap:24px;padding:26px 28px;border-radius:18px;
  background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);
  transition:.3s;position:relative;overflow:hidden}
.note-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--grad);opacity:0;transition:.3s}
.note-card:hover::before{opacity:1}
.note-card:hover{transform:translateY(-2px);box-shadow:0 18px 44px rgba(0,0,0,.32);border-color:rgba(244,210,156,.28)}
.note-num{font-size:46px;line-height:1;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;flex:none}
.note-title{font-size:19px;font-weight:800;margin-bottom:10px}
.note-text{max-width:660px}
.note-text p{margin:0 0 10px;color:#c8c8d0;font-size:14.5px;line-height:1.78}

/* PRICE */
.price-card{background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);
  border-radius:18px;padding:24px;position:relative;overflow:hidden;transition:.3s}
.price-card::after{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--grad)}
.price-card:hover{transform:translateY(-3px);border-color:rgba(244,210,156,.3)}
.price-card.best{border-color:rgba(244,210,156,.45)}
.best-badge{position:absolute;top:16px;right:16px;background:var(--grad);color:#1a1108;font-size:10px;
  font-weight:800;letter-spacing:.1em;padding:4px 10px;border-radius:999px}
.price-card .kicker{font-size:10.5px;letter-spacing:.16em;color:var(--gold);text-transform:uppercase;font-weight:700}
.price-card h3{font-size:21px;font-weight:800;margin:8px 0 6px}
.price-card>p{color:var(--muted);font-size:13.5px;margin-bottom:14px;min-height:38px}
.time-rows>div{display:flex;justify-content:space-between;padding:10px 0;border-top:1px solid var(--line);font-size:14.5px}
.time-rows>div b{font-weight:800}

/* DATA BOX */
.data-box{background:var(--grad-soft);border:1px solid rgba(244,210,156,.2);border-radius:18px;padding:28px}
.data-box h3{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);font-weight:800;margin-bottom:14px}
.data-box p{color:#c8c8d0;font-size:14px;line-height:1.75;margin-bottom:8px}
.data-box .src{font-size:12px;color:var(--dim);margin-top:10px}

/* STEPS */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.step{background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);border-radius:18px;padding:24px}
.step .n{font-size:38px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.step h3{font-size:17px;font-weight:800;margin:8px 0 6px}
.step p{color:var(--muted);font-size:13.5px}

/* REVIEWS */
.review{background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--line);border-radius:18px;padding:24px}
.review .stars{color:var(--gold);letter-spacing:2px;font-size:14px}
.review p{margin:12px 0;color:#c8c8d0;font-size:14px;line-height:1.7}
.review .who{font-size:12.5px;color:var(--muted)}

/* FAQ */
details{border:1px solid var(--line);border-radius:14px;margin-bottom:12px;background:var(--surface);overflow:hidden}
summary{cursor:pointer;list-style:none;padding:20px 24px;font-weight:700;font-size:15.5px;display:flex;justify-content:space-between;align-items:center;gap:16px}
summary::-webkit-details-marker{display:none}
summary span{color:var(--gold);font-size:22px;font-weight:300;transition:.2s}
details[open] summary span{transform:rotate(45deg)}
details>div{padding:0 24px 22px;color:var(--muted);font-size:14.5px;line-height:1.75}

/* CTA BAND */
.cta-band{background:var(--grad-soft);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.cta-band .wrap{text-align:center;padding:96px 24px}
.cta-band h2{margin-bottom:18px}
.cta-band p{color:var(--muted);max-width:520px;margin:0 auto 30px}

/* FOOTER */
.site-footer{background:#08080b;border-top:1px solid var(--line)}
.footer-wrap{max-width:1240px;margin:0 auto;padding:72px 24px 40px}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:40px;margin-bottom:44px}
.footer-grid h4{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:800;margin-bottom:16px}
.footer-grid a,.footer-grid li{display:block;color:var(--muted);font-size:13.5px;margin-bottom:9px;list-style:none}
.footer-grid a:hover{color:var(--rose)}
.footer-brand .brand{font-size:28px;margin-bottom:12px;display:inline-block}
.footer-brand p{color:var(--muted);font-size:13.5px;line-height:1.7;max-width:300px}
.footer-ops{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:24px;background:var(--grad-soft);border-radius:16px;margin-bottom:24px}
.footer-ops .blk small{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);font-weight:700;display:block;margin-bottom:6px}
.footer-ops .blk b{font-size:17px;font-weight:800}
.company-info{display:grid;grid-template-columns:repeat(3,1fr);gap:14px 28px;padding:24px 0;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted)}
.company-info .lbl{color:var(--dim);display:block;font-size:11px;margin-bottom:2px}
.footer-policies{display:flex;flex-wrap:wrap;gap:8px 20px;padding:20px 0;border-top:1px solid var(--line);font-size:13px}
.footer-policies a{color:var(--muted)}
.footer-policies a:hover{color:var(--rose)}
.footer-bottom{padding-top:20px;border-top:1px solid var(--line);font-size:12px;color:var(--dim);line-height:1.7}

/* REVEAL */
.reveal{opacity:0;transform:translateY(20px);transition:.8s}
.reveal.in{opacity:1;transform:none}

/* MOBILE FIXED CALL BAR */
.callbar{display:none}
.callbar a{display:flex;align-items:center;justify-content:center;gap:8px}
@media(max-width:1100px){
  .callbar{display:flex;gap:10px;position:fixed;left:0;right:0;bottom:0;z-index:120;
    padding:10px 14px;padding-bottom:calc(10px + env(safe-area-inset-bottom));
    background:rgba(11,11,14,.94);backdrop-filter:blur(12px);border-top:1px solid var(--line)}
  .callbar .c-call{flex:1;background:var(--grad);color:#1a1108;font-weight:800;font-size:15.5px;
    padding:15px;border-radius:13px}
  body{padding-bottom:78px}
}

/* CONTENT VISIBILITY */
.cv{content-visibility:auto;contain-intrinsic-size:auto 700px}

@media(max-width:1100px){
  .toggle{display:block}
  .menu{position:fixed;inset:64px 0 auto 0;flex-direction:column;align-items:stretch;gap:0;
    background:var(--bg);border-bottom:1px solid var(--line);padding:12px;max-height:0;overflow:hidden;transition:.3s;margin-left:0}
  .menu.open{max-height:90vh;overflow:auto;padding:12px}
  .menu>li>a{padding:14px}
  .submenu{position:static;opacity:1;visibility:visible;transform:none;box-shadow:none;border:none;background:transparent;
    max-height:0;overflow:hidden;transition:.25s;padding:0 0 0 14px}
  .submenu.open{max-height:500px;padding:0 0 8px 14px}
  .hero-inner{grid-template-columns:1fr;gap:40px}
  .hero-visual{max-width:420px}
  .g4,.g3,.steps{grid-template-columns:1fr 1fr}
  .footer-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:640px){
  .wrap{padding:80px 18px}
  .g4,.g3,.g2,.steps,.footer-grid,.company-info{grid-template-columns:1fr}
  .note-card{flex-direction:column;gap:10px;padding:22px}
  .note-num{font-size:36px}
  .footer-ops{grid-template-columns:1fr}
}
@media(hover:none){.glass,.floating{backdrop-filter:none!important}}
@media(prefers-reduced-motion:reduce){
  .marquee-track,.pulse{animation:none!important}
  .reveal{opacity:1!important;transform:none!important}
  html{scroll-behavior:auto}
}
"""

# 비크리티컬 JS (idle 로드)
JS = """
function idle(fn){if('requestIdleCallback'in window){requestIdleCallback(fn,{timeout:1500})}else{setTimeout(fn,1)}}
idle(function(){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'80px'});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  var t=document.querySelector('.toggle'),m=document.getElementById('primary-menu');
  if(t&&m){t.addEventListener('click',function(){var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o)})}
  document.querySelectorAll('.menu>li>a[aria-haspopup]').forEach(function(a){
    a.addEventListener('click',function(e){
      if(window.innerWidth<=1100){var sub=a.parentNode.querySelector('.submenu');
        if(sub){e.preventDefault();sub.classList.toggle('open')}}})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){
    document.querySelectorAll('.submenu.open,.menu.open').forEach(function(el){el.classList.remove('open')})}});
});
"""


def esc(s):
    return _html.escape(str(s), quote=True)


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + '</script>'


# ─────────────────────────────────────────────
# <head>
# ─────────────────────────────────────────────
def head(title, desc, path, *, jsonld_blocks=None, prefetch=None, og_image=None, extra_meta=""):
    url = C.DOMAIN + path
    og_image = og_image or (C.DOMAIN + "/assets/og-cover.jpg")
    blocks = "".join(jsonld_blocks or [])
    pf = ""
    if prefetch:
        pf = "".join(f'<link rel="prefetch" href="{p}" as="document">' for p in prefetch)
    return f"""<!doctype html><html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b0b0e">
<meta name="format-detection" content="telephone=no">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="googlebot" content="index,follow">
<meta name="referrer" content="strict-origin-when-cross-origin">{extra_meta}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(C.AUTHOR)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ko-KR" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(C.BRAND_FULL)}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="{esc(C.BRAND_FULL)} RSS" href="/rss.xml">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
{pf}
<style>{CSS}</style>
{blocks}
</head><body>"""


# ─────────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────────
def _submenu(items):
    return '<ul class="submenu">' + "".join(f'<li><a href="{href}">{esc(label)}</a></li>' for label, href in items) + "</ul>"


def header():
    svc = [(s["name"], f"/service/{s['slug']}/") for s in D.SERVICES]
    loc = [(r["kr"], f"/locations/{r['slug']}/") for r in D.REGIONS]
    ther = [(t["name"] + "인", f"/therapists/{t['slug']}/") for t in D.THERAPISTS]
    return f"""<header><nav class="nav" aria-label="주 메뉴">
<a class="brand" href="/" aria-label="{esc(C.BRAND_FULL)} 홈"><b>{esc(C.BRAND)}</b> <span>massage</span></a>
<button class="toggle" aria-expanded="false" aria-controls="primary-menu" aria-label="메뉴 열기">☰</button>
<ul id="primary-menu" class="menu">
<li><a href="/service/" aria-haspopup="true">서비스</a>{_submenu(svc)}</li>
<li><a href="/locations/" aria-haspopup="true">지역</a>{_submenu(loc)}</li>
<li><a href="/therapists/" aria-haspopup="true">관리사</a>{_submenu(ther)}</li>
<li><a href="/pricing/">요금</a></li>
<li><a href="/magazine/">매거진</a></li>
<li><a href="/reviews/">후기</a></li>
<li><a href="/about/">소개</a></li>
<li><a class="cta-pill" href="tel:{C.PHONE_TEL}">24시 예약</a></li>
</ul></nav></header>"""


# ─────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────
def footer():
    svc = "".join(f'<a href="/service/{s["slug"]}/">{esc(s["name"])}</a>' for s in D.SERVICES)
    loc = "".join(f'<a href="/locations/{r["slug"]}/">{esc(r["kr"])} 출장마사지</a>' for r in D.REGIONS)
    ci = C.COMPANY
    info = [
        ("회사명", ci["name"]), ("대표자", ci["ceo"]), ("사업자등록번호", ci["biz_no"]),
        ("주소", ci["addr"]), ("통신판매업신고", ci["mailorder_no"]), ("개인정보보호책임자", ci["privacy_officer"]),
    ]
    info_html = "".join(f'<div><span class="lbl">{esc(l)}</span>{esc(v)}</div>' for l, v in info)
    return f"""<footer class="site-footer"><div class="footer-wrap">
<div class="footer-grid">
  <div class="footer-brand">
    <a class="brand" href="/"><b>{esc(C.BRAND)}</b></a>
    <p>{esc(C.BRAND_FULL)}는 서울·경기·인천·부산 전 권역에 본사 디스패치 기반으로 검증된 관리사를 24시간 배차하는 출장 건강관리 서비스입니다.</p>
  </div>
  <div><h4>서비스</h4>{svc}</div>
  <div><h4>지역</h4>{loc}</div>
  <div><h4>안내</h4>
    <a href="/pricing/">요금 안내</a><a href="/therapists/">관리사 안내</a>
    <a href="/magazine/">매거진</a><a href="/reviews/">이용 후기</a><a href="/about/">회사 소개</a>
  </div>
</div>
<div class="footer-ops">
  <div class="blk"><small>운영 시간</small><b>{esc(C.HOURS)}</b></div>
  <div class="blk"><small>고객센터</small><b><a href="tel:{C.PHONE_TEL}">{esc(C.PHONE)}</a> · {esc(C.EMAIL)}</b></div>
</div>
<div class="company-info">{info_html}</div>
<div class="footer-policies">
  <a href="/policy/privacy/">개인정보처리방침</a>
  <a href="/policy/terms/">이용약관</a>
  <a href="/policy/youth/">청소년보호정책</a>
  <a href="/about/">회사 소개</a>
  <a href="/reviews/">이용 후기</a>
</div>
<div class="footer-bottom">
  본 서비스는 의료 행위가 아닌 건강관리·휴식 목적의 출장 서비스이며, 만 19세 이상 성인을 대상으로 합니다. 불법·퇴폐 서비스를 일절 제공하지 않습니다.<br>
  © 2026 {esc(C.BRAND_FULL)}. All rights reserved.
</div>
</div></footer>
<nav class="callbar" aria-label="빠른 예약">
  <a class="c-call" href="tel:{C.PHONE_TEL}" aria-label="전화 예약 {esc(C.PHONE)}">📞 24시 전화 예약 {esc(C.PHONE)}</a>
</nav>
<script>{JS}</script></body></html>"""


# ─────────────────────────────────────────────
# 재사용 블록
# ─────────────────────────────────────────────
def note_cards(items, start=1):
    out = ['<div class="notes">']
    for i, (title, paras) in enumerate(items, start):
        ps = "".join(f"<p>{esc(p)}</p>" for p in paras)
        out.append(f'<div class="note-card reveal"><div class="note-num">{i:02d}</div>'
                   f'<div><h3 class="note-title">{esc(title)}</h3><div class="note-text">{ps}</div></div></div>')
    out.append("</div>")
    return "".join(out)


def price_grid(services):
    cards = []
    for s in services:
        rows = "".join(f"<div><span>{t}</span><b>{p}</b></div>" for t, p in s["prices"])
        badge = '<span class="best-badge">BEST</span>' if s.get("best") else ""
        cls = "price-card best" if s.get("best") else "price-card"
        cards.append(f'<div class="{cls} reveal">{badge}<div class="kicker">{esc(s["kicker"])}</div>'
                     f'<h3>{esc(s["name"])}</h3><p>{esc(s["summary"])}</p>'
                     f'<div class="time-rows">{rows}</div></div>')
    return ('<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">'
            + "".join(cards) + "</div>")


def faq_block(qas):
    out = ['<div>']
    for q, a in qas:
        out.append(f'<details><summary>{esc(q)}<span>+</span></summary><div>{esc(a)}</div></details>')
    out.append("</div>")
    return "".join(out)


def faq_jsonld(qas):
    return jsonld({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas],
    })


def breadcrumb(trail):
    links = " <span style='color:var(--dim)'>›</span> ".join(
        (f'<a href="{href}">{esc(label)}</a>' if href else esc(label)) for label, href in trail)
    return f'<div class="breadcrumb">{links}</div>'


def breadcrumb_jsonld(trail):
    items = []
    for i, (label, href) in enumerate(trail, 1):
        item = {"@type": "ListItem", "position": i, "name": label}
        if href:
            item["item"] = C.DOMAIN + href
        items.append(item)
    return jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})


def cta_band(title="오늘 밤, 가장 가까운 관리사를 배차해 드립니다", sub=None):
    sub = sub or "전화 또는 카카오톡으로 지역과 코스를 알려주시면 본사 디스패처가 예상 도착 시간을 즉시 안내드립니다."
    return f"""<section class="cta-band"><div class="wrap reveal">
<span class="eyebrow"><span class="pulse"></span>RESERVE TONIGHT</span>
<h2>{esc(title)}</h2><p>{esc(sub)}</p>
<div class="actions" style="justify-content:center">
<a class="btn btn-primary" href="tel:{C.PHONE_TEL}">전화 예약 {esc(C.PHONE)} →</a>
<a class="btn btn-ghost" href="/pricing/">요금 보기</a>
</div></div></section>"""


def section_head(eyebrow, title, sub=None):
    s = f"<p>{esc(sub)}</p>" if sub else ""
    return (f'<div class="section-head reveal"><span class="eyebrow"><span class="pulse"></span>{esc(eyebrow)}</span>'
            f'<h2>{esc(title)}</h2>{s}</div>')


# ─────────────────────────────────────────────
# 공통 JSON-LD (Organization / WebSite / LocalBusiness)
# ─────────────────────────────────────────────
def org_jsonld():
    return {
        "@type": "Organization", "@id": C.DOMAIN + "/#org",
        "name": C.BRAND_FULL, "legalName": C.LEGAL_NAME, "url": C.DOMAIN + "/",
        "logo": C.DOMAIN + "/assets/logo.png", "email": C.EMAIL,
        "sameAs": list(C.SOCIAL.values()),
        "contactPoint": {"@type": "ContactPoint", "telephone": C.PHONE_TEL,
                         "contactType": "reservations", "availableLanguage": ["ko", "en"]},
    }


def website_jsonld():
    return {
        "@type": "WebSite", "@id": C.DOMAIN + "/#website",
        "url": C.DOMAIN + "/", "name": C.BRAND_FULL, "inLanguage": "ko-KR",
        "publisher": {"@id": C.DOMAIN + "/#org"},
        "potentialAction": {"@type": "SearchAction",
                            "target": {"@type": "EntryPoint", "urlTemplate": C.DOMAIN + "/locations/?q={query}"},
                            "query-input": "required name=query"},
    }


def localbusiness_jsonld(area=None, name=None, url=None):
    name = name or C.BRAND_FULL
    return {
        "@type": "HealthAndBeautyBusiness",
        "@id": (url or C.DOMAIN + "/") + "#business",
        "name": name, "url": url or C.DOMAIN + "/",
        "image": C.DOMAIN + "/assets/og-cover.jpg",
        "telephone": C.PHONE_TEL, "email": C.EMAIL, "priceRange": "₩₩",
        "areaServed": area or "서울·경기·인천·부산",
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": C.HOURS_OPENS, "closes": C.HOURS_CLOSES},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": C.STATS["rating"],
                            "reviewCount": C.STATS["review_count"], "bestRating": "5"},
    }
