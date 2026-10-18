"""Fiche sources d'un Reel (PDF 1 page, envoyable à l'audience).
Usage : python3 fiche_sources.py donnees.json sortie.pdf [apercu.png]"""
import sys, json
from commun import *

CSS = BASE_CSS + f"""
.top{{display:flex;justify-content:space-between;align-items:center}}
h1{{font-weight:900;font-size:30px;letter-spacing:-.03em;line-height:1.07;margin-top:9mm}}
.sub{{font-size:12.5px;margin-top:6px;line-height:1.4;color:{GRIS}}}
.it{{display:grid;grid-template-columns:26px 1fr;gap:10px;padding:10px 0;border-bottom:1.5px dashed {LIGNE}}}
.it:last-child{{border-bottom:0}}
.it .n{{width:24px;height:24px;border-radius:7px;background:{INK};color:#fff;font-weight:900;font-size:11.5px;display:flex;align-items:center;justify-content:center}}
.aff{{font-weight:900;font-size:13.5px;line-height:1.28;letter-spacing:-.01em}}
.ref{{font-size:11px;line-height:1.42;margin-top:3px}}
.ref .k{{font-weight:900;color:{BLUE}}}
.lk{{font-size:10.5px;line-height:1.45;margin-top:2px;word-break:break-word}}
.box{{border-radius:13px;padding:10px 14px;font-size:11px;line-height:1.45}}
.foot{{margin-top:auto;padding-top:7px;border-top:2px solid {INK};display:flex;justify-content:space-between;align-items:flex-end;gap:14px;font-size:9.5px;line-height:1.4}}
"""


def build(d):
    items = ''
    for i, a in enumerate(d['affirmations']):
        liens = ''.join(f'<div class="lk">→ <a href="{u}">{t}</a></div>' for t, u in a['liens'])
        items += (f'<div class="it"><div class="n">{i + 1}</div><div><div class="aff">« {a["dit"]} »</div>'
                  f'<div class="ref"><span class="k">{a.get("label","Ce que dit le texte :")}</span> {a["ref"]}</div>{liens}</div></div>')
    pas = ''.join(f'<li style="margin-left:14px">{x}</li>' for x in d['non_couvert'])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body><div class="page">
<div class="top">{LOGO}<span class="tag">Fiche sources · Reel {d['num']}</span></div>
<h1>{d['titre']}</h1>
<div class="sub">Chaque phrase de notre vidéo, avec le texte officiel qui la fonde. Cliquez sur les liens pour lire la source vous-même.</div>
<div class="card" style="padding:4px 16px;margin-top:6mm">{items}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:5mm">
 <div class="box" style="background:#fff;border:2px solid {INK}"><b style="font-weight:900;font-size:12px">Ce que la vidéo ne couvre pas</b><ul style="margin-top:4px">{pas}</ul></div>
 <div class="box" style="background:{MUST}"><b style="font-weight:900;font-size:12px">Information générale</b><div style="margin-top:4px">{d['avert']}</div>
 <div style="margin-top:6px;font-weight:900">Sources vérifiées le {d['date']}.</div></div>
</div>
<div class="foot"><div>Une erreur, un texte qui a changé ? Écrivez-nous en message privé : on corrige et on le dit.</div>
<div style="text-align:right;white-space:nowrap"><div style="font-weight:900;font-size:11.5px">Les règles du plombier, en 30 secondes.</div>@prouessia · prouessia.fr</div></div>
</div></body></html>"""


if __name__ == '__main__':
    d = json.load(open(sys.argv[1], encoding='utf8'))
    print('débordement px :', pdf(build(d), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
