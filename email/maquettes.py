"""Maquettes HTML des deux e-mails (à ouvrir dans le navigateur) :
- email/maquette-email-plombier.html : l'e-mail que reçoit le plombier, avec la signature Prouessia
- email/maquette-plan-du-jour.html   : le « Plan du jour » que reçoit la fondatrice
Code compatible messageries (tableaux + styles en ligne, polices système), le même HTML sera repris dans le SQL."""
import json, html, os

D = os.path.dirname(os.path.abspath(__file__))
RAW = 'https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/'
VIDEO = 'https://qibubxxhvhghktlpvrls.supabase.co/storage/v1/object/public/reels/demo/prouessia-relance.mp4'
HOOK = 'https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn'
INK, BLUE, MUST, PAPIER, GRIS, LIGNE, VERT = '#0B1B3A', '#1E40AF', '#F2B705', '#F7F5EF', '#5B6577', '#E5E2DA', '#1F7A4D'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
TEL = '[votre numéro]'      # à remplacer après réponse
SIREN = '[votre SIREN]'     # à remplacer après réponse
e = html.escape


def signature():
    return f'''
<table role="presentation" cellpadding="0" cellspacing="0" style="margin-top:28px;border-top:1px solid {LIGNE};padding-top:18px;width:100%">
 <tr><td style="padding-top:18px;vertical-align:top;width:56px"><img src="{RAW}icone-prouessia.png" width="44" height="44" alt="Prouessia" style="display:block;border-radius:11px"></td>
  <td style="padding-top:18px;padding-left:12px;vertical-align:top;font-family:{FONT}">
   <div style="font-size:15px;font-weight:700;color:{INK}">L’équipe Prouessia</div>
   <div style="font-size:13px;color:{GRIS};margin-top:2px">Le site et les devis des plombiers indépendants</div>
   <div style="font-size:13px;margin-top:8px;line-height:1.6">
    <a href="https://www.prouessia.fr" style="color:{BLUE};text-decoration:none;font-weight:600">prouessia.fr</a>
    <span style="color:{LIGNE}">&nbsp;|&nbsp;</span><a href="mailto:prouessia.contact@gmail.com" style="color:{INK};text-decoration:none">prouessia.contact@gmail.com</a>
    <span style="color:{LIGNE}">&nbsp;|&nbsp;</span><span style="color:{INK}">{TEL}</span></div>
   <div style="width:44px;height:3px;background:{MUST};margin-top:10px;border-radius:2px"></div>
  </td></tr></table>'''


def email_plombier(p):
    corps = (f'<p style="margin:0 0 14px">Bonjour,</p>'
             f'<p style="margin:0 0 14px">On a vu votre entreprise de plomberie à {e(p["ville"])}. On crée votre site à votre nom, '
             f'et les demandes de clients arrivent sur votre téléphone.</p>'
             f'<p style="margin:0 0 18px">Intéressé&nbsp;? Répondez simplement à ce message.</p>')
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(p["objet"])}</title></head>
<body style="margin:0;padding:0;background:#ffffff">
<div style="max-width:560px;margin:0 auto;padding:28px 22px;font-family:{FONT};font-size:15px;line-height:1.6;color:{INK}">
{corps}
<a href="{VIDEO}" style="display:block;text-decoration:none"><img src="{RAW}vignette-video.png" width="516" alt="▶ Voir la vidéo (26 s)" style="display:block;width:100%;max-width:516px;height:auto;border-radius:12px;border:1px solid {LIGNE}"></a>
<div style="font-size:13px;color:{GRIS};margin-top:8px">▶ <a href="{VIDEO}" style="color:{BLUE};font-weight:600;text-decoration:none">Voir la vidéo (26 s)</a></div>
{signature()}
<p style="font-size:11px;color:#9AA1AE;line-height:1.5;margin:26px 0 0">Vous recevez ce message car l’adresse {e(p["email"])} est publiée sur la fiche de votre entreprise.
<a href="{HOOK}?d=stop&p=ID" style="color:#9AA1AE">Ne plus recevoir nos messages</a>.<br>Prouessia · Vélizy-Villacoublay (78) · SIREN {SIREN}</p>
</div></body></html>'''


def badge(txt, ok=True):
    c, fond = (VERT, '#E8F5EE') if ok else ('#9A5B00', '#FFF4D6')
    return (f'<span style="display:inline-block;font-size:12px;font-weight:600;color:{c};background:{fond};border-radius:20px;'
            f'padding:3px 10px;margin:0 6px 6px 0">{"✓" if ok else "!"} {txt}</span>')


def carte_prospect(i, p):
    import re
    def cle(a):
        cp = re.findall(r'\b\d{5}\b', a); num = re.match(r'\s*(\d+)', a.split('Lavacourt')[-1].strip())
        return (cp[-1] if cp else None, num.group(1) if num else None)
    (c1, n1), (c2, n2) = cle(p['adresse']), cle(p['adresse_registre'])
    diff = c1 != c2 or (n1 and n2 and n1 != n2)
    alerte = (f'<div style="font-size:12px;color:#9A5B00;margin-top:4px">Siège au registre : {e(p["adresse_registre"])}</div>' if diff else '')
    dirigeant = f' · {e(p["dirigeant"].split(" (")[0])}' if p.get('dirigeant') else ''
    return f'''
