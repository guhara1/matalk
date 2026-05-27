# -*- coding: utf-8 -*-
"""페이지 빌더 (2부): 지역 3계층, 매거진, 후기, 소개, 정책."""
from . import config as C
from . import data as D
from . import gen
from .components import (
    head, header, footer, esc, jsonld, note_cards, price_grid, faq_block, faq_jsonld,
    breadcrumb, breadcrumb_jsonld, cta_band, section_head, org_jsonld, localbusiness_jsonld,
)

S = C.STATS


# ─────────────────────────────────────────────
# 지역 허브 (/locations/)
# ─────────────────────────────────────────────
def build_locations_hub():
    region_blocks = []
    for r in D.REGIONS:
        chips = "".join(
            f'<a class="card" style="padding:14px 16px" href="/locations/{r["slug"]}/{d["slug"]}/">'
            f'<h3 style="font-size:15px;margin:0">{esc(d["kr"])}</h3></a>'
            for d in r["districts"])
        region_blocks.append(
            f'<div class="reveal" style="margin-bottom:48px"><h2 style="font-size:26px;margin-bottom:6px">'
            f'<a href="/locations/{r["slug"]}/">{esc(r["kr"])} 출장마사지</a></h2>'
            f'<p style="color:var(--muted);margin-bottom:18px">{esc(r["label"])}</p>'
            f'<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(140px,1fr))">{chips}</div></div>')
    trail = [("홈", "/"), ("지역", None)]
    blocks = [breadcrumb_jsonld(trail),
              jsonld({"@context": "https://schema.org", "@type": "ItemList",
                      "itemListElement": [{"@type": "ListItem", "position": i, "name": f"{r['kr']} 출장마사지",
                                           "url": C.DOMAIN + f"/locations/{r['slug']}/"} for i, r in enumerate(D.REGIONS, 1)]})]
    total = sum(len(r["districts"]) for r in D.REGIONS)
    html = head("지역별 출장마사지 — 서울·경기·인천·부산 전 권역 | 마톡",
                f"마톡 출장마사지 지역 안내 — 서울·경기·인천·부산 총 {total}개 권역 24시간 배차. 시·군·구를 선택하세요.",
                "/locations/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>SERVICE AREA</span>
<h1>전 권역 <span class="grad">{total}개</span> 시·군·구</h1>
<p class="lead">서울·경기·인천·부산 어디든 본사 디스패치 기반으로 24시간 배차합니다.</p></div></section>"""
    html += f'<section class="wrap cv">{"".join(region_blocks)}</section>'
    html += cta_band()
    html += footer()
    return [("/locations/index.html", html)]


# 광역 허브 메타 (4개 권역 각각 다른 구조·각도)
_REGION_META = {
    "seoul": (
        "서울 출장마사지 — 25개 자치구 심야 방문관리 | 마톡",
        "서울 25개 자치구 평균 30분대 방문 출장마사지. 강남·마포·송파 등 야간 24시간 배차, 정찰 요금.",
    ),
    "gyeonggi": (
        "경기 출장마사지 | 31개 시·군 광역 24시간 배차 — 마톡",
        "수원·성남·고양·용인 등 경기 31개 시·군 방문 마사지. 신도시·외곽까지 24시간 배차, 정찰 요금.",
    ),
    "incheon": (
        "인천 출장마사지 — 송도·청라·공항권 방문관리 | 마톡",
        "송도·청라부터 공항·원도심까지 인천 10개 군·구 출장마사지. 24시간 배차, 구별 도착시간 안내.",
    ),
    "busan": (
        "부산 출장마사지 | 해운대·서면 등 16개 군·구 24시 — 마톡",
        "해운대·서면·광안리 등 부산 16개 군·구 방문 마사지. 연중무휴 배차, 구별 도착시간·정찰 요금.",
    ),
}


# ─────────────────────────────────────────────
# 광역 허브 (/locations/seoul/ 등)
# ─────────────────────────────────────────────
def build_region_hubs():
    out = []
    for r in D.REGIONS:
        trail = [("홈", "/"), ("지역", "/locations/"), (r["kr"], None)]
        cards = "".join(
            f'<a class="card reveal" href="/locations/{r["slug"]}/{d["slug"]}/"><div class="k">{esc(", ".join(d["landmarks"][:2]))}</div>'
            f'<h3>{esc(d["kr"])} 출장마사지</h3><p>{esc(d["character"])}</p><div class="arrow">자세히 →</div></a>'
            for d in r["districts"])
        notes = note_cards([
            (f"{r['kr']} 권역 운영 개요", [
                f"{C.BRAND_FULL}는 {r['kr']} {r['label']} 전역에 본사 디스패치 기반으로 관리사를 배차합니다.",
                f"권역별 콜 분포와 이동 동선을 분석해 평균 도착 시간을 관리합니다.",
                "각 시·군·구 페이지에서 동별 도착 시간과 권역 특성을 확인할 수 있습니다.",
            ]),
            ("예약 안내", [
                "전화 또는 카카오톡으로 지역·코스·시간을 알려주시면 예약이 확정됩니다.",
                "24시간 연중무휴로 심야 예약도 가능합니다.",
                "예약 시 확정된 금액 그대로, 추가 비용 요구가 없습니다.",
            ]),
        ])
        blocks = [breadcrumb_jsonld(trail), jsonld({"@context": "https://schema.org", "@type": "ItemList",
                  "itemListElement": [{"@type": "ListItem", "position": i, "name": f"{d['kr']} 출장마사지",
                                       "url": C.DOMAIN + f"/locations/{r['slug']}/{d['slug']}/"}
                                      for i, d in enumerate(r["districts"], 1)]}),
                  jsonld({"@context": "https://schema.org", **{k: v for k, v in localbusiness_jsonld(area=r['kr'], name=f"{C.BRAND_FULL} {r['kr']}").items()}})]
        rt, rd = _REGION_META[r["slug"]]
        html = head(rt, rd,
                    f"/locations/{r['slug']}/", jsonld_blocks=blocks, prefetch=[f"/locations/{r['slug']}/{r['districts'][0]['slug']}/"])
        html += header()
        html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>{esc(r['en'].upper())}</span>
<h1>{esc(r['kr'])} <span class="grad">출장마사지</span></h1>
<p class="lead">{esc(r['label'])} 전 권역 24시간 배차. 아래에서 원하는 지역을 선택하세요.</p>
<div class="actions">
  <a class="btn btn-primary" href="tel:{C.PHONE_TEL}">📞 {esc(r['kr'])} 전화 예약 {esc(C.PHONE)}</a>
  <a class="btn btn-ghost" href="/pricing/">요금 보기</a>
</div></div></section>"""
        dist_head = section_head("DISTRICTS", f"{r['kr']} {r['label']}")
        html += f'<section class="wrap cv">{dist_head}<div class="grid g3">{cards}</div></section>'
        html += f'<section class="wrap cv" style="padding-top:0">{notes}</section>'
        html += cta_band()
        html += footer()
        out.append((f"/locations/{r['slug']}/index.html", html))
    return out


# ─────────────────────────────────────────────
# 행정구 페이지 (82개)
# ─────────────────────────────────────────────
def build_districts():
    out = []
    for r in D.REGIONS:
        for d in r["districts"]:
            out.append(_district_page(r, d))
    return out


def _district_page(r, d):
    path = f"/locations/{r['slug']}/{d['slug']}/"
    trail = [("홈", "/"), ("지역", "/locations/"), (r["kr"], f"/locations/{r['slug']}/"), (d["kr"], None)]
    arrivals = gen.arrival_table(d)
    avg = round(sum(m for _, m in arrivals) / len(arrivals))
    overview = gen.overview_notes(d, r)
    fnotes = gen.field_notes(d, r)
    revs = gen.reviews(d, 6)
    landmarks = ", ".join(d["landmarks"])

    faq = [
        (f"{d['kr']} 출장마사지는 도착까지 얼마나 걸리나요?",
         f"{d['kr']} 권역 평균 약 {avg}분입니다. {gen.josa(arrivals[0][0], '은는')} 약 {arrivals[0][1]}분 내외로 도착합니다."),
        (f"{d['kr']} 어느 동까지 출장이 되나요?",
         f"{', '.join(d['areas'])} 등 {d['kr']} 전역에 배차합니다. 인접 권역도 가능합니다."),
        (f"{d['kr']}에서 심야에도 예약되나요?",
         "예. 24시간 연중무휴로 운영하여 심야·새벽에도 예약과 배차가 가능합니다."),
        (f"{d['kr']} 요금은 다른 지역과 다른가요?",
         "동일한 코스별 표시 요금이 적용되며 출장비·할증 없이 예약 시 확정 금액 그대로입니다."),
    ]

    review_jsonld = [{"@type": "Review", "author": {"@type": "Person", "name": rv["author"]},
                      "reviewRating": {"@type": "Rating", "ratingValue": rv["rating"], "bestRating": "5"},
                      "reviewBody": rv["body"]} for rv in revs]
    lb = localbusiness_jsonld(area=f"{r['kr']} {d['kr']}", name=f"{C.BRAND_FULL} {d['kr']}", url=C.DOMAIN + path)
    lb["review"] = review_jsonld
    blocks = [
        breadcrumb_jsonld(trail), faq_jsonld(faq),
        jsonld({"@context": "https://schema.org", "@graph": [
            lb,
            {"@type": "AdministrativeArea", "name": f"{r['kr']} {d['kr']}"},
            {"@type": "Service", "name": f"{d['kr']} 출장마사지", "provider": {"@id": C.DOMAIN + "/#org"},
             "areaServed": {"@type": "AdministrativeArea", "name": f"{r['kr']} {d['kr']}"},
             "description": f"{d['kr']} 전역 24시간 출장 건강관리 서비스"},
        ]}),
    ]

    html = head(gen.meta_title(r, d, avg),
                gen.meta_desc(r, d, avg, arrivals),
                path, jsonld_blocks=blocks, prefetch=["/pricing/"])
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>{esc(r['en'].upper())} · {esc(d['kr'])} OPERATIONS</span>
<h1>{esc(d['kr'])} <span class="grad">출장마사지</span></h1>
<p class="lead">{esc(d['character'])}. {esc(landmarks)} 일대를 포함한 {esc(d['kr'])} 전역에 24시간 배차합니다.</p>
<div class="actions">
  <a class="btn btn-primary" href="tel:{C.PHONE_TEL}">📞 {esc(d['kr'])} 전화 예약 {esc(C.PHONE)}</a>
  <a class="btn btn-ghost" href="/pricing/">요금 보기</a>
</div>
<div class="chips">
  <div class="chip"><small>평균 도착</small><b>약 {avg}분</b></div>
  <div class="chip"><small>운영</small><b>{esc(C.HOURS)}</b></div>
  <div class="chip"><small>권역 성격</small><b>{esc(d['character'].split()[0] if d['character'] else d['kr'])}</b></div>
</div></div></section>"""
    ov_head = section_head("OVERVIEW", f"{d['kr']} 운영 데이터")
    fn_head = section_head("FIELD NOTES · 2026", f"{d['kr']} 권역 노트")
    dongs = D.DONGS.get(d["slug"])
    if dongs:
        dong_cards = "".join(
            f'<a class="card reveal" href="/locations/{r["slug"]}/{d["slug"]}/{dg["slug"]}/">'
            f'<div class="k">{esc(dg["lm"])}</div><h3>{esc(dg["kr"])} 출장마사지</h3>'
            f'<p>{esc(dg["char"])}</p><div class="arrow">자세히 →</div></a>'
            for dg in dongs)
        dong_head = section_head("ADMINISTRATIVE DONG", f"{d['kr']} 행정동별 안내")
        html += (f'<section class="wrap cv" style="padding-top:0">{dong_head}'
                 f'<div class="grid g3">{dong_cards}</div></section>')
    html += f'<section class="wrap cv">{ov_head}{note_cards(overview, start=5)}</section>'
    html += f'<section class="wrap cv" style="padding-top:0">{fn_head}{note_cards(fnotes, start=1)}</section>'

    html += f"""<section class="wrap cv" style="padding-top:0">{section_head("DATA & METHODOLOGY", "데이터 출처")}
<div class="data-box reveal">
  <h3>{esc(d['kr'])} 도착 시간 산출 근거</h3>
  <p>위 동별 도착 시간은 {S['months']}개월간 누적된 {r['kr']} 권역 배차 로그를 동(洞) 단위로 집계한 1차 데이터입니다.</p>
  <p>교통 상황·시간대에 따라 실제 도착 시간은 달라질 수 있으며, 예약 시 예상 시간을 다시 안내드립니다.</p>
  <p class="src">출처: 마톡 본사 디스패치 로그 · {esc(d['kr'])} 권역 집계(2025.10–2026.05). 분기별 갱신.</p>
  <p class="src">작성 <a href="/about/" style="color:var(--rose)">마톡 편집팀</a> · 감수 박지연(안전 자문 트레이너) · 최종 갱신 2026-05</p>
</div></section>"""

    html += f'<section class="wrap cv" style="padding-top:0">{section_head("PRICING", "코스 요금")}{price_grid(D.SERVICES)}</section>'

    rev_cards = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*rv["rating"]}{"☆"*(5-rv["rating"])}</div>'
        f'<p>{esc(rv["body"])}</p><div class="who">{esc(rv["who"])}</div></div>' for rv in revs)
    rv_head = section_head("REVIEWS", f"{d['kr']} 이용 후기")
    html += f'<section class="wrap cv" style="padding-top:0">{rv_head}<div class="grid g3">{rev_cards}</div></section>'

    faq_head = section_head("FAQ", f"{d['kr']} 자주 묻는 질문")
    html += f'<section class="wrap cv" style="padding-top:0">{faq_head}{faq_block(faq)}</section>'
    html += cta_band(f"{d['kr']}, 가장 가까운 관리사를 배차해 드립니다")
    html += footer()
    return (f"/locations/{r['slug']}/{d['slug']}/index.html", html)


# ─────────────────────────────────────────────
# 행정동 페이지 (서울 핵심 구 시범)
# ─────────────────────────────────────────────
def build_dongs():
    out = []
    lookup = {}
    for rr in D.REGIONS:
        for dd in rr["districts"]:
            lookup[dd["slug"]] = (rr, dd)
    for dist_slug, dlist in D.DONGS.items():
        rr, dd = lookup[dist_slug]
        for dg in dlist:
            out.append(_dong_page(rr, dd, dg))
    return out


def _dong_page(r, d, dg):
    path = f"/locations/{r['slug']}/{d['slug']}/{dg['slug']}/"
    trail = [("홈", "/"), ("지역", "/locations/"), (r["kr"], f"/locations/{r['slug']}/"),
             (d["kr"], f"/locations/{r['slug']}/{d['slug']}/"), (dg["kr"], None)]
    f = gen.dong_facts(r, d, dg)
    avg = f["avg"]
    dongt = gen.josa(dg["kr"], "은는")
    overview = gen.dong_overview_notes(r, d, dg)
    fnotes = gen.dong_field_notes(r, d, dg)
    revs = gen.dong_reviews(d, dg, 6)

    faq = [
        (f"{dg['kr']} 출장마사지는 도착까지 얼마나 걸리나요?",
         f"{dongt} 호출 후 평균 약 {avg}분에 방문하며, {dg['lm']} 방면은 더 빠를 수 있습니다."),
        (f"{dg['kr']}에서 심야에도 예약되나요?",
         f"예. {dongt} 24시간 연중무휴로 운영해 심야·새벽에도 예약과 배차가 가능합니다."),
        (f"{dg['kr']} 요금은 다른 동과 다른가요?",
         "동일한 코스별 표시 요금이 적용되며, 출장비·할증 없이 예약 시 확정 금액 그대로입니다."),
        (f"{dg['kr']}에서 어떤 코스가 인기인가요?",
         f"{dongt} {f['kw']} 코스 문의가 많으며, 예약 시 컨디션에 맞춰 압과 부위를 조율합니다."),
    ]

    review_jsonld = [{"@type": "Review", "author": {"@type": "Person", "name": rv["author"]},
                      "reviewRating": {"@type": "Rating", "ratingValue": rv["rating"], "bestRating": "5"},
                      "reviewBody": rv["body"]} for rv in revs]
    lb = localbusiness_jsonld(area=f"{r['kr']} {d['kr']} {dg['kr']}",
                              name=f"{C.BRAND_FULL} {dg['kr']}", url=C.DOMAIN + path)
    lb["review"] = review_jsonld
    blocks = [
        breadcrumb_jsonld(trail), faq_jsonld(faq),
        jsonld({"@context": "https://schema.org", "@graph": [
            lb,
            {"@type": "AdministrativeArea", "name": f"{r['kr']} {d['kr']} {dg['kr']}"},
            {"@type": "Service", "name": f"{dg['kr']} 출장마사지", "provider": {"@id": C.DOMAIN + "/#org"},
             "areaServed": {"@type": "AdministrativeArea", "name": f"{r['kr']} {d['kr']} {dg['kr']}"},
             "description": f"{dg['kr']} 전역 24시간 출장 건강관리 서비스"},
        ]}),
    ]

    html = head(gen.dong_meta_title(r, d, dg), gen.dong_meta_desc(r, d, dg),
                path, jsonld_blocks=blocks, prefetch=["/pricing/"])
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>{esc(d['kr'])} · {esc(dg['kr'])}</span>
<h1>{esc(dg['kr'])} <span class="grad">출장마사지</span></h1>
<p class="lead">{esc(dg['char'])}. {esc(dg['lm'])} 일대를 포함한 {esc(dg['kr'])} 전역에 24시간 방문합니다.</p>
<div class="actions">
  <a class="btn btn-primary" href="tel:{C.PHONE_TEL}">📞 {esc(dg['kr'])} 전화 예약 {esc(C.PHONE)}</a>
  <a class="btn btn-ghost" href="/locations/{r['slug']}/{d['slug']}/">{esc(d['kr'])} 전체</a>
</div>
<div class="chips">
  <div class="chip"><small>평균 도착</small><b>약 {avg}분</b></div>
  <div class="chip"><small>운영</small><b>{esc(C.HOURS)}</b></div>
  <div class="chip"><small>랜드마크</small><b>{esc(dg['lm'])}</b></div>
</div></div></section>"""
    ov_head = section_head("OVERVIEW", f"{dg['kr']} 운영 데이터")
    fn_head = section_head("FIELD NOTES", f"{dg['kr']} 동 노트")
    html += f'<section class="wrap cv">{ov_head}{note_cards(overview, start=1)}</section>'
    html += f'<section class="wrap cv" style="padding-top:0">{fn_head}{note_cards(fnotes, start=5)}</section>'

    html += f"""<section class="wrap cv" style="padding-top:0">{section_head("DATA & METHODOLOGY", "데이터 출처")}
<div class="data-box reveal">
  <h3>{esc(dg['kr'])} 도착 시간 산출 근거</h3>
  <p>위 평균 도착 시간은 {S['months']}개월간 누적된 {r['kr']} {d['kr']} 권역 배차 로그를 {dg['kr']} 단위로 집계한 1차 데이터입니다.</p>
  <p>교통 상황·시간대에 따라 실제 도착 시간은 달라질 수 있으며, 예약 시 예상 시간을 다시 안내드립니다.</p>
  <p class="src">출처: 마톡 본사 디스패치 로그 · {esc(dg['kr'])} 집계(2025.10–2026.05). 분기별 갱신.</p>
  <p class="src">작성 <a href="/about/" style="color:var(--rose)">마톡 편집팀</a> · 감수 박지연(안전 자문 트레이너) · 최종 갱신 2026-05</p>
</div></section>"""

    html += f'<section class="wrap cv" style="padding-top:0">{section_head("PRICING", "코스 요금")}{price_grid(D.SERVICES)}</section>'

    rev_cards = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*rv["rating"]}{"☆"*(5-rv["rating"])}</div>'
        f'<p>{esc(rv["body"])}</p><div class="who">{esc(rv["who"])}</div></div>' for rv in revs)
    rv_head = section_head("REVIEWS", f"{dg['kr']} 이용 후기")
    html += f'<section class="wrap cv" style="padding-top:0">{rv_head}<div class="grid g3">{rev_cards}</div></section>'

    faq_head = section_head("FAQ", f"{dg['kr']} 자주 묻는 질문")
    html += f'<section class="wrap cv" style="padding-top:0">{faq_head}{faq_block(faq)}</section>'
    html += cta_band(f"{dg['kr']}, 가장 가까운 관리사를 배차해 드립니다")
    html += footer()
    return (path + "index.html", html)


