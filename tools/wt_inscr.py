"""賢者茶香境：柱頭方板（abacus）側面刻的德爾斐格言遮罩 → src/tex_wt_inscr.png
上半：ΓΝΩΘΙ ΣΑΥΤΟΝ（認識你自己，朝前）；下半：ΜΗΔΕΝ ΑΓΑΝ（凡事勿過度，朝右）。
古典時期阿提卡碑文的寫法：等寬的方格排列（stoichedon），字母是粗細一致、沒有襯線的大寫；用 DejaVu Sans 的希臘大寫，
每個字母放進同寬的格子裡置中。白 = 刻進去的字。"""
from PIL import Image, ImageDraw, ImageFont
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
W, H = 2048, 512
im = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(im)
font = ImageFont.truetype(FONT, 150)
def row(txt, y0, cells):
    cw = W * .92 / cells; x0 = (W - cw * len(txt)) / 2          # 每列都置中
    for i, ch in enumerate(txt):
        if ch == ' ': continue
        cx = x0 + cw * (i + .5)
        d.text((cx, y0 + 128), ch, font=font, fill=255, anchor='mm', stroke_width=3, stroke_fill=255)
row('ΓΝΩΘΙ ΣΑΥΤΟΝ', 0, 13)
row('ΜΗΔΕΝ ΑΓΑΝ', 256, 13)
im.save(os.path.join(ROOT, 'src/tex_wt_inscr.png'), optimize=True)
print('ok', im.size)