<tr><td style="padding:18px 0;border-top:1px solid {LIGNE}">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
  <td style="vertical-align:top;width:30px;font-size:13px;font-weight:700;color:{GRIS};padding-top:2px">{i}</td>
  <td style="vertical-align:top">
   <div style="font-size:16px;font-weight:700;color:{INK}">{e(p["nom"])}<span style="font-weight:400;color:{GRIS};font-size:14px">{dirigeant}</span></div>
   <div style="font-size:14px;color:{INK};margin-top:4px">{e(p["adresse"])}&nbsp;&nbsp;<a href="{e(p["maps"])}" style="color:{BLUE};font-weight:600;text-decoration:none;white-space:nowrap">Voir sur Google Maps →</a></div>
   {alerte}
   <div style="margin-top:10px">{badge("Entreprise active (registre)")}{badge("Aucun site trouvé")}<a href="{e(p["email_source"])}" style="text-decoration:none">{badge("Adresse publiée par l’artisan")}</a></div>
   <div style="font-size:13px;color:{GRIS};margin-top:4px">À : <b style="color:{INK};font-weight:600">{e(p["email"])}</b> · Objet : <b style="color:{INK};font-weight:600">{e(p["objet"])}</b></div>
   <div style="font-size:14px;line-height:1.55;color:{INK};background:{PAPIER};border-radius:10px;padding:12px 14px;margin-top:8px">{e(p["message"])}</div>
  </td>
  <td style="vertical-align:top;text-align:right;width:80px;padding-left:10px"><a href="{HOOK}?d=retire&p=ID" style="font-size:13px;color:#B42318;text-decoration:none;font-weight:600">Retirer</a></td>
 </tr></table></td></tr>'''


def bouton(txt):
    return (f'<a href="{HOOK}?d=plan" style="display:inline-block;background:{INK};color:#ffffff;font-weight:700;font-size:16px;'
            f'text-decoration:none;padding:15px 30px;border-radius:10px;border-bottom:4px solid {MUST}">{txt}</a>')


def plan(prospects):
    reel = f'''
