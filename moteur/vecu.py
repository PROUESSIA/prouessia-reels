"""Formule « vécu » (règles 10 à 13 d'AUTOMATION.md) — un Reel = un dossier NN/ avec NN/vecu.json :
{"titre": "Le client qui dit <b>«&nbsp;je vais réfléchir&nbsp;»</b>",
 "phrases": [{"html": "", "clip": "7376", "debut": 3.0, "cx": 0.35, "sens": 1},   # 1re phrase vide = le titre est dit
             {"html": "Vous vous <b>déplacez</b>", "clip": "85349", "debut": 1.0, "cx": 0.2, "sens": 1}, ...]}
Le texte dit = le texte affiché (balises retirées). Un clip différent par phrase, jamais utilisé dans les 10 dernières vidéos.

  python3 moteur/vecu.py NN texte          → affiche le texte à envoyer au hub (mode voix, voice Charon, style = STYLE)
  python3 moteur/vecu.py NN voix FICHIER   → FICHIER = le .txt écrit par le hub (JSON Gemini) : extrait la voix, la cale phrase par phrase
  python3 moteur/vecu.py NN video          → NN/video.mp4 (+ contrôle mouvement, + videos/clips/utilises.json)
"""
import os, sys, re, json, base64, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'moteur')); sys.path.insert(0, os.path.join(ROOT, 'essai'))
CLIPS = os.path.join(ROOT, 'videos', 'clips'); W, H = 1080, 1920
VOIX_NOM = 'Charon'
STYLE = ("Voix d'homme française, naturelle, comme un artisan qui parle à un collègue sur TikTok. Ton de constat posé, presque "
         "pince-sans-rire, sans aucune emphase publicitaire. Débit rapide (environ 5 mots par seconde). Phrases courtes enchaînées "
         "avec des micro-pauses très brèves. Seule la question finale monte légèrement.")
FIN = 'Prouessia, le partenaire des plombiers.'  # fin identique de chaque Reel (idees/100-idees-reels.pdf)
FIN_HTML = 'Prouessia, <b>le partenaire des plombiers</b><br><span style="font-size:60px;color:#fff">prouessia.fr</span>'
PAUSE = 0.2  # pause entre deux phrases (les références : 0,1 à 0,3 s)

APP = os.path.join(ROOT, 'videos', 'app')
BOITE = (286, 500, 508, 1100)  # x, y, largeur, hauteur de l'écran d'appli : l'écran du téléphone ENTIER (pas de zoom), proportions 1170×2532
def source(clip):
    # « app:07-signature-doigt » = capture de l'application (videos/app/), sinon clip libre de droits (videos/clips/)
    if clip.startswith('app:'):
        n = f'{APP}/norm/{clip[4:]}.mp4'   # version recadrée image par image (moteur/normaliser_app.py)
        return n if os.path.exists(n) else f'{APP}/{clip[4:]}.mp4'
    return f'{CLIPS}/{clip}.mp4'
def zone_utile(chemin, debut=0.0, duree=3.0):
    """Certaines captures vidéo n'occupent qu'un coin de l'image (le reste gris), et la taille peut changer en cours de vidéo :
    on mesure la zone utile sur 5 images de la portion utilisée et on garde la plus fréquente (cache _zones.json)."""
    import numpy as np
    from PIL import Image
    from collections import Counter
    cache = os.path.join(APP, '_zones.json'); z = json.load(open(cache)) if os.path.exists(cache) else {}
    k = f'{os.path.relpath(chemin, APP)}@{debut:.2f}+{duree:.2f}'
    if k not in z:
        tmp = os.path.join(APP, '_z.png'); vus = []
        for j in range(5):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{debut + duree * (j + .5) / 5:.2f}', '-i', chemin, '-frames:v', '1', tmp], check=True)
            a = np.asarray(Image.open(tmp).convert('L')).astype(int); g = abs(a - 128) < 3
            r = np.where(~g.all(1))[0]; c = np.where(~g.all(0))[0]
            vus.append((int(c.max()) + 1 if len(c) else a.shape[1], int(r.max()) + 1 if len(r) else a.shape[0]))
        os.remove(tmp); z[k] = list(Counter(vus).most_common(1)[0][0])
        json.dump(z, open(cache, 'w'), indent=0)
    return z[k]
def masque():
    from PIL import Image, ImageDraw
    f = os.path.join(APP, '_masque.png')
    if not os.path.exists(f):
        im = Image.new('L', BOITE[2:], 0); ImageDraw.Draw(im).rounded_rectangle([0, 0, BOITE[2] - 1, BOITE[3] - 1], 42, fill=255); im.save(f)
    return f
