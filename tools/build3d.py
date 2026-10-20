"""把 src/*-3d.src.html 的貼圖佔位（__TEX_*__）換成 data URI，輸出到根目錄的 *-3d.html。
用法：python3 tools/build3d.py [summer|esencia|goldleaf|fischersund|oolang|morning|all]"""
import base64, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
  'summer':  ('src/summer-bcn-3d.src.html', 'summer-bcn-3d.html', {
      '__TEX_LABEL__':'src/tex_label50.jpg', '__TEX_LABEL_BUMP__':'src/tex_label50_bump.jpg',
      '__TEX_CAP__':'src/tex_cap.jpg', '__TEX_CAP_BUMP__':'src/tex_cap_bump.jpg'}),
  'esencia': ('src/esencia-3d.src.html', 'esencia-3d.html', {
      '__TEX_LABEL__':'src/tex_esencia_label.jpg', '__TEX_LABEL_BUMP__':'src/tex_esencia_label_bump.jpg'}),
  'goldleaf': ('src/gold-leaf-3d.src.html', 'gold-leaf-3d.html', {
      '__TEX_FOIL__':'src/tex_gl_foil.png'}),
  'fischersund': ('src/fischersund-23-3d.src.html', 'fischersund-23-3d.html', {
      '__TEX_FS_PRINT__':'src/tex_fs23_print.png'}),
  'oolang': ('src/oolang-infini-3d.src.html', 'oolang-infini-3d.html', {
      '__TEX_OI_LOGO__':'src/tex_oi_logo.png', '__TEX_OI_BAND__':'src/tex_oi_band.png', '__TEX_OI_LETTERS__':'src/tex_oi_letters.png'}),
  'morning': ('src/morning-star-3d.src.html', 'morning-star-3d.html', {
      '__TEX_MS_PRINT__':'src/tex_ms_print.png', '__TEX_MS_EMBLEM__':'src/tex_ms_emblem.png', '__TEX_MS_RIM__':'src/tex_ms_rim.png'}),
}
def uri(p):
    mime = 'image/png' if p.endswith('.png') else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(open(os.path.join(ROOT,p),'rb').read()).decode()
def build(k):
    src, out, tex = PAGES[k]
    s = open(os.path.join(ROOT,src), encoding='utf8').read()
    for ph, f in tex.items(): s = s.replace(ph, uri(f))
    s = s.replace('__BACK_HREF__', './')
    assert '__TEX_' not in s, 'unreplaced placeholder'
    open(os.path.join(ROOT,out), 'w', encoding='utf8').write(s); print(out, len(s))
if __name__ == '__main__':
    for k in (PAGES if (len(sys.argv)<2 or sys.argv[1]=='all') else [sys.argv[1]]): build(k)
