#!/usr/bin/env python3
"""晨曉之星香境：青金石圓盤外圈的刻字遮罩（金線鑲嵌）。

圓盤外圈是一條環帶，展開成一張長條貼圖：橫向 u 對應角度（u = fract(-φ/2π)，φ 是盤面上從 +X 往 +Z 量的角），
直向從環帶內緣（字頂，朝圓心）到外緣（字底）。從盤外看過去，兩個名字都是正的、由左往右讀：
  - 正面（+Z，西方，Hesperos 的方向）u = 0.75：ΕΣΠΕΡΟΣ
  - 背面（-Z，東方，破曉的方向）u = 0.25：ΕΩΣΦΟΡΟΣ
兩側（±X）各一顆八芒星，環帶內外各一道細線。字型 GFS Porson（古典希臘大寫）。
輸出 src/tex_ms_rim.png（白 = 金線、黑 = 青金石）。
"""
import sys, math
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else 'src/tex_ms_rim.png'
FONT = '/usr/share/fonts/opentype/porson/GFSPorson.otf'
W, H = 4096, 112
SS = 3                                  # 超取樣
w, h = W * SS, H * SS
im = Image.new('L', (w, h), 0)
d = ImageDraw.Draw(im)
# 環帶內外的細線（內緣一道、外緣兩道）
for y0, t in [(int(h * .06), 2.2), (int(h * .9), 2.2), (int(h * .97), 1.4)]:
    d.rectangle([0, y0 - t * SS / 2, w, y0 + t * SS / 2], fill=255)
font = ImageFont.truetype(FONT, int(h * .5))
def word(txt, uc, track=.32):
    # 字距加寬，像刻在石上的碑文
    glyphs = [(c, font.getbbox(c)) for c in txt]
    adv = [font.getlength(c) for c in txt]
    total = sum(adv) + track * font.size * (len(txt) - 1)
    x = uc * w - total / 2
    base = int(h * .72)                 # 對齊基線
    for (c, bb), a in zip(glyphs, adv):
        d.text((x, base), c, font=font, fill=255, anchor='ls')
        x += a + track * font.size
def star(uc, R):
    cx, cy = uc * w, h * .48
    pts = []
    for i in range(16):
        a = i / 16 * math.pi * 2 - math.pi / 2
        rr = R if i % 2 == 0 else R * (.42 if i % 4 == 2 else .3)
        if i % 4 == 2: rr = R * .38
        pts.append((cx + math.cos(a) * rr * (1 if i % 4 else 1), cy + math.sin(a) * rr))
    d.polygon(pts, fill=255)
    d.ellipse([cx - R * .16, cy - R * .16, cx + R * .16, cy + R * .16], fill=0)
word('ΕΣΠΕΡΟΣ', .75)
word('ΕΩΣΦΟΡΟΣ', .25)
for uc in (0.0, .5, 1.0):
    star(uc, h * .3)
# 名字兩旁的小圓點
for uc, sp in [(.75, .085), (.25, .095)]:
    for s in (-1, 1):
        cx = (uc + s * sp) * w
        d.ellipse([cx - h * .045, h * .48 - h * .045, cx + h * .045, h * .48 + h * .045], fill=255)
im = im.resize((W, H), Image.LANCZOS)
im.save(OUT, optimize=True)
print(OUT, W, H)
