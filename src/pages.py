# -*- coding: utf-8 -*-
"""페이지 빌더. 각 함수는 (경로, HTML) 리스트를 반환하고 build.py가 기록합니다."""
from . import config as C
from . import data as D
from . import gen
from .components import (
    head, header, footer, esc, jsonld, note_cards, price_grid, faq_block, faq_jsonld,
    breadcrumb, breadcrumb_jsonld, cta_band, section_head, org_jsonld, website_jsonld,
    localbusiness_jsonld,
)

S = C.STATS


# ─────────────────────────────────────────────
# 메인 (/)
# ─────────────────────────────────────────────
def build_index():
    svc_cards = "".join(
        f'<a class="card reveal" href="/service/{s["slug"]}/"><div class="k">{esc(s["kicker"])}</div>'
        f'<h3>{esc(s["name"])}</h3><p>{esc(s["tagline"])}</p><div class="arrow">자세히 →</div></a>'
        for s in D.SERVICES)
    region_cards = "".join(
        f'<a class="card reveal" href="/locations/{r["slug"]}/"><div class="k">{esc(r["en"])}</div>'
        f'<h3>{esc(r["kr"])} 출장마사지</h3><p>{esc(r["label"])} 전 권역 24시간 배차</p><div class="arrow">지역 보기 →</div></a>'
        for r in D.REGIONS)
    steps = "".join(
        f'<div class="step reveal"><div class="n">{i:02d}</div><h3>{t}</h3><p>{p}</p></div>'
        for i, (t, p) in enumerate([
            ("문의", "전화 또는 카카오톡으로 지역·코스·시간을 알려주세요."),
            ("배차", "본사 디스패처가 가까운 검증 관리사를 매칭합니다."),
            ("도착", f"평균 약 {S['avg_arrival_min']}분 내 예약 장소로 방문합니다."),
            ("관리", "원하는 코스로 편안한 휴식을 즐기세요."),
        ], 1))
    voices = "".join(
        f'<div class="review reveal"><div class="stars">★★★★★</div><p>{esc(b)}</p><div class="who">{esc(w)}</div></div>'
        for b, w in [
            ("야근 후 집에서 바로 받을 수 있어 정말 편했어요. 도착도 빠르고 압 조절이 좋았습니다.", "서울 강남 · 김O준"),
            ("가격을 예약 때 들은 그대로만 받아서 신뢰가 갔어요. 추가 요구가 전혀 없었습니다.", "경기 분당 · 이O연"),
            ("심야에도 예약이 되는 게 가장 좋아요. 응대도 정중하고 마무리도 깔끔했습니다.", "부산 해운대 · 박O현"),
        ])
    team_cards = "".join(
        f'<div class="card reveal"><div class="k">{esc(t["exp"])}</div><h3>{esc(t["name"])}</h3>'
        f'<p style="color:var(--rose);font-weight:700;margin-bottom:6px">{esc(t["role"])}</p>'
        f'<p>{esc(t["bio"])}</p></div>'
        for t in C.TEAM)
    about_notes = note_cards([
        ("Who — 누가 운영하나요", [
            f"{C.BRAND_FULL}는 본사 디스패치 센터가 직접 관리사 배차와 응대를 운영합니다.",
            "운영팀장과 안전 자문 트레이너가 실명으로 책임 영역을 공개합니다.",
            "외주 중개가 아닌 자체 운영 체계로 품질을 관리합니다.",
        ]),
        ("How — 어떻게 운영하나요", [
            f"{S['months']}개월간 누적된 {S['dispatch_logs']:,}건의 배차 로그를 분석해 권역별 대기 위치를 최적화합니다.",
            "피크 시간대 콜 분포에 맞춰 인접 권역 관리사를 사전 대기시켜 도착 시간을 단축합니다.",
            "모든 코스는 자문 트레이너 가이드라인에 따라 강도·부위 기준이 표준화되어 있습니다.",
        ]),
        ("Why — 왜 만들었나요", [
            "출장 건강관리 시장의 불투명한 가격과 응대 문제를 개선하기 위해 시작했습니다.",
            "예약 시 확정된 금액 외 추가 요구가 없는 정직한 운영을 원칙으로 합니다.",
            "고객이 안심하고 휴식할 수 있는 표준을 만드는 것이 목표입니다.",
        ]),
        ("안전 — 어떻게 지키나요", [
            "관리사는 신원 확인과 표준 안전 교육을 이수한 인원만 배차됩니다.",
            "불법·퇴폐 서비스를 일절 제공하지 않으며 위반 시 즉시 배차를 중단합니다.",
            "통증·질환 부위는 사전 고지 시 강도를 낮추거나 피해 진행합니다.",
        ]),
        ("편집 정책 — 콘텐츠 기준", [
            "지역별 도착 시간·후기 데이터는 실 배차 로그와 고객 응답을 기반으로 작성합니다.",
            "검증되지 않은 효능·과장 표현을 사용하지 않습니다.",
            "정책·가격 변경 시 해당 페이지를 갱신하고 갱신 기준을 명시합니다.",
        ]),
    ], start=1)

    faq = D.FAQ_MAIN

    blocks = [jsonld({"@context": "https://schema.org", "@graph": [
        org_jsonld(), website_jsonld(),
        localbusiness_jsonld(),
        {"@type": "Article", "headline": f"{C.BRAND_FULL} — 서울·경기·인천·부산 24시간 출장 건강관리",
         "author": [{"@type": "Person", "name": t["name"], "jobTitle": t["role"]} for t in C.TEAM],
         "reviewedBy": {"@type": "Person", "name": "박지연", "jobTitle": "안전 자문 트레이너"},
         "publisher": {"@id": C.DOMAIN + "/#org"}, "datePublished": "2026-01-10", "dateModified": "2026-05-20"},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]})]

    html = head(
        f"{C.BRAND_FULL} | 서울·경기·인천·부산 24시간 방문 건강관리",
        f"{C.BRAND} 출장마사지 — 서울·경기·인천·부산 전 권역 24시간 배차. 평균 {S['avg_arrival_min']}분 도착, 확정 금액 그대로.",
        "/", jsonld_blocks=blocks, prefetch=["/pricing/", "/locations/"],
        extra_meta=(
            '<meta name="naver-site-verification" content="30363baba6fc86ad2bb4e417ae432a7accb60d1e">'
            '<meta name="google-site-verification" content="eBesLq6H_j5MQTaHNfknYR_4H1-7UuHkG2ohfTSRX6o">'
        ),
    )
    html += header()
    html += f"""<section class="hero"><div class="hero-inner">
<div class="hero-copy">
  <span class="eyebrow"><span class="pulse"></span>SEOUL · GYEONGGI · INCHEON · BUSAN</span>
  <h1>당신의 공간으로<br>도착하는 <span class="grad">최상의</span><br><span class="serif">휴식 한 시간.</span></h1>
  <p class="lead">{esc(C.BRAND_FULL)}는 본사 디스패치 기반으로 검증된 관리사를 24시간 배차합니다. 예약 시 확정된 금액 그대로, 추가 요구 없이.</p>
  <div class="actions">
    <a class="btn btn-primary" href="tel:{C.PHONE_TEL}">지금 예약하기 →</a>
    <a class="btn btn-ghost" href="/service/">코스 둘러보기</a>
  </div>
  <div class="trust"><span class="stars">★★★★★</span><span>{S['rating']} · 후기 {S['review_count']:,}건</span><span>· {esc(C.HOURS)}</span><span>· 평균 {S['avg_arrival_min']}분 도착</span></div>
</div>
<div class="hero-visual">
  <div class="floating fl-1"><span><span class="fl-label">LIVE</span><b>방금 강남 예약</b></span></div>
  <div class="glass">
    <h3><small>시그니처 코스</small>아로마 딥 릴렉스 90분</h3>
    <div class="book-row"><span>관리사</span><span>검증 · 한국/태국 외</span></div>
    <div class="book-row"><span>예상 도착</span><span>약 {S['avg_arrival_min']}분</span></div>
    <div class="book-row"><span>금액</span><span>예약 시 확정</span></div>
    <a class="bk" href="tel:{C.PHONE_TEL}">예약 →</a>
  </div>
  <div class="floating fl-2"><span><span class="fl-label">RATING</span><b>★ {S['rating']}</b></span></div>
</div>
</div></section>"""

    marquee_items = ["서울 25개 자치구", "경기 31개 시·군", "인천 10개 군·구", "부산 16개 군·구",
                     "24시간 연중무휴", f"평균 {S['avg_arrival_min']}분 도착", "본사 디스패치 운영", "확정 금액 그대로"]
    track = "".join(f"<span>{esc(x)}</span>" for x in marquee_items * 2)
    html += f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{track}</div></div>'

    html += f"""<section class="wrap cv" id="services">{section_head('SIGNATURE SERVICES','다섯 가지 시그니처 코스','컨디션과 목적에 맞춰 코스와 압을 함께 조율해 드립니다.')}
<div class="grid g4">{svc_cards}</div></section>"""

    html += f"""<section class="wrap cv" id="region" style="padding-top:0">{section_head('SERVICE AREA','서울·경기·인천·부산 전 권역','광역 허브에서 원하는 시·군·구를 선택하세요.')}
<div class="grid g4">{region_cards}</div></section>"""

    html += f"""<section class="wrap cv" id="process" style="padding-top:0">{section_head('HOW IT WORKS','예약은 네 단계로 끝납니다')}
<div class="steps">{steps}</div></section>"""

    html += f"""<section class="wrap cv" id="reviews" style="padding-top:0">{section_head('CLIENT VOICES','고객이 직접 남긴 후기')}
<div class="grid g3">{voices}</div>
<p style="margin-top:20px"><a class="arrow" href="/reviews/" style="color:var(--rose);font-weight:700">전체 후기 보기 →</a></p></section>"""

    html += f"""<section class="wrap cv" id="about" style="padding-top:0">{section_head('WHO · HOW · WHY','마톡을 운영하는 사람들','실명과 책임 영역을 공개하는 것이 신뢰의 출발이라고 믿습니다.')}
<div class="grid g3" style="margin-bottom:32px">{team_cards}</div>
{about_notes}
<div class="data-box reveal" style="margin-top:24px">
  <h3>Data &amp; Methodology</h3>
  <p>본 사이트의 도착 시간·콜 분포 데이터는 {S['months']}개월간 누적된 총 {S['dispatch_logs']:,}건의 배차 로그를 기반으로 합니다(서울 {S['seoul_logs']:,} · 경기 {S['gyeonggi_logs']:,} · 인천 {S['incheon_logs']:,} · 부산 {S['busan_logs']:,}).</p>
  <p>후기 평점은 실제 이용 고객의 응답 {S['review_count']:,}건을 집계한 값이며, 평균 평점은 {S['rating']}점입니다.</p>
  <p class="src">출처: 마톡 본사 디스패치 로그(2025.10–2026.05) · 고객 만족도 응답. 데이터는 분기별로 갱신합니다.</p>
</div></section>"""

    html += f"""<section class="wrap cv" id="faq" style="padding-top:0">{section_head('FAQ','자주 묻는 질문')}{faq_block(faq)}</section>"""
    html += cta_band()
    html += footer()
    return [("/index.html", html)]


