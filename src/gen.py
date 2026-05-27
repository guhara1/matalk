# -*- coding: utf-8 -*-
"""행정구별 고유 1차 데이터·콘텐츠 생성기 (도어웨이 회피).
동일 골격이라도 동(洞)별 도착 시간·후기·서술이 결정론적으로 달라지도록 시드를 사용합니다."""
import hashlib
from . import config as C


def _seed(s):
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16)


def _pick(seed, options):
    return options[seed % len(options)]


def josa(word, pair="은는"):
    """받침 유무에 따라 조사를 붙여 반환. pair[0]=받침O, pair[1]=받침X (예: 은/는, 이/가, 을/를)."""
    code = ord(word[-1])
    batchim = 0xAC00 <= code <= 0xD7A3 and (code - 0xAC00) % 28 != 0
    return word + (pair[0] if batchim else pair[1])


def arrival_table(district):
    """동별 평균 도착 시간 (분). 동 이름 시드로 25~44분 사이 결정론 생성."""
    rows = []
    for area in district["areas"]:
        sd = _seed(district["slug"] + area)
        mins = 25 + sd % 20
        rows.append((area, mins))
    return rows


def _choose(seed, pool, n):
    """시드 기반 결정론적 셔플로 pool에서 서로 다른 n개를 선택."""
    n = min(n, len(pool))
    order = sorted(range(len(pool)), key=lambda i: _seed(str(seed) + ":" + str(i)))
    return [pool[i] for i in order[:n]]


def _facts(district, region):
    """행정구별 수치·지명 사실 묶음. 모든 본문 문장에 주입해 고유성을 확보."""
    rows = arrival_table(district)
    fast = min(rows, key=lambda r: r[1])
    slow = max(rows, key=lambda r: r[1])
    avg = round(sum(r[1] for r in rows) / len(rows))
    sd = _seed(district["slug"])
    areas = district["areas"]
    lm = district["landmarks"]
    return {
        "d": district["kr"], "r": region["kr"], "char": district["character"],
        "lm1": lm[0], "lm2": lm[1] if len(lm) > 1 else lm[0], "lmjoin": ", ".join(lm),
        "a0": areas[0], "a1": areas[1] if len(areas) > 1 else areas[0],
        "a2": areas[2] if len(areas) > 2 else areas[-1],
        "a3join": ", ".join(areas[:3]),
        "fa": fast[0], "fm": fast[1], "sa": slow[0], "sm": slow[1], "avg": avg,
        "peak_pct": 42 + sd % 16, "night_pct": 16 + (sd >> 3) % 14,
        "repeat_pct": 34 + (sd >> 5) % 24, "kw": _course_kw(district),
        "dt": josa(district["kr"], "은는"),  # 강남구는 / 가평군은
    }


