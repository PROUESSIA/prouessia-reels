"""Maquettes HTML des deux e-mails (à ouvrir dans le navigateur), au style du back-office Prouessia :
fond gris-bleu clair, grandes cartes arrondies, cartes pastel (vert, lavande, crème), pilules bleu vif et bleu nuit.
- email/maquette-email-plombier.html : l'e-mail que reçoit le plombier, avec la signature Prouessia
- email/maquette-plan-du-jour.html   : le « Plan du jour » que reçoit la fondatrice
Code compatible messageries (tableaux + styles en ligne, polices système) ; le même HTML sera repris dans le SQL."""
import json, html, os, re

D = os.path.dirname(os.path.abspath(__file__))
RAW = 'https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/'
VIDEO = 'https://www.prouessia.fr/video'  # page vidéo du site (fichier : email/page-video.html)
HOOK = 'https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn'
# couleurs du back-office
NUIT, BLEU, FOND, TEXTE, GRIS, LIGNE = '#142445', '#3556DB', '#F2F3F7', '#1A2240', '#5D6478', '#E6E8EF'
VERT_F, VERT_T = '#E6F2DE', '#2E6B2F'
LAV_F, LAV_T = '#E3E8FA', '#3556DB'
CREME_F, CREME_T = '#FBF1D3', '#8A6200'
ROUGE = '#D93B3B'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
TEL = '06 05 87 45 21'
MAIL = 'contact@prouessia.fr'
LEGAL = 'Prouessia · SIRET 923 093 637 00018 · 50, avenue des Champs-Élysées, 75008 Paris'
e = html.escape


def point(c):
    return f'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{c};margin-right:8px;vertical-align:middle"></span>'


def pilule(txt, href, fond=BLEU, couleur='#ffffff', taille=15):
    return (f'<a href="{href}" style="display:inline-block;background:{fond};color:{couleur};font-weight:600;font-size:{taille}px;'
            f'text-decoration:none;padding:13px 26px;border-radius:999px">{txt}</a>')


def signature():
    return f'''
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:28px;background:{FOND};border-radius:18px">
 <tr><td style="padding:18px 20px;vertical-align:middle;width:52px"><img src="{RAW}icone-prouessia.png" width="46" height="46" alt="Prouessia" style="display:block;border-radius:12px"></td>
  <td style="padding:18px 20px 18px 6px;vertical-align:middle;font-family:{FONT}">
   <div style="font-size:16px;font-weight:600;color:{TEXTE}">L’équipe Prouessia</div>
   <div style="font-size:13px;color:{GRIS};margin-top:2px">Votre métier, en plus simple</div>
   <div style="font-size:13px;margin-top:8px;line-height:1.7">
    <a href="https://www.prouessia.fr" style="color:{BLEU};text-decoration:none;font-weight:600">prouessia.fr</a>
    <span style="color:#C3C7D3">&nbsp;·&nbsp;</span><a href="mailto:{MAIL}" style="color:{TEXTE};text-decoration:none">{MAIL}</a>
    <span style="color:#C3C7D3">&nbsp;·&nbsp;</span><a href="tel:+33605874521" style="color:{TEXTE};text-decoration:none">{TEL}</a></div>
  </td></tr></table>'''


