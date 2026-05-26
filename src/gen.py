# -*- coding: utf-8 -*-
"""행정구별 고유 1차 데이터·콘텐츠 생성기 (도어웨이 회피).
동일 골격이라도 동(洞)별 도착 시간·후기·서술이 결정론적으로 달라지도록 시드를 사용합니다."""
import hashlib
from . import config as C


def _seed(s):
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16)


def _pick(seed, options):
    return options[seed % len(options)]


def arrival_table(district):
    """동별 평균 도착 시간 (분). 동 이름 시드로 25~44분 사이 결정론 생성."""
    rows = []
    for area in district["areas"]:
        sd = _seed(district["slug"] + area)
        mins = 25 + sd % 20
        rows.append((area, mins))
    return rows


def time_distribution(district):
    sd = _seed(district["slug"] + "time")
    peak = _pick(sd, [
        "오후 8시~새벽 1시 사이 콜이 가장 집중됩니다",
        "퇴근 직후인 저녁 7시부터 밤 11시까지 예약이 몰립니다",
        "심야인 자정 전후와 새벽 시간대 수요가 꾸준합니다",
        "주말 오후와 일요일 저녁 콜 비중이 평일보다 높습니다",
    ])
    second = _pick(sd >> 3, [
        "주중 점심 직후의 짧은 휴식 예약도 일정하게 발생합니다",
        "출근 전 이른 아침 예약이 소수지만 꾸준히 들어옵니다",
        "주말에는 오전 콜이 평일 대비 눈에 띄게 늘어납니다",
        "연휴 기간에는 전 시간대 예약이 고르게 분산됩니다",
    ])
    return peak, second


def overview_notes(district, region):
    """OVERVIEW 노트 카드 4개 (05~08 위치)."""
    rows = arrival_table(district)
    fastest = min(rows, key=lambda r: r[1])
    slowest = max(rows, key=lambda r: r[1])
    avg = round(sum(r[1] for r in rows) / len(rows))
    dong_line = ", ".join(f"{a} 약 {m}분" for a, m in rows)
    peak, second = time_distribution(district)
    course = recommend_course(district)
    return [
        ("동(洞)별 평균 도착 시간 분포", [
            f"{district['kr']} 권역의 동별 평균 도착 시간은 다음과 같습니다 — {dong_line}.",
            f"가장 빠른 곳은 {fastest[0]}(약 {fastest[1]}분), 상대적으로 거리가 있는 곳은 {slowest[0]}(약 {slowest[1]}분)입니다.",
            f"권역 전체 평균은 약 {avg}분이며, 인접 권역 대기 관리사가 있을 경우 더 단축됩니다.",
        ]),
        ("시간대별 콜 분포 특징", [
            f"{district['kr']}는 {peak}.",
            f"{second}.",
            "본사 디스패처는 이 분포에 맞춰 피크 시간 전에 인접 권역 관리사를 미리 대기시킵니다.",
        ]),
        ("권역 성격에 맞는 추천 코스", [
            f"{district['kr']}는 {district['character']}입니다.",
            course,
            "예약 시 컨디션을 말씀해 주시면 코스와 압을 함께 조율해 드립니다.",
        ]),
        ("예약·결제·환불 한눈에", [
            "예약은 전화 또는 카카오톡으로 지역·코스·시간만 알려주시면 됩니다.",
            "코스와 시간은 예약 시 확정되며 추가 비용이 발생하지 않습니다.",
            "관리사 출발 전에는 전액 환불되며, 출발 이후 기준은 예약 시 안내드립니다.",
        ]),
    ]


def recommend_course(district):
    sd = _seed(district["slug"] + "course")
    return _pick(sd, [
        "장시간 앉아 일하는 분이 많아 어깨·허리 집중의 스웨디시·아로마 90분 코스 문의가 가장 많습니다.",
        "활동량이 많은 권역 특성상 딥티슈 계열 스포츠 코스와 타이 건식 스트레칭 선호도가 높습니다.",
        "심야 휴식 수요가 커 깊은 이완 중심의 아로마·로미로미 120분 코스가 꾸준히 예약됩니다.",
        "첫 방문 고객 비중이 높아 부담이 적은 스웨디시 60분으로 시작하는 경우가 많습니다.",
    ])


def field_notes(district, region):
    """FIELD NOTES 노트 카드 4개 (01~04)."""
    landmarks = ", ".join(district["landmarks"])
    return [
        ("권역의 특징", [
            f"{region['kr']} {district['kr']}는 {district['character']}으로, {landmarks} 일대를 중심으로 생활·이동 동선이 형성됩니다.",
            f"이 동선을 기준으로 {', '.join(district['areas'][:3])} 등 주요 생활권의 콜이 집중됩니다.",
            "마톡은 권역의 실제 이동 흐름에 맞춰 대기 위치를 배치합니다.",
        ]),
        ("관리사 배치 및 도착 시간", [
            f"{district['kr']} 내부와 인접 권역에 관리사를 분산 대기시켜 호출 후 이동 거리를 최소화합니다.",
            "피크 시간대에는 디스패처가 사전 대기 인원을 늘려 평균 도착 시간을 관리합니다.",
            "교통 상황에 따라 예상 시간이 바뀌면 예약 단계에서 다시 안내드립니다.",
        ]),
        ("안전 가이드 — 자문 트레이너 감수", [
            "모든 코스의 강도·부위 기준은 안전 자문 트레이너 박지연 트레이너의 가이드라인에 따라 설계되었습니다.",
            "관리사는 표준 안전 교육과 정기 재교육을 이수한 인원으로만 배차됩니다.",
            "통증·질환이 있는 부위는 사전에 알려주시면 해당 부위를 피하거나 강도를 낮춰 진행합니다.",
        ]),
        ("결제·예약 운영 원칙", [
            "예약 시 확정된 금액 외 현장 추가 요구는 일절 없습니다.",
            f"{C.BRAND_FULL}는 의료 행위가 아닌 건강관리·휴식 서비스를 제공하며 만 19세 이상을 대상으로 합니다.",
            "불법·퇴폐 서비스를 제공하지 않으며, 위반 시 즉시 배차를 중단합니다.",
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
