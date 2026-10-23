"""Styles « plan » (explication monochrome, ex. Google Maps) et « croquis » (dessin au crayon + écrans de l'appli).
Un dossier DIR/scenes.json : {"style": "plan"|"croquis", "phrases": [{"texte": "...", "gras": ["mot", ...], "scene": {"type": ..., ...}}]}
  python3 moteur/scenes.py DIR texte          → texte à envoyer au hub (mode voix, voice Charon, style = STYLE de vecu.py)
  python3 moteur/scenes.py DIR faux           → durées estimées (aperçu sans voix)
  python3 moteur/scenes.py DIR voix FICHIER   → cale la voix Gemini phrase par phrase (voix.wav, durees.json)
  python3 moteur/scenes.py DIR planche        → DIR/planche.png (une image par phrase)
  python3 moteur/scenes.py DIR video          → DIR/video.mp4
"""
import os, sys, re, json, base64, subprocess, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'moteur')); sys.path.insert(0, os.path.join(ROOT, 'essai'))
from vecu import zone_utile, APP, PAUSE
W, H, FPS = 1080, 1920, 30
FONTDIR = os.path.join(ROOT, 'moteur', 'fonts')

def fonts():
    b = lambda f: base64.b64encode(open(os.path.join(FONTDIR, f), 'rb').read()).decode()
    return ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b(f)}) format('woff2')}}" for n, w, f in
                   [('Inter', 700, 'inter-latin-700-normal.woff2'), ('Inter', 800, 'inter-latin-800-normal.woff2'), ('Inter', 900, 'inter-latin-900-normal.woff2'), ('Caveat', 700, 'caveat-latin-700-normal.woff2')])

def charger(d):
    c = json.load(open(os.path.join(d, 'scenes.json')))
    assert c['phrases'][-1]['scene']['type'] == 'fin'
    return c

def lignes(c):
    return [p['texte'] + ('' if p['texte'][-1] in '.?!…' else '.') for p in c['phrases']]

def texte(d):
    t = ' '.join(lignes(charger(d)))
    print(t.replace('Prouessia', 'Prouèssia'))

def syll(m):
    return max(1, len(re.findall(r'[aeiouyàâéèêëîïôöûùü]+', m.lower())))

def timeline(c, D):
    """D = durées par phrase (s) ; parole[i] = (début, fin) de la voix dans la phrase. Mots répartis par syllabes."""
    t, P = 0.0, []
    for i, (ph, du) in enumerate(zip(c['phrases'], D)):
        mots = ph['texte'].split(); parole = c.get('_parole', [None] * len(D))[i] or (0.05, du - PAUSE - (.8 if i == len(D) - 1 else 0))
        a0, a1 = t + parole[0], t + parole[1]; tot = sum(syll(m) for m in mots); acc = 0; ms = []
        norm = lambda w: re.sub(r'[.,!?…:;«»]', '', w).lower()
        gras = set()
        for item in ph.get('gras', []):   # chaque élément = un mot ou un groupe de mots, marqué à sa dernière place dans la phrase
            g = [norm(x) for x in item.split()]
            for j in range(len(mots) - len(g), -1, -1):
                if [norm(w) for w in mots[j:j + len(g)]] == g: gras |= set(range(j, j + len(g))); break
        for j, m in enumerate(mots): ms.append([m, round(a0 + (a1 - a0) * acc / tot, 3), j in gras]); acc += syll(m)
        P.append({**ph, 'debut': round(t, 3), 'fin': round(t + du, 3), 'mots': ms}); t += du
    return P, t

def faux(d):
    c = charger(d); D = [round(len(p['texte'].split()) / 4.6 + .35 + PAUSE, 2) for p in c['phrases']]; D[-1] += .8
    json.dump(D, open(os.path.join(d, 'durees.json'), 'w')); print('durées estimées', round(sum(D), 1), 's')

def voix(d, fichier):
    import numpy as np, soundfile as sf
    from aligner import aligner
    c = charger(d); L = lignes(c); t = open(fichier).read()
    m = re.search(r'"data":"([A-Za-z0-9+/=]+)"', t)
    brut = base64.b64decode(m.group(1)) if m else base64.b64decode(t.rsplit('|', 1)[0])
    wav = os.path.join(d, 'voix-brute.wav')
    if brut[:4] == b'RIFF': open(wav, 'wb').write(brut)
    else:
        open(wav + '.pcm', 'wb').write(brut)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', wav + '.pcm', wav], check=True); os.remove(wav + '.pcm')
    # silences resserrés (0,22 s max) et débit +10 % sans changer la hauteur, puis calage phrase par phrase
    serre = os.path.join(d, 'voix-serree.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-af', 'silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-38dB:stop_silence=0.22,atempo=1.1', serre], check=True)
    wav = serre
    x, sr = sf.read(wav); seg = aligner(wav, L); out, D, par = [], [], []
    for (a, b), ph in zip(seg, c['phrases']):
        s = x[int(max(0, a - .03) * sr):int((b + .05) * sr)]; ex = float(ph.get('scene', {}).get('pause', 0))
        out += [s, np.zeros(int((PAUSE + ex) * sr))]; D.append(round(len(s) / sr + PAUSE + ex, 3)); par.append([0.03, round(len(s) / sr - .05, 3)])
    D[-1] += .8
    sf.write(os.path.join(d, 'voix.wav'), np.concatenate(out), sr); json.dump(D, open(os.path.join(d, 'durees.json'), 'w'))
    json.dump(par, open(os.path.join(d, 'parole.json'), 'w'))
    mots = sum(len(l.split()) for l in L); tot = sum(D)
    print('voix calée :', round(tot, 1), 's,', round(mots / (tot - .8), 1), 'mots/s')
    for l, (a, b) in zip(L, seg): print(f'  {a:5.2f}-{b:5.2f} {l}')