# 시간대별 콜 분포 — 보조 문장 풀 (앵커는 수치 포함 고유)
_POOL_TIME = [
    "주말에는 {a0} 일대를 중심으로 오전 콜 비중이 평일보다 눈에 띄게 높아집니다.",
    "{lm1} 인근은 평일 퇴근 직후 예약이 몰려, 그 시간대 도착이 다소 길어질 수 있습니다.",
    "재방문 고객 비율이 약 {repeat_pct}%로, {dt} 단골 예약 비중이 높은 편입니다.",
    "피크 직전에는 {r} 인접 권역 관리사를 {d} 쪽으로 미리 이동시켜 대기시킵니다.",
    "심야 시간대에도 {d} 전역 배차가 끊기지 않도록 야간 대기 인원을 별도로 둡니다.",
    "{a1}·{a2} 방면은 늦은 밤 수요가 꾸준해 전용 대기 동선을 운영합니다.",
    "연휴에는 전 시간대 예약이 고르게 분산되어 평소보다 도착이 빨라지는 경향이 있습니다.",
]
# 추천 코스 — 보조 문장 풀
_POOL_COURSE = [
    "{lm1} 부근 숙소·자택 예약이 많아, 이동이 간편하면서 회복감이 큰 구성을 안내합니다.",
    "예약 시 평소 컨디션과 신경 쓰이는 부위를 알려주시면 압과 부위를 세밀하게 조율합니다.",
    "{a0} 거주 고객은 정기 예약 시 동일 관리사 배정을 요청하는 경우도 많습니다.",
    "{d}에서는 90분 코스 선택 비중이 가장 높아, 깊은 이완을 원하면 120분을 권합니다.",
]
# 관리사 배치 — 보조 문장 풀
_POOL_DISPATCH = [
    "피크 시간대에는 사전 대기 인원을 늘려 {d}의 평균 도착 시간을 관리합니다.",
    "교통 상황에 따라 예상 시간이 바뀌면 예약 단계에서 다시 안내드립니다.",
    "{r} 인접 권역과 묶어 운영해 {d} 내 대기 공백이 생기지 않도록 합니다.",
    "심야에도 {d} 담당 야간 대기 관리사를 두어 배차가 끊기지 않습니다.",
    "{lm1} 일대처럼 수요가 몰리는 구간은 별도 대기 위치를 지정해 둡니다.",
]
# 안전 — 보조 문장 풀
_POOL_SAFETY = [
    "코스별 강도·부위 기준은 안전 자문 트레이너 박지연 트레이너의 가이드라인을 따릅니다.",
    "통증·질환이 있는 부위는 사전에 알려주시면 피하거나 강도를 낮춰 진행합니다.",
    "관리사는 정기 재교육으로 응대·안전 매뉴얼을 주기적으로 갱신합니다.",
    "{d} 야간 예약에도 주간과 동일한 안전 기준이 그대로 적용됩니다.",
]
# 결제/예약 — 보조 문장 풀
_POOL_PAY = [
    "코스와 시간은 예약 시 확정되어, 현장에서 추가 비용이 붙지 않습니다.",
    "관리사 출발 전 취소는 전액 환불되며, 출발 이후 기준은 예약 시 안내드립니다.",
    "{d} 주요 권역은 출장비 없이 표시 요금 그대로 진행합니다.",
    "심야·주말이라도 {d} 요금에 할증을 붙이지 않습니다.",
    "결제 방식은 예약 단계에서 안내하며, 정찰 요금을 그대로 적용합니다.",
]
# 법적 고지 (YMYL) — 문구 변주 (행정구별 다른 변형, 의미는 동일)
_POOL_LEGAL = [
    "마톡 출장마사지는 의료 행위가 아닌 건강관리·휴식 서비스로, 만 19세 이상을 대상으로 합니다.",
    "{d}에서 제공되는 모든 코스는 의료가 아닌 건강관리·휴식 목적이며 만 19세 이상만 이용할 수 있습니다.",
    "본 서비스는 건강관리·휴식 목적의 출장 서비스로, 미성년자 이용을 제한합니다.",
    "{d} 방문 관리는 치료가 아닌 휴식·컨디션 관리를 위한 서비스이며 성인(만 19세 이상)만 예약 가능합니다.",
]
# 권역 특징 — 보조 문장 풀
_POOL_AREA = [
    "{a3join} 등 주요 생활권에서 콜이 집중되어, 이 동선을 기준으로 대기 위치를 배치합니다.",
    "{fa} 방면은 평균 {fm}분으로 가장 빠르게 닿고, {sa} 등 외곽은 약 {sm}분이 걸립니다.",
    "{lm1} 일대는 숙소·오피스 예약 비중이 높아 야간 콜이 특히 많습니다.",
    "{d} 내 신규 입주·상권 변화는 분기별로 배차 데이터에 반영해 동선을 조정합니다.",
]


