"""Moteur commun des Reels (style reel4 « funky doux »).
Un Reel = liste PH [(clé, texte dit, pause avant)] + fonction scenes(T, el, sfx) qui place les éléments.
- Sans .wav : durées estimées (aperçus seulement).  - Avec .wav : segments calés automatiquement sur les phrases."""
import os, sys, re, shutil, subprocess, difflib, unicodedata
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fiche as F            # polices
import reel4 as R4           # CSS + JS d'animation validés
import voix as V             # bruitages + mélange
from playwright.sync_api import sync_playwright

INK, BLUE, MUST, PAPIER, GRIS = '#0B1B3A', '#1E40AF', '#F2B705', '#F7F5EF', '#5B6577'
FPS = 30
LOGO = ('<div class="logo"><i><svg viewBox="0 0 24 24" width="28" height="28"><rect x="4" y="13" width="4" height="7" rx="2" fill="#fff"/>'
        '<rect x="10" y="9" width="4" height="11" rx="2" fill="#fff"/><rect x="16" y="5" width="4" height="15" rx="2" fill="#F2B705"/></svg></i>prouessia</div>')


def _norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9 ]+', ' ', s).split()


def aligner(phrases, segs, textes):
    """Partition contiguë des segments en len(phrases) groupes, maximise la ressemblance texte."""
    n, m = len(phrases), len(segs)
    P = [_norm(p) for p in phrases]; S = [_norm(t) for t in textes]
    sc = lambda i, a, b: difflib.SequenceMatcher(None, P[i], sum(S[a:b], [])).ratio()
    INF = -1e9
    best = [[INF] * (m + 1) for _ in range(n + 1)]; arg = [[0] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for i in range(1, n + 1):
        for b in range(i, m + 1):
            for a in range(i - 1, b):
                if best[i - 1][a] == INF: continue
                v = best[i - 1][a] + sc(i - 1, a, b)
                if v > best[i][b]: best[i][b], arg[i][b] = v, a
    res, b = [], m
    for i in range(n, 0, -1):
        a = arg[i][b]; res.append((segs[a][0], segs[b - 1][1], i - 1, a, b)); b = a
    res.reverse()
    return [(x[0], x[1]) for x in res], [(phrases[x[2]], ' | '.join(textes[x[3]:x[4]]), round(sc(x[2], x[3], x[4]), 2)) for x in res]


def plan(PH, wav=None, debut=0.4, bornes=None):
    """Retourne (pistes voix, T). T[clé] = début de la phrase sur la vidéo, T[clé+'_end'] = fin."""
    T, voix, t = {}, [], debut
    if not wav:
        for k, txt, pause in PH:
            t += pause; d = max(1.0, len(txt.split()) / 2.7)
            T[k], T[k + '_end'] = t, t + d; t += d
        T['_fin'] = t + 1.6
        return voix, T
    import soundfile as sf
    import caler
    if bornes is None:
        segs = caler.segments(wav, '-40dB', 0.15)
        textes = caler.transcrire(wav, segs)
        bornes, rapport = aligner([p[1] for p in PH], segs, textes)
        for r in rapport: print(f'  {r[2]:.2f}  {r[0][:55]:55s} <- {r[1][:60]}')
    take, sr = sf.read(wav)
    if take.ndim > 1: take = take.mean(1)
    if sr != V.SR:
        from scipy.signal import resample_poly
        take = resample_poly(take, V.SR, sr); sr = V.SR
    take = take.astype(np.float32)
    for (k, txt, pause), bo in zip(PH, bornes):
        t += pause
        if isinstance(bo, (int, float)):  # scène muette de bo secondes
            T[k], T[k + '_end'] = t, t + bo; t += bo; continue
        a, b = bo
        i, j = int(max(0, a - 0.04) * sr), min(len(take), int((b + 0.08) * sr))
        x = take[i:j].copy(); f = int(.012 * sr); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        x = x / max(1e-6, np.max(np.abs(x))) * 0.85
        d = len(x) / sr
        voix.append((t, x)); T[k], T[k + '_end'] = t, t + d; t += d
    T['_fin'] = t + 1.6
    return voix, T


class Scene:
    def __init__(self):
        self.out, self.sfx = [], []

    def el(self, inner, at, out_=999, kind='pop', style='', d=.45, r=0, w=0, ph=0):
        if at < 1.0: at = -1.0  # accroche : visible dès la 1re image (couverture et défilement)
        self.out.append(f'<div class="a" data-at="{at:.3f}" data-out="{out_:.3f}" data-d="{d}" data-k="{kind}" data-r="{r}" '
                        f'data-w="{w}" data-ph="{ph}" style="{style}">{inner}</div>')

    def bg(self, a, b, first=False):
        self.out.append(f'<div class="bg" data-at="{a:.3f}" data-out="{b:.3f}" style="background:{PAPIER};{"opacity:1" if first else ""}"></div>')

    # briques visuelles réutilisables -------------------------------------------------
    def logo(self):
        self.el(LOGO, .1, 999, 'up', 'left:60px;top:250px', .5)

    def tag(self, txt, at, b, top=420):
        self.el(f'<div style="background:{MUST};border-radius:14px;padding:10px 30px;font-weight:900;font-size:50px;letter-spacing:.01em">{txt}</div>',
                at, b, 'pop', f'left:70px;top:{top}px', .45)

    def source(self, txt, at, b, top=1420):
        self.el(f'<div style="font-weight:800;font-size:32px;background:#fff;border-radius:30px;padding:8px 26px;border:4px solid {INK}">{txt}</div>',
                at, b, 'up', f'left:60px;top:{top}px', .4)

    def signature(self, at):
        self.el(f'<div style="font-weight:900;font-size:96px;line-height:1.04;letter-spacing:-.035em;width:940px;white-space:normal">Les règles du plombier,<br>en '
                f'<span style="background:{INK};color:{MUST};border-radius:.2em;padding:0 .2em .04em">30 secondes.</span></div>', at, 999, 'up', 'left:70px;top:560px', .5)
        self.el(f'<div style="font-weight:800;font-size:40px;background:#fff;border:4px solid {INK};border-radius:40px;padding:10px 30px">@prouessia · prouessia.fr</div>',
                at + .5, 999, 'pop', 'left:70px;top:900px', .4)


def page(sc):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{F.FONTS}{R4.CSS}.bl{{color:{BLUE}}}</style></head>'
            f'<body>{"".join(sc.out)}<script>{R4.JS}</script></body></html>')


