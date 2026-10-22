"""Aperçu rapide : une image au milieu de chaque plan 3D → planche. python3 apercu_film.py ep01 sortie.png"""
import os, sys, json, base64
from playwright.sync_api import sync_playwright
from PIL import Image
ICI = os.path.dirname(os.path.abspath(__file__)); EPD = os.path.join(ICI, sys.argv[1])
tl = json.load(open(os.path.join(EPD, 'timeline.json'))); ims = []
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}); pg.goto('file://' + os.path.join(ICI, 'film.html'))
    pg.wait_for_function('window.pret === true', timeout=60000); pg.evaluate(f'setEpisode({json.dumps(tl)})')
    for pl in tl['plans']:
        for t in (pl['debut'] + .05, (pl['debut'] + pl['fin']) / 2):
            pg.evaluate(f'render({t})')
        d = pg.evaluate("document.querySelector('canvas').toDataURL('image/jpeg', 0.8)")
        f = '/tmp/_a.jpg'; open(f, 'wb').write(base64.b64decode(d.split(',')[1])); ims.append(Image.open(f).resize((216, 384)).copy())
    b.close()
n = len(ims); cols = 9; s = Image.new('RGB', (216 * cols, 384 * ((n + cols - 1) // cols)))
for i, im in enumerate(ims): s.paste(im, ((i % cols) * 216, (i // cols) * 384))
s.save(sys.argv[2])