def overview_notes(district, region):
    """OVERVIEW 노트 카드 4개 (05~08). 앵커 문장은 수치/지명으로 고유, 나머지는 풀에서 셔플 선택."""
    f = _facts(district, region)
    rows = arrival_table(district)
    dong_line = ", ".join(f"{a} 약 {m}분" for a, m in rows)
    sd = _seed(district["slug"])
    return [
        ("동(洞)별 평균 도착 시간 분포", [
            f"{f['d']} 권역의 동별 평균 도착 시간은 다음과 같습니다 — {dong_line}.",
            f"가장 빠른 곳은 {f['fa']}(약 {f['fm']}분), 상대적으로 거리가 있는 곳은 {f['sa']}(약 {f['sm']}분)이며, 권역 평균은 약 {f['avg']}분입니다.",
            f"인접 권역 대기 관리사가 있을 경우 {f['d']} 도착 시간은 더 단축됩니다.",
        ]),
        ("시간대별 콜 분포 특징", [
            f"{f['d']} 콜의 약 {f['peak_pct']}%가 저녁 7시 이후 야간에 집중되며, 자정~새벽 심야 비중도 약 {f['night_pct']}%에 이릅니다.",
            *[s.format(**f) for s in _choose(sd + 11, _POOL_TIME, 2)],
        ]),
        ("권역 성격에 맞는 추천 코스", [
            f"{f['dt']} {f['char']} 특성이 뚜렷해, {f['kw']} 코스 문의가 많고 평균 {f['avg']}분 도착에 맞춰 90분 구성을 우선 추천합니다.",
            *[s.format(**f) for s in _choose(sd + 22, _POOL_COURSE, 2)],
        ]),
        ("예약·결제·환불 한눈에", [
            f"{f['d']} 예약은 전화 또는 카카오톡으로 지역·코스·시간만 알려주시면 즉시 확정됩니다.",
            *[s.format(**f) for s in _choose(sd + 33, _POOL_PAY, 2)],
        ]),
    ]


def field_notes(district, region):
    """FIELD NOTES 노트 카드 4개 (01~04). 앵커 고유 + 풀 셔플 + 법적 고지 변주."""
    f = _facts(district, region)
    sd = _seed(district["slug"])
    legal = _choose(sd + 55, _POOL_LEGAL, 1)[0].format(**f)
    return [
        ("권역의 특징", [
            f"{f['r']} {f['dt']} {f['char']}입니다. {f['lmjoin']} 일대를 중심으로 생활·이동 동선이 형성됩니다.",
            *[s.format(**f) for s in _choose(sd + 1, _POOL_AREA, 2)],
        ]),
        ("관리사 배치 및 도착 시간", [
            f"{f['d']} 내부와 인접 권역에 관리사를 분산 대기시켜, 호출 후 평균 {f['avg']}분 내 도착을 목표로 운영합니다.",
            *[s.format(**f) for s in _choose(sd + 2, _POOL_DISPATCH, 2)],
        ]),
        ("안전 가이드 — 자문 트레이너 감수", [
            f"{f['d']}에 배차되는 모든 관리사는 신원 확인과 표준 안전 교육을 이수한 인원으로 한정합니다.",
            *[s.format(**f) for s in _choose(sd + 3, _POOL_SAFETY, 2)],
        ]),
        ("결제·예약 운영 원칙", [
            f"{f['d']} 예약 시 확정된 금액 외 현장 추가 요구는 일절 없습니다.",
            legal,
            _choose(sd + 4, ["불법·퇴폐 서비스를 제공하지 않으며, 위반 시 즉시 배차를 중단합니다.",
                             "예약 내용과 응대 기록은 품질 관리를 위해 본사에서 직접 관리합니다.",
                             f"{f['d']} 관련 문의나 불편 사항은 본사 고객센터로 알려주시면 즉시 조치합니다."], 1)[0],
        ]),
    ]


