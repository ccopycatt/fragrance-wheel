import numpy as np
from PIL import Image, ImageDraw, ImageFont
PAG='/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-regular.otf'
ADV='/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreadventor-regular.otf'
CAR='/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf'
PPU=340                     # 每單位像素
X0,X1,Y0,Y1=-3.0,3.0,1.5,8.0
W,H=int((X1-X0)*PPU), int((Y1-Y0)*PPU)
img=Image.new('L',(W,H),0); d=ImageDraw.Draw(img)
px=lambda x:(x-X0)*PPU; py=lambda y:(Y1-y)*PPU
def line(parts, cx, top, base, width, track=.10, stroke=0):
    """parts: [(text, font, scale)]；字母底線對齊 base，總寬 = width（以字距調整）、置中於 cx"""
    capH=(top-base)*PPU
    # 先依大寫字高決定字級
    def fsize(fp,scale):
        f=ImageFont.truetype(fp,400); bb=f.getbbox('H'); return int(400*capH*scale/(bb[3]-bb[1]))
    glyphs=[]
    for text,fp,scale in parts:
        f=ImageFont.truetype(fp,fsize(fp,scale))
        for ch in text: glyphs.append((ch,f))
    def total(sp):
        x=0; xs=[]
        for ch,f in glyphs: xs.append(x); x+=f.getlength(ch)+(sp if ch!=' ' else sp*1.2)
        return x-sp, xs
    sp=capH*track; w,xs=total(sp)
    tmp=Image.new('L',(int(w)+40,int(capH*2.2)),0); td=ImageDraw.Draw(tmp); yb0=int(capH*1.6)
    for (ch,f),x in zip(glyphs,xs):
        bb=f.getbbox('H'); td.text((20+x, yb0-bb[3]), ch, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    bb=tmp.getbbox(); tmp=tmp.crop((bb[0],0,bb[2],tmp.height))
    nw=int(width*PPU); tmp=tmp.resize((nw,tmp.height),Image.LANCZOS)
    img.paste(255, (int(px(cx)-nw/2), int(py(base))-yb0), tmp)
# 標誌：正方形外框＋同心、稍大的圓
s=1.70; cx,cy=0,6.75; lw=int(.032*PPU)
d.rectangle([px(cx-s/2),py(cy+s/2),px(cx+s/2),py(cy-s/2)], outline=255, width=lw)
R=s*1.085/2; d.ellipse([px(cx-R),py(cy+R),px(cx+R),py(cy-R)], outline=255, width=lw)
line([('O',PAG,1.0),('RMONDE ',PAG,.80),('J',PAG,1.0),('AYNE',PAG,.80)], 0, 5.25, 4.88, 5.17, .06, 1)
line([('GOLD LEAF',ADV,1.0)], 0, 3.80, 3.44, 2.99, .08, 1)
line([('EAU DE PARFUM',ADV,1.0)], 0, 3.25, 3.03, 2.49, .12, 1)
line([('CREATED IN LONDON',CAR,1.0)], 0, 2.11, 1.90, 3.22, .14, 1)
img.save('foil_mask.png', optimize=True)
print(W,H)
