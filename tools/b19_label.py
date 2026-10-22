# Le Labo Baie 19（50ml）的標籤印字遮罩：src/tex_b19_label.png
# 標籤是一整條紙繞在圓柱瓶身上：中間是印字的方框（左右各一道直線），兩側是空白的紙。這張只畫中間的方框（含左右直線），
# 頁面上再把它貼進整條紙的中間、合成紙色與墨色。
# 位置依零售商的 50ml 正面去背照（2000px）展開圓柱後量測：方框弧長 5.52、高 3.35（瓶身半徑 R = 2）。
# 字型（放在 tools/fonts/）：打字機字 Courier Prime；品名 BAIE 19 用 Archivo Narrow Bold；Compounded／Fresh 用 Liberation Sans；最下一行用 Archivo Narrow。
# 執行：python3 tools/b19_label.py
from PIL import Image, ImageDraw, ImageFont
import os
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts')
OUT = os.path.join(HERE, '..', 'src', 'tex_b19_label.png')
W, H = 2200, 1336                                   # 方框 5.52 × 3.35 單位，每單位約 398.6px
S = 4                                               # 先畫 4 倍大再縮小（字緣平滑）
img = Image.new('L', (W*S, H*S), 0); d = ImageDraw.Draw(img)
monoL = Image.new('L', (W*S, H*S), 0)               # 打字機字另外畫一層：照片上的字比 Courier Prime Regular 粗，畫完再把筆畫加粗約 2px

def font(name, size, wght=None):
    f = ImageFont.truetype(os.path.join(FD, name), int(size*S))
    if wght is not None: f.set_variation_by_axes([wght])
    return f

def text_box(s, f, x, baseline, w=None, h_scale=1., track=0., layer=None):
    """畫一行字：x、baseline 是標籤上的像素；w 給定就把整行水平縮放成這個寬；track 是字距（em 的比例）"""
    asc, desc = f.getmetrics()
    if track:
        adv = [f.getlength(ch) + track*f.size for ch in s]; tw = sum(adv) - track*f.size
    else:
        tw = f.getlength(s)
    tmp = Image.new('L', (int(tw)+8*S, int((asc+desc)*1.)+8*S), 0); td = ImageDraw.Draw(tmp)
    if track:
        cx = 4*S
        for ch, a in zip(s, adv): td.text((cx, 4*S), ch, fill=255, font=f); cx += a
    else:
        td.text((4*S, 4*S), s, fill=255, font=f)
    sx = (w*S/tw) if w else 1.
    tmp = tmp.resize((max(1, int(tmp.width*sx)), max(1, int(tmp.height*h_scale))), Image.LANCZOS)
    (layer or img).paste(255, (int(x*S - 4*S*sx), int(baseline*S - (asc+4*S)*h_scale)), tmp)

def mono(s, x, baseline, adv):
    """打字機字：每個字的寬度（advance）固定；Courier Prime 的 advance = 0.6 em，標籤上的字 x 高度比它大一點，垂直拉長 12%"""
    f = font('CourierPrime-Regular.ttf', adv/0.6)
    text_box(s, f, x, baseline, h_scale=1.12, layer=monoL)

ink = 255
# 方框：左右兩道直線、三道橫線（線寬約 4px）
for x in (2, W-6): d.rectangle([x*S, 0, (x+4)*S, H*S], fill=ink)
for y in (336, 638, 1105): d.rectangle([0, (y-2)*S, W*S, (y+2)*S], fill=ink)
# 品名：粗的窄體黑字
text_box('BAIE 19', font('ArchivoNarrow-VF.ttf', 205, 700), 76, 184, w=720)
mono('50ml e / 1.7 FL.OZ.LIQ.', 63, 318, 62.6)
mono('eau de parfum', 66, 463, 63.8)
mono('natural spray / vaporisateur', 66, 590, 64.1)
sans = font('LiberationSans-Regular.ttf', 84)
text_box('Compounded:', sans, 66, 842, w=612)
text_box('Fresh:', sans, 66, 980, w=sans.getlength('Fresh:')/S*612/(sans.getlength('Compounded:')/S))
mono('in our lab', 726, 862, 49.7)
mono('12 months after first spray', 726, 1013, 49.9)
# 最下一行：產地、品牌（粗體、字距開）、地址
small = font('ArchivoNarrow-VF.ttf', 78, 400)
text_box('Made in USA', small, 37, 1204, w=368)
text_box('-', small, 462, 1204)
text_box('LE LABO', font('ArchivoNarrow-VF.ttf', 74, 700), 530, 1204, w=285, track=.16)
text_box('-', small, 870, 1204)
text_box('233 Elizabeth Street, New York, NY 10012 USA', small, 923, 1204, w=1241)

from PIL import ImageFilter, ImageChops
img = ImageChops.lighter(img, monoL.filter(ImageFilter.MaxFilter(9)))
out = img.resize((W, H), Image.LANCZOS)
out.save(OUT, optimize=True); print(OUT, out.size)