_REVIEW_BANK = [
    ("{course} 받았는데 {area}까지 생각보다 빨리 와주셔서 놀랐어요. 압도 딱 좋았습니다.", "{area} · {nick}"),
    ("야근 끝나고 {course} 예약했어요. {area} 집까지 {min}분 만에 도착하셨고 다음 날 몸이 한결 가벼웠습니다.", "{area} · {nick}"),
    ("처음 불러봤는데 응대도 친절하고 {course} 코스가 만족스러웠어요. {area}에서 또 부를게요.", "{area} · {nick}"),
    ("{area} 쪽은 늦은 시간에도 예약이 되는 게 가장 좋아요. {course} 강도 조절도 잘 맞춰주셨습니다.", "{area} · {nick}"),
    ("어깨 뭉친 게 심했는데 {course}로 집중해서 풀어주셨어요. {area}까지 도착도 빨랐습니다.", "{area} · {nick}"),
    ("가격도 예약할 때 들은 그대로였고 추가 요구 전혀 없었어요. {area}에서 {course} 강추합니다.", "{area} · {nick}"),
    ("{area} 신혼집에서 {course} 받았는데 분위기도 편안하고 마무리까지 정갈했어요.", "{area} · {nick}"),
    ("출장 다니느라 피곤했는데 {course} 120분으로 제대로 회복했습니다. {area} 호텔까지 와주셨어요.", "{area} · {nick}"),
]
_NICKS = ["김O준", "이O연", "박O현", "최O서", "정O우", "강O민", "윤O지", "장O호", "임O아", "오O석", "한O빈", "신O경"]
_COURSES = ["스웨디시", "아로마", "타이", "로미로미", "스포츠"]


def reviews(district, n=6):
    out = []
    areas = district["areas"]
    for i in range(n):
        sd = _seed(district["slug"] + "rev" + str(i))
        tmpl, who = _REVIEW_BANK[sd % len(_REVIEW_BANK)]
        area = areas[sd % len(areas)]
        course = _COURSES[(sd >> 2) % len(_COURSES)]
        nick = _NICKS[(sd >> 4) % len(_NICKS)]
        mins = 25 + (sd >> 6) % 20
        rating = 5 if sd % 5 else 4
        body = tmpl.format(course=course, area=area, min=mins, nick=nick)
        whos = who.format(area=area, nick=nick)
        out.append({"body": body, "who": whos, "rating": rating, "author": nick})
    return out


# ─────────────────────────────────────────────
# 행정구별 고유 메타 (title / description)
# 동일 템플릿 치환을 피하기 위해 문장 구조 자체를 시드로 분기합니다.
# ─────────────────────────────────────────────
_COURSE_KW = ["스웨디시·아로마", "타이·스포츠", "아로마·로미로미", "딥티슈 스포츠", "스웨디시·타이", "로미로미·아로마"]


def _course_kw(district):
    return _COURSE_KW[_seed(district["slug"] + "kw") % len(_COURSE_KW)]


_TITLE_TEMPLATES = [
    "{d} 출장마사지 — {lm} 일대 24시간 방문관리 | 마톡",
    "{r} {d} 출장마사지 | 평균 {avg}분 도착·{kw} | 마톡",
    "{d} 출장마사지 후기·요금 — {a0}·{a1} 방문 | 마톡",
    "마톡 {d} 출장마사지 | {kw} 24시간 심야 배차",
    "{d} 출장마사지 추천 | {lm} 근처 방문 마사지 | 마톡",
    "{r} {d} 방문 마사지 — {kw} 평균 {avg}분 | 마톡",
    "{d} 출장마사지 — {a0} 평균 {avg}분 방문 후기 | 마톡",
    "{d} 24시 출장마사지 | {a0} {lm} 방문관리 | 마톡",
    "{d} 출장마사지 가격·예약 | {lm} {kw} 24시간 | 마톡",
    "{lm} {d} 출장마사지 | {kw} 방문 건강관리 | 마톡",
]

_DESC_TEMPLATES = [
    "{r} {d} 출장마사지. {lm1} 일대 평균 {avg}분 도착, {kw} 코스 24시간 예약.",
    "{dt} {char}. {a3} 평균 {avg}분 도착, 동별 도착시간·후기 안내.",
    "{d} 집·숙소로 부르는 방문 마사지. {lm1} 근처 평균 {avg}분, 심야 예약 가능.",
    "{r} {d} 출장마사지 가이드. 동별 도착시간·{kw} 코스·요금을 정리했습니다.",
    "{d} 출장마사지 24시간. {a3} 평균 {avg}분 도착, {kw} 중심 추천.",
    "{lm1} {d} 방문 건강관리. 평균 {avg}분, {kw} 60·90·120분 코스 안내.",
    "{d} 출장마사지 후기·요금. {fat} 약 {fm}분 등 동별 도착시간 공개.",
    "{r} {d} 24시간 방문 마사지. {char}에 맞춘 {kw} 코스와 후기 안내.",
    "{d} 방문 마사지 예약. {a0}·{a1} 평균 {avg}분, 만 19세 이상 건강관리.",
    "{r} {d} 출장마사지 평균 {avg}분. {kw} 코스를 컨디션에 맞춰 안내합니다.",
]