def preparer(d):
    c = charger(d); D = json.load(open(os.path.join(d, 'durees.json')))
    if os.path.exists(os.path.join(d, 'parole.json')): c['_parole'] = json.load(open(os.path.join(d, 'parole.json')))
    P, total = timeline(c, D); apps = {}
    for i, ph in enumerate(P):   # écrans d'appli : images extraites de la capture (zone utile seulement)
        sc = ph['scene']
        if sc['type'] != 'appli': continue
        src = os.path.join(APP, sc['capture'] + '.mp4'); deb = float(sc.get('debut', 0)); du = ph['fin'] - ph['debut'] + .2
        zw, zh = zone_utile(src, deb, du); od = os.path.join(d, 'app', str(i)); shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(deb), '-t', f'{du:.2f}', '-i', src, '-vf', f'crop={zw - 4}:{zh - 4}:0:0,fps={FPS},scale=648:-2', '-q:v', '3', f'{od}/%04d.jpg'], check=True)
        apps[str(i)] = ['file://' + os.path.join(od, f) for f in sorted(os.listdir(od))]
    return {'style': c['style'], 'phrases': P, 'total': total, 'apps': apps}

def page(pw, S):
    b = pw.chromium.launch(args=['--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': W, 'height': H}); pg.goto('file://' + os.path.join(ROOT, 'moteur', 'scenes.html'))
    pg.wait_for_function('window.pret === true'); pg.evaluate("f => document.getElementById('fonts').textContent = f", fonts())
    pg.evaluate('s => window.S = s', S); pg.wait_for_timeout(300); return b, pg

def planche(d):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    S = preparer(d); ims = []
    with sync_playwright() as p:
        b, pg = page(p, S)
        for ph in S['phrases']:
            t = ph['debut'] + (ph['fin'] - ph['debut']) * .8; pg.evaluate(f'render({t})'); pg.wait_for_timeout(60)
            f = os.path.join(d, '_p.png'); pg.screenshot(path=f); ims.append(Image.open(f).resize((270, 480)).copy())
        b.close()
    n = len(ims); cols = min(n, 7); s = Image.new('RGB', (270 * cols, 480 * ((n + cols - 1) // cols)), 'white')
    for i, im in enumerate(ims): s.paste(im, ((i % cols) * 270, (i // cols) * 480))
    s.save(os.path.join(d, 'planche.png')); os.remove(os.path.join(d, '_p.png')); print(os.path.join(d, 'planche.png'))

def video(d):
    from playwright.sync_api import sync_playwright
    S = preparer(d); fr = os.path.join(d, 'frames'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    N = int(S['total'] * FPS)
    with sync_playwright() as p:
        b, pg = page(p, S)
        for n in range(N):
            pg.evaluate(f'render({n / FPS})'); pg.screenshot(path=f'{fr}/{n:05d}.jpg', type='jpeg', quality=92)
        b.close()
    out = os.path.join(d, 'video.mp4'); a = os.path.join(d, 'voix.wav')
    aud = ['-i', a] if os.path.exists(a) else ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{fr}/%05d.jpg', *aud, '-filter_complex', f'[1:a]apad,atrim=0:{S["total"]:.2f},loudnorm=I=-14:TP=-1.5[a]',
                    '-map', '0:v', '-map', '[a]', '-t', f'{S["total"]:.2f}', '-c:v', 'libx264', '-preset', 'medium', '-profile:v', 'main', '-level', '4.0', '-pix_fmt', 'yuv420p', '-crf', '23',
                    '-maxrate', '1800k', '-bufsize', '3600k', '-g', '30', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], check=True)
    shutil.rmtree(fr); print(out, round(S['total'], 1), 's')

if __name__ == '__main__':
    d = os.path.join(ROOT, sys.argv[1]); q = sys.argv[2]
    {'texte': lambda: texte(d), 'faux': lambda: faux(d), 'voix': lambda: voix(d, sys.argv[3]), 'planche': lambda: planche(d), 'video': lambda: video(d)}[q]()