def dit(html):
    t = re.sub(r'<br\s*/?>', ' ', html); t = re.sub(r'<[^>]+>', '', t).replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', t).strip()
def charger(nn, verifier=True):
    c = json.load(open(os.path.join(ROOT, nn, 'vecu.json')))
    if not verifier:
        ph = c['phrases']; l = [(FIN + ' prouessia.fr') if p['html'] == FIN_HTML else (dit(p['html']) or dit(c['titre'])) for p in ph]
        return c, [x if x[-1] in '.?!…' else x + '.' for x in l]
    ph = c['phrases']; clips = [p['clip'] for p in ph]
    assert len(set(clips)) == len(clips), 'règle 12 : un clip différent par phrase'
    u = json.load(open(os.path.join(CLIPS, 'utilises.json')))
    interdits = set(u.get('retires', [])) | {k for v in u['videos'][-10:] if v['video'] != f'{nn}/video.mp4' for k in v['clips']}
    deja = interdits & {k for k in clips if not k.startswith('app:')}
    assert not deja, f'règle 12 : clips déjà utilisés récemment {sorted(deja)}'
    manquants = [k for k in clips if not os.path.exists(source(k))]
    assert not manquants, f'clips à télécharger d\'abord (videos/a_telecharger.txt) : {manquants}'
    lignes = [(FIN + ' prouessia.fr') if p['html'] == FIN_HTML else (dit(p['html']) or dit(c['titre'])) for p in ph]
    lignes = [l if l[-1] in '.?!…' else l + '.' for l in lignes]
    assert ph[-1]['html'] == FIN_HTML, 'la dernière phrase doit être FIN_HTML (fin identique)'
    assert 10 <= len(ph) <= 16, '10 à 16 phrases'
    return c, lignes

def texte(nn):
    _, l = charger(nn, False)
    # prononciation : « Prouèssia », « prouessia point fr »
    t = ' '.join(l).replace('prouessia.fr', 'prouessia point f r').replace('Prouessia', 'Prouèssia').replace('prouessia', 'prouèssia').replace('POV :', 'Pé O Vé :')
    t = re.sub(r'(\d+) h (\d+)', r'\1 heures \2', t)
    print(t)

def voix(nn, fichier):
    import numpy as np, soundfile as sf
    from aligner import aligner
    c, lignes = charger(nn, False); d = os.path.join(ROOT, nn)
    t = open(fichier).read()
    m = re.search(r'"data":"([A-Za-z0-9+/=]+)"', t)
    brut = base64.b64decode(m.group(1)) if m else base64.b64decode(t.rsplit('|', 1)[0])
    wav = os.path.join(d, 'voix-brute.wav')
    if brut[:4] == b'RIFF': open(wav, 'wb').write(brut)
    else:
        open(wav + '.pcm', 'wb').write(brut)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', wav + '.pcm', wav], check=True); os.remove(wav + '.pcm')
    x, sr = sf.read(wav)
    mots = os.path.join(ROOT, 'voix', 'transcrire', f'{nn}.json')
    if os.path.exists(mots):
        from aligner_mots import caler
        seg, manq = caler(mots, lignes); print('calage par les mots, phrases non reconnues :', manq)
    else:
        seg = aligner(wav, lignes)
        os.makedirs(os.path.dirname(mots), exist_ok=True); import shutil; shutil.copy(wav, mots[:-5] + '.wav')
        print('calage provisoire (silences) ; voix envoyée à la transcription : pousser voix/transcrire/ puis relancer')
    out, D = [], []
    for a, b in seg:
        # marges larges (la fin des mots est souvent sous-estimée) sans mordre sur la phrase voisine
        i = len(D); deb = max(0.0, a - .15, (seg[i - 1][1] + .02) if i else 0.0); fin = min(b + .4, (seg[i + 1][0] - .05) if i + 1 < len(seg) else len(x) / sr)
        s = x[int(deb * sr):int(max(fin, b) * sr)]; out += [s, np.zeros(int(PAUSE * sr))]; D.append(round(len(s) / sr + PAUSE, 3))
    D[-1] += .8
    sf.write(os.path.join(d, 'voix.wav'), np.concatenate(out), sr); json.dump(D, open(os.path.join(d, 'durees.json'), 'w'))
    mots = sum(len(l.split()) for l in lignes); tot = sum(D)
    print('voix calée :', round(tot, 1), 's,', round(mots / (tot - .8), 1), 'mots/s')
    for l, (a, b) in zip(lignes, seg): print(f'  {a:5.2f}-{b:5.2f} {l}')