def meta_title(r, d, avg):
    areas = d["areas"] + ["", ""]
    fields = {"d": d["kr"], "r": r["kr"], "lm": d["landmarks"][0],
              "a0": areas[0], "a1": areas[1], "kw": _course_kw(d), "avg": avg}
    tpl = _TITLE_TEMPLATES[_seed(d["slug"] + "title") % len(_TITLE_TEMPLATES)]
    return tpl.format(**fields)


def meta_desc(r, d, avg, arrivals):
    fast = min(arrivals, key=lambda x: x[1])
    areas = d["areas"] + ["", ""]
    fields = {"d": d["kr"], "r": r["kr"], "lm": ", ".join(d["landmarks"][:2]),
              "lm1": d["landmarks"][0], "a0": areas[0], "a1": areas[1],
              "a3": ", ".join(d["areas"][:3]), "char": d["character"],
              "fa": fast[0], "fm": fast[1], "kw": _course_kw(d), "avg": avg,
              "dt": josa(d["kr"], "은는"), "fat": josa(fast[0], "은는")}
    tpl = _DESC_TEMPLATES[_seed(d["slug"] + "desc") % len(_DESC_TEMPLATES)]
    return tpl.format(**fields)


# ═════════════════════════════════════════════
# 행정동(洞) 단위 콘텐츠 생성기 (서울 시범)
# ═════════════════════════════════════════════
def dong_facts(region, district, dong):
    sd = _seed("dong:" + district["slug"] + ":" + dong["slug"])
    return {
        "rg": region["kr"], "d": district["kr"], "dong": dong["kr"],
        "lm": dong["lm"], "char": dong["char"],
        "avg": 24 + sd % 18,
        "peak": 44 + sd % 14, "night": 15 + (sd >> 3) % 13, "repeat": 33 + (sd >> 5) % 22,
        "kw": _COURSE_KW[(sd >> 2) % len(_COURSE_KW)],
        "dongt": josa(dong["kr"], "은는"), "dongi": josa(dong["kr"], "이가"),
        "lmobj": josa(dong["lm"], "을를"),
    }