def rendre(nom, PH, scenes, wav=None, stills=None, dossier=os.environ.get('SORTIE', os.path.abspath('sortie')), bornes=None, debut=0.4):
    voix, T = plan(PH, wav, debut=debut, bornes=bornes)
    sc = Scene(); scenes(T, sc)
    html = page(sc)
    os.makedirs(dossier, exist_ok=True)
    w = os.path.join(dossier, '_w_' + nom); shutil.rmtree(w, ignore_errors=True); os.makedirs(w + '/f')
    p = os.path.join(w, 'page.html'); open(p, 'w', encoding='utf8').write(html)
    dur = T['_fin']; n = int(round(dur * FPS))
    with sync_playwright() as pw:
        nav = pw.chromium.launch(args=['--no-sandbox'])
        pg = nav.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + p); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        if stills is not None:
            if stills == 'auto':  # fin de chaque phrase (tout est affiché)
                stills = [T[k + '_end'] + min(.3, pause_suiv) for (k, _, _), pause_suiv in zip(PH, [p[2] for p in PH[1:]] + [1.0])]
            res = []
            for s in stills:
                pg.evaluate(f'window.render({s})'); f = os.path.join(dossier, f'{nom}_still_{s:05.2f}.png')
                pg.screenshot(path=f); res.append(f)
            nav.close(); shutil.rmtree(w, ignore_errors=True)
            return res, T
        for k in range(n):
            pg.evaluate(f'window.render({k / FPS})')
            pg.screenshot(path=os.path.join(w, 'f', f'f{k:05d}.jpg'), type='jpeg', quality=90)
        nav.close()
    a = os.path.join(w, 'audio.wav'); V.melange(voix, sc.sfx, dur, a)
    sortie = os.path.join(dossier, f'{nom}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', w + '/f/f%05d.jpg', '-i', a,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
                    '-r', str(FPS), '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', sortie], check=True)
    shutil.rmtree(w, ignore_errors=True)
    return sortie, T


def planche(images, sortie, cols=4):
    from PIL import Image
    ims = [Image.open(i).convert('RGB').resize((270, 480)) for i in images]
    rows = (len(ims) + cols - 1) // cols
    m = Image.new('RGB', (cols * 280 + 10, rows * 490 + 10), (210, 206, 196))
    for i, im in enumerate(ims): m.paste(im, (10 + (i % cols) * 280, 10 + (i // cols) * 490))
    m.save(sortie)


CHECK = (f'<svg width="40" height="40" viewBox="0 0 52 52" fill="none"><path d="M12 27 l9 10 l19 -23" stroke="{BLUE}" stroke-width="8" '
         f'stroke-linecap="round" stroke-linejoin="round"/></svg>')
DOC = (f'<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
       f'<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>')


def pill(icone, texte, fond='#fff', taille=46):
    return (f'<div style="display:flex;align-items:center;gap:18px;height:96px;padding:0 36px 0 18px;border:5px solid {INK};border-radius:24px;'
            f'background:{fond};font-weight:800;font-size:{taille}px;letter-spacing:-.02em"><div style="width:62px;height:62px;border-radius:14px;'
            f'border:5px solid {INK};background:#fff;display:flex;align-items:center;justify-content:center">{icone}</div>{texte}</div>')


def badge(n):
    return (f'<div style="width:118px;height:118px;border-radius:30px;background:{INK};color:{MUST};font-weight:900;font-size:80px;'
            f'display:flex;align-items:center;justify-content:center">{n}</div>')


def gros(nb, unite='', couleur=BLUE, taille=420):
    return (f'<div style="display:flex;align-items:flex-end;gap:24px"><div style="font-weight:900;font-size:{taille}px;line-height:.8;'
            f'letter-spacing:-.07em;color:{couleur}">{nb}</div><div style="font-weight:900;font-size:{taille * .25:.0f}px;'
            f'line-height:1;letter-spacing:-.03em;padding-bottom:{taille * .04:.0f}px">{unite}</div></div>')


def fond_noir(txt, taille=54):
    return (f'<div style="background:{INK};color:#fff;border-radius:20px;padding:16px 34px;font-weight:900;font-size:{taille}px;'
            f'letter-spacing:-.02em;line-height:1.1">{txt}</div>')


def main(NOM, PH, scenes, WAV, BORNES):
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'
    if mode == 'stills':
        im, T = rendre(NOM, PH, scenes, WAV, stills=[float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else 'auto', bornes=BORNES)
        planche(im, f'/home/claude/sortie/{NOM}_planche.png', cols=min(6, len(im))); print(round(T['_fin'], 1), 's', {k: round(v, 1) for k, v in T.items()})
    else:
        print(rendre(NOM, PH, scenes, WAV, bornes=BORNES))
