# 「№ 23」印字遮罩：Inter SemiBold，依官方正面照量測的字寬 1.61、字高 0.47（單位：瓶寬 4.6）
from PIL import Image, ImageDraw, ImageFont
PPU=600; TW,TH=2.3,.9
W,H=int(TW*PPU),int(TH*PPU)
img=Image.new('L',(W,H),0); d=ImageDraw.Draw(img)
f=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf',400)
txt='№ 23'
bb=d.textbbox((0,0),txt,font=f); capH=f.getbbox('H')[3]-f.getbbox('H')[1]
tmp=Image.new('L',(bb[2]-bb[0]+40,int(capH*1.8)),0); td=ImageDraw.Draw(tmp)
hb=f.getbbox('H'); td.text((20-bb[0], int(capH*.4)-hb[1]), txt, font=f, fill=255)
box=tmp.getbbox(); tmp=tmp.crop(box)
tw,th=int(1.61*PPU), int(.47*PPU*(tmp.height/capH))
tmp=tmp.resize((tw, int(tmp.height*(.47*PPU)/capH)), Image.LANCZOS)
img.paste(tmp, ((W-tmp.width)//2, (H-int(.47*PPU))//2 - (tmp.height-int(.47*PPU))))
img.save('print_mask.png', optimize=True); print(W,H,tmp.size)
