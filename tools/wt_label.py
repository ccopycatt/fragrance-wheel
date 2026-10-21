# OrDioLab Wise Tea 的菱形標籤：燙金（玫瑰銀箔）的字與圖樣遮罩
# 版面依 Yoyo 拍的正面、背面標籤特寫（正對標籤拍，菱形外框寬 575px、高 1170px）量測：
#   正面：Sage / Camomile / Wise Tea（Lora Medium，Camomile 寬 0.687 個標籤寬）、325S20、上下各一顆小菱形
#   背面：OrDiO 字母組合（Playfair Display Medium；r、瓶子圖示當作 i、O、D、o 錯落排列）、上下各一顆小菱形
# 輸出 src/tex_wt_label.png：貼圖範圍是標籤紙（金屬框內側的菱形）的外接長方形；R = 正面箔、G = 背面箔
from PIL import Image, ImageDraw, ImageFont
import os
R = os.path.dirname(os.path.abspath(__file__)) + '/..'
W, H, SS = 1024, 2048, 2                    # 輸出尺寸與超取樣倍數
w, h = W*SS, H*SS
LW, LH, FR = 2.6, 5.25, .11                 # 標籤外框寬高、金屬框寬（與 wise-tea-3d 的 LABEL 一致）
a, b = LW/2, LH/2
K = 1 - FR*(a*a+b*b)**.5/(a*b)              # 金屬框內側的菱形 = 外框等比縮小 K
def X(xo): return (.5 + (xo-.5)/K)*w         # 外框比例 → 貼圖像素
def Y(to): return (.5 + (to-.5)/K)*h
LORA = '/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'
PF = R + '/tools/fonts/PlayfairDisplay-Medium.ttf'

def glyph(font, s):
    """把字畫在透明底上，回傳裁到墨色範圍的灰階圖與基線在圖內的位置"""
    l, t, r, btm = font.getbbox(s)
    im = Image.new('L', (r-l+40, btm-t+40), 0); ImageDraw.Draw(im).text((20-l, 20-t), s, font=font, fill=255)
    bb = im.getbbox(); asc = font.getmetrics()[0]
    return im.crop(bb), (20-t+asc) - bb[1]    # 基線離裁切後上緣的距離

def paste_fit(dst, im, cx, cy, hh):
    """依高度 hh（像素）等比縮放，中心放在 (cx, cy)"""
    s = hh/im.height; im = im.resize((max(1, round(im.width*s)), max(1, round(hh))), Image.LANCZOS)
    dst.paste(255, (round(cx-im.width/2), round(cy-im.height/2)), im)

def diamond(d, cx, cy, ww, hh):
    d.polygon([(cx, cy-hh/2), (cx+ww/2, cy), (cx, cy+hh/2), (cx-ww/2, cy)], fill=255)

# ---- 正面
front = Image.new('L', (w, h), 0); df = ImageDraw.Draw(front)
lab_w = w/K                                       # 外框寬在貼圖上的像素寬（貼圖寬 = 內框寬 = 外框寬 × K）
size = 400
f = ImageFont.truetype(LORA, size); f.set_variation_by_name('Medium')
gw = glyph(f, 'Camomile')[0].width
size = round(size * (.687*lab_w) / gw)            # Camomile 寬 0.687 個外框寬
f = ImageFont.truetype(LORA, size); f.set_variation_by_name('Medium')
for s, tb in (('Sage', .41), ('Camomile', .487), ('Wise Tea', .564)):
    im, base = glyph(f, s)
    front.paste(255, (round(w/2-im.width/2), round(Y(tb)-base)), im)
f2 = ImageFont.truetype(LORA, 100); f2.set_variation_by_name('Medium')
im, base = glyph(f2, '325S20')
cap = Y(.626) - Y(.611)                            # 字高約 0.015 個外框高
s = cap/im.height; im = im.resize((round(im.width*s), round(cap)), Image.LANCZOS)
front.paste(255, (round(w/2-im.width/2), round(Y(.626)-cap)), im)
for t in (.165, .79): diamond(df, w/2, Y(t), .045*lab_w, Y(t+.0225)-Y(t-.0225))

# ---- 背面：OrDiO 字母組合
back = Image.new('L', (w, h), 0); db = ImageDraw.Draw(back)
pf = ImageFont.truetype(PF, 600)
for s, x0, x1, t0, t1 in (('O', .148, .391, .393, .532), ('D', .409, .63, .473, .609), ('r', .356, .487, .33, .39), ('o', .652, .779, .473, .521)):
    im = glyph(pf, s)[0]
    paste_fit(back, im, X((x0+x1)/2), (Y(t0)+Y(t1))/2, Y(t1)-Y(t0))
# 瓶子圖示（當作 i）：小圓球蓋、細頸、套環、肩部圓角的方瓶身；量測框 310–372 × 428–602（特寫裁切座標）
def bx(px): return X((px-10)/575)
def by(py): return Y((py-45)/1170)
db.ellipse([bx(329), by(430), bx(353), by(462)], fill=255)
db.rectangle([bx(334), by(456), bx(348), by(504)], fill=255)
db.rounded_rectangle([bx(322), by(500), bx(360), by(522)], radius=(bx(326)-bx(322)), fill=255)
db.rounded_rectangle([bx(310), by(517), bx(372), by(602)], radius=(bx(322)-bx(310)), fill=255)
for t in (.145, .78): diamond(db, w/2, Y(t), .045*lab_w, Y(t+.0225)-Y(t-.0225))

out = Image.merge('RGB', (front, back, Image.new('L', (w, h), 0))).resize((W, H), Image.LANCZOS)
out.save(R + '/src/tex_wt_label.png', optimize=True)
print('saved', out.size, 'K=%.4f' % K, 'font', size)