<tr><td style="padding:22px 26px;background:#ffffff">
 <div style="font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:{GRIS}">Reel du jour · publication mardi 20/10 à 9 h 05</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:12px"><tr>
  <td style="vertical-align:top;width:110px"><a href="#"><img src="{RAW.replace('email/', '10/')}cover.png" width="96" alt="Couverture" style="display:block;width:96px;border-radius:10px;border:1px solid {LIGNE}"></a></td>
  <td style="vertical-align:top">
   <div style="font-size:17px;font-weight:700;color:{INK};line-height:1.35">Plombiers ! Vrai ou faux : sans date sur le devis, vous avez tout votre temps.</div>
   <div style="font-size:14px;color:{GRIS};margin-top:6px">Instagram · TikTok · YouTube</div>
   <div style="margin-top:10px;font-size:14px"><a href="#" style="color:{BLUE};font-weight:600;text-decoration:none">▶ Voir la vidéo</a>
    <span style="color:{LIGNE}">&nbsp;|&nbsp;</span><a href="#" style="color:{BLUE};font-weight:600;text-decoration:none">Fiche sources</a>
    <span style="color:{LIGNE}">&nbsp;|&nbsp;</span><a href="#" style="color:#B42318;font-weight:600;text-decoration:none">Refuser ce Reel</a></div>
  </td></tr></table></td></tr>'''
    cartes = ''.join(carte_prospect(i + 1, p) for i, p in enumerate(prospects))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plan du jour</title></head>
<body style="margin:0;padding:0;background:{PAPIER}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPIER}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;font-family:{FONT};color:{INK}">
 <tr><td style="background:#ffffff;padding:22px 26px;border-radius:14px 14px 0 0;border-bottom:4px solid {MUST}">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
   <td><img src="{RAW}logo-prouessia.png" width="150" alt="Prouessia" style="display:block"></td>
   <td style="text-align:right;font-size:13px;color:{GRIS}">Plan du jour<br><b style="color:{INK};font-size:15px">Mardi 20 octobre</b></td></tr></table></td></tr>
 <tr><td style="background:{INK};padding:24px 26px;color:#ffffff">
  <div style="font-size:22px;font-weight:700">1 Reel et {len(prospects)} e-mails à valider</div>
  <div style="font-size:14px;color:#C9D1E3;margin-top:6px;line-height:1.5">Un clic valide tout : le Reel part à l’heure prévue et les e-mails partent aussitôt (15 maximum par jour). Retirez d’abord ce que vous ne voulez pas. Sans clic, rien ne part.</div>
  <div style="margin-top:18px"><a href="{HOOK}?d=plan" style="display:inline-block;background:{MUST};color:{INK};font-weight:700;font-size:16px;text-decoration:none;padding:14px 28px;border-radius:10px">Tout valider</a></div>
 </td></tr>
 {reel}
 <tr><td style="padding:22px 26px 6px;background:#ffffff;border-top:8px solid {PAPIER}">
  <div style="font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:{GRIS}">E-mails de prospection · plombiers sans site</div>
  <div style="font-size:13px;color:{GRIS};margin-top:6px;line-height:1.5">Chaque plombier est vérifié : entreprise active au registre officiel, aucun site trouvé, adresse e-mail publiée par l’artisan lui-même (cliquez sur le badge pour voir la page).
   <a href="email-plombier" style="color:{BLUE};text-decoration:none;font-weight:600">Aperçu de l’e-mail reçu →</a></div>
 </td></tr>
 <tr><td style="padding:0 26px 10px;background:#ffffff"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">{cartes}</table></td></tr>
 <tr><td style="background:#ffffff;padding:20px 26px 26px;text-align:center;border-radius:0 0 14px 14px;border-top:1px solid {LIGNE}">{bouton("Tout valider")}</td></tr>
 <tr><td style="padding:16px 26px;text-align:center;font-size:12px;color:{GRIS}">Prouessia · machine à Reels et prospection · rien ne part sans votre clic</td></tr>
</table></td></tr></table></body></html>'''


if __name__ == '__main__':
    pros = json.load(open(os.path.join(D, '..', 'prospection', 'annuaires', '2026-10-19-guide-artisan-sans-site.json')))
    propose = [p for p in pros if p['statut'] == 'propose']
    open(os.path.join(D, 'maquette-email-plombier.html'), 'w').write(email_plombier(propose[0]))
    open(os.path.join(D, 'maquette-plan-du-jour.html'), 'w').write(plan(propose).replace('href="email-plombier"', 'href="maquette-email-plombier.html"'))
    print('ok', len(propose))
