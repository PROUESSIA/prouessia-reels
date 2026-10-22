"""Court film « Sous pression » : python3 film.py ep01 [--sans3d] → ep01/film.mp4
L'épisode est décrit dans epNN/episode.json (textes, voix, segments, déroulé des plans) ; les décors et personnages sont dans film.html."""
import os, sys, json, base64, subprocess, re
import numpy as np, soundfile as sf
ICI = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(ICI)
sys.path.insert(0, os.path.join(ROOT, 'moteur'))
from commun import FONTS, MUST
W, H, FPS, SR = 1080, 1920, 30, 24000
EPD = os.path.join(ICI, sys.argv[1]); EP = json.load(open(os.path.join(EPD, 'episode.json')))

def mots_ligne(texte, a, b, chunks):
    """Mots d'une réplique avec leurs temps, répartis sur la parole (sans les silences) au prorata des lettres."""
    ws = texte.split(); parole = [(max(a, x), min(b, y)) for x, y in chunks if y > a and x < b] or [(a, b)]
    tot = sum(y - x for x, y in parole); poids = [len(w) + 1 for w in ws]; S = sum(poids); out = []; acc = 0
    def temps(f):  # fraction de parole → temps réel
        r = f * tot
        for x, y in parole:
            if r <= y - x: return x + r
            r -= y - x
        return parole[-1][1]
    for w, p in zip(ws, poids): out.append((w, temps(acc / S), temps((acc + p) / S))); acc += p
    return out
def chunks_de(wav):
    o = subprocess.run(['ffmpeg', '-i', wav, '-af', 'silencedetect=n=-35dB:d=0.15', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', o)]; e = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', o)]
    dur = sf.info(wav).duration; out = []; t = 0
    for a, b in zip(s, e + [dur]):
        if a > t: out.append((t, a))
        t = b
    if t < dur: out.append((t, dur))
    return out

def preparer():
    pistes, lignes = {}, {}
    for qui in EP['textes']:
        wav = os.path.join(EPD, f'{qui}-court.wav'); x, _ = sf.read(wav); pistes[qui] = x
        if os.path.exists(os.path.join(EPD, f'mots-{qui}.json')):      # transcription mot à mot (ElevenLabs)
            mots = json.load(open(os.path.join(EPD, f'mots-{qui}.json')))   # une liste de mots [mot, début, fin] par réplique
            assert len(mots) == len(EP['textes'][qui]), qui
            lignes[qui] = [(g[0][1], g[-1][2], [tuple(w) for w in g]) for g in mots]
        else:
            ch = chunks_de(wav); lignes[qui] = []
            for t, (a, b) in zip(EP['textes'][qui], EP['segments'][qui]): lignes[qui].append((a, b, mots_ligne(t, a, b, ch)))
    R = EP.get('rythme', {}); fp, fs, v = R.get('pauses', 1), R.get('silences', 1), R.get('vitesse', 1)
    if v != 1:   # voix accélérée sans changer la hauteur
        for qui in list(pistes):
            src = os.path.join(EPD, f'{qui}-court.wav'); dst = os.path.join(EPD, f'{qui}-v.wav')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', f'atempo={v}', '-ar', str(SR), dst], check=True)
            pistes[qui], _ = sf.read(dst)
            lignes[qui] = [(a / v, b / v, [(w, x / v, y / v) for w, x, y in ms]) for a, b, ms in lignes[qui]]
    out, t, items = [], 0.0, []
    for it in EP['deroule']:
        if 'qui' in it:
            a, b, ms = lignes[it['qui']][it['n']]; seg = pistes[it['qui']][int((a - .04) * SR):int((b + .08) * SR)]
            pz = it.get('pause', .3) * fp; out.append(np.zeros(int(pz * SR))); t0 = t; t += pz
            items.append({**it, 'debut': round(t0, 3), 'parole': [round(t, 3), round(t + len(seg) / SR, 3)], 'texte': EP['textes'][it['qui']][it['n']],
                          'mots': [(w, round(t + x - a + .04, 3), round(t + y - a + .04, 3)) for w, x, y in ms]})
            out.append(seg); t += len(seg) / SR
        else:
            du = it['duree'] * (fs if 'decor' in it else 1)
            items.append({**it, 'debut': round(t, 3), 'parole': None, 'mots': []}); out.append(np.zeros(int(du * SR))); t += du
    out.append(np.zeros(int(1.2 * SR))); total = t + 1.2
    piste = np.concatenate(out + [np.zeros(SR * 3)])
    for it in items:                                   # signature sonore : sonnerie et générique (aucune musique)
        if it.get('son'):
            x, _ = sf.read(os.path.join(ICI, 'sons', it['son'] + '.wav')); i = int(it['debut'] * SR); piste[i:i + len(x)] += x * it.get('volume', .5)
    out = [piste[:int(total * SR)]]
    for i, it in enumerate(items): it['fin'] = items[i + 1]['debut'] if i + 1 < len(items) else round(total, 3)
    sf.write(os.path.join(EPD, 'dialogue.wav'), np.concatenate(out), SR)
    # pour film.html : plans 3D + événements + répliques
    plans = [{'decor': it['decor'], 'debut': it['debut'], 'fin': it['fin'], 'cam': it['cam'], 'cible': it['cible'], 'regards': it.get('regards', {})} for it in items if 'decor' in it]
    evs = [{'decor': it['decor'], 'nom': e, 'debut': it['debut'], 'fin': it['fin']} for it in items if 'decor' in it for e in it.get('ev', [])]
    reps = [{'qui': it['qui'], 'debut': it['parole'][0], 'fin': it['parole'][1]} for it in items if it.get('parole')]
    json.dump({'plans': plans, 'evenements': evs, 'repliques': reps}, open(os.path.join(EPD, 'timeline.json'), 'w'), ensure_ascii=False)
    json.dump(items, open(os.path.join(EPD, 'items.json'), 'w'), ensure_ascii=False, indent=1)
    return items, total

