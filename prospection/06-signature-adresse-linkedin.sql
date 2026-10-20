-- Prouessia · signature des e-mails : adresse du siège, LinkedIn et nouveau numéro 07 49 49 17 77 (20/10/2026). Remplace aussi le fichier 05.
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
<span style="color:#C3C7D3">&nbsp;·&nbsp;</span><a href="tel:+33749491777" style="color:#1A2240;text-decoration:none;white-space:nowrap">07 49 49 17 77</a></div>
<div style="font-size:12px;color:#5D6478;margin-top:2px"><a href="https://www.google.com/maps/search/?api=1&amp;query=50+avenue+des+Champs-%C3%89lys%C3%A9es+75008+Paris" style="color:#5D6478;text-decoration:none">50, avenue des Champs-Élysées, 75008 Paris</a></div>
<div style="margin-top:10px"><a href="https://www.facebook.com/profile.php?id=61595467356122" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-facebook.png" width="28" height="28" alt="Facebook" style="display:block"></a><a href="https://www.instagram.com/prouessia" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-instagram.png" width="28" height="28" alt="Instagram" style="display:block"></a><a href="https://www.tiktok.com/@prouessia.fr" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-tiktok.png" width="28" height="28" alt="TikTok" style="display:block"></a><a href="https://www.youtube.com/@prouessia" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-youtube.png" width="28" height="28" alt="YouTube" style="display:block"></a><a href="https://www.linkedin.com/company/prouessia/" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-linkedin.png" width="28" height="28" alt="LinkedIn" style="display:block"></a></div>
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

-- Le lot d'e-mails du jour (format Resend /emails/batch), jours ouvrés, 15 maximum par jour
create or replace function prospects_lot(n integer default 15)
returns jsonb language plpgsql security definer set search_path = public as $$
declare lot jsonb; ids jsonb; deja integer;
  lien text := 'https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?d=stop&p=';
  pied text := E'\n\n—\nL''équipe Prouessia · prouessia.fr · contact@prouessia.fr · 07 49 49 17 77\nNe plus recevoir nos messages : ';
  video text := E'\n\nLa vidéo (45 s) : https://www.prouessia.fr/#video';
begin
  if extract(isodow from now() at time zone 'Europe/Paris') > 5 then
    return jsonb_build_object('nb', 0, 'batch_text', '[]', 'ids_text', '');
  end if;
  select count(*) into deja from prospects
   where (envoye_1_at at time zone 'Europe/Paris')::date = (now() at time zone 'Europe/Paris')::date
      or (envoye_2_at at time zone 'Europe/Paris')::date = (now() at time zone 'Europe/Paris')::date;
  n := greatest(0, n - deja);
  with choix as (
    select * from prospects
    where email is not null and (
      (statut = 'pret' and objet is not null and message is not null)
      or (statut = 'envoye_1' and envoye_1_at < now() - interval '5 days'))
    order by statut desc, created_at
    limit n
  )
  select coalesce(jsonb_agg(jsonb_build_object(
           'from', 'Prouessia <contact@prouessia.fr>',
           'to', jsonb_build_array(c.email),
           'reply_to', 'contact@prouessia.fr',
           'bcc', jsonb_build_array('contact@prouessia.fr'),   -- copie de chaque envoi dans la boîte contact@
           'subject', case when c.statut = 'pret' then c.objet else 'Re : ' || c.objet end,
           'html', email_html(c, c.statut <> 'pret'),
           'text', case when c.statut = 'pret' then c.message
                   else E'Bonjour, on revient vers vous : en 45 secondes, voyez comment Prouessia relance vos devis sans réponse, pendant que vous êtes sur le chantier.\n\nPas le bon moment ? Un clic en bas, et on arrête.' end
                   || video || pied || lien || c.id::text,
           'headers', jsonb_build_object('List-Unsubscribe', '<' || lien || c.id::text || '>')
         )), '[]'::jsonb),
         coalesce(jsonb_agg(c.id), '[]'::jsonb)
    into lot, ids
  from choix c;
  return jsonb_build_object('nb', jsonb_array_length(lot), 'batch_text', lot::text,
                            'ids_text', (select coalesce(string_agg(x, ','), '') from jsonb_array_elements_text(ids) x));
end $$;
