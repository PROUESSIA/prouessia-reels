"""Mini-série low-poly « Le devis de Mme Bernard » : dialogue (voix Gemini), scène 3D (scene.html), sous-titres mot à mot,
puis 3 plans d'appli (captures réelles) et la fin « Prouessia, le partenaire des plombiers ».
python3 compose.py            → tout (rendu 3D compris, ~12 min)
python3 compose.py --sans3d   → réutilise frames/ déjà rendues"""
import os, sys, json, base64, subprocess
import numpy as np, soundfile as sf
ICI = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(ICI)
sys.path.insert(0, os.path.join(ROOT, 'moteur'))
import vecu
from commun import FONTS, MUST
W, H, FPS = 1080, 1920, 30
SR = 24000

# (qui, fichier voix « court », début, fin dans le fichier, mots en gras, plan, pause avant)
MOTS = json.load(open(os.path.join(ICI, 'mots.json')))
SEG = {'ines': [(.22, 1.52), (1.94, 4.28), (4.62, 5.78), (6.20, 8.18), (8.60, 10.24)],
       'karim': [(.26, 1.52), (2.92, 5.34), (5.78, 6.36), (6.82, 8.2)],
       'narrateur': [(10.12, 10.98), (11.44, 12.2), (12.7, 13.36), (13.74, 16.64)]}
NARR = [[('Un', 10.12, 10.18), ('devis', 10.22, 10.42), ('fait', 10.46, 10.54), ('sur', 10.58, 10.7), ('place.', 10.74, 10.98)],
        [('Envoyé', 11.44, 11.74), ('en', 11.78, 11.84), ('un', 11.88, 11.94), ('clic.', 11.98, 12.2)],
        [('Relancé', 12.7, 13.02), ('tout', 13.04, 13.14), ('seul.', 13.18, 13.36)], []]
REPLIQUES = [  # qui, n° de réplique du personnage, nb de mots en gras à la fin, plan, pause avant
    ('ines', 0, 2, 'large', .15), ('karim', 0, 2, 'karim', .3), ('ines', 1, 2, 'ines', .3), ('karim', 1, 3, 'papiers', .3),
    ('ines', 2, 2, 'ines2', .3), ('karim', 2, 1, 'karim2', .25), ('ines', 3, 3, 'ines3', .3), ('ines', 4, 3, 'deux', .15),
    ('karim', 3, 3, 'karim3', .6),
    ('narrateur', 0, 2, 'app:01-nouveau-devis', .6), ('narrateur', 1, 3, 'app:05-envoyer-devis', .15),
    ('narrateur', 2, 2, 'app:14-relance-auto', .15), ('narrateur', 3, 0, 'fin', .25)]
APP = {'app:01-nouveau-devis': 3.0, 'app:05-envoyer-devis': 4.5, 'app:14-relance-auto': 6.0}  # seconde où l'action commence

