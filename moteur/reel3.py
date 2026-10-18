"""Reel « fiche technique » n°1 : devis de dépannage. python3 reel3.py [rapide]"""
import os, re, sys, shutil, subprocess, json
import numpy as np
from playwright.sync_api import sync_playwright
import fiche as F
import voix as V

HERE = F.HERE
ENCRE, BLEU, PAPIER, MOUT_CL, VERT = F.ENCRE, F.BLEU, F.PAPIER, F.MOUT_CL, F.VERT
FPS = 30
GAP = 0.22

ROWS = ["Date", "Nom du client", "Lieu", "Réparations", "Prix × quantité", "Déplacement", "Total HT · TVA · TTC",
        "Durée de validité", "Payant ou gratuit", "Pièces + « Lu et approuvé »"]

# (clé, légende avec *emphase*, texte parlé, pause avant)
PH = [
    ('a1', "Dès *le premier euro*, un dépannage chez un particulier exige un devis écrit.", None, 0.5),
    ('b1', "Le vôtre est-il *complet* ?", None, 0.55),
    ('c0', "*Dix points* à vérifier.", "Dix points à vérifier.", 0.5),
    ('r0', "La date de rédaction.", None, 0.35),
    ('r1', "Le nom du client.", None, GAP),
    ('r2', "Le lieu d'exécution.", None, GAP),
    ('r3', "La nature exacte des réparations.", None, GAP),
    ('r4', "Le détail : prix unitaire et quantité.", None, GAP),
    ('r5', "Les frais de déplacement.", None, GAP),
    ('r6', "Le total hors taxes, la TVA, et le total toutes taxes.", None, GAP),
    ('r7', "La durée de validité de l'offre.", None, GAP),
    ('r8', "Puis : *payant ou gratuit* ?", "Puis : le devis est-il payant, ou gratuit ?", 0.45),
    ('r9', "Et le choix du client sur les *pièces remplacées*, signé « Lu et approuvé ».", None, 0.3),
    ('d1', "*À retenir* : relisez votre modèle une fois. Il servira à chaque dépannage.", None, 0.7),
    ('e1', "La fiche à imprimer ? Commentez *DEVIS*.", "La fiche à imprimer ? Commentez : DEVIS.", 0.7),
    ('e2', "*Prouessia* : les règles du plombier, en 30 secondes.", "Prouèssia : les règles du plombier, en trente secondes.", 0.6),
]


def emph(s):
    return re.sub(r'\*(.+?)\*', r'<mark>\1</mark>', s)


SEGS = {'a1': (0.0, 4.54), 'b1': (5.82, 7.16), 'c0': (8.78, 10.18), 'r0': (11.66, 12.66), 'r1': (13.52, 14.34),
        'r2': (15.18, 16.32), 'r3': (17.18, 19.02), 'r4': (19.92, 22.82), 'r5': (23.84, 25.02), 'r6': (25.96, 30.40),
        'r7': (31.36, 33.12), 'r8': (34.12, 37.50), 'r9': (38.80, 43.32), 'd1': (44.54, 50.10), 'e1': (51.02, 54.46),
        'e2': (55.34, 58.72)}


SEGS_G = {'a1': (0.38, 5.43), 'b1': (6.74, 7.71), 'c0': (9.33, 10.45), 'r0': (11.71, 12.81), 'r1': (14.09, 14.94),
          'r2': (16.08, 17.20), 'r3': (18.42, 20.12), 'r4': (20.99, 23.78), 'r5': (24.95, 25.84), 'r6': (27.06, 31.53),
          'r7': (32.43, 34.35), 'r8': (35.26, 38.12), 'r9': (39.21, 43.27), 'd1': (44.24, 49.51), 'e1': (50.61, 52.93),
          'e2': (53.81, 56.45)}


def plan_eleven():
    import soundfile as sf
    g = os.environ.get('VOIX') == 'gemini'
    SEGS_ = SEGS_G if g else SEGS
    take, sr = sf.read(os.path.join(HERE, 'voixel', 'g24.wav' if g else 'take.wav')); take = take.astype(np.float32)
    voix, T, t = [], {}, 0.4
    for k, cap, parle, pause in PH:
        t += pause
        a, b = SEGS_[k]
        i, j = int(max(0, a - 0.04) * sr), min(len(take), int((b + 0.06) * sr))
        x = take[i:j].copy(); f = int(.012 * sr); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        x = x / max(1e-6, np.max(np.abs(x))) * 0.85
        d = len(x) / sr
        voix.append((t, x)); T[k] = t; T[k + '_end'] = t + d
        t += d
    T['_fin'] = t + 1.5
    return voix, T


def plan():
    if os.environ.get('VOIX') in ('eleven', 'gemini'): return plan_eleven()
    voix, T, t = [], {}, 0.4
    for k, cap, parle, pause in PH:
        t += pause
        a = V.parler(parle or re.sub(r'\*', '', cap), 0.97)
        d = len(a) / V.SR
        voix.append((t, a)); T[k] = t; T[k + '_end'] = t + d
        t += d
    T['_fin'] = t + 1.5
    return voix, T


