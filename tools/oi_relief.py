"""無極烏龍（新版瓶身）背面的玻璃浮雕：「Atelier」七個字母錯落排在背面，四周一圈圈像等高線的波紋，
是從字母輪廓與瓶身外緣往外擴散的等距線（Yoyo 手上那瓶的背面照，透視校正後量測位置）。
字形取自金屬標上的品牌字（src/tex_oi_logo.png 的第一行）。輸出 src/tex_oi_letters.png：背面字母的遮罩（從正面看的方向，x 往右、上方是瓶肩）；波紋由頁面算距離場後在著色器裡畫。
單位與香境一致：瓶寬 W=4.6、玻璃高 GH=8.28；波紋間距 0.082（約 56 道橫過瓶寬）。"""
import numpy as np, os
from PIL import Image, ImageFilter
from scipy import ndimage
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,GH=4.6,8.28; RT,RB=.78,.46
PPU=230                                   # 每單位像素 → 1058×1904
NX,NY=int(W*PPU),int(GH*PPU)
logo=np.asarray(Image.open(R+'/src/tex_oi_logo.png')).astype(float)/255
row=logo[250:525]
# 各字母在 row 裡的欄位範圍（i 的點另外算）
G={'A':(382,599),'t':(598,684),'e':(685,869),'l':(885,948),'i':(971,1040),'e2':(1055,1240),'r':(1252,1372)}
SCALE=.0044                              # 單位／像素：A 的字高約 0.25W
# 字母中心（u 橫向 0–1、v 由上往下 0–1，背面照量測）
POS={'A':(.21,.28),'t':(.47,.165),'e':(.71,.33),'l':(.17,.465),'i':(.45,.46),'e2':(.38,.69),'r':(.67,.63)}
src=np.zeros((NY,NX),bool)
for k,(x0,x1) in G.items():
    g=row[:,x0:x1]
    ys=np.where(g.max(1)>.5)[0]; g=g[ys.min():ys.max()+1]
    im=Image.fromarray((g*255).astype('uint8'))
    w=max(1,int(im.width*SCALE*PPU)); h=max(1,int(im.height*SCALE*PPU))
    im=im.resize((w,h),Image.LANCZOS).filter(ImageFilter.GaussianBlur(PPU*.012))   # 把照片取下的字邊抹平
    a=np.asarray(im).astype(float)/255>.5
    lab,n=ndimage.label(a)                                   # 去掉裁切時帶到的旁邊字母碎片（i 的點保留）
    if n>1:
        sz=ndimage.sum(np.ones_like(a),lab,range(1,n+1)); keep=[i+1 for i,z in enumerate(sz) if z>sz.max()*(.08 if k=='i' else .3)]
        a=np.isin(lab,keep)
    u,v=POS[k]; cx,cy=int(u*NX), int(v*NY)
    x0p,y0p=cx-w//2, cy-h//2
    src[max(0,y0p):y0p+h, max(0,x0p):x0p+w] |= a[max(0,-y0p):, max(0,-x0p):][:NY-max(0,y0p),:NX-max(0,x0p)]
letters=src.copy()
# 只輸出字母的遮罩；波紋（到字母的距離一圈圈往外）在頁面載入時算距離場、在玻璃著色器裡畫，任何距離看都清楚
Image.fromarray((letters*255).astype('uint8')).save(R+'/src/tex_oi_letters.png',optimize=True); print(letters.shape)
