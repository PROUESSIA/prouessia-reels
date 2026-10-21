"""Reel 12 · Urgence de nuit (style E, mini-scène) · formule « vraies vidéos » de essai/build.py.
python3 12/reel.py  → 12/video.mp4 + 12/controle.png + 12/cover.png"""
import os, sys, subprocess, base64
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'moteur'))
from commun import FONTS, INK, MUST
from playwright.sync_api import sync_playwright

CLIPS = os.path.join(ROOT, 'videos', 'clips')
VOIX = os.path.join(HERE, 'voix.mp3')
W, H = 1080, 1920
# (début, fin, clip, départ dans le clip, sens du panoramique, centre horizontal du sujet 0-1, texte HTML)
APPEL = '<div class="appel"><div class="tel">&#9742;</div><div><div class="qui">Client · 22&nbsp;h&nbsp;04</div><div class="msg">« Ça fuit sous l\'évier&nbsp;! »</div></div></div>'
SEG = [
    (0.00, 2.15, '257090', 3.0, -1, 0.2, APPEL + '<div class="t2">22&nbsp;h, une fuite.<br>Avant la caisse à outils&nbsp;: <b>le devis</b>.</div>'),
    (2.15, 3.95, '4728', 7.0, 1, 0.5, 'Avant la caisse à outils&nbsp;:<br><b>le devis</b>.'),
    (3.95, 7.05, '100344', 1.5, 1, 0.62, 'Chez un particulier&nbsp;:<br>obligatoire <b>dès le 1<sup>er</sup>&nbsp;euro</b>.'),
    (7.05, 8.80, '136086', 5.0, -1, 0.33, 'Remis <b>avant</b><br>l\'intervention.'),
    (8.80, 10.20, '51541', 8.0, 1, 0.45, 'Un devis<br><b>sans réponse</b>&nbsp;?'),
    (10.20, 12.35, '257090', 12.0, 1, 0.2, '<b>Prouessia</b> le relance tout seul, par e-mail.'),
    (12.35, 14.40, '136086', 8.5, 1, 0.33, 'Et vous, le devis de nuit&nbsp;:<br><b>vous le faites&nbsp;?</b>'),
    (14.40, 16.20, '4728', 11.0, -1, 0.5, 'Le devis de nuit&nbsp;:<br><b>vous le faites&nbsp;?</b><div class="q">Dites-le en commentaire</div>'),
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
.appel{{position:absolute;left:70px;right:130px;top:280px;display:flex;align-items:center;gap:28px;background:#fff;border-radius:36px;padding:26px 34px;box-shadow:0 18px 40px rgba(0,0,0,.35);color:{INK}}}
.tel{{width:110px;height:110px;border-radius:55px;background:#22A45D;color:#fff;font-size:64px;display:flex;align-items:center;justify-content:center;flex:none}}
.qui{{font-size:38px;font-weight:700;color:#5B6577}}
.msg{{font-size:54px;font-weight:900;letter-spacing:-.02em}}
.t2{{position:absolute;left:70px;right:130px;top:560px;color:#fff;font-weight:900;font-size:92px;line-height:1.08;letter-spacing:-.03em;text-shadow:0 4px 18px rgba(0,0,0,.35)}}
.t2 b{{background:{MUST};color:{INK};padding:0 14px;border-radius:14px;text-shadow:none}}
.q{{margin-top:34px;display:inline-block;font-size:48px;font-weight:800;background:#fff;color:{INK};padding:16px 26px;border-radius:999px;text-shadow:none}}
"""


def calques():
    os.makedirs(os.path.join(HERE, 'calques'), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        for i, s in enumerate(SEG):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="voile"></div>'
                           f'<div class="logo"><img src="data:image/png;base64,{ICONE}">prouessia</div>' + (s[6] if 'class="appel"' in s[6] else f'<div class="t">{s[6]}</div>') + '</body></html>')
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
    out = os.path.join(HERE, 'video.mp4')
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
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.3', '-i', o, '-frames:v', '1', os.path.join(HERE, 'cover.png')], check=True)
    print(o, subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', o], capture_output=True, text=True).stdout.strip())
