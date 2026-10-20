#!/usr/bin/env python3
"""晨曉之星：瓶身背面浮凸的品牌徽記（圓環＋中間的柱＋三足的 M）高度圖。

依 Yoyo 拍的背面照（back_hand.jpg、back_far.jpg）量測：徽記高 0.64 個瓶寬（圓環頂到底座），
上緣在瓶身圓柱段頂下 0.19、下緣在 0.60；圓環外徑 0.31 瓶寬。以下座標用近拍照裁切後的像素（徽記總高 700px）。
輸出 src/tex_ms_emblem.png：涵蓋寬 1.5、高 2.6（單位 = 場景長度，徽記高 2.42），每單位 360px；
白 = 浮凸最高處，邊緣是圓弧的斷面（像壓印出來的）。
"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

OUT = sys.argv[1] if len(sys.argv) > 1 else 'src/tex_ms_emblem.png'
EMB_H = 2.42                       # 徽記總高（單位）
SRC_H = 700.                       # 近拍照裡的總高（px）
k = EMB_H / SRC_H                  # 單位 / 照片 px
PPU = 360                          # 貼圖每單位像素
TW, TH = int(1.5 * PPU), int(2.6 * PPU)
SS = 2
cx0, cy0 = 300, 435                # 徽記中心（照片 px）
def P(x, y):                       # 照片 px → 超取樣貼圖 px
    return ((x - cx0) * k * PPU + TW / 2) * SS, ((y - cy0) * k * PPU + TH / 2) * SS
def R(r):
    return r * k * PPU * SS
im = Image.new('L', (TW * SS, TH * SS), 0)
d = ImageDraw.Draw(im)
def line(pts, hw):
    q = [P(*p) for p in pts]
    d.line(q, fill=255, width=int(R(hw * 2)), joint='curve')
    for x, y in q:
        rr = R(hw); d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
# 圓環
x, y = P(300, 250); ro, ri = R(152 + 18), R(152 - 18)
d.ellipse([x - ro, y - ro, x + ro, y + ro], fill=255); d.ellipse([x - ri, y - ri, x + ri, y + ri], fill=0)
# 圓環裡的漏斗形柱頭（倒梯形、圓角）
# 柱頭：上緣微拱、兩側往下鼓出再收進柱子（像倒過來的圓角三角形）
L, Rr = [], []
for i in range(21):
    t = i / 20; hw = 15 + 49 * (1 - t ** 2.4); y = 258 + 50 * t
    L.append(P(300 - hw, y)); Rr.append(P(300 + hw, y))
top = [P(300 + 64 * math.cos(a), 258 - 9 * math.sin(a)) for a in [i / 12 * math.pi for i in range(13)]]
d.polygon(Rr[::-1] + top[1:-1] + L, fill=255)
line([(244, 260), (356, 260)], 8)
# 柱
line([(300, 296), (300, 756)], 15)
# 張開的 V 形橫桿，兩端圓頭
line([(114, 488), (300, 536), (490, 480)], 17)
for xx, yy in [(112, 488), (492, 480)]:
    x, y = P(xx, yy); rr = R(19); d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
# 兩側的腳
line([(165, 505), (165, 754)], 15)
line([(440, 498), (440, 754)], 15)
# 圓圓的底座
for xx, rx in [(165, 52), (300, 48), (440, 52)]:            # 底座：上緣圓拱、底邊平
    x0, y0 = P(xx - rx, 744); x1, y1 = P(xx + rx, 788)
    d.rounded_rectangle([x0, y0, x1, y1], radius=R(18), fill=255)
m = np.asarray(im) > 127
dist = ndimage.distance_transform_edt(m) / SS          # 到邊緣的距離（貼圖 px）
w = R(16) / SS                                          # 圓弧斷面的半寬
h = np.sqrt(np.clip(1 - (1 - np.clip(dist / w, 0, 1)) ** 2, 0, 1))
h = ndimage.gaussian_filter(h, 1.2)
out = Image.fromarray((h * 255).astype(np.uint8)).resize((TW, TH), Image.LANCZOS)
out.save(OUT, optimize=True)
print(OUT, TW, TH)
