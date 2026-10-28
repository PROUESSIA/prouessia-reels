"""Les captures de videos/app/ changent de taille en cours de vidéo (écran dans un coin, puis plein cadre).
python3 moteur/normaliser_app.py → videos/app/norm/<nom>.mp4 : chaque image recadrée sur sa zone utile et remise à 780×1688."""
import os, subprocess, numpy as np
from PIL import Image
APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'videos', 'app'); OUT = os.path.join(APP, 'norm'); os.makedirs(OUT, exist_ok=True)
W, H, RW, RH = 1170, 2532, 780, 1688
AW, AH = 585, 1266   # analyse à mi-résolution (plus rapide)
for f in sorted(os.listdir(APP)):
    if not f.endswith('.mp4') or os.path.exists(os.path.join(OUT, f)): continue
    lit = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', os.path.join(APP, f), '-vf', f'fps=30,scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    ecrit = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', os.path.join(OUT, f)], stdin=subprocess.PIPE)
    prec = None; n = 0
    while True:
        b = lit.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        a = np.frombuffer(b, np.uint8).reshape(H, W, 3); l = a[::2, ::2].astype(int).mean(2); gris = np.abs(l - 128) < 4
        r = np.where(~gris.all(1))[0]; c = np.where(~gris.all(0))[0]
        if len(r) and len(c):
            w, h = 2 * (c.max() + 1), 2 * (r.max() + 1)
            if abs(w / h - W / H) < .03: prec = Image.fromarray(a[:h, :w]).resize((RW, RH), Image.LANCZOS)
        if prec is None: prec = Image.fromarray(a).resize((RW, RH))
        ecrit.stdin.write(prec.tobytes()); n += 1
    ecrit.stdin.close(); ecrit.wait(); print(f, n)
