"""python3 moteur/sources_reel.py NN  → NN/sources.json + NN/sources.pdf à partir de NN/vecu.json et du champ « affirmations » de NN/vecu.json."""
import os, sys, json, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); nn = sys.argv[1]
c = json.load(open(os.path.join(ROOT, nn, 'vecu.json')))
H = {}
for f in os.listdir(os.path.join(ROOT, 'videos', 'pixabay')):
    t = open(os.path.join(ROOT, 'videos', 'pixabay', f)).read().split('\n', 1)
    try: d = json.loads(t[1])
    except Exception: continue
    for h in d.get('hits', []): H[str(h['id'])] = h
vids = []
for p in c['phrases']:
    k = p['clip']
    if k.startswith('app:'): continue
    h = H.get(k, {}); vids.append({'id': k, 'sujet': (h.get('tags', '').split(',')[0] or 'vidéo').strip(), 'url': f'https://pixabay.com/videos/id-{k}/', 'auteur': h.get('user', 'Pixabay')})
titre = re.sub(r'&nbsp;', ' ', c['titre']); titre = re.sub(r'</?b>', '', titre)
S = {'num': nn, 'titre': titre, 'date': c.get('date', ''), 'affirmations': c['affirmations'], 'non_couvert': c.get('non_couvert', []),
     'avert': c.get('avert', 'Information générale, pas un conseil personnalisé.'), 'videos': vids,
     'licence_videos': 'Licence Pixabay : usage commercial, sans attribution obligatoire',
     'voix': 'Google AI Studio (Gemini TTS), voix « Charon », style de moteur/vecu.py ; aucune musique'}
json.dump(S, open(os.path.join(ROOT, nn, 'sources.json'), 'w'), ensure_ascii=False, indent=1)
subprocess.run(['python3', 'fiche_sources.py', os.path.join(ROOT, nn, 'sources.json'), os.path.join(ROOT, nn, 'sources.pdf')], cwd=os.path.join(ROOT, 'moteur'), check=True)
print(nn, 'sources ok', len(vids), 'vidéos')
