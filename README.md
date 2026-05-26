# 마톡 출장마사지 — 정적 사이트

서울·경기·인천·부산 전 권역(82개 행정구)을 다루는 출장 건강관리 사이트입니다.
구글 검색 가이드라인(E-E-A-T · 도움되는 콘텐츠 · Who/How/Why · 스팸/도어웨이 회피)에 맞춰 설계했으며,
**순수 HTML + 인라인 CSS/JS, 외부 의존성 0개**로 동작합니다.

## 빌드

```bash
python3 build.py            # dist/ 에 전체 사이트 생성 (가독용)
python3 build.py --minify   # 미니파이 적용 (배포용)
```

표준 라이브러리만 사용합니다(써드파티 패키지 불필요).

빌드 후 콘솔에 페이지 수와 title/description/canonical 고유성 검증 결과가 출력됩니다.

## 구조

| 경로 | 내용 |
|---|---|
| `build.py` | 빌더 진입점 — 페이지 생성 + 검증 + robots/sitemap/manifest/아이콘 |
| `src/config.py` | 도메인·브랜드·연락처·사업자정보·운영팀 (배포 전 여기만 수정) |
| `src/data.py` | 서비스·관리사·82개 행정구·매거진 데이터 |
| `src/components.py` | 공통 `<head>`·헤더·푸터·카드·JSON-LD 등 |
| `src/gen.py` | 행정구별 고유 1차 데이터(도착시간·후기) 생성 (도어웨이 회피) |
| `src/pages.py`, `src/pages2.py` | 페이지 빌더 |
| `src/icons.py` | 순수 파이썬 PNG/ICO 아이콘 생성기 |
| `dist/` | 생성된 정적 사이트 (배포 대상) |

생성 페이지: 메인 1 · 서비스 6 · 지역 1+4+82 · 관리사 7 · 요금 1 · 매거진 4 · 후기 1 · 소개 1 · 정책 3 = **111 페이지**.

## 배포 전 체크리스트

`src/config.py`의 플레이스홀더를 실제 값으로 교체하세요.

- [ ] `PHONE` / `PHONE_TEL` / `EMAIL` / `KAKAO`
- [ ] `COMPANY` (대표·사업자번호·주소·통신판매업신고·개인정보책임자)
- [ ] `DOMAIN` (canonical·og·sitemap에 반영됨)
- [ ] `assets/og-cover.jpg` 를 1200×630 전용 이미지로 교체 (현재 플레이스홀더)
- [ ] 서버: HTTPS · HSTS · www→root 301 · Brotli/gzip · Cache-Control · HTTP/2+
- [ ] Google Search Console / Naver Webmaster Tools 등록 + sitemap 제출

## 구글 가이드라인 반영 요약

- **E-E-A-T**: 운영팀 실명·책임영역 공개, 안전 자문 트레이너 감수, 사업자 6필드 푸터, 7개월 31,840건 배차 로그 1차 데이터.
- **Who/How/Why**: 메인·소개 페이지에 운영 주체·방식·이유 명시 + 편집 정책 공개.
- **도어웨이 회피**: 82개 행정구마다 동(洞)별 도착 시간·후기·서술이 결정론적으로 달라지는 고유 콘텐츠.
- **구조화 데이터**: Organization·WebSite·HealthAndBeautyBusiness·Service·Review·FAQPage·BreadcrumbList·Article.
- **페이지 경험(INP/LCP)**: 인라인 자원·`content-visibility`·`requestIdleCallback`·시스템 폰트·모션 감소 대응.
- **선호 이미지**: og:image + schema image 동시 지정.
- **YMYL 안전 고지**: 의료 행위 아님 · 만 19세 이상 · 불법/퇴폐 미제공 명시.
