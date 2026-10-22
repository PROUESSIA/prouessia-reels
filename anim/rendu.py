"""Rend la scène 3D image par image (Playwright + three.js) : python3 rendu.py timeline.json frames/ [fps] [t_debut t_fin] [pas]"""
import sys, json, os, base64, time
from playwright.sync_api import sync_playwright
tl = json.load(open(sys.argv[1])); out = sys.argv[2]; fps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0; t1 = float(sys.argv[5]) if len(sys.argv) > 5 else max(r['plan_fin'] for r in tl)
pas = int(sys.argv[6]) if len(sys.argv) > 6 else 1
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + os.path.abspath('scene.html')); pg.wait_for_function('window.pret === true', timeout=60000)
    pg.evaluate(f'setTimeline({json.dumps(tl)})')
    n0, n1 = int(t0 * fps), int(t1 * fps); d = time.time()
    for n in range(n0, n1, 1):
        if (n - n0) % pas: continue
        pg.evaluate(f'render({n / fps})')
        data = pg.evaluate("document.querySelector('canvas').toDataURL('image/jpeg', 0.92)")
        open(f'{out}/{n:05d}.jpg', 'wb').write(base64.b64decode(data.split(',')[1]))
    print(n1 - n0, 'images en', round(time.time() - d), 's')
    b.close()
