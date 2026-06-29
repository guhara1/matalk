# -*- coding: utf-8 -*-
"""사이트 전역 설정. 도메인 연결 시 이 파일만 수정하면 됩니다."""

DOMAIN = "https://matalk.netlify.app"

BRAND = "마톡"
BRAND_FULL = "마톡 출장마사지"
BRAND_EN = "Matalk"
LEGAL_NAME = "YH LAB"

# 연락처
PHONE = "0508-202-4743"            # 표시용
PHONE_TEL = "+825082024743"        # tel: 링크용 (0508-202-4743)
EMAIL = "help@pacifichealthoptions.com"
KAKAO = "@마톡"

# 사업자 정보
COMPANY = {
    "name": "YH LAB",
    "ceo": "김유환",
    "biz_no": "815-26-00585",
    "addr": "경기도 파주시 청석로 268",
    "mailorder_no": "[통신판매업신고번호]",
    "privacy_officer": "김유환",
}

SOCIAL = {
    "instagram": "https://instagram.com/matalk.kr",
    "blog": "https://blog.naver.com/matalk",
}

# 운영
HOURS = "24시간 연중무휴"
HOURS_OPENS = "00:00"
HOURS_CLOSES = "23:59"

# E-E-A-T 신뢰 수치 (실 운영 데이터 — 교체 가능)
STATS = {
    "months": 7,
    "dispatch_logs": 31840,
    "seoul_logs": 16200,
    "gyeonggi_logs": 8900,
    "incheon_logs": 3540,
    "busan_logs": 3200,
    "rating": "4.96",
    "review_count": 2380,
    "avg_arrival_min": 32,
}

# 운영팀 (Authoritativeness / Expertise 신호)
TEAM = [
    {"name": "김세영", "role": "서울·경기권 운영팀장", "exp": "업계 12년",
     "bio": "수도권 디스패치 운영을 총괄하며 권역별 배차 표준과 응대 매뉴얼을 설계합니다."},
    {"name": "정하늘", "role": "인천·부산권 운영팀장", "exp": "업계 9년",
     "bio": "해안권·신도시 권역의 동선 데이터와 야간 콜 분포를 분석해 배차 시간을 단축합니다."},
    {"name": "박지연", "role": "안전 자문 트레이너", "exp": "KSPO 스포츠마사지 트레이너 · 재활케어 8년",
     "bio": "관리사 안전 가이드라인과 코스별 강도 기준을 감수하고 정기 재교육을 진행합니다."},
]

AUTHOR = "마톡 편집팀"

# 네이버 사이트 소유확인 — HTML 파일 방식 (루트에 그대로 서빙)
NAVER_VERIFY_FILENAME = "naver68be76df5230847bd9dbd542517f65c4.html"
NAVER_VERIFY_CONTENT = "naver-site-verification: naver68be76df5230847bd9dbd542517f65c4.html"
