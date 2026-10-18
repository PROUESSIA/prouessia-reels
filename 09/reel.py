"""Reel 09 — Frais de déplacement sur le devis (style B, question directe).  python3 reel.py [stills [t1,t2]|video]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'moteur'))
from moteur import *

NOM = '09-frais-deplacement'
WAV = '/home/claude/voix/09.wav'
PH = [('h1', "Plombiers ! Vous facturez le déplacement ? Alors il doit être écrit sur le devis.", 0.0),
      ('a1', "Pour un dépannage chez un particulier, le devis écrit est obligatoire dès le premier euro.", 0.45),
      ('b1', "Et le texte est clair : les frais de déplacement font partie des mentions du devis.", 0.4),
      ('b2', "À côté de la date, du lieu, de la nature des travaux et du prix.", 0.4),
      ('c1', "Sans oublier le total hors taxes, la TVA, le TTC, et la durée de validité.", 0.45),
      ('d1', "Notre conseil : une ligne à part, avec son prix. Le client sait tout avant de signer.", 0.5),
      ('e1', "Et si votre devis reste sans réponse ? Prouèssia le relance tout seul par e-mail.", 0.45),
      ('f1', "Prouèssia : les règles du plombier, en trente secondes.", 0.5)]
BORNES = [(0.0, 4.33), (4.79, 8.98), (9.41, 13.23), (13.70, 17.42), (18.08, 22.86), (23.68, 28.56), (29.25, 33.3), (34.06, 37.37)]
OFF = {'facturez': 1.03, 'alors': 2.59, 'euro': 2.7, 'frais': 1.31, 'date': .95, 'lieu': 1.55, 'nature': 2.1, 'prix': 3.23,
       'ht': .6, 'tva': 1.82, 'ttc': 2.55, 'duree': 3.5, 'ligne': 1.0, 'client': 3.41, 'relance': 2.18}

VAN = (f'<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
       f'<path d="M3 6h11v9H3zM14 9h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8" fill="{MUST}"/><circle cx="17" cy="17.5" r="1.8" fill="{MUST}"/></svg>')
MAIL = (f'<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
        f'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>')


def ligne_devis(lib, val, fond='#fff', barre=False):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;width:860px;padding:22px 30px;border-radius:18px;background:{fond};'
            f'font-weight:800;font-size:46px;letter-spacing:-.02em"><span>{lib}</span><span style="color:{BLUE};font-weight:900">{val}</span></div>')


def carte_devis(lignes):
    return (f'<div style="width:940px;background:#fff;border:5px solid {INK};border-radius:28px;padding:30px 36px 34px;box-shadow:0 18px 0 {INK}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><span style="font-weight:900;font-size:58px;letter-spacing:-.03em">DEVIS</span>'
            f'<span style="font-weight:800;font-size:32px;color:{GRIS}">Dépannage</span></div>{lignes}</div>')


def scenes(T, s):
    S = {'0': (0.0, T['a1'] - .15), '1': (T['a1'] - .1, T['b1'] - .15), '2': (T['b1'] - .1, T['b2'] - .15), '3': (T['b2'] - .1, T['c1'] - .15),
         '4': (T['c1'] - .1, T['d1'] - .15), '5': (T['d1'] - .1, T['e1'] - .15), '6': (T['e1'] - .1, T['f1'] - .15), '7': (T['f1'] - .1, 999)}
    for k, (a, b) in S.items(): s.bg(a, b, k == '0')
    s.logo()

    a, b = S['0']
    s.tag('PLOMBIERS&nbsp;!', 0, b, top=400)
    s.el(f'<h1 style="font-size:112px;width:960px;line-height:1.06">Vous facturez<br>le <span class="hi">déplacement</span>&nbsp;?</h1>', 0, b, 'up', 'left:70px;top:520px', .5)
    s.el(f'<div style="width:120px;height:120px;border-radius:28px;background:{MUST};border:5px solid {INK};display:flex;align-items:center;justify-content:center">{VAN}</div>',
         T['h1'] + OFF['facturez'], b, 'pop', 'left:850px;top:400px', .4, r=-8)
    s.el(carte_devis(ligne_devis('Frais de déplacement', '✓', MUST)), T['h1'] + OFF['alors'], b, 'slap', 'left:70px;top:860px', .45)
    s.sfx += [(T['h1'] + OFF['facturez'], 'tic'), (T['h1'] + OFF['alors'], 'thump')]

    a, b = S['1']
    s.el(f'<h1 style="font-size:116px;width:940px">Dépannage chez un <span class="hi">particulier</span></h1>', T['a1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(fond_noir(f'Devis <span style="color:{MUST}">écrit</span> obligatoire', 60), T['a1'] + 1.3, b, 'pop', 'left:70px;top:760px', .45)
    s.el(gros('1<sup style="font-size:.35em;vertical-align:top">er</sup>', 'euro', BLUE, 360), T['a1'] + OFF['euro'], b, 'slap', 'left:50px;top:930px', .45)
    s.source('Arrêté du 24 janvier 2017 · vérifié le 12.10.2026', T['a1'] + 1.6, b, top=1380)
    s.sfx += [(a, 'whoosh'), (T['a1'] + 1.3, 'tic'), (T['a1'] + OFF['euro'], 'thump')]

    a, b = S['2']
    s.tag('LE TEXTE EST CLAIR', T['b1'] + .05, b)
    s.el(carte_devis(ligne_devis('Date', '✓') + ligne_devis('Lieu', '✓') + ligne_devis('Frais de déplacement', 'obligatoire', MUST)),
         T['b1'] + OFF['frais'], b, 'up', 'left:70px;top:600px', .5)
    s.el(f'<div style="font-weight:800;font-size:40px;color:{GRIS}">une des mentions du devis détaillé</div>', T['b1'] + OFF['frais'] + 1.0, b, 'up', 'left:80px;top:1190px', .4)
    s.sfx += [(a, 'whoosh'), (T['b1'] + OFF['frais'], 'thump')]

    a, b = S['3']
    s.el(f'<h1 style="font-size:112px;width:940px">À côté de…</h1>', T['b2'] + .05, b, 'up', 'left:70px;top:420px', .5)
    for i, (lib, k) in enumerate([('La date', 'date'), ('Le lieu', 'lieu'), ('La nature des travaux', 'nature'), ('Le prix', 'prix')]):
        s.el(pill(CHECK, lib), T['b2'] + OFF[k], b, 'slide', f'left:70px;top:{640 + i * 140}px', .4)
        s.sfx.append((T['b2'] + OFF[k] + .2, 'tic'))
    s.sfx.append((a, 'whoosh'))

    a, b = S['4']
    s.el(f'<h1 style="font-size:112px;width:940px">Sans <span class="hi">oublier</span></h1>', T['c1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    for i, (lib, k) in enumerate([('Total HT', 'ht'), ('TVA', 'tva'), ('Total TTC', 'ttc')]):
        s.el(f'<div style="width:290px;box-sizing:border-box;text-align:center;background:#fff;border:5px solid {INK};border-radius:24px;padding:20px 0;font-weight:900;font-size:56px;letter-spacing:-.03em">{lib}</div>',
             T['c1'] + OFF[k], b, 'pop', f'left:{70 + i * 315}px;top:660px', .4)
        s.sfx.append((T['c1'] + OFF[k] + .1, 'tic'))
    s.el(fond_noir(f'Durée de <span style="color:{MUST}">validité</span>', 64), T['c1'] + OFF['duree'], b, 'slap', 'left:70px;top:880px', .45)
    s.sfx += [(a, 'whoosh'), (T['c1'] + OFF['duree'], 'thump')]

    a, b = S['5']
    s.tag('NOTRE CONSEIL', T['d1'] + .05, b)
    s.el(carte_devis(ligne_devis('Main-d’œuvre', '…') + ligne_devis('Pièces', '…') + ligne_devis('Frais de déplacement', 'son prix', MUST)),
         T['d1'] + OFF['ligne'], b, 'up', 'left:70px;top:580px', .5)
    s.el(f'<h1 style="font-size:84px;width:940px">Le client sait tout <span class="hi">avant de signer</span>.</h1>', T['d1'] + OFF['client'], b, 'up', 'left:70px;top:1150px', .45)
    s.sfx += [(a, 'whoosh'), (T['d1'] + OFF['ligne'] + .2, 'tic'), (T['d1'] + OFF['client'], 'thump')]

    a, b = S['6']
    s.el(f'<h1 style="font-size:124px;width:940px">Devis <span class="hi">sans réponse</span>&nbsp;?</h1>', T['e1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(pill(MAIL, 'Relancé tout seul par e-mail', MUST, 50), T['e1'] + OFF['relance'], b, 'slide', 'left:70px;top:820px', .4)
    s.el(f'<div style="font-weight:800;font-size:44px;color:{GRIS}">avec Prouessia</div>', T['e1'] + OFF['relance'] + .7, b, 'up', 'left:80px;top:960px', .4)
    s.sfx += [(a, 'whoosh'), (T['e1'] + OFF['relance'] + .2, 'thump')]

    s.signature(T['f1'] + .05)
    s.source('Vérifié le 12.10.2026 · sources officielles', T['f1'] + .9, 999, top=1040)
    s.sfx += [(S['7'][0], 'whoosh')]


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'
    if mode == 'stills':
        im, T = rendre(NOM, PH, scenes, WAV, debut=0.0, stills=[float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else 'auto', bornes=BORNES)
        planche(im, f'/home/claude/sortie/{NOM}_planche.png', cols=5); print(round(T['_fin'], 1), 's', {k: round(v, 1) for k, v in T.items()})
    else:
        print(rendre(NOM, PH, scenes, WAV, bornes=BORNES, debut=0.0))
