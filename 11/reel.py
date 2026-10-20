"""Reel 11 — Validité du devis de dépannage (style D, l'oubli).  python3 reel.py [stills [t1,t2]|video]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'moteur'))
from moteur import *

NOM = '11-validite-devis'
WAV = os.path.join(HERE, 'voix.wav')
PH = [('h1', "Plombiers ! Une ligne obligatoire sur votre devis de dépannage : sa durée de validité.", 0.0),
      ('a1', "Chez un particulier, un devis écrit est obligatoire dès le premier euro.", 0.35),
      ('a2', "C'est l'arrêté du vingt-quatre janvier deux mille dix-sept.", 0.35),
      ('a3', "Il liste les mentions : la date, le client, le lieu, les réparations, les prix, le déplacement.", 0.35),
      ('a4', "Et aussi : la durée de validité de l'offre.", 0.3),
      ('c1', "Notre conseil : écrivez-la en clair, par exemple, offre valable un mois.", 0.4),
      ('d1', "Et si le devis reste sans réponse ? Prouèssia le relance tout seul par e-mail.", 0.35),
      ('k1', "Écrivez DEVIS en commentaire : on vous envoie notre fiche à imprimer.", 0.35),
      ('f1', "Prouèssia : les règles du plombier, en trente secondes.", 0.45)]
BORNES = [(0.0, 5.34), (5.91, 9.57), (10.05, 12.10), (12.78, 19.10), (19.78, 22.08), (22.89, 27.36), (28.15, 32.19), (32.78, 35.99), (36.63, 39.76)]
# repères mesurés sur la transcription (secondes depuis le début de la phrase)
OFF = {'ligne': 1.3, 'duree': 4.0, 'part': 0.5, 'euro': 2.9, 'an': 1.3,
       'date': 1.0, 'client': 2.4, 'lieu': 3.0, 'repa': 4.0, 'prix': 4.9, 'depl': 5.8,
       'valid': 1.0, 'clair': 1.3, 'mois': 3.45, 'relance': 2.2, 'devis': 0.5}

MAIL = (f'<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
        f'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>')
MAIL90 = MAIL.replace('width="40" height="40"', 'width="90" height="90"')
LOUPE = (f'<svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round">'
         f'<circle cx="10" cy="10" r="6.5" fill="#fff"/><path d="M15 15l6 6"/></svg>')
ROUGE = '#C0392B'


def ligne(lib, val='', fond='#fff', taille=44):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;width:860px;padding:16px 28px;border-radius:16px;background:{fond};'
            f'font-weight:800;font-size:{taille}px;letter-spacing:-.02em;border-bottom:3px dashed #D9D4C7"><span>{lib}</span>'
            f'<span style="color:{BLUE};font-weight:900">{val}</span></div>')


def carte(lignes, titre='Dépannage'):
    return (f'<div style="width:940px;background:#fff;border:5px solid {INK};border-radius:28px;padding:26px 36px 30px;box-shadow:0 18px 0 {INK}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><span style="font-weight:900;font-size:58px;letter-spacing:-.03em">DEVIS</span>'
            f'<span style="font-weight:800;font-size:32px;color:{GRIS}">{titre}</span></div>{lignes}</div>')


def cercle(larg, haut):
    return (f'<div style="width:{larg}px;height:{haut}px;border:8px solid {ROUGE};border-radius:{haut // 2}px;box-sizing:border-box"></div>')


def scenes(T, s):
    S = {'0': (0.0, T['a1'] - .15), '1': (T['a1'] - .1, T['a2'] - .15), '2': (T['a2'] - .1, T['a3'] - .15), '3': (T['a3'] - .1, T['a4'] - .15),
         '4': (T['a4'] - .1, T['c1'] - .15), '5': (T['c1'] - .1, T['d1'] - .15), '6': (T['d1'] - .1, T['k1'] - .15), '7': (T['k1'] - .1, T['f1'] - .15),
         '8': (T['f1'] - .1, 999)}
    for k, (a, b) in S.items(): s.bg(a, b, k == '0')
    s.logo()

    # 0 · accroche : tout lisible dès l'image 0 — le devis zoomé, la ligne manquante entourée
    a, b = S['0']
    s.tag('PLOMBIERS&nbsp;!', 0, b, top=380)
    s.el(f'<h1 style="font-size:92px;width:940px;line-height:1.06">Une ligne <span class="hi">obligatoire</span> sur votre devis de dépannage</h1>',
         0, b, 'up', 'left:70px;top:490px', .5)
    s.el(carte(ligne('Réparation', '…') + ligne('Prix', '…') + ligne('Durée de validité', '?', '#FFF4D6')),
         0, b, 'up', 'left:70px;top:880px', .5)
    s.el(cercle(912, 116), T['h1'] + OFF['ligne'], b, 'pop', 'left:84px;top:1158px', .4, w=2)
    s.el(f'<div style="width:140px;height:140px;border-radius:30px;background:{MUST};border:5px solid {INK};display:flex;align-items:center;justify-content:center">{LOUPE}</div>',
         T['h1'] + 1.0, b, 'pop', 'left:860px;top:760px', .4, r=-8, w=4)
    s.sfx += [(T['h1'] + 1.0, 'tic'), (T['h1'] + OFF['ligne'], 'thump'), (T['h1'] + OFF['duree'], 'tic')]

    # 1 · chez un particulier, dès le premier euro
    a, b = S['1']
    s.el(f'<h1 style="font-size:112px;width:940px">Chez un <span class="hi">particulier</span></h1>', T['a1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(pill(DOC, 'Devis écrit obligatoire', '#fff', 50), T['a1'] + 1.4, b, 'slide', 'left:70px;top:720px', .4)
    s.el(f'<div style="font-weight:800;font-size:60px">dès le…</div>', T['a1'] + 2.2, b, 'up', 'left:80px;top:880px', .4)
    s.el(gros('1<sup style="font-size:.35em">er</sup>', 'euro', BLUE, 340), T['a1'] + OFF['euro'], b, 'slap', 'left:60px;top:980px', .45, w=1.5)
    s.el(f'<div style="width:110px;height:110px;border-radius:28px;background:{MUST};border:5px solid {INK}"></div>', T['a1'] + .4, b, 'drift', 'left:880px;top:1250px', .5, r=12)
    s.sfx += [(a, 'whoosh'), (T['a1'] + 1.6, 'tic'), (T['a1'] + OFF['euro'], 'thump')]

    # 2 · le texte
    a, b = S['2']
    s.tag('LE TEXTE', T['a2'] + .05, b)
    s.el(f'<h1 style="font-size:104px;width:940px">Arrêté du <span class="hi">24 janvier 2017</span></h1>', T['a2'] + .05, b, 'up', 'left:70px;top:560px', .5)
    s.el(fond_noir('Devis de dépannage à domicile', 54), T['a2'] + OFF['an'], b, 'pop', 'left:70px;top:900px', .4, w=2)
    s.source('Légifrance · DGCCRF · vérifié le 12.10.2026', T['a2'] + OFF['an'] + .2, b, top=1380)
    s.sfx += [(a, 'whoosh'), (T['a2'] + OFF['an'], 'tic')]

    # 3 · les mentions, cochées une à une
    a, b = S['3']
    s.el(f'<h1 style="font-size:84px;width:940px">Les <span class="hi">mentions</span></h1>', T['a3'] + .05, b, 'up', 'left:70px;top:400px', .5)
    items = [('La date', 'date'), ('Le client', 'client'), ('Le lieu', 'lieu'), ('Les réparations', 'repa'), ('Les prix', 'prix'), ('Le déplacement', 'depl')]
    for i, (lib, k) in enumerate(items):
        x, y = (70 if i % 2 == 0 else 560), 560 + (i // 2) * 150
        s.el(pill(CHECK, lib, '#fff', 40), T['a3'] + OFF[k], b, 'slide', f'left:{x}px;top:{y}px', .35)
        s.sfx.append((T['a3'] + OFF[k] + .15, 'tic'))
    s.el(f'<div style="width:110px;height:110px;border-radius:28px;background:{MUST};border:5px solid {INK}"></div>', T['a3'] + .4, b, 'drift', 'left:880px;top:1100px', .5, r=12)
    s.sfx += [(a, 'whoosh')]

    # 4 · et la durée de validité (la ligne oubliée)
    a, b = S['4']
    s.el(f'<h1 style="font-size:96px;width:940px">Et aussi&nbsp;:</h1>', T['a4'] + .05, b, 'up', 'left:70px;top:420px', .45)
    s.el(carte(ligne('Déplacement', '✓') + ligne('Total TTC', '✓') + ligne('Durée de validité', '?', '#FFF4D6', 50)),
         T['a4'] + .3, b, 'up', 'left:70px;top:580px', .45)
    s.el(cercle(900, 120), T['a4'] + OFF['valid'], b, 'slap', 'left:90px;top:870px', .4, w=2)
    s.el(fond_noir(f'<span style="color:{MUST}">obligatoire</span> aussi', 64), T['a4'] + OFF['valid'] + .5, b, 'pop', 'left:70px;top:1150px', .4, r=-3)
    s.sfx += [(a, 'whoosh'), (T['a4'] + OFF['valid'], 'thump')]

    # 5 · notre conseil
    a, b = S['5']
    s.tag('NOTRE CONSEIL', T['c1'] + .05, b)
    s.el(f'<h1 style="font-size:96px;width:940px">Écrivez-la <span class="hi">en clair</span></h1>', T['c1'] + OFF['clair'], b, 'up', 'left:70px;top:560px', .45)
    s.el(carte(ligne('Durée de validité', 'un mois', MUST, 50), 'exemple'), T['c1'] + 2.4, b, 'up', 'left:70px;top:800px', .45)
    s.el(f'<div style="font-weight:900;font-size:58px;color:{BLUE}">« Offre valable un mois »</div>', T['c1'] + OFF['mois'], b, 'pop', 'left:80px;top:1130px', .4, w=1.5)
    s.sfx += [(a, 'whoosh'), (T['c1'] + 2.5, 'tic'), (T['c1'] + OFF['mois'], 'thump')]

    # 6 · Prouessia
    a, b = S['6']
    s.el(f'<h1 style="font-size:124px;width:940px">Devis <span class="hi">sans réponse</span>&nbsp;?</h1>', T['d1'] + .05, b, 'up', 'left:70px;top:420px', .5)
    s.el(pill(MAIL, 'Relancé tout seul par e-mail', MUST, 50), T['d1'] + OFF['relance'], b, 'slide', 'left:70px;top:820px', .4)
    s.el(f'<div style="font-weight:800;font-size:44px;color:{GRIS}">avec Prouessia</div>', T['d1'] + OFF['relance'] + .6, b, 'up', 'left:80px;top:960px', .4)
    s.el(f'<div style="width:130px;height:130px;border-radius:30px;background:#fff;border:5px solid {INK};display:flex;align-items:center;justify-content:center">{MAIL90}</div>',
         T['d1'] + .9, b, 'pop', 'left:840px;top:1120px', .4, r=-6, w=3)
    s.sfx += [(a, 'whoosh'), (T['d1'] + OFF['relance'] + .2, 'thump')]

    # 7 · mot-clé DEVIS
    a, b = S['7']
    s.el(f'<div style="font-weight:800;font-size:60px">Écrivez en commentaire&nbsp;:</div>', T['k1'] + .05, b, 'up', 'left:70px;top:440px', .4)
    s.el(f'<div style="background:{INK};color:{MUST};border-radius:28px;padding:20px 60px;font-weight:900;font-size:180px;letter-spacing:.02em">DEVIS</div>',
         T['k1'] + OFF['devis'], b, 'slap', 'left:70px;top:580px', .4, w=2)
    s.el(pill(DOC, 'Notre fiche à imprimer', '#fff', 48), T['k1'] + 1.7, b, 'slide', 'left:70px;top:920px', .4)
    s.el(f'<div style="font-weight:800;font-size:44px;color:{GRIS}">en message privé</div>', T['k1'] + 2.2, b, 'up', 'left:80px;top:1060px', .4)
    s.sfx += [(a, 'whoosh'), (T['k1'] + OFF['devis'], 'thump'), (T['k1'] + 1.8, 'tic')]

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
