"""Reel d'essai « nouvelle formule » : vraies vidéos (Pixabay), mouvement dès 0 s, écran plein, voix naturelle, 15 s.
python3 essai/build.py  → essai/reel-essai.mp4 + essai/controle.png"""
import os, sys, subprocess, base64
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'moteur'))
from commun import FONTS, INK, MUST
from playwright.sync_api import sync_playwright

CLIPS = os.path.join(ROOT, 'videos', 'clips')
VOIX = os.path.join(HERE, 'voix-a.mp3')
W, H = 1080, 1920
# (début, fin, clip, départ dans le clip, sens du panoramique, centre horizontal du sujet 0-1, texte HTML)
SEG = [
    (0.00, 2.40, '136086', 0.3, -1, 0.33, 'Votre devis de dépannage est peut-être <b>incomplet</b>.'),
    (2.40, 5.15, '100344', 0.0, -1, 0.62, 'Chez un particulier&nbsp;:<br><b>durée de validité</b> obligatoire.'),
    (5.15, 7.80, '4728', 2.0, 1, 0.5, 'Arrêté du<br><b>24 janvier 2017</b>.'),
    (7.80, 10.65, '100344', 4.5, 1, 0.62, 'Écrivez-la en clair&nbsp;:<br><b>«&nbsp;Offre valable un&nbsp;mois&nbsp;»</b>'),
    (10.65, 13.60, '257090', 1.0, -1, 0.2, 'Client muet&nbsp;?<br><b>Prouessia</b> le relance tout seul.'),
    (13.60, 15.90, '51541', 3.0, 1, 0.45, 'Vous la mettez,<br><b>cette ligne</b>&nbsp;?<div class="q">Dites-le en commentaire</div>'),
]
ICONE = base64.b64encode(open(os.path.join(ROOT, 'email', 'icone-prouessia.png'), 'rb').read()).decode()
CSS = f"""{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif}}
.voile{{position:absolute;left:0;top:0;width:100%;height:1250px;background:linear-gradient(180deg,rgba(11,27,58,.88) 0%,rgba(11,27,58,.72) 45%,rgba(11,27,58,0) 100%)}}
.logo{{position:absolute;left:70px;top:130px;display:flex;align-items:center;gap:18px;color:#fff;font-weight:800;font-size:40px}}
.logo img{{width:64px;height:64px;border-radius:16px}}
.t{{position:absolute;left:70px;right:130px;top:300px;color:#fff;font-weight:900;font-size:96px;line-height:1.08;letter-spacing:-.03em;text-shadow:0 4px 18px rgba(0,0,0,.35)}}
.t b{{background:{MUST};color:{INK};padding:0 14px;border-radius:14px;box-decoration-break:clone;-webkit-box-decoration-break:clone;text-shadow:none}}
.q{{margin-top:34px;display:inline-block;font-size:48px;font-weight:800;background:#fff;color:{INK};padding:16px 26px;border-radius:999px;text-shadow:none}}
"""


def calques():
    os.makedirs(os.path.join(HERE, 'calques'), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        for i, s in enumerate(SEG):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="voile"></div>'
                           f'<div class="logo"><img src="data:image/png;base64,{ICONE}">prouessia</div><div class="t">{s[6]}</div></body></html>')
            pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(HERE, 'calques', f'{i}.png'), omit_background=True)
        b.close()


def video():
    inp, fil = [], []
    for i, (a, z, clip, off, sens, cx, _) in enumerate(SEG):
        d = z - a
        inp += ['-ss', str(off), '-t', f'{d + .05:.2f}', '-i', os.path.join(CLIPS, clip + '.mp4')]
        # couvre 1080×1920 (zoom 15 % de marge) et glisse latéralement : du mouvement dès la 1re image
        x = f"max(0\\,min(iw-{W}\\,iw*{cx}-{W/2}+{sens}*260*(t/{d:.2f}-0.5)))"
        fil.append(f"[{i}:v]fps=30,scale=-2:{int(H*1.15)},crop={W}:{H}:{x}:(ih-{H})/2,setsar=1,trim=duration={d:.2f},setpts=PTS-STARTPTS[v{i}]")
    n = len(SEG)
    for i in range(n):
        inp += ['-loop', '1', '-t', f'{SEG[i][1]-SEG[i][0]:.2f}', '-i', os.path.join(HERE, 'calques', f'{i}.png')]
        fil.append(f"[{n+i}:v]fps=30,format=rgba,trim=duration={SEG[i][1]-SEG[i][0]:.2f},setpts=PTS-STARTPTS[c{i}]")
        fil.append(f"[v{i}][c{i}]overlay=0:0:shortest=1[o{i}]")
    fil.append(''.join(f'[o{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0,format=yuv420p[v]')
    inp += ['-i', VOIX]
    fil.append(f"[{2*n}:a]apad=pad_dur=1,atrim=0:{SEG[-1][1]:.2f},loudnorm=I=-14:TP=-1.5[a]")
    out = os.path.join(HERE, 'reel-essai.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fil), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    return out


def controle(out):
    """Règles 6 et 7 : images à 0,1/0,5/1/2/3/4 s, différence entre images consécutives."""
    import numpy as np
    from PIL import Image
    ts = [0.1, 0.5, 1, 2, 3, 4]
    ims = []
    for t in ts:
        f = os.path.join(HERE, f'_c{t}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', out, '-frames:v', '1', f], check=True)
        ims.append(np.asarray(Image.open(f).convert('L').resize((270, 480)), dtype=float))
    diffs = [float(abs(ims[i+1] - ims[i]).mean()) for i in range(len(ims) - 1)]
    print('différences entre images consécutives :', [round(d, 1) for d in diffs], '(seuil 2,0)')
    ok = all(d > 2.0 for d in diffs)
    rows = [Image.open(os.path.join(HERE, f'_c{t}.png')).resize((270, 480)) for t in ts]
    sheet = Image.new('RGB', (270 * len(rows), 480)); [sheet.paste(r, (270 * i, 0)) for i, r in enumerate(rows)]
    sheet.save(os.path.join(HERE, 'controle.png'))
    for t in ts: os.remove(os.path.join(HERE, f'_c{t}.png'))
    print('règle mouvement :', 'OK' if ok else 'ÉCHEC')
    return ok


if __name__ == '__main__':
    calques(); o = video(); controle(o)
    print(o, subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', o], capture_output=True, text=True).stdout.strip())
