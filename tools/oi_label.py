"""無極烏龍（新版 Cologne Absolue）標籤遮罩。
來源：src/ref_oi_label.jpg（官方正面去背照 2000×2000 的金色標籤區，裁切範圍 x700–1290、y800–1250）。
- tex_oi_logo.png：金屬標上的白字。「Atelier Cologne」是品牌專用字形，從照片取色差遮罩、放大 6 倍、平滑後重新二值化；
  「PARIS」太小，改用 Carlito Bold 依量測位置重新排字。
- tex_oi_band.png：藍色名牌上的「OOLANG INFINI」，Carlito Bold 重新排字（量測：字寬佔名牌 312/603、字高 25/168、垂直置中、左緣 149/603）。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB='/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf'
im=Image.open(R+'/src/ref_oi_label.jpg').convert('RGB').crop((8,10,579,439))     # = 原圖 x708–1279、y810–1239（金屬標本體）
a=np.asarray(im).astype(float); r,b=a[...,0],a[...,2]
sat=(r-b)/np.maximum(r,1)
m=np.clip((.2-sat)/.1,0,1)*np.clip((b-150)/40,0,1)
m=ndimage.median_filter(m,3)
bd=14; m[:bd]=0; m[-bd:]=0; m[:,:bd]=0; m[:,-bd:]=0          # 標籤邊緣與白色背景的交界不是字
S=6
M=Image.fromarray((m*255).astype('uint8')).resize((im.width*S,im.height*S),Image.BICUBIC).filter(ImageFilter.GaussianBlur(5))
x=np.asarray(M).astype(float)/255
lab,n=ndimage.label(x>.5); sizes=ndimage.sum(np.ones_like(x),lab,range(1,n+1))
keep=np.isin(lab,1+np.where(sizes>4000)[0])
x=np.clip((x-.5)/.08+.5,0,1)*ndimage.binary_dilation(keep,iterations=6)
# PARIS：找出位置後清掉，重新排字
H,W=x.shape
lab,n=ndimage.label(x>.5); cm=ndimage.center_of_mass(x>.5,lab,range(1,n+1))
sel=[i+1 for i,(cy,cx_) in enumerate(cm) if .71*H<cy<.80*H and .3*W<cx_<.7*W]
ys,xs=np.where(np.isin(lab,sel)); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
x[y0-8:y1+9, x0-8:x1+9]=0
img=Image.fromarray((x*255).astype('uint8'))
f=ImageFont.truetype(FB,400); hb=f.getbbox('H'); capH=y1-y0
f=ImageFont.truetype(FB,int(400*capH/(hb[3]-hb[1])))
tmp=Image.new('L',(int((x1-x0)*1.6),int(capH*2)),0); d=ImageDraw.Draw(tmp)
sp=capH*.12; cx=10
for ch in 'PARIS':
    d.text((cx,int(capH*.4)-f.getbbox('H')[1]),ch,font=f,fill=255); cx+=f.getlength(ch)+sp
tmp=tmp.crop(tmp.getbbox()).resize((x1-x0,capH+1),Image.LANCZOS)
img.paste(255,(x0,y0),tmp)
img=img.resize((W//2,H//2),Image.LANCZOS)        # 1713×1287
img.save(R+'/src/tex_oi_logo.png',optimize=True); print('logo',img.size,(x0,y0,x1,y1))
# 名牌字
BW,BH=1800,int(1800*168/603)
band=Image.new('L',(BW,BH),0)
capH=BH*25/168; f=ImageFont.truetype(FB,400); hb=f.getbbox('H'); f=ImageFont.truetype(FB,int(400*capH/(hb[3]-hb[1])))
tmp=Image.new('L',(BW*2,int(capH*3)),0); d=ImageDraw.Draw(tmp); cx=20; sp=capH*.16
for ch in 'OOLANG INFINI':
    d.text((cx,int(capH)-f.getbbox('H')[1]),ch,font=f,fill=255); cx+=f.getlength(ch)+(sp*1.6 if ch==' ' else sp)
tmp=tmp.crop(tmp.getbbox()); tw=int(BW*312/603); tmp=tmp.resize((tw,int(tmp.height*tw/tmp.width)),Image.LANCZOS)
band.paste(255,(int(BW*149/603),int(BH/2-tmp.height/2)),tmp)
band.save(R+'/src/tex_oi_band.png',optimize=True); print('band',band.size,tmp.size, capH)