def email_plombier(p):
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(p["objet"])}</title></head>
<body style="margin:0;padding:0;background:#ffffff">
<div style="max-width:560px;margin:0 auto;padding:28px 22px;font-family:{FONT};font-size:15px;line-height:1.6;color:{TEXTE}">
<p style="margin:0 0 14px">Bonjour,</p>
<p style="margin:0 0 14px">Combien de vos devis dorment sans réponse&nbsp;? Souvent, c’est un client qui signe ailleurs.</p>
<p style="margin:0 0 14px">Prouessia relance vos clients automatiquement, pendant que vous êtes sur le chantier.</p>
<p style="margin:0 0 20px">Intéressé&nbsp;? Répondez simplement.</p>
<a href="{VIDEO}" style="display:block;text-decoration:none;max-width:360px"><img src="{RAW}apercu-video.gif" width="360" height="360" alt="Prouessia relance vos devis sans réponse (vidéo de 26 s)" style="display:block;width:100%;max-width:360px;height:auto;border-radius:18px;background:#EEEDE8"></a>
<div style="margin-top:14px">{pilule("▶&nbsp; Regarder avec le son (26 s)", VIDEO, taille=14)}</div>
{signature()}
<p style="font-size:11px;color:#9AA1AE;line-height:1.5;margin:22px 0 0">Vous recevez ce message car l’adresse {e(p["email"])} est publiée sur la fiche de votre entreprise.
<a href="{HOOK}?d=stop&p=ID" style="color:#9AA1AE">Ne plus recevoir nos messages</a>.<br>{LEGAL}</p>
</div></body></html>'''


def chip(txt, href=None):
    c = (f'<span style="display:inline-block;font-size:12px;font-weight:600;color:{VERT_T};background:{VERT_F};border-radius:999px;'
         f'padding:4px 11px;margin:0 6px 6px 0">✓ {txt}</span>')
    return f'<a href="{e(href)}" style="text-decoration:none">{c}</a>' if href else c


def cle(a):
    cp = re.findall(r'\b\d{5}\b', a)
    num = re.match(r'\s*(\d+)', a.split('Lavacourt')[-1].strip())
    return (cp[-1] if cp else None, num.group(1) if num else None)


def carte_prospect(i, p):
    (c1, n1), (c2, n2) = cle(p['adresse']), cle(p['adresse_registre'])
    alerte = ''
    if c1 != c2 or (n1 and n2 and n1 != n2):
        alerte = (f'<div style="font-size:12px;color:{CREME_T};background:{CREME_F};border-radius:12px;padding:7px 12px;margin-top:8px">'
                  f'Adresse du siège au registre : {e(p["adresse_registre"])}</div>')
    dirigeant = e(p['dirigeant'].split(' (')[0]) if p.get('dirigeant') else ''
    return f'''