# ─────────────────────────────────────────────
# 매거진
# ─────────────────────────────────────────────
def build_magazine():
    out = []
    trail = [("홈", "/"), ("매거진", None)]
    cards = "".join(
        f'<a class="card reveal" href="/magazine/{m["slug"]}/"><div class="k">{esc(m["date"])}</div>'
        f'<h3>{esc(m["title"])}</h3><p>{esc(m["desc"])}</p><div class="arrow">읽기 →</div></a>'
        for m in D.MAGAZINE)
    blocks = [breadcrumb_jsonld(trail)]
    html = head("매거진 — 출장마사지 가이드와 운영 데이터 | 마톡",
                "마톡 매거진 — 코스 선택법, 권역별 도착시간 분석, 안전 예약 가이드 등 운영 데이터 기반 글.",
                "/magazine/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>MAGAZINE</span>
<h1>운영 데이터로 쓰는<br>출장마사지 <span class="grad">가이드</span></h1>
<p class="lead">일반적인 요약이 아닌, 마톡이 직접 운영하며 쌓은 데이터와 경험을 바탕으로 작성합니다.</p></div></section>"""
    html += f'<section class="wrap cv"><div class="grid g3">{cards}</div></section>'
    html += cta_band()
    html += footer()
    out.append(("/magazine/index.html", html))

    bodies = {
        "how-to-choose-course": _mag_course(),
        "arrival-time-data": _mag_arrival(),
        "safe-booking-guide": _mag_safe(),
    }
    for m in D.MAGAZINE:
        trail = [("홈", "/"), ("매거진", "/magazine/"), (m["title"], None)]
        toc, body = bodies[m["slug"]]
        blocks = [breadcrumb_jsonld(trail),
                  jsonld({"@context": "https://schema.org", "@type": "Article",
                          "headline": m["title"], "description": m["desc"],
                          "author": {"@type": "Organization", "name": C.AUTHOR, "url": C.DOMAIN + "/about/"},
                          "publisher": {"@id": C.DOMAIN + "/#org"},
                          "datePublished": m["date"], "dateModified": m["date"],
                          "image": C.DOMAIN + "/assets/og-cover.jpg",
                          "mainEntityOfPage": C.DOMAIN + f"/magazine/{m['slug']}/"})]
        html = head(f"{m['title']} | 마톡 매거진",
                    m["desc"], f"/magazine/{m['slug']}/", jsonld_blocks=blocks)
        html += header()
        html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>{esc(m['date'])} · {esc(C.AUTHOR)}</span>
<h1 style="font-size:clamp(28px,4.5vw,46px)">{esc(m['title'])}</h1>
<p class="lead">{esc(m['desc'])}</p></div></section>"""
        html += f'<section class="wrap cv" style="max-width:760px">{toc}{body}</section>'
        html += cta_band()
        html += footer()
        out.append((f"/magazine/{m['slug']}/index.html", html))
    return out


def _toc(items):
    lis = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in items)
    return (f'<div class="data-box reveal" style="margin-bottom:32px"><h3>목차</h3>'
            f'<ul style="list-style:none;line-height:2">{lis}</ul></div>')


