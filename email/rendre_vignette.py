"""Vignette de la vidéo de démo pour les e-mails (email/vignette-video.png, 1200x675)."""
import sys, os, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'moteur'))
from commun import FONTS
from playwright.async_api import async_playwright
ICON = ('<svg viewBox="0 0 24 24" width="30" height="30"><rect x="4" y="13" width="4" height="7" rx="2" fill="#fff"/>'
        '<rect x="10" y="9" width="4" height="11" rx="2" fill="#fff"/><rect x="16" y="5" width="4" height="15" rx="2" fill="#F2B705"/></svg>')
H = f'''<html><head><style>{FONTS}
body{{margin:0;width:1200px;height:675px;background:#0B1B3A;font-family:Inter;color:#fff;position:relative;overflow:hidden}}
.logo{{position:absolute;left:64px;top:56px;display:flex;align-items:center;gap:14px;font-weight:900;font-size:34px;letter-spacing:-.02em}}
.logo i{{width:50px;height:50px;border-radius:14px;background:#1E40AF;display:flex;align-items:center;justify-content:center}}
.txt{{position:absolute;left:64px;top:0;bottom:0;width:700px;display:flex;flex-direction:column;justify-content:center;gap:26px}}
h1{{margin:0;font-weight:900;font-size:58px;line-height:1.1;letter-spacing:-.025em}}
h1 span{{color:#F2B705}}
p{{margin:0;font-weight:700;font-size:30px;color:#C9D1E3;width:600px;line-height:1.35}}
.play{{position:absolute;right:150px;top:215px;width:240px;height:240px;border-radius:50%;background:#F2B705;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 22px rgba(242,183,5,.18)}}
.dur{{position:absolute;right:205px;top:505px;font-weight:800;font-size:30px;background:rgba(255,255,255,.12);padding:8px 22px;border-radius:30px}}
.bar{{position:absolute;left:0;bottom:0;width:100%;height:14px;background:#F2B705}}
</style></head><body>
<div class="logo"><i>{ICON}</i>prouessia</div>
<div class="txt"><h1>Un devis sans réponse&nbsp;?<br><span>On le relance pour vous.</span></h1>
<p>Regardez comment ça marche, en&nbsp;26&nbsp;secondes.</p></div>
<div class="play"><svg width="110" height="110" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#0B1B3A"/></svg></div>
<div class="dur">▶ 0:26</div><div class="bar"></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1200, 'height': 675})
        await pg.set_content(H); await pg.wait_for_timeout(200)
        await pg.screenshot(path='email/vignette-video.png'); await b.close()
asyncio.run(main())