def scenes(T):
    """Retourne (html des éléments, événements sfx)."""
    els, sfx = [], []

    def el(inner, at, out=None, kind='fade', style='', dur=.3, cls=''):
        els.append(f'<div class="el {cls}" data-at="{at:.3f}" data-out="{(out if out is not None else 999):.3f}" '
                   f'data-k="{kind}" data-d="{dur}" style="{style}">{inner}</div>')

    # ---- scène 1 : seuil
    s1a, s1b = 0.0, T['b1'] - 0.15
    el('<div class="mono" style="position:absolute;left:84px;top:470px;font-size:40px;color:#5B6577">Seuil du devis</div>', T['a1'] + .3, s1b)
    el('<div style="position:absolute;left:84px;top:540px;font-weight:900;font-size:430px;line-height:1;letter-spacing:-.06em;color:#1E40AF">0&nbsp;€</div>', T['a1'] + 1.4, s1b, 'slap', dur=.25)
    el(F.cote_h(84, 996, 1090, 'DEVIS ÉCRIT EXIGÉ', True), T['a1'] + 2.2, s1b, 'draw')
    sfx += [(T['a1'] + 1.4, 'thump')]

    # ---- scène 2 : titre + document
    s2a, s2b = T['b1'] - 0.1, T['c0'] - 0.15
    doc = F.frame_couverture
    # on réutilise le document SVG de la couverture
    src = doc()
    m = re.search(r'(<svg style="position:absolute;left:230px;top:872px".*?</svg>)', src, re.S)
    docsvg = m.group(1).replace('top:872px', 'top:700px;transform:scale(.82);transform-origin:0 0').replace('8 MENTIONS', 'À VÉRIFIER')
    el(f'<h1 style="position:absolute;left:84px;right:84px;top:420px;font-size:124px">Votre devis est-il <mark>complet</mark>&nbsp;?</h1>', s2a + .1, s2b, 'up')
    el(docsvg, s2a + .5, s2b, 'up', dur=.5)
    sfx += [(s2a, 'whoosh')]

    # ---- scène 3 : liste
    s3a = T['c0'] - 0.1; s3b = T['d1'] - 0.2
    el(f'<h1 style="position:absolute;left:84px;right:84px;top:400px;font-size:130px"><span class="bl">10</span> points</h1>', s3a + .1, s3b, 'up')
    sfx += [(s3a, 'whoosh')]
    y0, pas = 640, 78
    for i, r in enumerate(ROWS):
        y = y0 + i * pas
        t0 = T[f'r{i}']; t1 = T[f'r{i+1}'] if i < 9 else T['r9_end'] + .3
        box = (f'<svg style="position:absolute;left:84px;top:{y}px" width="46" height="46" viewBox="0 0 52 52" fill="none">'
               f'<rect x="3" y="3" width="46" height="46" rx="6" stroke="{BLEU}" stroke-width="5" fill="#fff"/></svg>')
        lab = (f'<div style="position:absolute;left:156px;top:{y-5}px;font-weight:800;font-size:52px;line-height:56px;letter-spacing:-.01em;white-space:nowrap">'
               f'<span class="hlw" data-at="{t0:.3f}" data-out="{t1:.3f}">{r}</span></div>')
        el(box + lab, t0, s3b, 'right', dur=.22)
        chk = (f'<svg style="position:absolute;left:84px;top:{y}px" width="46" height="46" viewBox="0 0 52 52" fill="none">'
               f'<path class="chk" d="M13 27 l9 10 l18 -22" stroke="{BLEU}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>')
        el(chk, t0 + .35, s3b, 'check', dur=.25)
        sfx += [(t0 + .35, 'tic')]

    # ---- scène 4 : à retenir
    s4a = T['d1'] - 0.1; s4b = T['e1'] - 0.2
    el(f'<h1 style="position:absolute;left:84px;right:84px;top:520px;font-size:120px">Relisez votre <mark>modèle</mark> une fois.</h1>', s4a + .1, s4b, 'up')
    sfx += [(s4a, 'whoosh')]

    # ---- scène 5 : mot-clé
    s5a = T['e1'] - 0.1
    el(f'<div style="position:absolute;left:84px;right:84px;top:440px;border:4px solid {ENCRE};background:#fff;padding:44px 20px 56px;text-align:center">'
       f'<div class="mono" style="font-size:34px;color:#5B6577">Commentez le mot</div>'
       f'<div style="font-weight:900;font-size:230px;line-height:1.05;letter-spacing:-.03em;margin-top:26px"><mark>DEVIS</mark></div>'
       f'</div>', s5a + .15, None, 'slap', dur=.28)
    el(f'<div style="position:absolute;left:84px;right:84px;top:1010px;font-weight:900;font-size:64px;letter-spacing:-.02em;text-align:center">'
       f'<span class="bl">Les règles du plombier,<br>en 30 secondes.</span></div>', T['e2'], None, 'up')
    el('<div class="mono" style="position:absolute;left:84px;right:84px;top:1230px;text-align:center;font-size:32px;color:#5B6577">@prouessia · prouessia.fr</div>', T['e2'] + .5, None)
    sfx += [(s5a, 'whoosh'), (s5a + .15, 'thump')]
    return els, sfx