def video(nn):
    from commun import FONTS, MUST
    from playwright.sync_api import sync_playwright
    c, lignes = charger(nn); d = os.path.join(ROOT, nn); P = c['phrases']
    D = json.load(open(os.path.join(d, 'durees.json'))); assert len(D) == len(P); TOTAL = sum(D)
    ico = base64.b64encode(open(os.path.join(ROOT, 'email', 'icone-prouessia.png'), 'rb').read()).decode()
    css = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif}}
.v{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0,rgba(0,0,0,.15) 30%,rgba(0,0,0,.15) 70%,rgba(0,0,0,.45) 100%)}}
.titre,.ph{{position:absolute;left:60px;right:60px;text-align:center;color:#fff;font-weight:900;text-transform:uppercase;letter-spacing:-.01em;
 text-shadow:0 0 3px #000,0 3px 0 #000,0 6px 22px rgba(0,0,0,.7);-webkit-text-stroke:2px #000;paint-order:stroke fill}}
.titre{{top:250px;font-size:64px;line-height:1.08}} .ph{{top:760px;font-size:96px;line-height:1.05}} b{{color:{MUST}}}
.logo{{position:absolute;left:0;right:0;bottom:250px;display:flex;justify-content:center;align-items:center;gap:14px;color:#fff;font-weight:800;font-size:34px;opacity:.9;text-shadow:0 2px 8px #000}}
.logo img{{width:48px;height:48px;border-radius:12px}}
.ph.bas{{top:{BOITE[1]+BOITE[3]+30}px;font-size:62px}} .ph.bas.long{{font-size:52px}} .v.app{{background:linear-gradient(180deg,rgba(0,0,0,.35) 0,rgba(0,0,0,0) 25%)}}"""
    carte = c.get('gabarit') == 'carte'
    if carte:
        css += f""".voile{{position:absolute;left:0;top:0;width:100%;height:1250px;background:linear-gradient(180deg,rgba(11,27,58,.88) 0%,rgba(11,27,58,.72) 45%,rgba(11,27,58,0) 100%)}}
.voile.app{{height:100%;background:linear-gradient(180deg,rgba(11,27,58,.5) 0,rgba(11,27,58,0) 22%,rgba(11,27,58,0) 66%,rgba(11,27,58,.9) 80%)}}
.lg{{position:absolute;left:70px;top:130px;display:flex;align-items:center;gap:18px;color:#fff;font-weight:800;font-size:40px}} .lg img{{width:64px;height:64px;border-radius:16px}}
.t{{position:absolute;left:70px;right:110px;top:300px;color:#fff;font-weight:900;font-size:92px;line-height:1.08;letter-spacing:-.03em;text-shadow:0 4px 18px rgba(0,0,0,.35)}}
.t.bas{{top:1640px;font-size:58px;right:70px}} .t.apres{{top:600px}}
.t b{{background:{MUST};color:#0B1B3A;padding:0 14px;border-radius:14px;box-decoration-break:clone;-webkit-box-decoration-break:clone;text-shadow:none}}
.appel{{position:absolute;left:70px;right:110px;top:280px;display:flex;align-items:center;gap:28px;background:#fff;border-radius:36px;padding:26px 34px;box-shadow:0 18px 40px rgba(0,0,0,.35);color:#0B1B3A}}
.tel{{width:110px;height:110px;border-radius:55px;background:#22A45D;color:#fff;font-size:64px;display:flex;align-items:center;justify-content:center;flex:none}}
.qui{{font-size:38px;font-weight:700;color:#5B6577}} .msg{{font-size:52px;font-weight:900;letter-spacing:-.02em}}"""
    def calque(i, ph):
        app = ph['clip'].startswith('app:')
        if not carte:
            return (f'<div class="v{" app" if app else ""}"></div><div class="titre">{c["titre"]}</div>'
                    f'<div class="ph{(" bas long" if len(dit(ph["html"])) > 38 else " bas") if app else ""}">{ph["html"]}</div><div class="logo"{' style="bottom:auto;top:170px"' if app else ''}><img src="data:image/png;base64,{ico}">prouessia</div>')
        h = ph['html'] or c['titre']; a = ph.get('appel')
        carteh = (f'<div class="appel"><div class="tel">&#9742;</div><div><div class="qui">{a[0]}</div><div class="msg">{a[1]}</div></div></div>') if a else ''
        return (f'<div class="voile{" app" if app else ""}"></div><div class="lg"><img src="data:image/png;base64,{ico}">prouessia</div>{carteh}'
                f'<div class="t{" bas" if app else (" apres" if a else "")}">{h}</div>')
    cq = os.path.join(d, 'calques'); os.makedirs(cq, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        for i, ph in enumerate(P):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{calque(i, ph)}</body></html>')
            pg.wait_for_timeout(120); pg.screenshot(path=f'{cq}/{i}.png', omit_background=True)
        b.close()
    inp, fil, n = [], [], len(P)
    for i, ph in enumerate(P):
        du = D[i]; inp += ['-ss', str(ph.get('debut', 0)), '-t', f'{du + .05:.2f}', '-i', source(ph['clip'])]
        if ph['clip'].startswith('app:'):
            # écran d'appli net dans un cadre arrondi (zoom sur la zone utile : cy = centre vertical 0-1, zoom ≥ 1), fond = la même vidéo floutée et assombrie
            bx, by, bw, bh = BOITE; z = float(ph.get('zoom', 1)); cy = float(ph.get('cy', .5))
            cw = f"min(iw\\,ih*{bw}/{bh})/{z}"; ch = f"min(iw\\,ih*{bw}/{bh})/{z}*{bh}/{bw}"
            zw, zh = zone_utile(source(ph['clip']), float(ph.get('debut', 0)), du)
            fil.append(f"[{i}:v]crop={zw - zw % 2 - 4}:{zh - zh % 2 - 4}:0:0,fps=30,setsar=1,trim=duration={du:.2f},setpts=PTS-STARTPTS,split[a{i}][b{i}]")
            fil.append(f"[a{i}]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.35:saturation=0.6[f{i}]")
            fil.append(f"[b{i}]crop={cw}:{ch}:(iw-{cw})/2:max(0\\,min(ih-{ch}\\,ih*{cy}-{ch}/2)),scale={bw}:{bh}:flags=lanczos,format=rgba[g{i}]")
            fil.append(f"movie={masque()}:loop=0,setpts=N/30/TB,format=gray,scale={bw}:{bh}[m{i}];[g{i}][m{i}]alphamerge[h{i}];[f{i}][h{i}]overlay={bx}:{by}:shortest=1,setsar=1[v{i}]")
        else:
            x = f"max(0\\,min(iw-{W}\\,iw*{ph.get('cx', .5)}-{W/2}+{ph.get('sens', 1)}*300*(t/{du:.2f}-0.5)))"
            fil.append(f"[{i}:v]fps=30,scale=-2:{int(H*(1.18+.03*(i%3)))},crop={W}:{H}:{x}:(ih-{H})/2,setsar=1,trim=duration={du:.2f},setpts=PTS-STARTPTS[v{i}]")
    for i in range(n):
        inp += ['-loop', '1', '-t', f'{D[i]:.2f}', '-i', f'{cq}/{i}.png']
        fil += [f"[{n+i}:v]fps=30,format=rgba,trim=duration={D[i]:.2f},setpts=PTS-STARTPTS[c{i}]", f"[v{i}][c{i}]overlay=0:0:shortest=1[o{i}]"]
    fil.append(''.join(f'[o{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0,format=yuv420p[v]')
    inp += ['-i', os.path.join(d, 'voix.wav')]  # règle 10 : la voix, rien d'autre
    fil.append(f"[{2*n}:a]apad,atrim=0:{TOTAL:.2f},loudnorm=I=-14:TP=-1.5[a]")
    out = os.path.join(d, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fil), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-profile:v', 'main', '-level', '4.0', '-pix_fmt', 'yuv420p', '-crf', '23', '-maxrate', '1700k', '-bufsize', '3400k', '-g', '30', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], check=True)
    import build; build.HERE = d; ok = build.controle(out)
    assert ok, 'règle 6 : mouvement insuffisant, refaire'
    u = json.load(open(os.path.join(CLIPS, 'utilises.json')))
    u['videos'] = [v for v in u['videos'] if v['video'] != f'{nn}/video.mp4'] + [{'video': f'{nn}/video.mp4', 'clips': [p['clip'] for p in P if not p['clip'].startswith('app:')]}]
    json.dump(u, open(os.path.join(CLIPS, 'utilises.json'), 'w'), ensure_ascii=False, indent=1)
    print(out, round(TOTAL, 1), 's')

if __name__ == '__main__':
    nn, quoi = sys.argv[1], sys.argv[2]
    {'texte': lambda: texte(nn), 'voix': lambda: voix(nn, sys.argv[3]), 'video': lambda: video(nn)}[quoi]()