def rendu3d(items):
    from playwright.sync_api import sync_playwright
    fr = os.path.join(EPD, 'frames'); os.makedirs(fr, exist_ok=True); tl = json.load(open(os.path.join(EPD, 'timeline.json')))
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': W, 'height': H}); pg.goto('file://' + os.path.join(ICI, 'film.html'))
        pg.wait_for_function('window.pret === true', timeout=60000); pg.evaluate(f'setEpisode({json.dumps(tl)})')
        for it in items:
            if 'decor' not in it: continue
            for n in range(int(it['debut'] * FPS), int(it['fin'] * FPS) + 1):
                f = f'{fr}/{n:05d}.jpg'
                if os.path.exists(f): continue
                pg.evaluate(f'render({n / FPS})')
                d = pg.evaluate("document.querySelector('canvas').toDataURL('image/jpeg', 0.92)"); open(f, 'wb').write(base64.b64decode(d.split(',')[1]))
        b.close()

CSS = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif}}
.st{{position:absolute;left:70px;right:70px;top:1150px;text-align:center;color:#fff;font-weight:700;font-size:60px;line-height:1.15;-webkit-text-stroke:3px #000;paint-order:stroke fill;text-shadow:0 3px 14px rgba(0,0,0,.8)}}
.st b{{font-weight:900;color:{MUST}}} .x{{visibility:hidden}}
.inc{{position:absolute;left:0;right:0;top:250px;text-align:center;color:#fff;font-weight:800;font-size:44px;letter-spacing:.08em;-webkit-text-stroke:2px #000;paint-order:stroke fill}}
.serie{{position:absolute;left:60px;top:150px;color:#fff;font-weight:900;font-size:34px;letter-spacing:.12em;-webkit-text-stroke:2px #000;paint-order:stroke fill}} .serie span{{color:{MUST}}}"""

def calques(items, total):
    from playwright.sync_api import sync_playwright
    d = os.path.join(EPD, 'st'); os.makedirs(d, exist_ok=True); seq = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); k = [0]
        def img(html):
            f = os.path.join(d, f'{k[0]:03d}.png'); k[0] += 1
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>'); pg.wait_for_timeout(50)
            pg.screenshot(path=f, omit_background=True); return f
        serie = f'<div class="serie">{EP["serie"].upper()} <span>· ÉP. {EP["numero"]}</span></div>'
        for it in items:
            if it.get('carte') and not it['mots']: seq.append((img(''), it['fin'] - it['debut'])); continue
            haut = serie if it['debut'] < 4 else ''
            inc = f'<div class="inc">{it["incrust"]}</div>' if it.get('incrust') else ''
            if not it['mots']:
                st = f'<div class="st">{it["soustitre"]}</div>' if it.get('soustitre') else ''
                seq.append((img(haut + inc + st), it['fin'] - it['debut'])); continue
            ws = [w for w, _, _ in it['mots']]; ng = it.get('gras', 0); t = it['debut']
            for j, (w, a, bb) in enumerate(it['mots']):
                if a > t: seq.append((seq[-1][0] if j else img(haut + inc), a - t)); t = a
                sp = lambda i, x: f'<span class="{"" if i <= j else "x"}">{x}</span>'
                n1 = ' '.join(sp(i, x) for i, x in enumerate(ws[:len(ws) - ng])); n2 = ' '.join(sp(i + len(ws) - ng, x) for i, x in enumerate(ws[len(ws) - ng:]))
                fin = it['mots'][j + 1][1] if j + 1 < len(ws) else it['fin']
                seq.append((img(haut + inc + f'<div class="st">{n1} {"<b>" + n2 + "</b>" if ng else ""}</div>'), fin - t)); t = fin
        b.close()
    with open(os.path.join(d, 'liste.txt'), 'w') as fh:
        for f, du in seq: fh.write(f"file '{f}'\nduration {max(du, .001):.3f}\n")
        fh.write(f"file '{seq[-1][0]}'\n")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(d, 'liste.txt'), '-vf', f'fps={FPS},format=rgba', '-c:v', 'qtrle', os.path.join(EPD, 'calques.mov')], check=True)

def carte(nom, fond, du, out):
    from playwright.sync_api import sync_playwright
    ico = base64.b64encode(open(os.path.join(ROOT, 'email', 'icone-prouessia.png'), 'rb').read()).decode()
    if nom == 'sponsor':
        corps = f"""<div class="s" style="margin:0">présenté par</div><div class="m"><img src="data:image/png;base64,{ico}">Prouessia</div>"""
    elif nom == 'tel_eteint':   # gros plan : le téléphone de Julien, écran noir
        corps = """<div style="width:430px;height:880px;border-radius:64px;background:#0b0b0d;border:14px solid #2a2b30;box-shadow:0 30px 80px rgba(0,0,0,.8),inset 0 0 0 2px #444;
position:relative;overflow:hidden"><div style="position:absolute;inset:0;background:linear-gradient(125deg,rgba(255,255,255,.10) 0%,rgba(255,255,255,0) 38%)"></div>
<div style="position:absolute;top:22px;left:50%;transform:translateX(-50%);width:120px;height:30px;border-radius:20px;background:#000"></div></div>"""
    else:
        corps = f"""<div class="t">{EP['serie'].upper()}</div><div class="e">Épisode {EP['numero'] + 1}<br><b>demain, 18 h</b></div><div class="s2">Abonnez-vous pour ne pas rater la suite</div>
<div class="f">Histoire et personnages fictifs · avec <b>Prouessia</b>, le partenaire des plombiers</div>"""
    html = f"""<html><head><meta charset="utf-8"><style>{FONTS}*{{margin:0}}body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif;color:#fff;text-align:center;
display:flex;flex-direction:column;align-items:center;justify-content:center;text-shadow:0 4px 20px rgba(0,0,0,.7)}}
.t{{font-weight:900;font-size:110px;letter-spacing:.06em;line-height:1}} .s{{margin-top:60px;font-size:44px;font-weight:600;opacity:.85}}
.m{{margin-top:26px;display:flex;align-items:center;gap:22px;font-weight:900;font-size:84px}} .m img{{width:110px;height:110px;border-radius:26px}}
.p{{margin-top:14px;font-size:44px;font-weight:700;color:{MUST}}} .e{{margin-top:70px;font-size:64px;font-weight:700;line-height:1.2}} .e b{{color:{MUST};font-weight:900}}
.s2{{margin-top:40px;font-size:40px;font-weight:600;opacity:.85}} .f{{position:absolute;bottom:300px;left:80px;right:80px;font-size:30px;opacity:.75}}</style></head><body>{corps}</body></html>"""
    png = os.path.join(EPD, f'carte-{nom}.png')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path=png, omit_background=True); b.close()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', f'{du:.3f}', '-i', fond, '-loop', '1', '-t', f'{du:.3f}', '-i', png, '-filter_complex',
                    f"[0:v]boxblur=28:3,eq=brightness=-0.42:saturation=0.35,scale={int(W*1.12)}:-2,zoompan=z='1+0.0009*on':d=1:s={W}x{H}:fps={FPS}[b];[1:v]format=rgba,fps={FPS}[c];[b][c]overlay=0:0,format=yuv420p[v]",
                    '-map', '[v]', '-t', f'{du:.3f}', '-c:v', 'libx264', '-crf', '18', out], check=True)