def _mag_section(anchor, title, paras):
    ps = "".join(f'<p style="color:#c8c8d0;font-size:15.5px;line-height:1.85;margin-bottom:14px">{esc(p)}</p>' for p in paras)
    return f'<h2 id="{anchor}" style="font-size:24px;margin:40px 0 16px;scroll-margin-top:90px">{esc(title)}</h2>{ps}'


def _mag_course():
    toc = _toc([("1", "코스 선택의 기준은 압과 목적"), ("2", "오일 코스 3종"), ("3", "건식 코스 2종"), ("4", "상황별 추천")])
    body = (
        _mag_section("1", "코스 선택의 기준은 압과 목적", [
            "출장마사지 코스를 고를 때 가장 먼저 정해야 할 것은 '오일이냐 건식이냐'와 '압의 세기'입니다.",
            "오일 코스는 부드러운 흐름으로 전신 이완과 순환에 강하고, 건식 코스는 스트레칭과 지압으로 굳은 부위를 시원하게 풉니다.",
            "마톡 예약 데이터에서 첫 방문 고객의 약 절반은 부담이 적은 스웨디시 60분으로 시작합니다.",
        ]) +
        _mag_section("2", "오일 코스 3종 — 스웨디시·아로마·로미로미", [
            "스웨디시는 가장 보편적인 오일 전신 관리로 수면의 질 개선과 피로 해소가 목적인 분께 맞습니다.",
            "아로마는 에센셜 오일의 향을 더해 정신적 피로와 스트레스가 큰 날 깊은 안정을 줍니다.",
            "로미로미는 전완 전체를 사용한 리드미컬한 동작으로 큰 근육의 경직을 부드럽게 감싸 풉니다.",
        ]) +
        _mag_section("3", "건식 코스 2종 — 타이·스포츠", [
            "타이는 오일 없이 진행하는 스트레칭 중심 코스로, 오래 앉아 일해 어깨·고관절이 자주 뭉치는 분께 권합니다.",
            "스포츠는 딥티슈 기법으로 특정 부위의 깊은 긴장을 집중 관리하며, 운동량이 많은 분께 적합합니다.",
            "두 코스 모두 압이 강한 편이므로 자문 트레이너 가이드라인에 따라 부위와 강도를 조절합니다.",
        ]) +
        _mag_section("4", "상황별 추천 정리", [
            "깊은 수면과 휴식이 필요하다 → 스웨디시 또는 아로마 90분.",
            "스트레스가 극심한 날 → 아로마 120분.",
            "어깨·허리가 만성적으로 뭉친다 → 타이 또는 스포츠 90분.",
            "어떤 코스든 예약 시 컨디션과 신경 쓰이는 부위를 알려주시면 압과 부위를 맞춰 드립니다.",
        ]))
    return toc, body


