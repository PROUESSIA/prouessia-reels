"""STYLE 5 « motion » (validé le 30/10/2026) : un Reel = un dossier NN/ avec NN/motion.json.

NN/motion.json :
{"titre": "La relance part toute seule", "idees": [31, 39], "cta": true,
 "phrases": [{"dit": "Le devis est parti lundi.", "scene": "texte", "fond": "ink", "lignes": ["Le devis", "est parti", "lundi."], "jaune": [2], "badge": ["LUN.", "26"]},
             {"dit": "...", "scene": "app", "haut": ["La relance", "part toute seule"], "capture": "extras/14-reglage-relance", "pastille": "Activée ✓"},
             ...,
             {"dit": "Prouessia, le partenaire des plombiers.", "scene": "fin"}],
 "affirmations": [...], "non_couvert": [...], "date": "JJ.MM.AAAA"}
Scènes : voir motion/modele/film.js (texte, surligne, app, question, fin). La dernière phrase est toujours « fin ».
Le texte dit = « dit » (mot pour mot ce qui est écrit à l'écran, à quelques mots près pour les scènes app).

  python3 motion/faire.py NN texte          → texte à envoyer au hub (mode voix, voice Charon, style = STYLE de moteur/vecu.py)
  python3 motion/faire.py NN voix FICHIER   → 1re fois : copie la voix dans voix/transcrire/NN.wav (pousser, attendre l'action) ;
                                              2e fois : calage mot à mot → NN/motion/audio/vo.wav + timing.json (+ phrase DEVIS)
  python3 motion/faire.py NN video          → NN/video.mp4 (1080×1920, 30 i/s, < 8 Mo), NN/cover.png, NN/controle.png, NN/sources.pdf
"""
import os, sys, re, json, base64, shutil, subprocess
ICI = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(ICI)
sys.path.insert(0, os.path.join(ROOT, 'essai')); sys.path.insert(0, os.path.join(ROOT, 'moteur'))
nn, quoi = sys.argv[1], sys.argv[2]
D = os.path.join(ROOT, nn); F = os.path.join(D, 'motion'); CFG = json.load(open(os.path.join(D, 'motion.json')))
P = CFG['phrases']; assert P[-1]['scene'] == 'fin', 'la dernière phrase doit être la scène « fin »'
assert 6 <= len(P) <= 12, '6 à 12 phrases'
CTA_WAV = os.path.join(ROOT, 'voix', 'cta-devis.wav')

def lignes():
    return [p['dit'] if p['dit'][-1] in '.?!…' else p['dit'] + '.' for p in P]

if quoi == 'texte':
    t = ' '.join(lignes()).replace('Prouessia', 'Prouèssia')
    print(re.sub(r'(\d+) h (\d+)', r'\1 heures \2', t))

elif quoi == 'voix':
    import numpy as np, soundfile as sf
    os.makedirs(os.path.join(F, 'audio'), exist_ok=True)
    brute = os.path.join(F, 'audio', 'vo-brute.wav')
    t = open(sys.argv[3]).read(); m = re.search(r'"data":"([A-Za-z0-9+/=]+)"', t)
    b = base64.b64decode(m.group(1)) if m else base64.b64decode(t.rsplit('|', 1)[0])
    if b[:4] == b'RIFF': open(brute, 'wb').write(b)
    else:
        open(brute + '.pcm', 'wb').write(b)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', brute + '.pcm', brute], check=True); os.remove(brute + '.pcm')
    mots = os.path.join(ROOT, 'voix', 'transcrire', f'{nn}.json')
    if not os.path.exists(mots):
        shutil.copy(brute, mots[:-5] + '.wav')
        print('voix copiée dans voix/transcrire/ : pousser, attendre l\'action « Transcrire une voix », git pull, puis relancer cette commande'); sys.exit()
    from aligner_mots import caler
    L = lignes(); seg, manq = caler(mots, L); print('calage par les mots, phrases non reconnues :', manq)
    x, sr = sf.read(brute); out = [np.zeros(int(.35 * sr))]; t0 = .35; ph = []
    for i, (a, bb) in enumerate(seg):
        deb = max(0, a - .15, (seg[i - 1][1] + .02) if i else 0); fin = min(bb + .4, (seg[i + 1][0] - .05) if i + 1 < len(seg) else len(x) / sr)
        s = x[int(deb * sr):int(max(fin, bb) * sr)]
        w = int(.01 * sr); e = np.array([np.sqrt(np.mean(s[k:k + w] ** 2)) for k in range(0, len(s) - w, w)]); v = np.where(e > max(.012, e.max() * .04))[0]
        if len(v): s = s[max(0, v[0] * w - int(.04 * sr)):(v[-1] + 1) * w + int(.06 * sr)]
        ph.append({'a': round(t0, 3), 'b': round(t0 + len(s) / sr, 3), 'text': L[i]}); out.append(s); t0 += len(s) / sr
        gap = .45 if P[i]['scene'] in ('texte', 'surligne', 'question') else .25; out.append(np.zeros(int(gap * sr))); t0 += gap
    cta = None
    if CFG.get('cta', True):
        y, sry = sf.read(CTA_WAV); assert sry == sr
        cta = {'a': round(t0 + .2, 3), 'b': round(t0 + .2 + len(y) / sr, 3)}; out += [np.zeros(int(.2 * sr)), y]
    out.append(np.zeros(int(1.6 * sr)))
    v = np.concatenate(out); sf.write(os.path.join(F, 'audio', 'vo.wav'), v, sr)
    json.dump({'phrases': ph, 'cta': cta}, open(os.path.join(F, 'timing.json'), 'w'), ensure_ascii=False, indent=1)
    print('voix calée :', round(len(v) / sr, 1), 's')
    for p in ph: print(f"  {p['a']:5.2f}-{p['b']:5.2f} {p['text']}")