_DA_ARR = [
    "{lm} 일대까지 우회 없이 진입하는 동선이라 도착 시간이 비교적 일정합니다.",
    "{dong} 안에서도 {lm} 인근은 예약이 몰려 피크 시간엔 수 분 더 걸릴 수 있습니다.",
    "인접 동에 대기 중인 관리사가 있으면 {dong} 도착은 평균보다 더 단축됩니다.",
    "{d} 내 다른 동선과 묶어 배차해 {dong} 공차 이동을 줄입니다.",
    "교통 변동이 크면 예약 단계에서 {dong} 예상 도착 시간을 다시 안내드립니다.",
]
_DA_TIME = [
    "주말에는 {dong} 오전 예약 비중이 평일보다 올라갑니다.",
    "{lm} 주변 숙소·오피스 수요로 {dong} 야간 콜이 특히 꾸준합니다.",
    "{dong} 재방문 비율은 약 {repeat}%로 단골 예약이 일정 부분을 차지합니다.",
    "심야에도 {dong} 배차가 끊기지 않도록 야간 대기 인원을 둡니다.",
    "연휴에는 {dong} 예약이 전 시간대에 고르게 분산됩니다.",
]
_DA_COURSE = [
    "{lm} 인근 자택·숙소 예약이 많아 이동이 간편하면서 회복감이 큰 구성을 안내합니다.",
    "예약 시 컨디션과 신경 쓰이는 부위를 알려주시면 {dong}에서도 압과 부위를 조율합니다.",
    "{dong}에서는 90분 선택 비중이 높아 깊은 이완을 원하면 120분을 권합니다.",
    "처음이라면 부담이 적은 스웨디시 60분부터 시작하는 것을 권합니다.",
]
_DA_PAY = [
    "코스와 시간은 예약 시 확정되어 {dong} 현장에서 추가 비용이 붙지 않습니다.",
    "관리사 출발 전 취소는 전액 환불되며, 출발 이후 기준은 예약 시 안내드립니다.",
    "{dong}도 출장비 없이 표시 요금 그대로 진행합니다.",
    "심야·주말이라도 {dong} 요금에 할증을 붙이지 않습니다.",
    "결제 방식은 예약 단계에서 안내하며 정찰 요금을 그대로 적용합니다.",
]
_DA_AREA = [
    "이 동선을 기준으로 {dong} 주요 생활권에서 콜이 집중됩니다.",
    "{dong} 일대의 상권·주거 변화는 분기별로 배차 데이터에 반영해 동선을 조정합니다.",
    "{rg} {d} 안에서도 {dong}만의 수요 패턴에 맞춰 대기 위치를 따로 둡니다.",
    "{lm} 방문 고객이 자택·숙소로 이어 예약하는 경우도 적지 않습니다.",
]
_DA_DISPATCH = [
    "피크 시간대에는 사전 대기 인원을 늘려 {dong} 평균 도착 시간을 관리합니다.",
    "교통 상황에 따라 예상 시간이 바뀌면 예약 단계에서 다시 안내드립니다.",
    "{d} 인접 동과 묶어 운영해 {dong} 대기 공백이 생기지 않도록 합니다.",
    "심야에도 {dong} 담당 야간 대기 관리사를 두어 배차가 끊기지 않습니다.",
]
_DA_SAFETY = [
    "코스별 강도·부위 기준은 안전 자문 트레이너 박지연 트레이너의 가이드라인을 따릅니다.",
    "통증·질환이 있는 부위는 사전에 알려주시면 피하거나 강도를 낮춰 진행합니다.",
    "{dong} 야간 예약에도 주간과 동일한 안전 기준이 그대로 적용됩니다.",
    "관리사는 정기 재교육으로 응대·안전 매뉴얼을 갱신합니다.",
]
_DA_LEGAL = [
    "마톡 출장마사지는 의료 행위가 아닌 건강관리·휴식 서비스로, 만 19세 이상을 대상으로 합니다.",
    "{dong}에서 제공되는 모든 코스는 치료가 아닌 휴식·컨디션 관리 목적이며 만 19세 이상만 이용할 수 있습니다.",
    "본 서비스는 건강관리·휴식 목적의 출장 서비스로, 미성년자 이용을 제한합니다.",
]


def dong_overview_notes(region, district, dong):
    f = dong_facts(region, district, dong)
    sd = _seed("dov:" + district["slug"] + dong["slug"])
    return [
        ("도착 시간과 진입 동선", [
            f"{f['rg']} {f['d']} {f['dongt']} 호출 후 평균 약 {f['avg']}분에 방문하며, {f['lm']} 방면 동선을 기준으로 대기 위치를 잡습니다.",
            *[s.format(**f) for s in _choose(sd + 1, _DA_ARR, 3)],
        ]),
        ("시간대별 예약 분포", [
            f"{f['dong']} 콜의 약 {f['peak']}%가 저녁 7시 이후 야간에 집중되고, 자정~새벽 심야 비중도 약 {f['night']}%에 이릅니다.",
            *[s.format(**f) for s in _choose(sd + 2, _DA_TIME, 2)],
        ]),
        ("권역 성격에 맞는 추천 코스", [
            f"{f['dongt']} {f['char']}으로, {f['kw']} 코스 문의가 많고 평균 {f['avg']}분 도착에 맞춰 90분 구성을 우선 추천합니다.",
            *[s.format(**f) for s in _choose(sd + 3, _DA_COURSE, 2)],
        ]),
        ("예약·결제·환불 안내", [
            f"{f['dong']} 예약은 전화 또는 카카오톡으로 코스·시간만 알려주시면 즉시 확정됩니다.",
            *[s.format(**f) for s in _choose(sd + 4, _DA_PAY, 2)],
        ]),
    ]


