"""Reel n°1 devis de dépannage — style « funky » (couleurs pleines, formes rondes, animations rebondissantes).
python3 reel4.py   (VOIX=eleven)  ;  STILLS=t1,t2 pour des images fixes"""
import os, sys, shutil, subprocess, json
from playwright.sync_api import sync_playwright
import fiche as F
import voix as V
import reel3 as R

HERE = F.HERE
INK, BLUE, MUST, CREAM = '#0B1B3A', '#1E40AF', '#F2B705', '#FFF4CC'
PAPIER = '#F7F5EF'
FPS = 30

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{font-family:'Inter',sans-serif;color:{INK};background:#F7F5EF;position:relative}}
.a{{position:absolute;opacity:0;white-space:nowrap}}
.bg{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}}
h1{{font-weight:900;letter-spacing:-.035em;line-height:1.02;white-space:normal}}
.hi{{display:inline-block;background:{MUST};color:{INK};padding:0 .18em .04em;border-radius:.22em;}}
.pill{{display:flex;align-items:center;gap:22px;height:84px;padding:0 34px 0 14px;border:4px solid {INK};border-radius:22px;
 background:#fff;box-shadow:0 0 0 {INK};font-weight:800;font-size:44px;letter-spacing:-.02em}}
.pill .o{{width:54px;height:54px;border-radius:12px;border:5px solid {INK};background:#fff;flex:none}}
.pill .o svg{{display:block}}
.chk{{stroke-dasharray:1;stroke-dashoffset:1}}
.logo{{display:flex;align-items:center;gap:14px;padding:0;
 font-weight:900;font-size:34px;letter-spacing:-.01em;}}
.logo i{{width:52px;height:52px;border-radius:14px;background:{BLUE};display:flex;align-items:center;justify-content:center}}
"""

JS = """
(function(){
const cl=x=>Math.max(0,Math.min(1,x)); const ease=x=>1-Math.pow(1-x,3);
const back=x=>{const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const els=[...document.querySelectorAll('.a')], bgs=[...document.querySelectorAll('.bg')],
      chks=[...document.querySelectorAll('.chk')], pills=[...document.querySelectorAll('.pill')];
window.render=function(t){
 for(const b of bgs){const at=+b.dataset.at,out=+b.dataset.out; b.style.opacity=cl((t-at)/.18)*(1-cl((t-out)/.18));}
 for(const e of els){
  const at=+e.dataset.at,out=+e.dataset.out,d=+e.dataset.d,k=e.dataset.k,r=+e.dataset.r||0,w=+e.dataset.w||0,ph=+e.dataset.ph||0;
  const p=cl((t-at)/d), b=back(p), q=cl((t-out)/.18);
  let o=cl(p*4)*(1-q), tr='';
  if(k=='pop') tr=`scale(${.4+.6*b})`;
  if(k=='slap') tr=`scale(${1+(1-b)*.5})`;
  if(k=='slide') tr=`translateX(${(1-b)*-160}px)`;
  if(k=='up') tr=`translateY(${(1-b)*80}px)`;
  if(k=='drift') tr=`translateY(${Math.sin(t*1.4+ph)*18}px) rotate(${r+Math.sin(t*.9+ph)*8}deg)`;
  else tr+=` rotate(${r+(w?Math.sin(t*4+ph)*w:0)}deg)`;
  e.style.opacity=o; e.style.transform=tr;
 }
 for(const c of chks){const at=+c.dataset.at; c.style.strokeDashoffset=1-ease(cl((t-at)/.22));}
 for(const p of pills){const a=+p.dataset.ha,z=+p.dataset.ho; p.style.background=(t>=a&&t<z)?'%s':'#fff';}
};
window.render(0);
})();
""" % MUST


def deco(kind, x, y, s, col, at, out, r=0, ph=0):
    if kind == 'circle':
        inner = f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:{col}"></div>'
    elif kind == 'ring':
        inner = f'<div style="width:{s}px;height:{s}px;border-radius:50%;border:{max(8, s//7)}px solid {col}"></div>'
    elif kind == 'plus':
        inner = (f'<div style="position:relative;width:{s}px;height:{s}px"><i style="position:absolute;left:0;top:{s*.38}px;width:{s}px;height:{s*.24}px;'
                 f'border-radius:{s}px;background:{col}"></i><i style="position:absolute;top:0;left:{s*.38}px;height:{s}px;width:{s*.24}px;border-radius:{s}px;background:{col}"></i></div>')
    elif kind == 'squig':
        inner = (f'<svg width="{s*2}" height="{s*.6}" viewBox="0 0 200 60" fill="none"><path d="M6 40 Q30 -4 55 30 T105 30 T155 30 T196 24" '
                 f'stroke="{col}" stroke-width="14" stroke-linecap="round"/></svg>')
    else:  # star
        inner = (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 4 L61 38 L96 38 L67 59 L78 94 L50 73 L22 94 L33 59 L4 38 L39 38Z" '
                 f'fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></svg>')
    return (f'<div class="a" data-at="{at:.3f}" data-out="{out:.3f}" data-d=".4" data-k="drift" data-r="{r}" data-ph="{ph}" '
            f'style="left:{x}px;top:{y}px">{inner}</div>')


def construire(T):
    out = []
    sfx = []
    S = {'1': (0.0, T['b1'] - .15), '2': (T['b1'] - .1, T['c0'] - .15), '3': (T['c0'] - .1, T['d1'] - .2),
         '4': (T['d1'] - .1, T['e1'] - .2), '5': (T['e1'] - .1, 999)}
    bgc = {'1': PAPIER, '2': PAPIER, '3': PAPIER, '4': PAPIER, '5': PAPIER}
    for k, (a, b) in S.items():
        out.append(f'<div class="bg" data-at="{a:.3f}" data-out="{b:.3f}" style="background:{bgc[k]};{"opacity:1" if k=="1" else ""}"></div>')

    def el(inner, at, out_, kind='pop', style='', d=.45, r=0, w=0, ph=0):
        out.append(f'<div class="a" data-at="{at:.3f}" data-out="{out_:.3f}" data-d="{d}" data-k="{kind}" data-r="{r}" data-w="{w}" data-ph="{ph}" style="{style}">{inner}</div>')

    logo = ('<div class="logo"><i><svg viewBox="0 0 24 24" width="28" height="28"><rect x="4" y="13" width="4" height="7" rx="2" fill="#fff"/>'
            '<rect x="10" y="9" width="4" height="11" rx="2" fill="#fff"/><rect x="16" y="5" width="4" height="15" rx="2" fill="#F2B705"/></svg></i>prouessia</div>')
    el(logo, .1, 999, 'up', 'left:60px;top:250px', .5)

    # ---- 1 : seuil
    a, b = S['1']
    el('<div style="background:#fff;border:5px solid %s;border-radius:20px;padding:12px 30px;font-weight:800;font-size:46px;box-shadow:0 0 0 %s">Un dépannage chez un particulier</div>' % (INK, INK),
       T['a1'] + .05, b, 'pop', 'left:60px;top:420px', .4, r=0)
    el(f'<div style="font-weight:900;font-size:560px;line-height:1;letter-spacing:-.07em;color:{BLUE};">0&nbsp;€</div>',
       T['a1'] + .2, b, 'slap', 'left:30px;top:560px', .45, r=0)
    el(f'<div style="background:{INK};color:#fff;border-radius:16px;padding:18px 40px;font-weight:900;font-size:58px;line-height:1.1;text-align:center;letter-spacing:-.02em">'
       f'Devis écrit<br><span style="color:{MUST}">obligatoire</span></div>', T['a1'] + 1.4, b, 'pop', 'left:300px;top:1180px', .45, r=0)
    el('<div style="font-weight:800;font-size:32px;background:#fff;border-radius:30px;padding:8px 26px;border:4px solid %s">Arrêté du 24 janv. 2017</div>' % INK,
       T['a1'] + 2.1, b, 'up', 'left:60px;top:1420px', .4, r=0)
    sfx += [(T['a1'] + .2, 'thump')]

    # ---- 2 : titre + doc
    a, b = S['2']
    el(f'<h1 style="font-size:150px;width:900px">Votre devis<br>est-il <span class="hi">complet</span>&nbsp;?</h1>', a + .1, b, 'up', 'left:70px;top:420px', .5)
    rows = ''.join(f'<div style="display:flex;align-items:center;gap:20px;margin-top:22px"><div style="width:44px;height:44px;border-radius:50%;border:5px solid {INK};'
                   f'background:{"%s" % BLUE if i < 4 else "#fff"}"></div><div style="height:22px;border-radius:12px;background:{"%s" % MUST if i==4 else "#C9CFDB"};width:{[330,260,380,300,350][i]}px"></div></div>'
                   for i in range(5))
    el(f'<div style="width:620px;background:#fff;border:6px solid {INK};border-radius:24px;padding:44px 48px 52px;box-shadow:0 0 0 {INK}">'
       f'<div style="height:34px;width:250px;border-radius:18px;background:{INK}"></div>{rows}</div>', a + .7, b, 'pop', 'left:230px;top:1000px', .55, r=0)
    sfx += [(a, 'whoosh')]

    # ---- 3 : liste
    a, b = S['3']
    el(f'<h1 style="font-size:150px"><span class="bl">10</span> points</h1>', a + .1, b, 'up', 'left:70px;top:350px', .5, r=0)
    y0, pas = 570, 100
    for i, r in enumerate(R.ROWS):
        t0 = T[f'r{i}']; t1 = T[f'r{i+1}'] if i < 9 else T['r9_end'] + .3
        x = 70
        svg = (f'<svg width="44" height="44" viewBox="0 0 52 52" fill="none" style="margin:2px"><path class="chk" data-at="{t0+.3:.3f}" d="M12 27 l9 10 l19 -23" '
               f'stroke="{BLUE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>')
        el(f'<div class="pill" data-ha="{t0:.3f}" data-ho="{t1:.3f}"><div class="o">{svg}</div>{r}</div>', t0, b, 'slide',
           f'left:{x}px;top:{y0 + i * pas}px', .4, r=0)
        sfx += [(t0 + .3, 'tic')]
    sfx += [(a, 'whoosh')]

    # ---- 4 : à retenir
    a, b = S['4']
    el(f'<div style="background:{MUST};border-radius:14px;padding:10px 30px;font-weight:900;font-size:50px;letter-spacing:.01em">À RETENIR</div>',
       a + .1, b, 'pop', 'left:70px;top:420px', .45, r=0)
    el(f'<h1 style="font-size:150px;width:920px">Relisez votre <span class="hi">modèle</span> une fois.</h1>', a + .3, b, 'up', 'left:70px;top:560px', .55)
    sfx += [(a, 'whoosh')]

    # ---- 5 : mot-clé
    a, b = S['5']
    el(f'<div style="font-weight:900;font-size:76px;letter-spacing:-.03em">Commentez</div>', a + .1, 999, 'up', 'left:70px;top:420px', .4)
    el(f'<div style="position:relative;background:#fff;border:7px solid {INK};border-radius:28px;padding:30px 60px 40px;box-shadow:0 0 0 {INK}">'
       f'<div style="font-weight:900;font-size:250px;letter-spacing:-.05em;line-height:1.05;color:{BLUE}">DEVIS</div>'
       f'<div style="position:absolute;left:90px;bottom:-52px;width:0;height:0;border-left:40px solid transparent;border-right:40px solid transparent;border-top:60px solid {INK}"></div></div>',
       a + .35, 999, 'slap', 'left:70px;top:560px', .5, r=0)
    el(f'<div style="font-weight:900;font-size:68px;line-height:1.08;letter-spacing:-.03em;width:900px;white-space:normal">Les règles du plombier,<br>en <span style="background:{INK};color:{MUST};border-radius:.2em;padding:0 .2em .04em">30 secondes.</span></div>',
       T['e2'], 999, 'up', 'left:70px;top:1130px', .5)
    el(f'<div style="font-weight:800;font-size:40px;background:#fff;border:4px solid {INK};border-radius:40px;padding:10px 30px">@prouessia · prouessia.fr</div>',
       T['e2'] + .5, 999, 'pop', 'left:70px;top:1380px', .4, r=0)
    sfx += [(a, 'whoosh'), (a + .35, 'thump')]
    return ''.join(out), sfx


def main():
    voix, T = R.plan()
    corps, sfx = construire(T)
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{F.FONTS}{CSS}</style></head><body>{corps}<script>{JS}</script></body></html>'
    out = os.path.join(HERE, 'sortie4'); os.makedirs(out, exist_ok=True)
    w = os.path.join(out, '_w'); shutil.rmtree(w, ignore_errors=True); os.makedirs(w + '/f')
    p = os.path.join(w, 'page.html'); open(p, 'w', encoding='utf8').write(html)
    dur = T['_fin']; fps = FPS; n = int(round(dur * fps))
    with sync_playwright() as pw:
        nav = pw.chromium.launch(args=['--no-sandbox'])
        pg = nav.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + p); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        if os.environ.get('STILLS'):
            for s in os.environ['STILLS'].split(','):
                pg.evaluate(f'window.render({float(s)})'); pg.screenshot(path=os.path.join(out, f'still_{float(s):05.1f}.png'))
            nav.close(); print('dur', dur, {k: round(v, 1) for k, v in T.items() if k in ('a1', 'b1', 'c0', 'd1', 'e1', 'e2')}); return
        for k in range(n):
            pg.evaluate(f'window.render({k / fps})')
            pg.screenshot(path=os.path.join(w, 'f', f'f{k:05d}.jpg'), type='jpeg', quality=90)
        nav.close()
    wav = os.path.join(w, 'audio.wav'); V.melange(voix, sfx, dur, wav)
    sortie = os.path.join(out, 'devis-depannage-funky-%s.mp4' % (os.environ.get('VOIX') or 'kokoro'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', w + '/f/f%05d.jpg', '-i', wav,
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
                    '-r', str(fps), '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', sortie], check=True)
    shutil.rmtree(w, ignore_errors=True)
    print(sortie, dur)


if __name__ == '__main__':
    main()
