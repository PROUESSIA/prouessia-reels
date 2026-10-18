"""Gabarit « fiche technique » : fond papier quadrillé, cartouche, cotes, surligneur moutarde."""
import os, base64, json
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, 'icons.json'), encoding='utf8'))
ENCRE, BLEU, PAPIER, MOUT, MOUT_CL, ROUGE, VERT = '#0B1B3A', '#1E40AF', '#F7F5EF', '#CA8A04', '#F2B705', '#B42318', '#15803D'


def b64(f): return base64.b64encode(open(os.path.join(HERE, 'fonts', f), 'rb').read()).decode()


FONTS = ''.join(
    f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2')}}"
    for fam, w, f in [('Inter', 700, 'inter-latin-700-normal.woff2'), ('Inter', 800, 'inter-latin-800-normal.woff2'),
                      ('Inter', 900, 'inter-latin-900-normal.woff2'), ('Plex', 500, 'ibm-plex-mono-latin-500-normal.woff2'),
                      ('Plex', 600, 'ibm-plex-mono-latin-600-normal.woff2')])

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{font-family:'Inter',sans-serif;color:{ENCRE};background-color:{PAPIER};position:relative;
 background-image:linear-gradient(#E6E1D3 1.5px,transparent 1.5px),linear-gradient(90deg,#E6E1D3 1.5px,transparent 1.5px);
 background-size:54px 54px;background-position:27px 27px}}
