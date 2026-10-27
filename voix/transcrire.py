"""Transcrit chaque voix/transcrire/<nom>.wav en <nom>.json (mots horodatés). Lancé par .github/workflows/transcrire.yml."""
import glob, json, os
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
for w in sorted(glob.glob('voix/transcrire/*.wav')):
    j = w[:-4] + '.json'
    if os.path.exists(j): continue
    segs, _ = m.transcribe(w, language='fr', word_timestamps=True)
    mots = [{'mot': x.word.strip(), 'debut': round(x.start, 3), 'fin': round(x.end, 3)} for s in segs for x in s.words]
    json.dump(mots, open(j, 'w'), ensure_ascii=False, indent=0); print(w, len(mots))