def montage(items, total):
    d = os.path.join(EPD, 'parts'); os.makedirs(d, exist_ok=True); parts = []; fr = os.path.join(EPD, 'frames')
    for i, it in enumerate(items):
        du = it['fin'] - it['debut']; out = os.path.join(d, f'{i:02d}.mp4')
        if it.get('carte'):
            n = int(it['debut'] * FPS) - 1
            while not os.path.exists(f'{fr}/{n:05d}.jpg'): n -= 1
            carte(it['carte'], f'{fr}/{n:05d}.jpg', du, out)
        else:
            src = json.load(open(os.path.join(EPD, 'items-rendu.json'))) if '--reutiliser' in sys.argv else None
            n0 = int((src[i]['debut'] if src else it['debut']) * FPS); nb = int(round(du * FPS))
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-start_number', str(n0), '-i', f'{fr}/%05d.jpg', '-frames:v', str(nb),
                            '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out], check=True)
        parts.append(out)
    with open(os.path.join(d, 'liste.txt'), 'w') as fh:
        for p in parts: fh.write(f"file '{p}'\n")
    img = os.path.join(d, 'images.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(d, 'liste.txt'), '-c', 'copy', img], check=True)
    out = os.path.join(EPD, 'film.mp4')
    fin_fond = next((it['debut'] for it in items if it.get('carte') == 'fin'), total)
    fond = EP.get('fond', 'tension'); vol = EP.get('volume_fond', .32)
    af = (f"[2:a]asplit=2[d1][d2];[3:a]atrim=0:{fin_fond:.2f},afade=t=in:d=0.4,afade=t=out:st={fin_fond - .6:.2f}:d=0.6,volume={vol}[f];"
          f"[f][d1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[fd];[d2][fd]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', img, '-i', os.path.join(EPD, 'calques.mov'), '-i', os.path.join(EPD, 'dialogue.wav'), '-i', os.path.join(ICI, 'sons', fond + '.wav'),
                    '-filter_complex', '[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v];' + af, '-map', '[v]', '-map', '[a]',
                    '-t', f'{total:.3f}', '-c:v', 'libx264', '-preset', 'medium', '-profile:v', 'main', '-level', '4.0', '-pix_fmt', 'yuv420p', '-crf', '23', '-maxrate', '1800k', '-bufsize', '3600k', '-g', '30', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], check=True)
    return out

if __name__ == '__main__':
    items, total = preparer()
    for it in items: print(f"{it['debut']:6.2f}-{it['fin']:6.2f} {it.get('qui', it.get('plan', '')):10} {it.get('decor', it.get('carte', ''))}  {it.get('texte', '')}")
    print('total', round(total, 1))
    if '--prep' in sys.argv: sys.exit()
    if '--sans3d' not in sys.argv: rendu3d(items)
    calques(items, total); print(montage(items, total))
