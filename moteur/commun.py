"""Identité Prouessia pour les PDF (fiches à imprimer, fiches sources)."""
import os, base64
from playwright.sync_api import sync_playwright

FONTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
INK, BLUE, MUST, PAPIER, GRIS, LIGNE = '#0B1B3A', '#1E40AF', '#F2B705', '#F7F5EF', '#5B6577', '#D9D5C7'


def _b64(f):
    return base64.b64encode(open(os.path.join(FONTDIR, f), 'rb').read()).decode()


FONTS = ''.join(
    f"@font-face{{font-family:'Inter';font-weight:{w};src:url(data:font/woff2;base64,{_b64(f)}) format('woff2')}}"
    for w, f in [(700, 'inter-latin-700-normal.woff2'), (800, 'inter-latin-800-normal.woff2'), (900, 'inter-latin-900-normal.woff2')])

LOGO = ('<div class="logo"><i><svg viewBox="0 0 24 24" width="17" height="17"><rect x="4" y="13" width="4" height="7" rx="2" fill="#fff"/>'
        '<rect x="10" y="9" width="4" height="11" rx="2" fill="#fff"/><rect x="16" y="5" width="4" height="15" rx="2" fill="#F2B705"/></svg></i>prouessia</div>')

BASE_CSS = f"""
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:210mm;height:297mm}}
body{{font-family:'Inter',sans-serif;font-weight:700;color:{INK};background:{PAPIER};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{position:relative;width:210mm;height:297mm;padding:13mm 14mm 11mm;overflow:hidden;display:flex;flex-direction:column}}
.logo{{display:flex;align-items:center;gap:8px;font-weight:900;font-size:17px;letter-spacing:-.01em}}
.logo i{{width:30px;height:30px;border-radius:9px;background:{BLUE};display:flex;align-items:center;justify-content:center}}
.hi{{background:{MUST};border-radius:.22em;padding:0 .16em .03em}}
.tag{{display:inline-block;background:{MUST};border-radius:7px;padding:3px 10px;font-weight:900;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase}}
.card{{background:#fff;border:2px solid {INK};border-radius:13px}}
a{{color:{BLUE};text-decoration:underline;text-underline-offset:2px}}
.muted{{color:{GRIS}}}
"""


def pdf(html, sortie, png=None):
    with sync_playwright() as pw:
        nav = pw.chromium.launch(args=['--no-sandbox'])
        pg = nav.new_page(viewport={'width': 794, 'height': 1123})
        pg.set_content(html); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        over = pg.evaluate("(()=>{const p=document.querySelector('.page');return p.scrollHeight-p.clientHeight})()")
        pg.pdf(path=sortie, format='A4', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        if png:
            pg.screenshot(path=png, full_page=True)
        nav.close()
    return over
