"""Reel 03 — Garantie décennale : ce qu'elle couvre.  python3 reel03.py [stills [t1,t2]|video]"""
import sys
from moteur import *
from reel02 import pill, CHECK, CROSS

NOM = '03-garantie-decennale-v3'
WAV = '/home/claude/voix/03b.wav'
PH = [('h1', "Un ballon d'eau chaude ? Garanti deux ans, pas dix.", 0.0),
      ('a1', "Garantie décennale : qu'est-ce qu'elle couvre vraiment ?", 0.6),
      ('b1', "Dix ans, à partir de la réception des travaux.", 0.6),
      ('b2', "Elle vise les dommages qui menacent la solidité de l'ouvrage, ou le rendent impropre à son usage.", 0.4),
      ('c1', "Les canalisations et le chauffage central peuvent être concernés : ce sont des équipements indissociables du bâtiment.", 0.6),
      ('c3', "Le ballon, lui, se retire sans abîmer le bâti : c'est la garantie de bon fonctionnement, deux ans.", 0.6),
      ('d1', "Le constructeur professionnel doit être assuré en décennale.", 0.6),
      ('d2', "Et les références de votre assurance doivent figurer sur vos factures.", 0.35),
      ('e1', "À retenir : dix ans pour ce qui fait corps avec le bâti, deux ans pour ce qui se retire.", 0.6),
      ('f1', "Prouèssia : les règles du plombier, en trente secondes.", 0.6)]
BORNES = [(0.0, 3.45), (4.18, 6.62), (7.11, 9.8), (10.5, 15.37), (16.15, 21.94), (22.73, 28.13), (28.83, 31.71), (32.33, 35.39),
          (36.09, 41.35), (42.03, 44.94)]
OFF = {'deuxh': 1.36, 'pasdix': 2.96, 'question': 1.54, 'reception': 1.0, 'solidite': 2.1, 'impropre': 3.5, 'chauffage': 1.1, 'indiss': 3.9,
       'retire': 0.9, 'bonfonct': 3.6, 'deuxans': 5.04, 'retire2': 3.71, 'factures': 0.6}

DOC = (f'<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
       f'<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>')


def gros(nb, unite, couleur=BLUE, taille=420):
    return (f'<div style="display:flex;align-items:flex-end;gap:24px"><div style="font-weight:900;font-size:{taille}px;line-height:.8;'
            f'letter-spacing:-.07em;color:{couleur}">{nb}</div><div style="font-weight:900;font-size:{taille * .25:.0f}px;'
            f'line-height:1;letter-spacing:-.03em;padding-bottom:{taille * .04:.0f}px">{unite}</div></div>')


BARRE = 560