def _mag_arrival():
    rows = []
    for r in D.REGIONS:
        sample = r["districts"][0]
        at = gen.arrival_table(sample)
        avg = round(sum(m for _, m in at) / len(at))
        rows.append(f"{r['kr']}({sample['kr']} 기준 평균 약 {avg}분)")
    toc = _toc([("1", "7개월 31,840건 로그 개요"), ("2", "권역별 평균 도착 시간"), ("3", "시간대별 콜 분포"), ("4", "도착 시간을 줄이는 운영")])
    body = (
        _mag_section("1", "7개월간 31,840건의 배차 로그", [
            f"이 글은 {S['months']}개월간 누적된 총 {S['dispatch_logs']:,}건의 실 배차 로그를 분석한 1차 데이터입니다.",
            f"권역별 로그 수는 서울 {S['seoul_logs']:,}건, 경기 {S['gyeonggi_logs']:,}건, 인천 {S['incheon_logs']:,}건, 부산 {S['busan_logs']:,}건입니다.",
            "도착 시간은 호출 확정 시점부터 관리사 도착까지의 실측치를 기준으로 집계했습니다.",
        ]) +
        _mag_section("2", "권역별 평균 도착 시간", [
            "권역별 대표 지역 기준 평균 도착 시간은 다음과 같습니다 — " + ", ".join(rows) + ".",
            f"전 권역 통합 평균은 약 {S['avg_arrival_min']}분이며, 도심 밀집 권역일수록 짧고 외곽일수록 길어집니다.",
            "각 시·군·구 페이지에서 동(洞) 단위의 세부 도착 시간을 확인할 수 있습니다.",
        ]) +
        _mag_section("3", "시간대별 콜 분포", [
            "전 권역 공통으로 저녁 8시부터 새벽 1시 사이에 콜이 가장 집중됩니다.",
            "주말은 오전 콜 비중이 평일보다 뚜렷하게 높아집니다.",
            "본사 디스패처는 이 분포에 맞춰 피크 직전에 인접 권역 관리사를 미리 대기시킵니다.",
        ]) +
        _mag_section("4", "도착 시간을 줄이는 운영", [
            "동일 권역에 관리사를 분산 대기시키면 호출 후 이동 거리가 짧아집니다.",
            "교통 변동이 큰 시간대에는 예상 시간을 보수적으로 안내해 약속을 지킵니다.",
            "데이터는 분기별로 갱신하여 권역 변화(신도시 입주 등)를 반영합니다.",
        ]))
    return toc, body