.cadre{{position:absolute;left:44px;right:44px;top:200px;bottom:300px;border:3px solid {ENCRE}}}
.cadre::after{{content:'';position:absolute;inset:10px;border:1px solid {ENCRE}}}
.mono{{font-family:'Plex',monospace;font-weight:600;letter-spacing:.04em;text-transform:uppercase}}
.ent{{position:absolute;left:84px;right:84px;top:262px;display:flex;justify-content:space-between;align-items:center}}
.marque{{display:flex;align-items:center;gap:16px;font-weight:800;font-size:38px;letter-spacing:-.01em}}
.marque i{{width:56px;height:56px;border-radius:14px;background:{BLEU};display:flex;align-items:center;justify-content:center}}
.num{{font-size:28px;border:3px solid {ENCRE};padding:8px 18px;background:#fff}}
.tag{{position:absolute;left:84px;font-size:28px;background:{MOUT_CL};padding:10px 20px;color:{ENCRE}}}
h1{{position:absolute;left:84px;right:84px;font-weight:900;letter-spacing:-.03em;line-height:1.02}}
mark{{background:{MOUT_CL};color:{ENCRE};padding:0 .12em;margin:0 -.04em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.cart{{position:absolute;left:84px;right:84px;bottom:344px;display:grid;grid-template-columns:1.1fr 1.2fr .8fr;border:3px solid {ENCRE};background:#fff}}
.cart div{{padding:14px 20px;border-right:3px solid {ENCRE}}} .cart div:last-child{{border-right:0}}
.cart small{{display:block;font-family:'Plex';font-weight:500;font-size:20px;letter-spacing:.08em;color:#5B6577;text-transform:uppercase}}
.cart b{{display:block;font-weight:800;font-size:30px;margin-top:4px;line-height:1.1}}
.bl{{color:{BLEU}}}
"""


def page(corps, fiche='04 / 12', sujet='', source='', date='12.10.2026'):
    logo = ('<svg viewBox="0 0 24 24" width="32" height="32"><rect x="4" y="13" width="4" height="7" rx="2" fill="#fff"/>'
            '<rect x="10" y="9" width="4" height="11" rx="2" fill="#fff"/><rect x="16" y="5" width="4" height="15" rx="2" fill="#F2B705"/></svg>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body>'
            f'<div class="cadre"></div>'
            f'<div class="ent"><div class="marque"><i>{logo}</i>PROUESSIA</div><div class="num mono">Fiche {fiche}</div></div>'
            f'{corps}'
            f'<div class="cart"><div><small>Sujet</small><b>{sujet}</b></div><div><small>Source</small><b>{source}</b></div>'
            f'<div><small>Vérifié le</small><b>{date}</b></div></div></body></html>')


def ic(nom, taille, coul=BLEU):
    return f'<span style="display:inline-block;width:{taille}px;height:{taille}px;color:{coul}">{ICONS[nom]}</span>'


def cote_h(x1, x2, y, label, big=False):
    """Ligne de cote horizontale avec flèches et libellé centré."""
    fs = 34 if big else 28
    w = x2 - x1
    return (f'<svg style="position:absolute;left:{x1}px;top:{y - 70}px" width="{w}" height="120" viewBox="0 0 {w} 120">'
            f'<line x1="2" y1="40" x2="2" y2="100" stroke="{BLEU}" stroke-width="4"/><line x1="{w - 2}" y1="40" x2="{w - 2}" y2="100" stroke="{BLEU}" stroke-width="4"/>'
            f'<line x1="2" y1="70" x2="{w - 2}" y2="70" stroke="{BLEU}" stroke-width="4"/>'
            f'<path d="M2 70 l22 -11 v22z M{w - 2} 70 l-22 -11 v22z" fill="{BLEU}"/>'
            f'<rect x="{w / 2 - len(label) * fs * .36 - 18}" y="46" width="{len(label) * fs * .72 + 36}" height="48" fill="{PAPIER}"/>'
            f'<text x="{w / 2}" y="82" text-anchor="middle" font-family="Plex" font-weight="600" font-size="{fs}" fill="{BLEU}" letter-spacing="1">{label}</text></svg>')


def frame_couverture():
    doc = (f'<svg style="position:absolute;left:230px;top:872px" width="620" height="560" viewBox="0 0 620 560" fill="none">'
           f'<rect x="4" y="4" width="500" height="540" rx="10" fill="#fff" stroke="{ENCRE}" stroke-width="5"/>'
           f'<rect x="40" y="40" width="220" height="26" fill="{ENCRE}"/><rect x="40" y="80" width="150" height="14" fill="#9AA3B5"/>'
           + ''.join(f'<rect x="40" y="{128 + i * 50}" width="30" height="30" rx="4" stroke="{BLEU}" stroke-width="4"/>'
                     f'<rect x="92" y="{137 + i * 50}" width="{[300, 250, 340, 210, 280, 320, 260, 230][i]}" height="14" fill="#C9CFDB"/>' for i in range(8))
           + ''.join(f'<path d="M46 {143 + i * 50} l9 10 l17 -22" stroke="{BLEU}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>' for i in range(7))
           + f'<rect x="80" y="{128 + 7 * 50 - 8}" width="400" height="46" fill="{MOUT_CL}" opacity=".9"/>'
           f'<rect x="92" y="{137 + 7 * 50}" width="230" height="14" fill="{ENCRE}"/>'
           f'<line x1="570" y1="4" x2="570" y2="544" stroke="{BLEU}" stroke-width="4"/><line x1="548" y1="4" x2="592" y2="4" stroke="{BLEU}" stroke-width="4"/><line x1="548" y1="544" x2="592" y2="544" stroke="{BLEU}" stroke-width="4"/>'
           f'<path d="M570 4 l-11 22 h22z M570 544 l-11 -22 h22z" fill="{BLEU}"/>'
           f'<rect x="548" y="200" width="44" height="160" fill="{PAPIER}"/>'
           f'<text transform="rotate(-90 570 280)" x="570" y="290" text-anchor="middle" font-family="Plex" font-weight="600" font-size="28" fill="{BLEU}" letter-spacing="1">8 MENTIONS</text></svg>')
    corps = (f'<div class="tag mono" style="top:372px">Ce que dit le texte</div>'
             f'<h1 style="top:450px;font-size:112px">Votre devis de dépannage est-il <mark>complet</mark>&nbsp;?</h1>' + doc)
    return page(corps, '01 / 12', 'Devis de dépannage', 'Arrêté du 24 janv. 2017')


def frame_chiffres():
    corps = (f'<div class="tag mono" style="top:372px">Entretien chaudière</div>'
             f'<h1 style="top:450px;font-size:112px">La loi impose <mark>une visite</mark> par an</h1>'
             f'<div style="position:absolute;left:84px;top:790px;display:flex;align-items:flex-end;gap:26px">'
             f'<div class="bl" style="font-weight:900;font-size:430px;line-height:.8;letter-spacing:-.06em">1</div>'
             f'<div style="font-weight:800;font-size:60px;line-height:1.05;padding-bottom:10px">visite<br>par an</div></div>'
             + cote_h(84, 996, 1160, '4 kW  →  400 kW', True)
             + f'<div class="mono" style="position:absolute;left:84px;top:1196px;font-size:26px;color:#5B6577">Chaudières concernées</div>'
             + cote_h(84, 700, 1330, '15 JOURS')
             + f'<div class="mono" style="position:absolute;left:84px;top:1366px;font-size:26px;color:#5B6577">Délai pour remettre l’attestation</div>')
    return page(corps, '03 / 12', 'Entretien chaudière', 'Décret n° 2009-649')


def frame_liste():
    rows = ["Date du devis", "Nom du client", "Lieu d’exécution", "Nature exacte des réparations", "Quantités et prix unitaires",
            "Frais de déplacement", "Total HT, TVA et TTC", "Durée de validité"]
    items = ''
    for i, r in enumerate(rows):
        y = 700 + i * 84
        hl = (i == 7)
        box = (f'<svg style="position:absolute;left:84px;top:{y}px" width="52" height="52" viewBox="0 0 52 52" fill="none">'
               f'<rect x="3" y="3" width="46" height="46" rx="6" stroke="{BLEU}" stroke-width="5" fill="#fff"/>'
               + (f'<path d="M13 27 l9 10 l18 -22" stroke="{BLEU}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' if i < 7 else '') + '</svg>')
        label = f'<div style="position:absolute;left:162px;top:{y + 2}px;font-weight:800;font-size:42px;line-height:1.1;letter-spacing:-.01em"><span style="{"background:" + MOUT_CL + ";padding:2px 10px;margin-left:-10px" if hl else ""}">{r}</span></div>'
        sep = f'<div style="position:absolute;left:84px;right:84px;top:{y + 66}px;border-top:2px dashed #C9CFDB"></div>' if i < 7 else ''
        items += box + label + sep
    corps = (f'<div class="tag mono" style="top:372px">À vérifier avant d’envoyer</div>'
             f'<h1 style="top:450px;font-size:104px"><span class="bl">8</span> mentions sur votre devis</h1>' + items)
    return page(corps, '01 / 12', 'Devis de dépannage', 'Arrêté du 24 janv. 2017')


def rendre(sortie):
    frames = [frame_couverture(), frame_chiffres(), frame_liste()]
    ims = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch(args=['--no-sandbox'])
        pg = nav.new_page(viewport={'width': 1080, 'height': 1920})
        for i, f in enumerate(frames):
            pg.set_content(f); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
            p = os.path.join(HERE, f'fiche{i}.png'); pg.screenshot(path=p); ims.append(Image.open(p).convert('RGB'))
        nav.close()
    w, h = 540, 960; g = 28
    m = Image.new('RGB', (w * 3 + g * 4, h + g * 2), (236, 233, 224))
    for i, im in enumerate(ims): m.paste(im.resize((w, h), Image.LANCZOS), (g + i * (w + g), g))
    m.save(sortie)
    return ims


if __name__ == '__main__':
    rendre(os.path.join(HERE, 'fiche-apercu.png'))