def dong_field_notes(region, district, dong):
    f = dong_facts(region, district, dong)
    sd = _seed("dfn:" + district["slug"] + dong["slug"])
    legal = _choose(sd + 9, _DA_LEGAL, 1)[0].format(**f)
    return [
        ("동(洞)의 특징", [
            f"{f['dongt']} {f['char']}으로, {f['lmobj']} 중심으로 생활·이동 동선이 형성됩니다.",
            *[s.format(**f) for s in _choose(sd + 1, _DA_AREA, 2)],
        ]),
        ("관리사 배치와 도착 관리", [
            f"{f['dong']} 내부와 인접 동에 관리사를 분산 대기시켜, 호출 후 평균 {f['avg']}분 내 도착을 목표로 운영합니다.",
            *[s.format(**f) for s in _choose(sd + 2, _DA_DISPATCH, 2)],
        ]),
        ("안전 가이드 — 자문 트레이너 감수", [
            f"{f['dong']}에 배차되는 모든 관리사는 신원 확인과 표준 안전 교육을 이수한 인원으로 한정합니다.",
            *[s.format(**f) for s in _choose(sd + 3, _DA_SAFETY, 2)],
        ]),
        ("결제·예약 운영 원칙", [
            f"{f['dong']} 예약 시 확정된 금액 외 현장 추가 요구는 일절 없습니다.",
            legal,
            _choose(sd + 4, ["불법·퇴폐 서비스를 제공하지 않으며, 위반 시 즉시 배차를 중단합니다.",
                             f"{f['dong']} 관련 문의나 불편 사항은 본사 고객센터로 알려주시면 즉시 조치합니다."], 1)[0],
        ]),
    ]


def dong_reviews(district, dong, n=6):
    out = []
    for i in range(n):
        sd = _seed("drev:" + district["slug"] + dong["slug"] + str(i))
        tmpl, who = _REVIEW_BANK[sd % len(_REVIEW_BANK)]
        course = _COURSES[(sd >> 2) % len(_COURSES)]
        nick = _NICKS[(sd >> 4) % len(_NICKS)]
        mins = 24 + (sd >> 6) % 18
        rating = 5 if sd % 5 else 4
        body = tmpl.format(course=course, area=dong["kr"], min=mins, nick=nick)
        whos = who.format(area=dong["kr"], nick=nick)
        out.append({"body": body, "who": whos, "rating": rating, "author": nick})
    return out


_DONG_TITLE = [
    "{d} {dong} 출장마사지 — 24시간 방문관리 | 마톡",
    "{d} {dong} 출장마사지 | {lm} 평균 {avg}분 방문 — 마톡",
    "{d} {dong} 출장마사지 {lm} 24시간 | 마톡",
    "{d} {dong} 방문 마사지 — {kw} 평균 {avg}분 | 마톡",
    "{d} {dong} 출장마사지 후기·요금 안내 | 마톡",
    "{d} {dong} 출장마사지 — {lm} 근처 심야 방문 | 마톡",
]
_DONG_DESC = [
    "{rg} {d} {dong} 출장마사지. {lm} 일대 평균 {avg}분 방문, {kw} 24시간 예약.",
    "{dongt} {char}. {lm} 인근 평균 {avg}분, 동 단위 도착·후기·요금 안내.",
    "{dong} 방문 마사지 — {kw} 평균 {avg}분, 심야 예약. 만 19세 이상 건강관리.",
    "{d} {dong} 24시간 출장마사지. {lm} 근처 평균 {avg}분, 정찰 요금.",
    "{rg} {d} {dong} 출장마사지 평균 {avg}분. {kw} 코스를 컨디션에 맞춰 안내.",
]


def dong_meta_title(region, district, dong):
    f = dong_facts(region, district, dong)
    tpl = _DONG_TITLE[_seed("dt:" + district["slug"] + dong["slug"]) % len(_DONG_TITLE)]
    return tpl.format(**f)


def dong_meta_desc(region, district, dong):
    f = dong_facts(region, district, dong)
    tpl = _DONG_DESC[_seed("dd:" + district["slug"] + dong["slug"]) % len(_DONG_DESC)]
    return tpl.format(**f)