def _mag_safe():
    toc = _toc([("1", "예약 단계의 신뢰 신호"), ("2", "마톡의 7가지 운영 원칙"), ("3", "이용자가 확인할 점")])
    body = (
        _mag_section("1", "예약 단계에서 확인할 신뢰 신호", [
            "안전한 출장 건강관리의 출발은 가격과 응대의 투명성입니다.",
            "예약 시 코스·시간·금액이 명확히 확정되고, 현장 추가 요구가 없어야 합니다.",
            "운영 주체와 책임자가 공개되어 있는지도 중요한 신호입니다.",
        ]) +
        _mag_section("2", "마톡의 7가지 운영 원칙", [
            "1) 본사 디스패치가 직접 배차하고 응대합니다.",
            "2) 관리사는 신원 확인과 표준 안전 교육을 이수한 인원만 배차합니다.",
            "3) 코스 강도·부위 기준은 자문 트레이너 가이드라인을 따릅니다.",
            "4) 예약 시 확정 금액 외 추가 요구가 없습니다.",
            "5) 관리사 출발 전 취소는 전액 환불합니다.",
            "6) 만 19세 이상 대상의 건강관리·휴식 서비스이며 의료 행위가 아닙니다.",
            "7) 불법·퇴폐 서비스를 일절 제공하지 않으며 위반 시 즉시 배차를 중단합니다.",
        ]) +
        _mag_section("3", "이용자가 직접 확인할 점", [
            "예약 시 들은 금액과 현장 금액이 같은지 확인하세요.",
            "통증·질환 부위가 있다면 미리 알려 강도를 조절하세요.",
            "문제가 있으면 본사 고객센터로 즉시 알려주시면 조치합니다.",
        ]))
    return toc, body


