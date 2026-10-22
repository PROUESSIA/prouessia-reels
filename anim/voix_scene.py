"""Découpe les voix des personnages en répliques, resserre les silences internes, et monte la piste de dialogue.
Sortie : dialogue.wav + timeline.json (début/fin de chaque réplique)."""
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, '../essai'); from aligner import aligner
L = json.load(open('script.json'))
def resserrer(s, sr, max_sil=0.22, seuil=0.02):
    w = int(.02 * sr); e = np.array([np.abs(s[i:i + w]).mean() for i in range(0, len(s), w)]); calme = e < seuil
    out = []; i = 0
    while i < len(calme):
        j = i
        while j < len(calme) and calme[j] == calme[i]: j += 1
        seg = s[i * w:j * w]
        if calme[i] and (j - i) * .02 > max_sil and i > 0 and j < len(calme): seg = seg[:int(max_sil * sr)]
        out.append(seg); i = j
    return np.concatenate(out)
pistes = {}
for perso in ('ines', 'karim', 'narrateur'):
    lignes = [r['texte'] for r in L['repliques'] if r['qui'] == perso]
    x, sr = sf.read(f'{perso}.wav'); seg = aligner(f'{perso}.wav', lignes)
    pistes[perso] = [resserrer(x[int(max(0, a - .03) * sr):int((b + .06) * sr)], sr) for a, b in seg]
idx = {k: 0 for k in pistes}; t = 0.0; out = []; tl = []
for r in L['repliques']:
    s = pistes[r['qui']][idx[r['qui']]]; idx[r['qui']] += 1
    pause = r.get('pause_avant', .25)
    out.append(np.zeros(int(pause * sr))); t += pause
    tl.append({**r, 'debut': round(t, 3), 'fin': round(t + len(s) / sr, 3)}); out.append(s); t += len(s) / sr
out.append(np.zeros(int(.6 * sr)))
sf.write('dialogue.wav', np.concatenate(out), sr); json.dump(tl, open('timeline.json', 'w'), ensure_ascii=False, indent=1)
for r in tl: print(f"{r['debut']:6.2f}-{r['fin']:6.2f} {r['qui']:9} {r['texte']}")
print('total', round(t + .6, 2))
