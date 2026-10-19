"""Reel 10 — Délai d'intervention : sans date sur le devis, 30 jours maximum (style C, vrai ou faux).  python3 reel.py [stills [t1,t2]|video]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'moteur'))
from moteur import *

NOM = '10-delai-intervention'
WAV = os.path.join(HERE, 'voix.wav')
PH = [('h1', "Plombiers ! Vrai ou faux : sans date sur le devis, vous avez tout votre temps.", 0.0),
      ('r1', "Réponse : c'est faux.", 0.4),
      ('a1', "Chez un particulier, sans date ni délai écrits sur le devis, la loi fixe une limite.", 0.4),
      ('a2', "Vous devez intervenir sans retard injustifié, et au plus tard trente jours après son accord.", 0.4),
      ('a3', "C'est écrit dans le Code de la consommation.", 0.35),
      ('b1', "Et un devis accepté vous engage : les travaux, la durée et le prix écrits dessus.", 0.4),
      ('c1', "Notre conseil : mettez toujours une date ou un délai sur vos devis.", 0.45),
      ('d1', "Et si votre devis reste sans réponse ? Prouèssia le relance tout seul par e-mail.", 0.4),
      ('f1', "Prouèssia : les règles du plombier, en trente secondes.", 0.5)]
BORNES = [(0.0, 4.57), (5.30, 6.57), (7.28, 11.82), (12.43, 16.84), (17.48, 18.95), (19.85, 24.90), (25.65, 28.88), (29.54, 33.93), (34.66, 37.80)]
# repères mesurés sur la transcription (secondes depuis le début de la phrase)
OFF = {'vrai': 1.18, 'sans': 2.37, 'faux': 0.75, 'sansdate': 1.6, 'limite': 3.4, 'retard': 1.3, 'trente': 2.9, 'accord': 3.9,
       'code': 0.6, 'travaux': 2.3, 'duree': 3.3, 'prix': 4.1, 'date': 2.0, 'relance': 2.49}

CAL = (f'<svg width="96" height="96" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
       f'<rect x="3" y="5" width="18" height="16" rx="2" fill="#fff"/><path d="M3 10h18M8 3v4M16 3v4"/>'
       f'<text x="12" y="19" text-anchor="middle" font-size="8" font-weight="900" fill="{BLUE}" stroke="none">?</text></svg>')
MAIL = (f'<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
        f'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>')
CROSS = (f'<svg width="40" height="40" viewBox="0 0 52 52" fill="none"><path d="M14 14 L38 38 M38 14 L14 38" stroke="#C0392B" stroke-width="8" '
         f'stroke-linecap="round"/></svg>')

CAL80 = CAL.replace('width="96" height="96"', 'width="80" height="80"')
MAIL90 = MAIL.replace('width="40" height="40"', 'width="90" height="90"')
CROSS100 = CROSS.replace('width="40" height="40"', 'width="100" height="100"')


def ligne_devis(lib, val, fond='#fff'):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;width:860px;padding:22px 30px;border-radius:18px;background:{fond};'
            f'font-weight:800;font-size:46px;letter-spacing:-.02em"><span>{lib}</span><span style="color:{BLUE};font-weight:900">{val}</span></div>')


def carte_devis(lignes, titre='Devis'):
    return (f'<div style="width:940px;background:#fff;border:5px solid {INK};border-radius:28px;padding:30px 36px 34px;box-shadow:0 18px 0 {INK}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><span style="font-weight:900;font-size:58px;letter-spacing:-.03em">DEVIS</span>'
            f'<span style="font-weight:800;font-size:32px;color:{GRIS}">{titre}</span></div>{lignes}</div>')


def vf(txt, fond, coul):
    return (f'<div style="width:430px;box-sizing:border-box;text-align:center;background:{fond};color:{coul};border:5px solid {INK};border-radius:28px;'
            f'padding:18px 0;font-weight:900;font-size:96px;letter-spacing:-.03em">{txt}</div>')


def scenes(T, s):
    S = {'0': (0.0, T['r1'] - .15), '1': (T['r1'] - .1, T['a1'] - .15), '2': (T['a1'] - .1, T['a2'] - .15), '3': (T['a2'] - .1, T['a3'] - .15),
         '4': (T['a3'] - .1, T['b1'] - .15), '5': (T['b1'] - .1, T['c1'] - .15), '6': (T['c1'] - .1, T['d1'] - .15), '7': (T['d1'] - .1, T['f1'] - .15),
         '8': (T['f1'] - .1, 999)}
    for k, (a, b) in S.items(): s.bg(a, b, k == '0')
    s.logo()

    # 0 · accroche : tout lisible dès l'image 0
    a, b = S['0']
    s.tag('PLOMBIERS&nbsp;!', 0, b, top=400)
    s.el(f'<div style="display:flex;gap:40px">{vf("VRAI&nbsp;?", INK, "#fff")}{vf("FAUX&nbsp;?", MUST, INK)}</div>', 0, b, 'pop', 'left:70px;top:520px', .45)
    s.el(f'<h1 style="font-size:100px;width:940px;line-height:1.06">Sans <span class="hi">date</span> sur le devis, vous avez tout votre temps.</h1>',
         0, b, 'up', 'left:70px;top:740px', .5)
    s.el(f'<div style="width:150px;height:150px;border-radius:30px;background:{MUST};border:5px solid {INK};display:flex;align-items:center;justify-content:center">{CAL}</div>',
         T['h1'] + OFF['vrai'], b, 'pop', 'left:830px;top:1130px', .4, r=-8, w=4)
    s.el(f'<div style="font-weight:900;font-size:200px;color:{BLUE};line-height:1">?</div>', T['h1'] + OFF['sans'] + .2, b, 'pop', 'left:700px;top:1150px', .4, r=10, w=5, ph=1)
    s.sfx += [(T['h1'] + OFF['vrai'], 'tic'), (T['h1'] + OFF['sans'] + .2, 'thump')]

    # 1 · réponse : faux
    a, b = S['1']
    s.el(f'<div style="font-weight:800;font-size:64px;color:{GRIS}">Réponse&nbsp;:</div>', T['r1'] + .02, b, 'up', 'left:80px;top:470px', .4)
    s.el(f'<div style="display:flex;align-items:center;gap:30px">{vf("FAUX", INK, MUST)}<div style="width:150px;height:150px;border-radius:30px;background:#fff;border:5px solid {INK};display:flex;align-items:center;justify-content:center">{CROSS100}</div></div>',
         T['r1'] + OFF['faux'], b, 'slap', 'left:70px;top:600px', .4, w=2)
    s.sfx += [(a, 'whoosh'), (T['r1'] + OFF['faux'], 'thump')]

    # 2 · chez un particulier, sans date ni délai
    a, b = S['2']
    s.el(f'<h1 style="font-size:112px;width:940px">Chez un <span class="hi">particulier</span></h1>', T['a1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(pill(CROSS, 'Pas de date, pas de délai écrits', '#fff', 46), T['a1'] + OFF['sansdate'], b, 'slide', 'left:70px;top:760px', .4)
    s.el(fond_noir(f'La loi fixe une <span style="color:{MUST}">limite</span>', 72), T['a1'] + OFF['limite'], b, 'slap', 'left:70px;top:940px', .45, w=1.5)
    s.sfx += [(a, 'whoosh'), (T['a1'] + OFF['sansdate'] + .2, 'tic'), (T['a1'] + OFF['limite'], 'thump')]

    # 3 · 30 jours après l'accord
    a, b = S['3']
    s.el(f'<h1 style="font-size:96px;width:940px">Sans <span class="hi">retard injustifié</span></h1>', T['a2'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(f'<div style="font-weight:800;font-size:56px">et au plus tard…</div>', T['a2'] + 1.0, b, 'up', 'left:80px;top:690px', .4)
    s.el(gros('30', 'jours', BLUE, 400), T['a2'] + OFF['trente'], b, 'slap', 'left:50px;top:800px', .45, w=1.5)
    s.el(fond_noir(f'après son <span style="color:{MUST}">accord</span>', 60), T['a2'] + OFF['accord'], b, 'pop', 'left:70px;top:1180px', .4)
    s.sfx += [(a, 'whoosh'), (T['a2'] + OFF['trente'], 'thump'), (T['a2'] + OFF['accord'], 'tic')]

    # 4 · Code de la consommation
    a, b = S['4']
    s.tag('LE TEXTE', T['a3'] + .05, b)
    s.el(f'<h1 style="font-size:104px;width:940px">Code de la <span class="hi">consommation</span></h1>', T['a3'] + .05, b, 'up', 'left:70px;top:560px', .5)
    s.el(fond_noir('Article L216-1', 64), T['a3'] + OFF['code'], b, 'pop', 'left:70px;top:900px', .4, w=2)
    s.source('economie.gouv.fr · vérifié le 12.10.2026', T['a3'] + OFF['code'] + .3, b, top=1380)
    s.sfx += [(a, 'whoosh'), (T['a3'] + OFF['code'], 'tic')]

    # 5 · devis accepté = engagement
    a, b = S['5']
    s.el(f'<h1 style="font-size:100px;width:940px">Devis accepté&nbsp;: <span class="hi">vous êtes engagé</span></h1>', T['b1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    for i, (lib, k) in enumerate([('Les travaux', 'travaux'), ('La durée', 'duree'), ('Le prix', 'prix')]):
        s.el(pill(CHECK, lib), T['b1'] + OFF[k], b, 'slide', f'left:70px;top:{760 + i * 140}px', .4)
        s.sfx.append((T['b1'] + OFF[k] + .2, 'tic'))
    s.el(f'<div style="border:6px solid {BLUE};color:{BLUE};border-radius:20px;padding:6px 26px;font-weight:900;font-size:64px;letter-spacing:.04em">ENGAGÉ</div>',
         T['b1'] + 1.1, b, 'slap', 'left:620px;top:780px', .4, r=-10, w=2)
    s.sfx += [(a, 'whoosh'), (T['b1'] + 1.1, 'thump')]

    # 6 · notre conseil
    a, b = S['6']
    s.tag('NOTRE CONSEIL', T['c1'] + .05, b)
    s.el(f'<div style="width:120px;height:120px;border-radius:28px;background:{MUST};border:5px solid {INK};display:flex;align-items:center;justify-content:center">{CAL80}</div>',
         T['c1'] + 1.2, b, 'pop', 'left:860px;top:420px', .4, r=8, w=3)
    s.el(carte_devis(ligne_devis('Travaux', '…') + ligne_devis('Prix', '…') + ligne_devis('Date d’intervention', 'écrite', MUST)),
         T['c1'] + .6, b, 'up', 'left:70px;top:580px', .5)
    s.el(f'<h1 style="font-size:84px;width:940px">Une <span class="hi">date</span> ou un <span class="hi">délai</span>. Toujours.</h1>', T['c1'] + OFF['date'], b, 'up', 'left:70px;top:1150px', .45)
    s.sfx += [(a, 'whoosh'), (T['c1'] + .8, 'tic'), (T['c1'] + OFF['date'], 'thump')]

    # 7 · Prouessia
    a, b = S['7']
    s.el(f'<h1 style="font-size:124px;width:940px">Devis <span class="hi">sans réponse</span>&nbsp;?</h1>', T['d1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(f'<div style="width:130px;height:130px;border-radius:30px;background:#fff;border:5px solid {INK};display:flex;align-items:center;justify-content:center">{MAIL90}</div>',
         T['d1'] + 1.0, b, 'pop', 'left:840px;top:1100px', .4, r=-6, w=3)
    s.el(pill(MAIL, 'Relancé tout seul par e-mail', MUST, 50), T['d1'] + OFF['relance'], b, 'slide', 'left:70px;top:820px', .4)
    s.el(f'<div style="font-weight:800;font-size:44px;color:{GRIS}">avec Prouessia</div>', T['d1'] + OFF['relance'] + .7, b, 'up', 'left:80px;top:960px', .4)
    s.sfx += [(a, 'whoosh'), (T['d1'] + OFF['relance'] + .2, 'thump')]

    s.signature(T['f1'] + .05)
    s.el(f'<div style="width:110px;height:110px;border-radius:28px;background:{MUST};border:5px solid {INK}"></div>', T['f1'] + .3, 999, 'drift', 'left:880px;top:1180px', .5, r=12)
    s.source('Vérifié le 12.10.2026 · sources officielles', T['f1'] + .9, 999, top=1040)
    s.sfx += [(S['8'][0], 'whoosh')]


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'
    out = os.path.join(HERE, '..', 'sortie')
    if mode == 'stills':
        im, T = rendre(NOM, PH, scenes, WAV, debut=0.0, dossier=out, stills=[float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else 'auto', bornes=BORNES)
        planche(im, os.path.join(out, f'{NOM}_planche.png'), cols=5); print(round(T['_fin'], 1), 's', {k: round(v, 1) for k, v in T.items()})
    else:
        print(rendre(NOM, PH, scenes, WAV, bornes=BORNES, debut=0.0, dossier=out))