EXTRA_CSS = f"""
.el{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;pointer-events:none}}
.hlw{{background:linear-gradient({MOUT_CL},{MOUT_CL}) no-repeat left center/0% 100%;padding:2px 10px;margin-left:-10px}}
.chk{{stroke-dasharray:1;stroke-dashoffset:1}}
.cap{{position:absolute;left:84px;right:84px;top:1322px;height:130px;display:flex;align-items:center;justify-content:center;opacity:0}}
.cap span{{background:#fff;border:3px solid {ENCRE};padding:10px 24px;font-weight:800;font-size:44px;line-height:1.18;text-align:center;letter-spacing:-.01em}}
.cap mark{{padding:0 .1em}}
"""

JS = """
(function(){
const cl=(x)=>Math.max(0,Math.min(1,x)); const ease=(x)=>1-Math.pow(1-x,3);
const els=[...document.querySelectorAll('.el')], caps=[...document.querySelectorAll('.cap')], hl=[...document.querySelectorAll('.hlw')];
window.render=function(t){
 for(const e of els){
  const at=+e.dataset.at,out=+e.dataset.out,d=+e.dataset.d,k=e.dataset.k;
  const p=ease(cl((t-at)/d)); const q=cl((t-out)/.25);
  let o=p*(1-q), tr='';
  if(k=='up') tr=`translateY(${(1-p)*26}px)`;
  if(k=='right') tr=`translateX(${(1-p)*-30}px)`;
  if(k=='slap'){tr=`scale(${1+(1-p)*.18})`; e.style.transformOrigin='50% 40%';}
  if(k=='draw'||k=='check'){ }
  e.style.opacity=o; e.style.transform=tr;
  if(k=='check'){const c=e.querySelector('.chk'); if(c) c.style.strokeDashoffset=1-p;}
 }
 for(const h of hl){const at=+h.dataset.at,out=+h.dataset.out; const p=ease(cl((t-at-.05)/.3)); const q=cl((t-out)/.2);
  h.style.backgroundSize=(p*100)+'% '+((1-q)*100)+'%';}
 for(const c of caps){const a=+c.dataset.at,b=+c.dataset.out; c.style.opacity=(t>=a&&t<b)?1:0;}
};
window.render(0);
})();
"""


def construire(T, els, rapide=False):
    caps = ''
    for k, cap, parle, pause in PH:
        continue
        caps += f'<div class="cap" data-at="{T[k]-0.05:.3f}" data-out="{T[k+"_end"]+0.12:.3f}"><span>{emph(cap)}</span></div>'
    # même cadre/cartouche que fiche.page, sans corps
    base = F.page('', '01 / 12', 'Devis de dépannage', 'Arrêté du 24 janv. 2017', '12.10.2026')
    base = base.replace('</style>', EXTRA_CSS + '</style>').replace('</body>', f'{"".join(els)}{caps}<script>{JS}</script></body>')
    return base


def main():
    rapide = len(sys.argv) > 1 and sys.argv[1] == 'rapide'
    voix, T = plan()
    els, sfx = scenes(T)
    html = construire(T, els)
    out = os.path.join(HERE, 'sortie3'); os.makedirs(out, exist_ok=True)
    w = os.path.join(out, '_w'); shutil.rmtree(w, ignore_errors=True); os.makedirs(w + '/f')
    p = os.path.join(w, 'page.html'); open(p, 'w', encoding='utf8').write(html)
    json.dump({k: round(v, 2) for k, v in T.items()}, open(os.path.join(out, 'timings.json'), 'w'))
    dur = T['_fin']; fps = 12 if rapide else FPS; n = int(round(dur * fps))
    with sync_playwright() as pw:
        nav = pw.chromium.launch(args=['--no-sandbox'])
        pg = nav.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + p); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        stills = os.environ.get('STILLS')
        if stills:
            for s in stills.split(','):
                pg.evaluate(f'window.render({float(s)})'); pg.screenshot(path=os.path.join(out, f'still_{float(s):05.1f}.png'))
            nav.close(); print('dur', dur); return
        for k in range(n):
            pg.evaluate(f'window.render({k / fps})')
            pg.screenshot(path=os.path.join(w, 'f', f'f{k:05d}.jpg'), type='jpeg', quality=90)
        nav.close()
    wav = os.path.join(w, 'audio.wav'); V.melange(voix, sfx, dur, wav)
    sortie = os.path.join(out, ('devis-depannage-fiche-leger-' + os.environ['VOIX'] + '.mp4' if os.environ.get('VOIX') else 'devis-depannage-fiche.mp4'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', w + '/f/f%05d.jpg', '-i', wav,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
                    '-r', str(fps), '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', sortie], check=True)
    shutil.rmtree(w, ignore_errors=True)
    print(sortie, dur)


if __name__ == '__main__':
    main()