def voix():
    pistes = {k: sf.read(os.path.join(ICI, f'{k}-court.wav'))[0] for k in SEG}
    out, t, tl = [], 0.0, []
    for qui, n, gras, plan, pause in REPLIQUES:
        a, b = SEG[qui][n]; s = pistes[qui][int((a - .04) * SR):int((b + .08) * SR)]
        out.append(np.zeros(int(pause * SR))); t += pause
        mots = (MOTS[qui][n] if qui != 'narrateur' else NARR[n])
        tl.append({'qui': qui, 'plan': plan, 'debut': round(t, 3), 'fin': round(t + len(s) / SR, 3), 'gras': gras,
                   'mots': [(m, round(t + ms - a + .04, 3), round(t + me - a + .04, 3)) for m, ms, me in mots]})
        out.append(s); t += len(s) / SR
    out.append(np.zeros(int(1.0 * SR))); total = t + 1.0
    for i, r in enumerate(tl):   # chaque plan commence au début de sa pause et finit au début du suivant
        r['plan_debut'] = 0 if i == 0 else round(tl[i - 1]['fin'], 3)
    for i, r in enumerate(tl): r['plan_fin'] = tl[i + 1]['plan_debut'] if i + 1 < len(tl) else round(total, 3)
    sf.write(os.path.join(ICI, 'dialogue.wav'), np.concatenate(out), SR)
    json.dump(tl, open(os.path.join(ICI, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
    return tl, total

CSS = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif}}
.st{{position:absolute;left:70px;right:70px;top:TOPpx;text-align:center;color:#fff;font-weight:700;font-size:62px;line-height:1.15;letter-spacing:-.01em;
text-shadow:0 0 4px rgba(0,0,0,.9),0 3px 14px rgba(0,0,0,.8)}} .st b{{font-weight:900;color:{MUST};display:block}} .st .x{{visibility:hidden}}"""

def sous_titres(tl, total):
    """Une image par mot (le texte apparaît mot à mot, comme les références) → piste RGBA."""
    from playwright.sync_api import sync_playwright
    d = os.path.join(ICI, 'st'); os.makedirs(d, exist_ok=True); liste = []; t = 0.0; k = 0
    vide = os.path.join(d, 'vide.png')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        pg.set_content('<html><body></body></html>'); pg.screenshot(path=vide, omit_background=True)
        for r in tl:
            if not r['mots']: continue
            top = 1290 if r['plan'].startswith('app:') else 1120
            mots = [m for m, _, _ in r['mots']]; ng = r['gras']
            for j, (m, ms, me) in enumerate(r['mots']):
                if ms > t:
                    liste.append((vide if j == 0 else liste[-1][0], ms - t)); t = ms
                def span(i, w): return f'<span class="{"" if i <= j else "x"}">{w}</span>'
                normal = ' '.join(span(i, w) for i, w in enumerate(mots[:len(mots) - ng]))
                gras = ' '.join(span(i + len(mots) - ng, w) for i, w in enumerate(mots[len(mots) - ng:]))
                html = f'<div class="st">{normal}{"<b>" + gras + "</b>" if ng else ""}</div>'
                f = os.path.join(d, f'{k:03d}.png'); k += 1
                pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS.replace("TOP", str(top))}</style></head><body>{html}</body></html>')
                pg.wait_for_timeout(60); pg.screenshot(path=f, omit_background=True)
                fin = r['mots'][j + 1][1] if j + 1 < len(r['mots']) else r['fin'] + .35
                liste.append((f, fin - t)); t = fin
        b.close()
    liste.append((vide, max(.1, total - t)))
    with open(os.path.join(d, 'liste.txt'), 'w') as fh:
        for f, du in liste: fh.write(f"file '{f}'\nduration {du:.3f}\n")
        fh.write(f"file '{liste[-1][0]}'\n")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(d, 'liste.txt'),
                    '-vf', f'fps={FPS},format=rgba', '-c:v', 'qtrle', os.path.join(ICI, 'sous-titres.mov')], check=True)

def fin_carte(fond):
    from playwright.sync_api import sync_playwright
    ico = base64.b64encode(open(os.path.join(ROOT, 'email', 'icone-prouessia.png'), 'rb').read()).decode()
    html = f"""<html><head><meta charset="utf-8"><style>{FONTS}*{{margin:0}}body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif;
display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center}}
img{{width:190px;height:190px;border-radius:44px;box-shadow:0 10px 40px rgba(0,0,0,.5)}}
h1{{font-weight:900;font-size:78px;line-height:1.08;margin:50px 70px 0;letter-spacing:-.02em;text-shadow:0 4px 20px rgba(0,0,0,.7)}} h1 b{{color:{MUST}}}
p{{margin-top:34px;font-weight:800;font-size:52px;background:{MUST};color:#0B1B3A;padding:14px 34px;border-radius:999px}}</style></head>
<body><img src="data:image/png;base64,{ico}"><h1>Prouessia,<br><b>le partenaire<br>des plombiers</b></h1><p>prouessia.fr</p></body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(ICI, 'fin.png'), omit_background=True); b.close()

def montage(tl, total):
    parts = []; d = os.path.join(ICI, 'parts'); os.makedirs(d, exist_ok=True)
    t3d = next(r['plan_debut'] for r in tl if r['plan'].startswith('app:'))
    # 1) la scène 3D
    p3 = os.path.join(d, '0-scene.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(ICI, 'frames', '%05d.jpg'), '-t', f'{t3d:.3f}',
                    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', p3], check=True); parts.append(p3)
    # 2) les plans d'appli (cadre arrondi sur fond flouté)
    bx, by, bw, bh = vecu.BOITE
    for i, r in enumerate([r for r in tl if r['plan'].startswith('app:')]):
        du = r['plan_fin'] - r['plan_debut']; src = vecu.source(r['plan']); deb = APP[r['plan']]
        zw, zh = vecu.zone_utile(src, deb, du); cw, ch = 'iw', f'iw*{bh}/{bw}'
        f = (f"[0:v]crop={zw - zw % 2 - 4}:{zh - zh % 2 - 4}:0:0,fps={FPS},setsar=1,trim=duration={du:.3f},setpts=PTS-STARTPTS,split[a][b];"
             f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.35:saturation=0.6[f];"
             f"[b]crop={cw}:{ch}:0:max(0\\,min(ih-{ch}\\,ih*0.45-{ch}/2)),scale={bw}:{bh}:flags=lanczos,format=rgba[g];"
             f"movie={vecu.masque()}:loop=0,setpts=N/{FPS}/TB,format=gray,scale={bw}:{bh}[m];[g][m]alphamerge[h];[f][h]overlay={bx}:{by}:shortest=1,format=yuv420p[v]")
        pa = os.path.join(d, f'{i + 1}-app.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(deb), '-t', f'{du + .1:.3f}', '-i', src, '-filter_complex', f, '-map', '[v]',
                        '-c:v', 'libx264', '-crf', '18', pa], check=True); parts.append(pa)
    # 3) la fin : dernière image de la cuisine floutée + carte, léger zoom
    r = tl[-1]; du = r['plan_fin'] - r['plan_debut']; fin_carte(None)
    der = sorted(os.listdir(os.path.join(ICI, 'frames')))[int(t3d * FPS) - 1]
    pf = os.path.join(d, '9-fin.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', f'{du:.3f}', '-i', os.path.join(ICI, 'frames', der), '-loop', '1', '-t', f'{du:.3f}', '-i', os.path.join(ICI, 'fin.png'),
                    '-filter_complex', f"[0:v]boxblur=25:3,eq=brightness=-0.3,scale={int(W*1.12)}:-2,zoompan=z='1+0.0008*on':d=1:s={W}x{H}:fps={FPS}[b];[1:v]format=rgba,fps={FPS}[c];[b][c]overlay=0:0,format=yuv420p[v]",
                    '-map', '[v]', '-t', f'{du:.3f}', '-c:v', 'libx264', '-crf', '18', pf], check=True); parts.append(pf)
    with open(os.path.join(d, 'liste.txt'), 'w') as fh:
        for p in parts: fh.write(f"file '{p}'\n")
    img = os.path.join(d, 'images.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(d, 'liste.txt'), '-c', 'copy', img], check=True)
    out = os.path.join(ICI, 'reel-serie.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', img, '-i', os.path.join(ICI, 'sous-titres.mov'), '-i', os.path.join(ICI, 'dialogue.wav'),
                    '-filter_complex', '[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v];[2:a]loudnorm=I=-14:TP=-1.5[a]', '-map', '[v]', '-map', '[a]',
                    '-t', f'{total:.3f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    return out

if __name__ == '__main__':
    tl, total = voix()
    for r in tl: print(f"{r['debut']:6.2f}-{r['fin']:6.2f} {r['qui']:9} {r['plan']}")
    print('total', round(total, 2))
    if '--voix' in sys.argv: sys.exit()
    if '--sans3d' not in sys.argv:
        t3d = next(r['plan_debut'] for r in tl if r['plan'].startswith('app:'))
        subprocess.run([sys.executable, os.path.join(ICI, 'rendu.py'), os.path.join(ICI, 'timeline.json'), os.path.join(ICI, 'frames'), str(FPS), '0', f'{t3d + .2:.2f}'], check=True, cwd=ICI)
    sous_titres(tl, total)
    print(montage(tl, total))