# ─────────────────────────────────────────────
# 서비스
# ─────────────────────────────────────────────
def build_services():
    out = []
    # hub
    cards = "".join(
        f'<a class="card reveal" href="/service/{s["slug"]}/"><div class="k">{esc(s["kicker"])}</div>'
        f'<h3>{esc(s["name"])}</h3><p>{esc(s["summary"])}</p><div class="arrow">자세히 →</div></a>'
        for s in D.SERVICES)
    trail = [("홈", "/"), ("서비스", None)]
    blocks = [breadcrumb_jsonld(trail), jsonld({"@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [{"@type": "ListItem", "position": i, "name": s["name"],
                             "url": C.DOMAIN + f"/service/{s['slug']}/"} for i, s in enumerate(D.SERVICES, 1)]})]
    html = head("출장마사지 코스 안내 — 스웨디시·아로마·타이·로미로미·스포츠 | 마톡",
                "마톡 5종 출장마사지 코스 안내 — 스웨디시·아로마·타이·로미로미·스포츠의 특징과 시간별 요금.",
                "/service/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact">{''}
<div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>SIGNATURE SERVICES</span>
<h1>다섯 가지 코스,<br>당신의 컨디션에 맞춰</h1>
<p class="lead">오일 코스부터 건식 스트레칭, 딥티슈 회복까지. 목적에 맞는 코스를 선택하고 예약 시 압과 부위를 조율하세요.</p></div></section>"""
    html += f'<section class="wrap cv"><div class="grid g3">{cards}</div></section>'
    html += f'<section class="wrap cv" style="padding-top:0">{section_head("PRICING","전체 코스 요금")}{price_grid(D.SERVICES)}</section>'
    html += cta_band()
    html += footer()
    out.append(("/service/index.html", html))

    # each service
    for s in D.SERVICES:
        trail = [("홈", "/"), ("서비스", "/service/"), (s["name"], None)]
        ther = next((t for t in D.THERAPISTS if t["slug"] in ("thai", "korean")), D.THERAPISTS[0])
        overview = note_cards([
            (f"{s['name']} 코스란?", [s["summary"]] + s["detail"]),
            ("이런 분께 권합니다", [
                "코스의 강도와 목적을 미리 알고 선택하시면 만족도가 높습니다.",
                s["detail"][1],
                "예약 시 평소 컨디션과 신경 쓰이는 부위를 알려주시면 맞춤 조율이 가능합니다.",
            ]),
        ], start=1)
        deep = note_cards([
            ("진행 방식", [
                "예약하신 장소(자택·숙소 등)로 검증된 관리사가 방문해 진행합니다.",
                "코스 시작 전 컨디션을 확인하고 압과 부위를 함께 정합니다.",
                "마무리까지 정갈하게 진행하며, 추가 비용 요구는 없습니다.",
            ]),
            ("안전 기준", [
                "강도·부위 기준은 안전 자문 트레이너 가이드라인을 따릅니다.",
                "통증·질환 부위는 사전 고지 시 피하거나 강도를 낮춥니다.",
                "만 19세 이상 대상의 건강관리·휴식 서비스이며 의료 행위가 아닙니다.",
            ]),
        ], start=3)
        faq = [
            (f"{s['name']}는 어떤 분께 맞나요?", s["detail"][1]),
            (f"{s['name']} 코스 시간은 어떻게 되나요?",
             "60분·90분·120분 중 선택할 수 있으며, 깊은 휴식이 필요하면 90분 이상을 권합니다."),
            ("압 조절이 가능한가요?", "예. 코스 시작 전과 진행 중 모두 압과 부위를 조율할 수 있습니다."),
            ("출장 지역은 어디까지 되나요?", "서울·경기·인천·부산 전 권역에 24시간 배차합니다."),
        ]
        blocks = [
            breadcrumb_jsonld(trail), faq_jsonld(faq),
            jsonld({"@context": "https://schema.org", "@type": "Service",
                    "name": f"{s['name']} 출장마사지", "serviceType": s["name"],
                    "provider": {"@id": C.DOMAIN + "/#org"},
                    "areaServed": "서울·경기·인천·부산", "description": s["summary"],
                    "offers": [{"@type": "Offer", "name": f"{s['name']} {t}", "price": p.replace(",", "").replace("원", ""),
                                "priceCurrency": "KRW"} for t, p in s["prices"]]}),
        ]
        html = head(f"{s['name']} 출장마사지 — 코스 특징·추천·요금 | 마톡",
                    f"{s['name']} 출장마사지 — 60·90·120분 요금과 추천 대상, 안전 기준 안내. 수도권·부산 24시간 배차.",
                    f"/service/{s['slug']}/", jsonld_blocks=blocks, prefetch=["/pricing/"])
        html += header()
        html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>{esc(s['kicker'])}</span>
<h1>{esc(s['name'])} <span class="grad">출장마사지</span></h1>
<p class="lead">{esc(s['tagline'])}</p>
<div class="chips">
  <div class="chip"><small>코스 유형</small><b>{esc(s['kicker'])}</b></div>
  <div class="chip"><small>시간</small><b>60·90·120분</b></div>
  <div class="chip"><small>출장 지역</small><b>수도권·부산</b></div>
</div></div></section>"""
        html += f'<section class="wrap cv">{section_head("OVERVIEW","코스 개요")}{overview}</section>'
        html += f'<section class="wrap cv" style="padding-top:0">{section_head("DEEP DIVE","진행과 안전")}{deep}</section>'
        price_title = section_head("PRICING", f"{s['name']} 요금")
        html += f'<section class="wrap cv" style="padding-top:0">{price_title}{price_grid([s])}</section>'
        html += f'<section class="wrap cv" style="padding-top:0">{section_head("FAQ","자주 묻는 질문")}{faq_block(faq)}</section>'
        html += cta_band()
        html += footer()
        out.append((f"/service/{s['slug']}/index.html", html))
    return out


# ─────────────────────────────────────────────
# 관리사
# ─────────────────────────────────────────────
def build_therapists():
    out = []
    cards = "".join(
        f'<a class="card reveal" href="/therapists/{t["slug"]}/"><div class="k">{esc(t["flag"])}</div>'
        f'<h3>{esc(t["name"])}인 관리사</h3><p>{esc(t["desc"])}</p><div class="arrow">자세히 →</div></a>'
        for t in D.THERAPISTS)
    trail = [("홈", "/"), ("관리사", None)]
    blocks = [breadcrumb_jsonld(trail)]
    html = head("관리사 안내 — 국적별 강점과 매칭 기준 | 마톡 출장마사지",
                "마톡 출장마사지 관리사 안내 — 한국·중국·태국·베트남·러시아·일본 국적별 강점과 코스 매칭 기준.",
                "/therapists/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>THERAPISTS</span>
<h1>검증된 관리사,<br>코스에 맞춰 매칭</h1>
<p class="lead">국적별 강점이 다릅니다. 원하는 코스와 압을 알려주시면 가장 적합한 관리사를 배차해 드립니다.</p></div></section>"""
    html += f'<section class="wrap cv"><div class="grid g3">{cards}</div></section>'
    html += cta_band()
    html += footer()
    out.append(("/therapists/index.html", html))

    for t in D.THERAPISTS:
        trail = [("홈", "/"), ("관리사", "/therapists/"), (t["name"] + "인", None)]
        notes = note_cards([
            (f"{t['name']}인 관리사의 강점", [t["desc"]] + t["detail"]),
            ("매칭 기준", [
                "예약 시 희망 국적을 말씀하시면 가능 여부를 확인해 우선 배차합니다.",
                "시간대·권역에 따라 가능 인원이 다를 수 있어 사전 문의를 권장합니다.",
                "요청 사항은 디스패처가 관리사에게 사전 전달합니다.",
            ]),
            ("공통 안전 기준", [
                "모든 관리사는 신원 확인과 표준 안전 교육을 이수한 인원만 배차됩니다.",
                "코스 강도·부위 기준은 자문 트레이너 가이드라인을 따릅니다.",
                "불법·퇴폐 서비스를 일절 제공하지 않습니다.",
            ]),
        ])
        faq = [
            (f"{t['name']}인 관리사를 꼭 지정할 수 있나요?",
             "예약 시 희망을 말씀하시면 우선 배차하나, 시간대·권역에 따라 가능 인원이 제한될 수 있습니다."),
            ("의사소통은 괜찮나요?", t["detail"][-1] if "한국어" in t["detail"][-1] else "기본 응대가 가능하며, 세부 요청은 디스패처가 사전 전달합니다."),
            ("어떤 코스와 잘 맞나요?", t["detail"][0]),
        ]
        blocks = [breadcrumb_jsonld(trail), faq_jsonld(faq)]
        html = head(f"{t['name']}인 관리사 안내 — 강점·매칭 | 마톡 출장마사지",
                    f"{t['name']}인 관리사 안내. {t['desc']} 코스별 매칭 기준을 확인하세요.",
                    f"/therapists/{t['slug']}/", jsonld_blocks=blocks)
        html += header()
        html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>{esc(t['flag'])} THERAPIST</span>
<h1>{esc(t['name'])}인 <span class="grad">관리사</span></h1>
<p class="lead">{esc(t['desc'])}</p></div></section>"""
        html += f'<section class="wrap cv">{section_head("OVERVIEW","강점과 매칭")}{notes}</section>'
        html += f'<section class="wrap cv" style="padding-top:0">{section_head("FAQ","자주 묻는 질문")}{faq_block(faq)}</section>'
        html += cta_band()
        html += footer()
        out.append((f"/therapists/{t['slug']}/index.html", html))
    return out


# ─────────────────────────────────────────────
# 요금
# ─────────────────────────────────────────────
def build_pricing():
    trail = [("홈", "/"), ("요금", None)]
    notes = note_cards([
        ("정직한 가격 원칙", [
            "예약 시 코스와 시간을 확정하면 그 금액 외 추가 요구가 일절 없습니다.",
            "심야·주말이라고 임의로 금액을 올리지 않습니다.",
            "현장에서 별도 비용을 요구받으시면 즉시 본사로 알려주세요.",
        ]),
        ("결제와 환불", [
            "결제 방식은 예약 단계에서 안내드립니다.",
            "관리사 출발 전 취소는 전액 환불됩니다.",
            "출발 이후 취소 기준은 예약 시 명확히 고지합니다.",
        ]),
    ])
    faq = [
        ("표시된 금액 외에 추가 비용이 있나요?", "없습니다. 예약 시 확정된 금액이 전부입니다."),
        ("심야에는 요금이 더 비싼가요?", "코스별 표시 요금이 동일하게 적용됩니다."),
        ("출장비가 따로 있나요?", "주요 권역은 출장비 없이 표시 요금으로 진행합니다. 원거리 권역은 예약 시 안내드립니다."),
        ("환불은 어떻게 되나요?", "관리사 출발 전에는 전액 환불됩니다."),
    ]
    blocks = [breadcrumb_jsonld(trail), faq_jsonld(faq),
              jsonld({"@context": "https://schema.org", "@type": "OfferCatalog", "name": "마톡 코스 요금",
                      "itemListElement": [{"@type": "Offer", "name": f"{s['name']} {t}",
                                           "price": p.replace(",", "").replace("원", ""), "priceCurrency": "KRW"}
                                          for s in D.SERVICES for t, p in s["prices"]]})]
    html = head("요금 안내 — 코스별 60·90·120분 가격 | 마톡 출장마사지",
                "마톡 출장마사지 요금 — 5종 코스 60·90·120분 가격. 확정 금액 그대로, 추가 비용 없음.",
                "/pricing/", jsonld_blocks=blocks)
    html += header()
    html += f"""<section class="hero hero-compact"><div style="max-width:1240px;margin:0 auto;padding:0 24px">{breadcrumb(trail)}
<span class="eyebrow"><span class="pulse"></span>PRICING</span>
<h1>투명한 <span class="grad">요금</span> 안내</h1>
<p class="lead">예약 시 확정된 금액 그대로. 심야·주말 할증이나 현장 추가 요구가 없습니다.</p></div></section>"""
    html += f'<section class="wrap cv">{section_head("ALL COURSES","전체 코스 요금")}{price_grid(D.SERVICES)}</section>'
    html += f'<section class="wrap cv" style="padding-top:0">{section_head("POLICY","결제·환불 원칙")}{notes}</section>'
    html += f'<section class="wrap cv" style="padding-top:0">{section_head("FAQ","자주 묻는 질문")}{faq_block(faq)}</section>'
    html += cta_band()
    html += footer()
    return [("/pricing/index.html", html)]
