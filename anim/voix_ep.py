"""Voix d'un épisode : python3 anim/voix_ep.py epNN decoder → <qui>.wav + <qui>-court.wav (+ copie dans voix/transcrire/epNN-<qui>.wav)
                     python3 anim/voix_ep.py epNN mots    → mots-<qui>.json (mots horodatés de la transcription, rangés par réplique) + segments"""
import os, sys, re, json, base64, subprocess, shutil
ICI = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(ICI)
sys.path.insert(0, os.path.join(ROOT, 'essai'))
ep = sys.argv[1]; D = os.path.join(ICI, ep); EP = json.load(open(os.path.join(D, 'episode.json')))
TR = os.path.join(ROOT, 'voix', 'transcrire')
if sys.argv[2] == 'decoder':
    for qui in EP['textes']:
        f = os.path.join(D, f'voix-{qui}-gemini.txt')
        if not os.path.exists(f): print('manque', f); continue
        t = open(f).read(); m = re.search(r'"data":"([A-Za-z0-9+/=]+)"', t)
        brut = base64.b64decode(m.group(1)) if m else base64.b64decode(t.rsplit('|', 1)[0]); w = os.path.join(D, f'{qui}.wav')
        if brut[:4] == b'RIFF': open(w, 'wb').write(brut)
        else:
            open(w + '.pcm', 'wb').write(brut)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', w + '.pcm', w], check=True); os.remove(w + '.pcm')
        shutil.copy(w, os.path.join(D, f'{qui}-court.wav')); shutil.copy(w, os.path.join(TR, f'{ep}-{qui}.wav')); print(qui, 'ok')
else:
    from aligner_mots import norm, caler
    for qui, lignes in EP['textes'].items():
        j = os.path.join(TR, f'{ep}-{qui}.json'); M = json.load(open(j))
        seg, manq = caler(j, lignes); EP.setdefault('segments', {})[qui] = [[round(a, 2), round(b, 2)] for a, b in seg]
        # mots affichés = mots du texte (orthographe du script), temps répartis sur les mots transcrits de la réplique
        out = []
        for l, (a, b) in zip(lignes, seg):
            ws = l.split(); tm = [m for m in M if m['debut'] >= a - .01 and m['fin'] <= b + .01] or [{'debut': a, 'fin': b}]
            n = len(ws); out.append([[w, round(tm[min(len(tm) - 1, int(i * len(tm) / n))]['debut'], 3), round(tm[min(len(tm) - 1, int((i + 1) * len(tm) / n - 1e-9))]['fin'], 3)] for i, w in enumerate(ws)])
        json.dump(out, open(os.path.join(D, f'mots-{qui}.json'), 'w'), ensure_ascii=False); print(qui, 'non reconnues', manq, EP['segments'][qui])
    json.dump(EP, open(os.path.join(D, 'episode.json'), 'w'), ensure_ascii=False, indent=1)
