-- Prouessia · ajout de Facebook dans la signature des e-mails (20/10/2026)
-- À coller une fois dans Supabase > SQL Editor > Run. Rien n'est envoyé en lançant ce fichier.

-- e-mail HTML complet pour un prospect (premier envoi ou relance)
create or replace function email_html(p prospects, relance boolean)
returns text language plpgsql stable set search_path = public as $$
declare
  modele text := '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__OBJET__</title></head>
<body style="margin:0;padding:0;background:#ffffff">
<div style="max-width:560px;margin:0 auto;padding:28px 22px;font-family:-apple-system,BlinkMacSystemFont,''Segoe UI'',Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#1A2240">
__CORPS__
<a href="https://www.prouessia.fr/#video" style="display:block;text-decoration:none;max-width:516px"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/apercu-presentation.gif" width="516" alt="Prouessia en vidéo (45 s)" style="display:block;width:100%;max-width:516px;height:auto;border-radius:18px;background:#16181D"></a>
<div style="margin-top:14px"><a href="https://www.prouessia.fr/#video" style="display:inline-block;background:#142445;color:#ffffff;font-weight:600;font-size:14px;text-decoration:none;padding:13px 22px;border-radius:999px;white-space:nowrap;margin:0 8px 8px 0">▶&nbsp; Regarder la vidéo (45 s)</a><a href="https://www.prouessia.fr" style="display:inline-block;background:#3556DB;color:#ffffff;font-weight:600;font-size:14px;text-decoration:none;padding:13px 22px;border-radius:999px;white-space:nowrap;margin:0 8px 8px 0">Découvrir Prouessia</a></div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:28px;background:#F2F3F7;border-radius:18px">
<tr><td style="padding:18px 20px;vertical-align:middle;width:52px"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/icone-prouessia.png" width="46" height="46" alt="Prouessia" style="display:block;border-radius:12px"></td>
<td style="padding:18px 20px 18px 6px;vertical-align:middle;font-family:-apple-system,BlinkMacSystemFont,''Segoe UI'',Roboto,Helvetica,Arial,sans-serif">
<div style="font-size:16px;font-weight:600;color:#1A2240">L’équipe Prouessia<span style="display:none;font-size:0;line-height:0;max-height:0;overflow:hidden;opacity:0">__UNIQUE__</span></div>
<div style="font-size:13px;color:#5D6478;margin-top:2px">Votre métier, en plus simple</div>
<div style="font-size:13px;margin-top:8px;line-height:1.7">
<a href="https://www.prouessia.fr" style="color:#3556DB;text-decoration:none;font-weight:600">prouessia.fr</a>
<span style="color:#C3C7D3">&nbsp;·&nbsp;</span><a href="mailto:contact@prouessia.fr" style="color:#1A2240;text-decoration:none;white-space:nowrap">contact@prouessia.fr</a>
<span style="color:#C3C7D3">&nbsp;·&nbsp;</span><a href="tel:+33605874521" style="color:#1A2240;text-decoration:none;white-space:nowrap">06 05 87 45 21</a></div>
<div style="margin-top:10px"><a href="https://www.facebook.com/profile.php?id=61595467356122" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-facebook.png" width="28" height="28" alt="Facebook" style="display:block"></a><a href="https://www.instagram.com/prouessia" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-instagram.png" width="28" height="28" alt="Instagram" style="display:block"></a><a href="https://www.tiktok.com/@prouessia.fr" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-tiktok.png" width="28" height="28" alt="Tiktok" style="display:block"></a><a href="https://www.youtube.com/@prouessia" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-youtube.png" width="28" height="28" alt="Youtube" style="display:block"></a></div>
</td></tr></table>
<p style="font-size:11px;color:#9AA1AE;line-height:1.5;margin:22px 0 0">Vous recevez ce message car l’adresse __EMAIL__ est publiée sur la fiche de votre entreprise.
<a href="https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?d=stop&p=__ID__" style="color:#9AA1AE">Ne plus recevoir nos messages</a>.<br>Prouessia · SIRET 923 093 637 00018 · 50, avenue des Champs-Élysées, 75008 Paris<span style="display:none;font-size:0;line-height:0;max-height:0;overflow:hidden;opacity:0">__UNIQUE__</span></p>
</div></body></html>';
  corps text;
  suite text;
begin
  if relance then
    corps := '<p style="margin:0 0 14px">Bonjour,</p><p style="margin:0 0 14px">On revient vers vous&nbsp;: en 45 secondes, voyez comment Prouessia relance vos devis sans réponse, pendant que vous êtes sur le chantier.</p><p style="margin:0 0 20px">Pas le bon moment&nbsp;? Un clic en bas, et on arrête.</p>';
  else
    suite := regexp_replace(coalesce(p.message, ''), '^Bonjour,\s*', '');
    corps := '<p style="margin:0 0 14px">' || 'Bonjour,</p>' || '<p style="margin:0 0 20px">' || html_txt(upper(left(suite, 1)) || substr(suite, 2)) || '</p>';
  end if;
  return replace(replace(replace(replace(replace(modele,
    '__CORPS__', corps),
    '__OBJET__', html_txt(p.objet)),
    '__EMAIL__', html_txt(p.email)),
    '__ID__', p.id::text),
    '__UNIQUE__', p.id::text || '-' || to_char(now(), 'YYYYMMDDHH24MISS'));
end $$;

