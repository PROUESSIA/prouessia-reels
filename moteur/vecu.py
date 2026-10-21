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

def dit(html):
    t = re.sub(r'<br\s*/?>', ' ', html); t = re.sub(r'<[^>]+>', '', t).replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', t).strip()
def charger(nn):
    c = json.load(open(os.path.join(ROOT, nn, 'vecu.json')))
    ph = c['phrases']; clips = [p['clip'] for p in ph]
    assert len(set(clips)) == len(clips), 'règle 12 : un clip différent par phrase'
    u = json.load(open(os.path.join(CLIPS, 'utilises.json')))
    interdits = set(u.get('retires', [])) | {k for v in u['videos'][-10:] if v['video'] != f'{nn}/video.mp4' for k in v['clips']}
    deja = interdits & set(clips)
    assert not deja, f'règle 12 : clips déjà utilisés récemment {sorted(deja)}'
    manquants = [k for k in clips if not os.path.exists(f'{CLIPS}/{k}.mp4')]
    assert not manquants, f'clips à télécharger d\'abord (videos/a_telecharger.txt) : {manquants}'
    lignes = [(FIN + ' prouessia.fr') if p['html'] == FIN_HTML else (dit(p['html']) or dit(c['titre'])) for p in ph]
    lignes = [l if l[-1] in '.?!…' else l + '.' for l in lignes]
    assert ph[-1]['html'] == FIN_HTML, 'la dernière phrase doit être FIN_HTML (fin identique)'
    assert 10 <= len(ph) <= 16, '10 à 16 phrases'
    return c, lignes

def texte(nn):
    _, l = charger(nn)
    # prononciation : « Prouèssia », « prouessia point fr »
    t = ' '.join(l).replace('prouessia.fr', 'prouessia point f r').replace('Prouessia', 'Prouèssia').replace('prouessia', 'prouèssia')
    print(t)

def voix(nn, fichier):
    import numpy as np, soundfile as sf
    from aligner import aligner
    c, lignes = charger(nn); d = os.path.join(ROOT, nn)
    t = open(fichier).read()
    m = re.search(r'"data":"([A-Za-z0-9+/=]+)"', t)
    brut = base64.b64decode(m.group(1)) if m else base64.b64decode(t.rsplit('|', 1)[0])
    wav = os.path.join(d, 'voix-brute.wav')
    if brut[:4] == b'RIFF': open(wav, 'wb').write(brut)
    else:
        open(wav + '.pcm', 'wb').write(brut)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', wav + '.pcm', wav], check=True); os.remove(wav + '.pcm')
    x, sr = sf.read(wav); seg = aligner(wav, lignes); out, D = [], []
    for a, b in seg:
        s = x[int(max(0, a - .03) * sr):int((b + .05) * sr)]; out += [s, np.zeros(int(PAUSE * sr))]; D.append(round(len(s) / sr + PAUSE, 3))
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
.logo img{{width:48px;height:48px;border-radius:12px}}"""
    cq = os.path.join(d, 'calques'); os.makedirs(cq, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        for i, ph in enumerate(P):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="v"></div><div class="titre">{c["titre"]}</div>'
                           f'<div class="ph">{ph["html"]}</div><div class="logo"><img src="data:image/png;base64,{ico}">prouessia</div></body></html>')
            pg.wait_for_timeout(120); pg.screenshot(path=f'{cq}/{i}.png', omit_background=True)
        b.close()
    inp, fil, n = [], [], len(P)
    for i, ph in enumerate(P):
        du = D[i]; inp += ['-ss', str(ph.get('debut', 0)), '-t', f'{du + .05:.2f}', '-i', f'{CLIPS}/{ph["clip"]}.mp4']
        x = f"max(0\\,min(iw-{W}\\,iw*{ph.get('cx', .5)}-{W/2}+{ph.get('sens', 1)}*300*(t/{du:.2f}-0.5)))"
        fil.append(f"[{i}:v]fps=30,scale=-2:{int(H*(1.18+.03*(i%3)))},crop={W}:{H}:{x}:(ih-{H})/2,setsar=1,trim=duration={du:.2f},setpts=PTS-STARTPTS[v{i}]")
    for i in range(n):
        inp += ['-loop', '1', '-t', f'{D[i]:.2f}', '-i', f'{cq}/{i}.png']
        fil += [f"[{n+i}:v]fps=30,format=rgba,trim=duration={D[i]:.2f},setpts=PTS-STARTPTS[c{i}]", f"[v{i}][c{i}]overlay=0:0:shortest=1[o{i}]"]
    fil.append(''.join(f'[o{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0,format=yuv420p[v]')
    inp += ['-i', os.path.join(d, 'voix.wav')]  # règle 10 : la voix, rien d'autre
    fil.append(f"[{2*n}:a]apad,atrim=0:{TOTAL:.2f},loudnorm=I=-14:TP=-1.5[a]")
    out = os.path.join(d, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fil), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264',
                    '-preset', 'medium', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    import build; build.HERE = d; ok = build.controle(out)
    assert ok, 'règle 6 : mouvement insuffisant, refaire'
    u = json.load(open(os.path.join(CLIPS, 'utilises.json')))
    u['videos'] = [v for v in u['videos'] if v['video'] != f'{nn}/video.mp4'] + [{'video': f'{nn}/video.mp4', 'clips': [p['clip'] for p in P]}]
    json.dump(u, open(os.path.join(CLIPS, 'utilises.json'), 'w'), ensure_ascii=False, indent=1)
    print(out, round(TOTAL, 1), 's')

if __name__ == '__main__':
    nn, quoi = sys.argv[1], sys.argv[2]
    {'texte': lambda: texte(nn), 'voix': lambda: voix(nn, sys.argv[3]), 'video': lambda: video(nn)}[quoi]()