<tr><td style="padding:0 0 12px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:22px">
  <tr><td style="padding:20px 22px">
   <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
    <td style="vertical-align:top;width:46px"><div style="width:36px;height:36px;border-radius:50%;background:{LAV_F};color:{LAV_T};font-weight:600;font-size:14px;line-height:36px;text-align:center">{i}</div></td>
    <td style="vertical-align:top">
     <div style="font-size:16px;font-weight:600;color:{TEXTE}">{e(p["nom"])}</div>
     <div style="font-size:13px;color:{GRIS};margin-top:1px">{dirigeant}</div>
    </td>
    <td style="vertical-align:top;text-align:right;width:90px"><a href="{HOOK}?d=retire&p=ID" style="display:inline-block;font-size:13px;color:{ROUGE};text-decoration:none;font-weight:600;border:1px solid #F3C9C9;border-radius:999px;padding:5px 12px">Retirer</a></td>
   </tr></table>
   <div style="font-size:14px;color:{TEXTE};margin-top:12px">{e(p["adresse"])}</div>
   <div style="margin-top:6px"><a href="{e(p["maps"])}" style="font-size:13px;color:{BLEU};font-weight:600;text-decoration:none">Voir sur Google Maps →</a></div>
   {alerte}
   <div style="margin-top:12px">{chip("Entreprise active")}{chip("Aucun site trouvé")}{chip("Adresse publiée par l’artisan", p["email_source"])}</div>
   <div style="background:{FOND};border-radius:16px;padding:14px 16px;margin-top:6px">
    <div style="font-size:12px;color:{GRIS}">À <b style="color:{TEXTE};font-weight:600">{e(p["email"])}</b> · Objet <b style="color:{TEXTE};font-weight:600">{e(p["objet"])}</b></div>
    <div style="font-size:14px;line-height:1.55;color:{TEXTE};margin-top:6px">{e(p["message"])}</div>
   </div>
  </td></tr></table></td></tr>'''


def plan(prospects):
    n = len(prospects)
    cartes = ''.join(carte_prospect(i + 1, p) for i, p in enumerate(prospects))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plan du jour</title></head>
<body style="margin:0;padding:0;background:{FOND}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{FOND}"><tr><td align="center" style="padding:26px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;font-family:{FONT};color:{TEXTE}">

 <tr><td style="padding:0 4px 22px">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
   <td style="vertical-align:middle"><img src="{RAW}logo-prouessia.png" width="170" alt="Prouessia · Votre métier, en plus simple" style="display:block;width:170px;height:auto"></td>
  </tr></table></td></tr>

 <tr><td style="padding:0 4px 18px">
  <div style="font-size:14px;color:{GRIS}">Mardi 20 octobre</div>
  <div style="font-size:30px;font-weight:600;color:{TEXTE};letter-spacing:-.01em;margin-top:2px">Le plan du jour</div>
 </td></tr>

 <tr><td style="padding:0 0 14px">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{VERT_F};border-radius:26px"><tr><td style="padding:24px 26px">
   <div style="font-size:15px;font-weight:600;color:{VERT_T}">{point("#3F9A43")}À valider aujourd’hui</div>
   <div style="margin-top:12px"><span style="font-size:44px;font-weight:600;color:{TEXTE};letter-spacing:-.02em">{n}</span>
    <span style="font-size:15px;color:{TEXTE}">&nbsp;e-mails de prospection · 1 Reel</span></div>
   <div style="font-size:14px;color:{GRIS};margin-top:8px;line-height:1.5">Un clic valide tout : le Reel part à l’heure prévue, les e-mails partent aussitôt (15 maximum par jour). Retirez d’abord ce que vous ne voulez pas. Sans clic, rien ne part.</div>
   <div style="margin-top:18px">{pilule("+&nbsp; Tout valider", HOOK + "?d=plan")}</div>
  </td></tr></table></td></tr>

 <tr><td style="padding:0 0 26px">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{LAV_F};border-radius:26px"><tr><td style="padding:22px 24px">
   <div style="font-size:15px;font-weight:600;color:{LAV_T}">{point(LAV_T)}Reel du jour · mardi 20/10 à 9 h 05</div>
   <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px"><tr>
    <td style="vertical-align:top;width:104px"><img src="{RAW.replace('email/', '10/')}cover.png" width="88" alt="Couverture" style="display:block;width:88px;border-radius:14px"></td>
    <td style="vertical-align:top">
     <div style="font-size:16px;font-weight:600;color:{TEXTE};line-height:1.4">Plombiers ! Vrai ou faux : sans date sur le devis, vous avez tout votre temps.</div>
     <div style="font-size:13px;color:{GRIS};margin-top:6px">Instagram · TikTok · YouTube</div>
     <div style="margin-top:12px">
      <a href="#" style="display:inline-block;background:{NUIT};color:#fff;font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">▶ Voir la vidéo</a>
      <a href="#" style="display:inline-block;background:#fff;color:{TEXTE};font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">Fiche sources</a>
      <a href="#" style="display:inline-block;background:#fff;color:{ROUGE};font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">Refuser</a>
     </div></td></tr></table>
  </td></tr></table></td></tr>

 <tr><td style="padding:0 4px 12px">
  <div style="font-size:20px;font-weight:600;color:{TEXTE}">Plombiers à contacter <span style="display:inline-block;background:{ROUGE};color:#fff;font-size:12px;font-weight:700;border-radius:999px;padding:2px 9px;vertical-align:middle">{n}</span></div>
  <div style="font-size:13px;color:{GRIS};margin-top:6px;line-height:1.5">Tous sans site et vérifiés : entreprise active au registre officiel, aucun site trouvé, adresse e-mail publiée par l’artisan lui-même (le badge ouvre la page).
   <a href="email-plombier" style="color:{BLEU};text-decoration:none;font-weight:600">Aperçu de l’e-mail reçu →</a></div>
 </td></tr>
 <tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0">{cartes}</table></td></tr>

 <tr><td style="padding:14px 0 6px;text-align:center">{pilule("+&nbsp; Tout valider", HOOK + "?d=plan")}</td></tr>
 <tr><td style="padding:16px 0;text-align:center;font-size:12px;color:{GRIS}">Prouessia · rien ne part sans votre clic</td></tr>
</table></td></tr></table></body></html>'''


if __name__ == '__main__':
    pros = json.load(open(os.path.join(D, '..', 'prospection', 'annuaires', '2026-10-19-guide-artisan-sans-site.json')))
    propose = [p for p in pros if p['statut'] == 'propose']
    open(os.path.join(D, 'maquette-email-plombier.html'), 'w').write(email_plombier(propose[0]))
    open(os.path.join(D, 'maquette-plan-du-jour.html'), 'w').write(plan(propose).replace('href="email-plombier"', 'href="maquette-email-plombier.html"'))
    print('ok', len(propose))
