#!/usr/bin/env python3
"""晨曉之星（Liquides Imaginaires Morning Star）瓶身印字遮罩。

字形取自台灣官方故事頁的標題「MORNING STAR」（白字、字高 58px），去掉星點後放大約 2.9 倍，
照官方去背正面照量測的位置排成兩行：
  - 量測單位：瓶身半徑 R（正面照瓶寬 301px → R = 150.5px）
  - 字高（大寫）0.166R，兩行基線距 0.241R
  - MORNING 沿圓柱展開的弧長 1.342R，STAR 0.635R（與標題的字距比例一致，整行等比縮放即可）
輸出 src/tex_ms_print.png：寬 1.5R（弧長）、高 0.625R，每 R 1024px；字是白、底是黑。
貼圖中心 = 文字區塊中心（瓶身圓柱段高度的 0.504 處，正面中線）。
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = sys.argv[1] if len(sys.argv) > 1 else 'ref/story_tw.jpg'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'src/tex_ms_print.png'

PX_R = 1024
TW, TH = int(1.5 * PX_R), int(0.625 * PX_R)
CAP = 0.166 * PX_R
LEAD = 0.241 * PX_R

im = Image.open(SRC).convert('L')
a = np.asarray(im).astype(np.float32)
band = a[95:185, 380:1135]                     # 標題那一行（含一點上下餘白）
# 估背景：深藍底的亮度約 40～50；字是白色
bg = ndimage.median_filter(band, size=31)
ink = np.clip((band - bg - 25) / 150, 0, 1)
# 去掉星點：只留面積夠大的連通區
lab, n = ndimage.label(ink > .35)
sizes = ndimage.sum(np.ones_like(ink), lab, range(1, n + 1))
keep = np.zeros(n + 1, bool)
keep[1:] = sizes > 120
mask = ink * ndimage.binary_dilation(keep[lab], iterations=2)

cols = mask.max(0) > .3
xs = np.where(cols)[0]
# 兩個字之間最寬的空白就是 MORNING 與 STAR 的分界
gaps = []
run = None
for i in range(xs.min(), xs.max() + 1):
    if not cols[i]:
        run = i if run is None else run
    elif run is not None:
        gaps.append((i - run, run, i)); run = None
_, g0, g1 = max(gaps)
rows = np.where(mask.max(1) > .3)[0]
top, bot = rows.min(), rows.max()                 # 大寫字高（M、O 的上緣到基線）
cap_src = None
mcol = mask[:, xs.min():g0]
r2 = np.where(mcol.max(1) > .3)[0]
cap_src = r2.max() - r2.min()
words = {'MORNING': mask[:, xs.min():g0], 'STAR': mask[:, g1:xs.max() + 1]}
base_src = r2.max()                               # 基線（字底）

k = CAP / cap_src
out = np.zeros((TH, TW), np.float32)
cy = TH / 2
lines = [('MORNING', cy - LEAD / 2), ('STAR', cy + LEAD / 2)]   # 兩行的基線置中
ARC = {'MORNING': 1.342, 'STAR': 0.635}                          # 正面照量到的弧長（單位 R）
for w, base_y in lines:
    g = words[w]
    h, wd = g.shape
    gi = Image.fromarray((g * 255).astype(np.uint8)).resize((int(round(ARC[w] * PX_R)), int(round(h * k))), Image.LANCZOS)   # 寬度對齊量測弧長（比標題字距寬約 3%）
    ga = np.asarray(gi).astype(np.float32) / 255
    # 原圖基線位置 → 目標基線（字底對齊在 base_y + CAP/2，讓兩行中心落在 cy）
    oy = int(round(base_y + CAP / 2 - base_src * k))
    ox = int(round(TW / 2 - ga.shape[1] / 2))
    y0, x0 = max(oy, 0), max(ox, 0)
    y1, x1 = min(oy + ga.shape[0], TH), min(ox + ga.shape[1], TW)
    out[y0:y1, x0:x1] = np.maximum(out[y0:y1, x0:x1], ga[y0 - oy:y1 - oy, x0 - ox:x1 - ox])
    print(w, 'width/R = %.3f' % (ga.shape[1] / PX_R))
# 放大後的邊緣再收一點，讓筆畫邊界俐落
out = np.clip((out - .5) * 2.2 + .5, 0, 1)
Image.fromarray((out * 255).astype(np.uint8)).save(OUT, optimize=True)
print('cap src', cap_src, 'scale %.2f' % k, OUT, TW, TH)