def scenes(T, s):
    S = {'0': (0.0, T['a1'] - .15), '1': (T['a1'] - .1, T['b1'] - .15), '2': (T['b1'] - .1, T['c1'] - .15), '3': (T['c1'] - .1, T['c3'] - .15),
         '4': (T['c3'] - .1, T['d1'] - .15), '5': (T['d1'] - .1, T['e1'] - .15), '6': (T['e1'] - .1, T['f1'] - .15),
         '7': (T['f1'] - .1, 999)}
    for k, (a, b) in S.items(): s.bg(a, b, k == '0')
    s.logo()

    a, b = S['0']
    # Image 0 : toute l'accroche est lisible ; la voix démarre tout de suite.
    s.el(f'<h1 style="font-size:124px;width:940px">Un ballon d’eau <span class="hi">chaude</span>&nbsp;?</h1>', 0, b, 'up', 'left:70px;top:420px', .5)
    s.el(f'<div style="width:330px;height:330px;border-radius:50%;background:{MUST}"></div>', T['h1'] + OFF['deuxh'], b, 'pop', 'left:58px;top:850px', .4)
    s.el(gros('2', 'ans'), 0, b, 'slap', 'left:50px;top:820px', .45)
    s.el(f'<div style="font-weight:900;font-size:120px;letter-spacing:-.05em;color:{GRIS}">pas 10&nbsp;ans</div>', 0, b, 'pop', 'left:70px;top:1230px', .45)
    s.el(f'<div style="width:{BARRE}px;height:16px;border-radius:8px;background:{INK}"></div>', T['h1'] + OFF['pasdix'], b, 'slide', 'left:62px;top:1292px', .3)
    s.sfx += [(T['h1'] + OFF['deuxh'], 'thump'), (T['h1'] + OFF['pasdix'], 'tic')]

    a, b = S['1']
    s.el(f'<h1 style="font-size:140px;width:940px">Garantie<br><span class="hi">décennale</span></h1>', T['a1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(f'<div style="background:#fff;border:5px solid {INK};border-radius:24px;padding:20px 40px;font-weight:900;font-size:72px;letter-spacing:-.03em">'
         f'Qu’est-ce qu’elle couvre&nbsp;?</div>', T['a1'] + OFF['question'], b, 'pop', 'left:70px;top:820px', .45)
    s.sfx += [(a, 'whoosh'), (T['a1'] + OFF['question'], 'thump')]

    a, b = S['2']
    s.el(gros('10', 'ans'), T['b1'] + .02, b, 'slap', 'left:50px;top:420px', .45)
    s.el(f'<div style="background:{INK};color:#fff;border-radius:20px;padding:16px 34px;font-weight:900;font-size:54px;letter-spacing:-.02em">'
         f'à partir de la <span style="color:{MUST}">réception</span></div>', T['b1'] + OFF['reception'], b, 'pop', 'left:70px;top:820px', .45)
    s.el(pill(CHECK, 'Solidité de l’ouvrage'), T['b2'] + OFF['solidite'], b, 'slide', 'left:70px;top:1010px', .4)
    s.el(pill(CHECK, 'Impropre à son usage'), T['b2'] + OFF['impropre'], b, 'slide', 'left:70px;top:1150px', .4)
    s.source('service-public.gouv.fr · vérifié le 12.10.2026', T['b1'] + 1.2, b)
    s.sfx += [(a, 'whoosh'), (T['b1'] + .02, 'thump'), (T['b2'] + OFF['solidite'] + .2, 'tic'), (T['b2'] + OFF['impropre'] + .2, 'tic')]

    a, b = S['3']
    s.el(pill(CHECK, 'Canalisations'), T['c1'] + .05, b, 'slide', 'left:70px;top:420px', .4)
    s.el(pill(CHECK, 'Chauffage central'), T['c1'] + OFF['chauffage'], b, 'slide', 'left:70px;top:560px', .4)
    s.el(f'<h1 style="font-size:104px;width:940px">Équipements <span class="hi">indissociables</span> du bâtiment</h1>',
         T['c1'] + OFF['indiss'], b, 'up', 'left:70px;top:780px', .5)
    s.el(f'<div style="font-weight:800;font-size:40px;color:{GRIS}">→ décennale, 10 ans</div>', T['c1'] + OFF['indiss'] + .7, b, 'up', 'left:74px;top:1120px', .4)
    s.sfx += [(a, 'whoosh'), (T['c1'] + .25, 'tic'), (T['c1'] + OFF['chauffage'] + .2, 'tic')]

    a, b = S['4']
    s.el(f'<h1 style="font-size:124px;width:940px">Le ballon d’eau <span class="hi">chaude</span></h1>', T['c3'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(f'<div style="font-weight:800;font-size:46px;color:{GRIS}">Il se retire sans abîmer le bâti.</div>', T['c3'] + OFF['retire'], b, 'up', 'left:74px;top:740px', .4)
    s.el(gros('2', 'ans'), T['c3'] + OFF['deuxans'], b, 'slap', 'left:50px;top:850px', .45)
    s.el(f'<div style="background:{INK};color:#fff;border-radius:20px;padding:14px 32px;font-weight:900;font-size:50px;letter-spacing:-.02em">'
         f'Garantie de <span style="color:{MUST}">bon fonctionnement</span></div>', T['c3'] + OFF['bonfonct'], b, 'pop', 'left:70px;top:1250px', .45)
    s.sfx += [(a, 'whoosh'), (T['c3'] + OFF['deuxans'], 'thump')]

    a, b = S['5']
    s.el(f'<h1 style="font-size:112px;width:940px">Constructeur pro&nbsp;: <span class="hi">assuré</span> en décennale</h1>', T['d1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(pill(DOC, 'Sur vos factures&nbsp;: votre assurance', MUST, 44), T['d2'] + OFF['factures'], b, 'slide', 'left:70px;top:900px', .4)
    s.el(f'<div style="font-weight:800;font-size:38px;color:{GRIS}">assureur · contrat · couverture géographique</div>', T['d2'] + OFF['factures'] + .9, b, 'up', 'left:80px;top:1030px', .4)
    s.sfx += [(a, 'whoosh'), (T['d2'] + OFF['factures'] + .2, 'tic')]

    a, b = S['6']
    s.tag('À RETENIR', T['e1'] + .05, b)
    s.el(f'<div style="display:flex;align-items:center;gap:30px"><div style="font-weight:900;font-size:150px;letter-spacing:-.05em;color:{BLUE}">10&nbsp;ans</div>'
         f'<div style="font-weight:800;font-size:48px;line-height:1.1">fait corps<br>avec le bâti</div></div>', T['e1'] + .9, b, 'up', 'left:70px;top:560px', .5)
    s.el(f'<div style="display:flex;align-items:center;gap:30px"><div style="font-weight:900;font-size:150px;letter-spacing:-.05em;color:{BLUE}">2&nbsp;ans</div>'
         f'<div style="font-weight:800;font-size:48px;line-height:1.1">se retire</div></div>', T['e1'] + OFF['retire2'], b, 'up', 'left:70px;top:800px', .5)
    s.sfx += [(a, 'whoosh')]

    s.signature(T['f1'] + .05)
    s.source('Vérifié le 12.10.2026 · sources officielles', T['f1'] + .9, 999, top=1040)
    s.sfx += [(S['7'][0], 'whoosh')]


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'
    if mode == 'stills':
        im, T = rendre(NOM, PH, scenes, WAV, debut=0.0, stills=[float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else 'auto', bornes=BORNES)
        planche(im, f'/home/claude/sortie/{NOM}_planche.png', cols=6); print(round(T['_fin'], 1), 's', {k: round(v, 1) for k, v in T.items()})
    else:
        print(rendre(NOM, PH, scenes, WAV, bornes=BORNES, debut=0.0))