elif quoi == 'video':
    import numpy as np, soundfile as sf
    MOD = os.path.join(ICI, 'modele')
    for sous in ('lib', 'fonts'):
        shutil.copytree(os.path.join(MOD, sous), os.path.join(F, sous), dirs_exist_ok=True)
    for f in ('film.js', 'index.html'): shutil.copy(os.path.join(MOD, f), os.path.join(F, f))
    os.makedirs(os.path.join(F, 'assets'), exist_ok=True); shutil.copy(os.path.join(MOD, 'assets', 'logo.png'), os.path.join(F, 'assets', 'logo.png'))
    for i, p in enumerate(P):
        if p['scene'] == 'app':
            src = os.path.join(ROOT, 'videos', 'app', p['capture'] + '.png'); assert os.path.exists(src), f'capture introuvable : {src}'
            shutil.copy(src, os.path.join(F, 'assets', f'cap{i}.png'))
    tj = json.load(open(os.path.join(F, 'timing.json')))
    dur = round(len(sf.read(os.path.join(F, 'audio', 'vo.wav'))[0]) / 24000, 2)
    json.dump({'titre': CFG['titre'], 'phrases': P, 'cta': CFG.get('cta', True), 'mot': CFG.get('mot', 'DEVIS')}, open(os.path.join(F, 'script.json'), 'w'), ensure_ascii=False, indent=1)
    beats = [float(i) for i in range(int(dur) + 2)]
    json.dump({'offset': 0, 'period': 1, 'bpm': 60, 'beats': beats, 'downbeats': beats[::4], 'sections': [], 'energy': []}, open(os.path.join(F, 'beats.json'), 'w'))
    json.dump({'title': CFG['titre'], 'duration': dur, 'formats': ['9x16'], 'poster': tj['phrases'][min(3, len(P) - 1)]['a'] + 1}, open(os.path.join(F, 'film.json'), 'w'))
    # Playwright : celui de la machine (lien vers l'installation globale, même version que le navigateur installé)
    nm = os.path.join(ICI, 'node_modules', 'playwright')
    if not os.path.exists(nm):
        g = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
        os.makedirs(os.path.dirname(nm), exist_ok=True)
        for pk in ('playwright', 'playwright-core'):
            if os.path.exists(os.path.join(g, pk)) and not os.path.exists(os.path.join(ICI, 'node_modules', pk)): os.symlink(os.path.join(g, pk), os.path.join(ICI, 'node_modules', pk))
    subprocess.run(['node', os.path.join(ICI, 'outils', 'render.mjs'), '--film', 'motion', '--format', '9x16', '--video-only'], cwd=D, check=True)
    vid = os.path.join(D, 'out', 'motion', 'video_9x16.mp4'); out = os.path.join(D, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', os.path.join(F, 'audio', 'vo.wav'), '-filter_complex', '[1:a]loudnorm=I=-14:TP=-1.5[a]',
                    '-map', '0:v', '-map', '[a]', '-r', '30', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'main', '-level', '4.0', '-pix_fmt', 'yuv420p',
                    '-b:v', '1600k', '-maxrate', '1800k', '-bufsize', '3600k', '-g', '30', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], check=True)
    # contrôles : taille, une image par phrase (planche), aucune phrase muette
    taille = os.path.getsize(out); assert taille < 8e6, f'vidéo trop lourde : {taille}'
    x, sr = sf.read(os.path.join(F, 'audio', 'vo.wav'))
    for p in tj['phrases']:
        sg = x[int(p['a'] * sr):int(p['b'] * sr)]; w = int(.01 * sr)
        parle = sum(1 for j in range(0, max(0, len(sg) - w), w) if np.sqrt(np.mean(sg[j:j + w] ** 2)) > .02) * .01
        assert parle >= max(.25, .08 * len(p['text'].split())), f"phrase presque muette : {p['text']}"
    from PIL import Image
    ims = []
    for p in tj['phrases'] + ([tj['cta']] if tj.get('cta') else []):
        f = os.path.join(F, '_c.png'); subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{p['a'] + (p['b'] - p['a']) * .7:.2f}", '-i', out, '-frames:v', '1', f], check=True)
        ims.append(Image.open(f).resize((270, 480)).copy())
    sh = Image.new('RGB', (270 * min(6, len(ims)), 480 * ((len(ims) + 5) // 6)))
    for i, im in enumerate(ims): sh.paste(im, ((i % 6) * 270, (i // 6) * 480))
    sh.save(os.path.join(D, 'controle.png'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{tj['phrases'][0]['a'] + .9:.2f}", '-i', out, '-frames:v', '1', os.path.join(D, 'cover.png')], check=True)
    # fiche sources
    S = {'num': nn, 'titre': CFG['titre'], 'date': CFG.get('date', ''), 'affirmations': CFG['affirmations'], 'non_couvert': CFG.get('non_couvert', []),
         'avert': CFG.get('avert', 'Information générale, pas un conseil personnalisé.'), 'videos': [],
         'licence_videos': 'Animation réalisée par Prouessia (aucune vidéo extérieure ; écrans : compte de démonstration)',
         'voix': 'Google AI Studio (Gemini TTS), voix « Charon » ; aucune musique'}
    json.dump(S, open(os.path.join(D, 'sources.json'), 'w'), ensure_ascii=False, indent=1)
    subprocess.run(['python3', 'fiche_sources.py', os.path.join(D, 'sources.json'), os.path.join(D, 'sources.pdf')], cwd=os.path.join(ROOT, 'moteur'), check=True)
    print(out, round(taille / 1e6, 1), 'Mo ; planche :', os.path.join(D, 'controle.png'))
