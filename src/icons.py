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


def _in_monogram(fx, fy):
    """프랙션 좌표(0~1)가 'M' 모노그램 획 안에 있는지."""
    left, right, top, bot = 0.32, 0.68, 0.35, 0.65
    vx, vy = 0.50, 0.55          # 가운데 V 꼭짓점
    hw = 0.052                   # 획 반폭
    segs = (
        (left, top, left, bot),      # 왼쪽 세로
        (right, top, right, bot),     # 오른쪽 세로
        (left, top, vx, vy),          # 왼쪽 사선
        (right, top, vx, vy),         # 오른쪽 사선
    )
    return any(_seg_dist(fx, fy, *s) <= hw for s in segs)


def _render(size, *, maskable=False):
    """RGBA 바이트 생성. 라운드 다크 배경 위 그라데이션 원 + 다크 M 모노그램."""
    px = bytearray()
    cx = cy = size / 2
    r_circle = size * (0.46 if maskable else 0.40)
    radius_bg = size * 0.22
    hx, hy = size * 0.36, size * 0.30  # specular 하이라이트 중심
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
            dist = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            fx, fy = (x + 0.5) / size, (y + 0.5) / size
            if dist <= r_circle and not _in_monogram(fx, fy):
                t = dist / r_circle
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


def _png(size, raw):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # RGBA
    idat = zlib.compress(raw, 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def png_bytes(size, maskable=False):
    return _png(size, _render(size, maskable=maskable))


def ico_bytes(size=32):
    """PNG-embedded ICO."""
    png = png_bytes(size)
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", size if size < 256 else 0, size if size < 256 else 0,
                        0, 0, 1, 32, len(png), 22)
    return header + entry + png
