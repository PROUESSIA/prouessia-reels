"""Rend le logo Prouessia en PNG (fond transparent) pour les e-mails : email/logo-prouessia.png (x3) et email/icone-prouessia.png."""
import sys, os, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'moteur'))
from commun import FONTS
from playwright.async_api import async_playwright
ICON = ('<svg viewBox="0 0 24 24" width="{s}" height="{s}"><rect x="4" y="13" width="4" height="7" rx="2" fill="#fff"/>'
        '<rect x="10" y="9" width="4" height="11" rx="2" fill="#fff"/><rect x="16" y="5" width="4" height="15" rx="2" fill="#F2B705"/></svg>')
def page(txt):
    return (f'<html><head><style>{FONTS}body{{margin:0;background:transparent}}'
            '.l{display:inline-flex;align-items:center;gap:10px;font-family:Inter;font-weight:900;font-size:26px;letter-spacing:-.02em;color:#0B1B3A;padding:2px}'
            '.i{width:38px;height:38px;border-radius:11px;background:#1E40AF;display:flex;align-items:center;justify-content:center}</style></head>'
            f'<body><div class="l"><div class="i">{ICON.format(s=24)}</div>{txt}</div></body></html>')
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(device_scale_factor=3)
        for nom, txt in (('logo-prouessia', 'prouessia'), ('icone-prouessia', '')):
            await pg.set_content(page(txt)); await pg.wait_for_timeout(200)
            await pg.locator('.l').screenshot(path=f'email/{nom}.png', omit_background=True)
        await b.close()
asyncio.run(main())
