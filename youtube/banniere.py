"""Bannière YouTube 2560×1440 (zone sûre centrale 1546×423) → youtube/banniere.png"""
import os, sys, base64
sys.path.insert(0, 'moteur')
from commun import FONTS, INK, MUST
from playwright.sync_api import sync_playwright
ico = base64.b64encode(open('email/icone-prouessia.png','rb').read()).decode()
html = f"""<html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:2560px;height:1440px;background:{INK};font-family:Inter,sans-serif;position:relative;overflow:hidden}}
.bande{{position:absolute;left:0;right:0;top:0;height:1440px;
 background:linear-gradient(180deg,#000 0,#000 420px,{INK} 420px,{INK} 1020px,#000 1020px)}}
.trait{{position:absolute;left:0;right:0;height:10px;background:{MUST}}}
.zone{{position:absolute;left:507px;top:508px;width:1546px;height:423px;display:flex;align-items:center;gap:50px;justify-content:center}}
.zone img{{width:170px;height:170px;border-radius:38px;flex:none}}
.nom{{color:#fff;font-weight:900;font-size:50px;letter-spacing:-.01em;margin-bottom:14px;opacity:.85}}
h1{{color:#fff;font-weight:900;font-size:80px;line-height:1.05;letter-spacing:-.03em}}
h1 b{{background:{MUST};color:{INK};padding:0 18px;border-radius:16px}}
.sous{{color:#fff;opacity:.8;font-weight:700;font-size:36px;margin-top:20px}}
.sous span{{color:{MUST};opacity:1}}
</style></head><body><div class="bande"></div>
<div class="trait" style="top:410px"></div><div class="trait" style="top:1020px"></div>
<div class="zone"><img src="data:image/png;base64,{ico}"><div>
<div class="nom">prouessia</div>
<h1>Le partenaire <b>des plombiers</b></h1>
<div class="sous">Devis, factures, règles du métier · <span>prouessia.fr</span></div>
</div></div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':2560,'height':1440})
    pg.set_content(html); pg.wait_for_timeout(400)
    pg.screenshot(path='youtube/banniere.png'); b.close()
from PIL import Image
im = Image.open('youtube/banniere.png'); print(im.size, os.path.getsize('youtube/banniere.png')//1024, 'Ko')
im.crop((507,508,2053,931)).save('/tmp/claude-0/-home-claude/0d2ec442-8b50-5cf5-89e8-ff56ed7ae875/scratchpad/zone.png')
im.resize((1280,720)).save('/tmp/claude-0/-home-claude/0d2ec442-8b50-5cf5-89e8-ff56ed7ae875/scratchpad/apercu.png')
