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


def _render(size, *, maskable=False):
    """RGBA 바이트 생성. 라운드 다크 배경 위 그라데이션 원."""
    px = bytearray()
    cx = cy = size / 2
    r_circle = size * (0.46 if maskable else 0.40)
    radius_bg = size * 0.22  # 라운드 코너 반경
    # specular 하이라이트 중심 (좌상단)
    hx, hy = size * 0.36, size * 0.30
    for y in range(size):
        row = bytearray([0])  # filter type 0
        for x in range(size):
            # 라운드 사각 배경 알파
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
            if dist <= r_circle:
                t = dist / r_circle
                col = list(_grad(t))
                # specular 하이라이트
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