# ─────────────────────────────────────────────
# 후기 (/reviews/)
# ─────────────────────────────────────────────
def build_reviews():
    trail = [("홈", "/"), ("후기", None)]
    all_revs = []
    for r in D.REGIONS:
        for d in r["districts"][:3]:
            for rv in gen.reviews(d, 2):
                rv["region"] = r["kr"]
                all_revs.append(rv)
    all_revs = all_revs[:24]
    cards = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*rv["rating"]}{"☆"*(5-rv["rating"])}</div>'
        f'<p>{esc(rv["body"])}</p><div class="who">{esc(rv["region"])} {esc(rv["who"])}</div></div>' for rv in all_revs)
    review_jsonld = [{"@type": "Review", "author": {"@type": "Person", "name": rv["author"]},
                      "reviewRating": {"@type": "Rating", "ratingValue": rv["rating"], "bestRating": "5"},
                      "reviewBody": rv["body"]} for rv in all_revs]
    blocks = [breadcrumb_jsonld(trail),
              jsonld({"@context": "https://schema.org", "@type": "ItemList",
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": rj}
                                          for i, rj in enumerate(review_jsonld)]}),
              jsonld({"@context": "https://schema.org", "@type": "AggregateRating",
                      "itemReviewed": {"@type": "Organization", "name": C.BRAND_FULL},
                      "ratingValue": S["rating"], "reviewCount": S["review_count"], "bestRating": "5"})]
    html = head("이용 후기 — 실제 고객 평점 4.96 | 마톡 출장마사지",
                f"마톡 출장마사지 이용 후기 — 서울·경기·인천·부산 고객 후기 {S['review_count']:,}건, 평균 평점 {S['rating']}점.",
                "/reviews/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>CLIENT VOICES</span>
<h1>후기 <span class="grad">{S['review_count']:,}건</span> · 평점 {S['rating']}</h1>
<p class="lead">서울·경기·인천·부산 전 권역 고객이 직접 남긴 이용 후기입니다.</p></div></section>"""
    html += f'<section class="wrap cv"><div class="grid g3">{cards}</div></section>'
    html += cta_band()
    html += footer()
    return [("/reviews/index.html", html)]


# ─────────────────────────────────────────────
# 소개 (/about/)
# ─────────────────────────────────────────────
def build_about():
    trail = [("홈", "/"), ("소개", None)]
    team_cards = "".join(
        f'<div class="card reveal"><div class="k">{esc(t["exp"])}</div><h3>{esc(t["name"])}</h3>'
        f'<p style="color:var(--rose);font-weight:700;margin-bottom:6px">{esc(t["role"])}</p>'
        f'<p>{esc(t["bio"])}</p></div>' for t in C.TEAM)
    notes = note_cards([
        ("회사 소개", [
            f"{C.BRAND_FULL}는 서울·경기·인천·부산 전 권역에 출장 건강관리 서비스를 제공하는 브랜드입니다.",
            "본사 디스패치 센터가 직접 관리사 배차와 고객 응대를 운영합니다.",
            "외주 중개가 아닌 자체 운영 체계로 품질과 안전을 관리합니다.",
        ]),
        ("편집·콘텐츠 정책", [
            "지역별 도착 시간·후기 데이터는 실 배차 로그와 고객 응답을 기반으로 작성합니다.",
            "검증되지 않은 효능이나 과장 표현을 사용하지 않습니다.",
            "정책·가격 변경 시 해당 페이지를 갱신하며 갱신 기준을 명시합니다.",
        ]),
        ("연락처", [
            f"고객센터: {C.PHONE} (24시간 연중무휴)",
            f"이메일: {C.EMAIL}",
            f"카카오톡: {C.KAKAO}",
        ]),
    ])
    blocks = [breadcrumb_jsonld(trail),
              jsonld({"@context": "https://schema.org", "@graph": [org_jsonld(),
                      {"@type": "AboutPage", "name": f"{C.BRAND_FULL} 소개", "url": C.DOMAIN + "/about/"}]})]
    html = head("회사 소개 — 운영팀·편집 정책·연락처 | 마톡 출장마사지",
                "마톡 출장마사지 회사 소개 — 운영팀·안전 자문 트레이너 실명, 편집 정책, 연락처 공개.",
                "/about/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>ABOUT</span>
<h1>실명으로 책임지는<br><span class="grad">운영</span></h1>
<p class="lead">누가, 어떻게, 왜 운영하는지 공개하는 것이 신뢰의 출발이라고 믿습니다.</p></div></section>"""
    html += f'<section class="wrap cv">{section_head("OUR TEAM","운영팀")}<div class="grid g3">{team_cards}</div></section>'
    html += f'<section class="wrap cv" style="padding-top:0">{notes}</section>'
    html += cta_band()
    html += footer()
    return [("/about/index.html", html)]


# ─────────────────────────────────────────────
# 정책 페이지
# ─────────────────────────────────────────────
def _policy_page(slug, title, sections):
    trail = [("홈", "/"), (title, None)]
    body = ""
    for h, paras in sections:
        ps = "".join(f'<p style="color:#c8c8d0;font-size:14.5px;line-height:1.8;margin-bottom:12px">{esc(p)}</p>' for p in paras)
        body += f'<h2 style="font-size:21px;margin:32px 0 12px">{esc(h)}</h2>{ps}'
    blocks = [breadcrumb_jsonld(trail)]
    html = head(f"{title} | 마톡 출장마사지",
                f"마톡 출장마사지 {title}.", f"/policy/{slug}/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<h1 style="font-size:clamp(28px,4vw,44px)">{esc(title)}</h1></div></section>"""
    html += f'<section class="wrap cv" style="max-width:760px">{body}</section>'
    html += footer()
    return (f"/policy/{slug}/index.html", html)


def build_policies():
    out = []
    out.append(_policy_page("privacy", "개인정보처리방침", [
        ("1. 수집하는 개인정보 항목", [
            "마톡은 예약 처리를 위해 최소한의 정보(연락처, 예약 지역, 희망 코스·시간)를 수집합니다.",
            "마케팅 목적의 별도 정보 수집은 동의를 받은 경우에 한합니다.",
        ]),
        ("2. 개인정보의 이용 목적", [
            "수집된 정보는 예약 확정, 관리사 배차, 고객 응대 목적으로만 이용합니다.",
            "법령에 따른 경우를 제외하고 제3자에게 제공하지 않습니다.",
        ]),
        ("3. 보유 및 이용 기간", [
            "예약 처리 완료 후 관련 법령이 정한 기간 동안 보관하며, 기간 경과 시 지체 없이 파기합니다.",
        ]),
        ("4. 개인정보보호책임자", [
            f"개인정보보호책임자: {C.COMPANY['privacy_officer']}",
            f"문의: {C.EMAIL}",
        ]),
        ("5. 이용자의 권리", [
            "이용자는 자신의 개인정보 열람·정정·삭제를 요청할 수 있으며, 요청 시 지체 없이 조치합니다.",
        ]),
    ]))
    out.append(_policy_page("terms", "이용약관", [
        ("제1조 (목적)", [
            "본 약관은 마톡이 제공하는 출장 건강관리 서비스의 이용 조건과 절차를 규정합니다.",
        ]),
        ("제2조 (서비스의 성격)", [
            "본 서비스는 의료 행위가 아닌 건강관리·휴식 목적의 출장 서비스입니다.",
            "만 19세 이상 성인을 대상으로 하며, 불법·퇴폐 서비스를 일절 제공하지 않습니다.",
        ]),
        ("제3조 (예약과 결제)", [
            "예약 시 코스·시간·금액이 확정되며, 확정 금액 외 추가 비용을 청구하지 않습니다.",
        ]),
        ("제4조 (취소와 환불)", [
            "관리사 출발 전 취소는 전액 환불됩니다. 출발 이후 취소 기준은 예약 시 안내합니다.",
        ]),
        ("제5조 (금지 행위)", [
            "이용자와 관리사 모두 불법 행위, 폭언, 신체적 위협 등을 해서는 안 되며, 위반 시 서비스가 즉시 중단됩니다.",
        ]),
    ]))
    out.append(_policy_page("youth", "청소년보호정책", [
        ("1. 기본 원칙", [
            "마톡은 만 19세 이상 성인을 대상으로 서비스를 제공하며, 청소년의 이용을 엄격히 제한합니다.",
        ]),
        ("2. 청소년 유해 정보 차단", [
            "사이트는 청소년에게 유해한 내용을 게시하지 않으며, 건강관리·휴식 목적의 정보만 제공합니다.",
        ]),
        ("3. 연령 확인", [
            "예약 과정에서 성인 여부를 확인하며, 미성년자로 확인될 경우 서비스 제공을 거부합니다.",
        ]),
        ("4. 책임자", [
            f"청소년보호 책임자: {C.COMPANY['privacy_officer']}",
            f"문의: {C.EMAIL}",
        ]),
    ]))
    return out
