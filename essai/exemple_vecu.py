"""Exemple « formule vécu » (inspirée des vidéos de référence, sans copier) :
titre fixe en haut + phrase centrale qui change toutes les ~1,5 s + plan différent à chaque phrase + fin en question.
python3 essai/exemple_vecu.py → essai/exemple-vecu.mp4"""
import os, sys, subprocess, base64, math, wave, struct, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'moteur')); sys.path.insert(0, HERE)
from commun import FONTS, INK, MUST
from playwright.sync_api import sync_playwright
CLIPS = os.path.join(ROOT, 'videos', 'clips'); W, H = 1080, 1920
TITRE = 'Le client qui dit <b>«&nbsp;je vais réfléchir&nbsp;»</b>'
# (phrase, clip, départ dans le clip, centre horizontal 0-1, sens du panoramique)
P = [
 ('Tu te <b>déplaces</b>', '4728', 0.5, .5, 1),
 ('Tu trouves <b>la fuite</b>', '257090', 2.0, .25, -1),
 ('Tu fais le devis <b>sur place</b>', '100344', 0.5, .6, 1),
 ('Il te dit&nbsp;: <b>«&nbsp;je vais réfléchir&nbsp;»</b>', '51541', 1.0, .45, -1),
 ('<b>Une semaine.</b><br>Rien.', '136086', 1.0, .3, 1),
 ('Tu n\'oses pas <b>relancer</b>', '257090', 9.0, .7, 1),
 ('Tu ne veux pas passer <b>pour un vendeur</b>', '4728', 6.0, .35, -1),
 ('<b>Trois semaines</b> plus tard…', '51541', 8.0, .6, 1),
 ('Il a signé <b>avec un autre</b>', '136086', 6.0, .7, -1),
 ('Celui qui <b>a rappelé</b>', '100344', 5.0, .4, -1),
 ('Astuce&nbsp;: écris <b>«&nbsp;offre valable 1&nbsp;mois&nbsp;»</b> sur le devis', '257090', 14.0, .2, 1),
 ('Ça te donne <b>une raison</b> de rappeler', '4728', 10.5, .6, 1),
 ('Et toi, <b>tu relances</b> ou tu attends&nbsp;?', '51541', 13.0, .4, -1),
]
def duree(t):
    import re; n = len(re.sub('<[^>]+>|&nbsp;', ' ', t)); return round(min(2.6, 1.0 + 0.045 * n), 2)
D = [duree(p[0]) for p in P]; D[-1] += 1.2; TOTAL = sum(D)
ICONE = base64.b64encode(open(os.path.join(ROOT, 'email', 'icone-prouessia.png'), 'rb').read()).decode()
CSS = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif}}
.v{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0,rgba(0,0,0,.15) 30%,rgba(0,0,0,.15) 70%,rgba(0,0,0,.45) 100%)}}
.titre,.ph{{position:absolute;left:60px;right:60px;text-align:center;color:#fff;font-weight:900;text-transform:uppercase;letter-spacing:-.01em;
 text-shadow:0 0 3px #000,0 3px 0 #000,0 6px 22px rgba(0,0,0,.7);-webkit-text-stroke:2px #000;paint-order:stroke fill}}
.titre{{top:250px;font-size:64px;line-height:1.08}}
.ph{{top:760px;font-size:96px;line-height:1.05}}
b{{color:{MUST}}}
.logo{{position:absolute;left:0;right:0;bottom:250px;display:flex;justify-content:center;align-items:center;gap:14px;color:#fff;font-weight:800;font-size:34px;opacity:.9;text-shadow:0 2px 8px #000}}
.logo img{{width:48px;height:48px;border-radius:12px}}"""
def calques():
    d = os.path.join(HERE, 'calques-vecu'); os.makedirs(d, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        for i, (t, *_ ) in enumerate(P):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="v"></div>'
                           f'<div class="titre">{TITRE}</div><div class="ph">{t}</div>'
                           f'<div class="logo"><img src="data:image/png;base64,{ICONE}">prouessia</div></body></html>')
            pg.wait_for_timeout(120); pg.screenshot(path=f'{d}/{i}.png', omit_background=True)
        b.close()
def musique(path):
    """Petit beat 96 BPM synthétisé (kick, charleston, basse) — libre de droits, sans voix."""
    sr = 44100; n = int(sr * (TOTAL + .2)); s = [0.0] * n; beat = 60 / 96
    notes = [55, 55, 41.2, 49]  # La, La, Mi, Sol (Hz basse)
    for k in range(int(TOTAL / beat) + 1):
        t0 = int(k * beat * sr)
        for j in range(int(.25 * sr)):  # kick
            if t0 + j < n and k % 2 == 0: s[t0 + j] += .9 * math.sin(2 * math.pi * (50 + 90 * math.exp(-j / 900)) * j / sr) * math.exp(-j / 5000)
        th = t0 + int(beat / 2 * sr)
        for j in range(int(.05 * sr)):  # charleston
            if th + j < n: s[th + j] += .18 * (random.random() * 2 - 1) * math.exp(-j / 500)
        f = notes[(k // 4) % 4]
        for j in range(int(beat * .9 * sr)):  # basse
            if t0 + j < n: s[t0 + j] += .28 * math.sin(2 * math.pi * f * j / sr) * math.exp(-j / 9000)
    m = max(abs(x) for x in s)
    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h', int(x / m * 26000)) for x in s))
def video():
    inp, fil = [], []; n = len(P)
    for i, (t, clip, off, cx, sens) in enumerate(P):
        d = D[i]; inp += ['-ss', str(off), '-t', f'{d + .05:.2f}', '-i', f'{CLIPS}/{clip}.mp4']
        x = f"max(0\\,min(iw-{W}\\,iw*{cx}-{W/2}+{sens}*300*(t/{d:.2f}-0.5)))"
        z = 1.18 + .03 * (i % 3)
        fil.append(f"[{i}:v]fps=30,scale=-2:{int(H*z)},crop={W}:{H}:{x}:(ih-{H})/2,setsar=1,trim=duration={d:.2f},setpts=PTS-STARTPTS[v{i}]")
    for i in range(n):
        inp += ['-loop', '1', '-t', f'{D[i]:.2f}', '-i', f'{HERE}/calques-vecu/{i}.png']
        fil.append(f"[{n+i}:v]fps=30,format=rgba,trim=duration={D[i]:.2f},setpts=PTS-STARTPTS[c{i}]")
        fil.append(f"[v{i}][c{i}]overlay=0:0:shortest=1[o{i}]")
    fil.append(''.join(f'[o{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0,format=yuv420p[v]')
    mus = f'{HERE}/musique-vecu.wav'; musique(mus); inp += ['-i', mus]
    fil.append(f"[{2*n}:a]atrim=0:{TOTAL:.2f},afade=t=out:st={TOTAL-1:.2f}:d=1,loudnorm=I=-16:TP=-1.5[a]")
    out = f'{HERE}/exemple-vecu.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fil), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    return out
if __name__ == '__main__':
    calques(); o = video()
    from build import controle
    import build; build.HERE = HERE; controle(o)
    print(o, round(TOTAL, 1), 's', D)
