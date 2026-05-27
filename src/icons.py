# -*- coding: utf-8 -*-
"""순수 파이썬 아이콘 생성기 (zlib/struct만 사용 — 외부 의존성 0).
브랜드 로즈골드 라디얼 그라데이션 원 + 다크 라운드 배경."""
import struct
import zlib
import math

BG = (11, 11, 14)          # #0b0b0e
G_IN = (244, 210, 156)     # #f4d29c
G_MID = (233, 184, 167)    # #e9b8a7
G_OUT = (201, 138, 107)    # #c98a6b


def _lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _grad(t):
    # 0=중심(밝음) → 1=가장자리(딥)
    if t < 0.55:
        return _lerp(G_IN, G_MID, t / 0.55)
    return _lerp(G_MID, G_OUT, (t - 0.55) / 0.45)


def _seg_dist(px, py, ax, ay, bx, by):
    """점(px,py)에서 선분 (ax,ay)-(bx,by) 까지의 거리."""
    dx, dy = bx - ax, by - ay
    seg2 = dx * dx + dy * dy
    if seg2 == 0:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / seg2
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


# 말풍선 본체(라운드 사각형) 파라미터 — 프랙션 좌표(0~1)
_B_CX, _B_CY = 0.50, 0.435
_B_HW, _B_HH = 0.270, 0.175
_B_CR = 0.105
# 꼬리 삼각형 (왼쪽 아래로 향함)
_TAIL = ((0.345, 0.575), (0.315, 0.745), (0.475, 0.595))
# 타이핑 점 3개
_DOTS = ((0.355, 0.435), (0.500, 0.435), (0.645, 0.435))
_DOT_R = 0.044


def _rrect_inside(fx, fy):
    dx = abs(fx - _B_CX) - (_B_HW - _B_CR)
    dy = abs(fy - _B_CY) - (_B_HH - _B_CR)
    qx, qy = max(dx, 0.0), max(dy, 0.0)
    return math.hypot(qx, qy) + min(max(dx, dy), 0.0) - _B_CR <= 0.0


def _tri_inside(fx, fy):
    (ax, ay), (bx, by), (cx_, cy_) = _TAIL
    d1 = (fx - bx) * (ay - by) - (ax - bx) * (fy - by)
    d2 = (fx - cx_) * (by - cy_) - (bx - cx_) * (fy - cy_)
    d3 = (fx - ax) * (cy_ - ay) - (cx_ - ax) * (fy - ay)
    neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (neg and pos)


def _in_bubble(fx, fy):
    return _rrect_inside(fx, fy) or _tri_inside(fx, fy)


def _in_dot(fx, fy):
    return any(math.hypot(fx - dx, fy - dy) <= _DOT_R for dx, dy in _DOTS)


def _render(size, *, maskable=False):
    """RGBA 바이트 생성. 라운드 다크 배경 위 로즈골드 말풍선 + 다크 타이핑 점 3개."""
    px = bytearray()
    cx = cy = size / 2
    r_norm = size * 0.40            # 그라데이션 정규화 반경
    radius_bg = size * 0.22
    hx, hy = size * 0.36, size * 0.28  # specular 하이라이트 중심
    for y in range(size):
        row = bytearray([0])  # filter type 0
        for x in range(size):
            inside_bg = True
            if not maskable:
                dx = max(radius_bg - x, x - (size - radius_bg), 0)
                dy = max(radius_bg - y, y - (size - radius_bg), 0)
                if dx * dx + dy * dy > radius_bg * radius_bg:
                    inside_bg = False
            if not inside_bg:
                row += bytes([0, 0, 0, 0])
                continue
            fx, fy = (x + 0.5) / size, (y + 0.5) / size
            if _in_bubble(fx, fy) and not _in_dot(fx, fy):
                dist = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                t = min(1.0, dist / r_norm)
                col = list(_grad(t))
                hd = math.hypot(x - hx, y - hy)
                hl = max(0.0, 1 - hd / (size * 0.4))
                for i in range(3):
                    col[i] = min(255, round(col[i] + hl * 55))
                row += bytes(col + [255])
            else:
                row += bytes(BG + (255,))
        px += row
    return bytes(px)


def _png(w, raw, h=None):
    h = h or w
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)  # RGBA
    idat = zlib.compress(raw, 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def png_bytes(size, maskable=False):
    return _png(size, _render(size, maskable=maskable))


def _render_cover(w, h):
    """1200x630 OG 커버: 다크 배경 그라데이션 + 중앙 로즈골드 말풍선."""
    px = bytearray()
    cx, cy = w / 2, h / 2
    s = min(w, h)                         # 말풍선 기준 정사각 크기
    bx0, by0 = cx - s / 2, cy - s / 2     # 말풍선 영역 좌상단
    bg_diag = math.hypot(w, h) / 2
    for y in range(h):
        row = bytearray([0])
        for x in range(w):
            fx, fy = (x + 0.5 - bx0) / s, (y + 0.5 - by0) / s
            if 0 <= fx <= 1 and 0 <= fy <= 1 and _in_bubble(fx, fy) and not _in_dot(fx, fy):
                dist = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                col = list(_grad(min(1.0, dist / (s * 0.42))))
                hd = math.hypot(x - (bx0 + s * 0.36), y - (by0 + s * 0.30))
                hl = max(0.0, 1 - hd / (s * 0.4))
                for i in range(3):
                    col[i] = min(255, round(col[i] + hl * 55))
                row += bytes(col + [255])
            else:
                # 배경: 중앙에서 멀어질수록 더 어둡게
                d = math.hypot(x - cx, y - cy) / bg_diag
                v = max(0, round(18 - d * 12))
                row += bytes([v, v, max(v, round(v * 1.1)), 255])
        px += row
    return bytes(px)


def og_cover_bytes(w=1200, h=630):
    return _png(w, _render_cover(w, h), h)


def ico_bytes(size=32):
    """PNG-embedded ICO."""
    png = png_bytes(size)
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", size if size < 256 else 0, size if size < 256 else 0,
                        0, 0, 1, 32, len(png), 22)
    return header + entry + png
