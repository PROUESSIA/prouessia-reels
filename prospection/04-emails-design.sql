-- Prouessia · e-mails au nouveau design (validé le 20/10/2026)
-- À coller une seule fois dans Supabase > SQL Editor > Run. Rien n'est envoyé en lançant ce fichier.
-- 1) adresse + lien Google Maps des plombiers  2) e-mail HTML au plombier depuis contact@prouessia.fr
-- 3) « Plan du jour » au nouveau design. Fichier généré par email/generer_sql.py.

alter table prospects add column if not exists adresse text;
alter table prospects add column if not exists adresse_registre text;   -- rempli seulement si différente de l'adresse publiée
alter table prospects add column if not exists maps text;

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
<div style="margin-top:10px"><a href="https://www.instagram.com/prouessia" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-instagram.png" width="28" height="28" alt="Instagram" style="display:block"></a><a href="https://www.tiktok.com/@prouessia.fr" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-tiktok.png" width="28" height="28" alt="Tiktok" style="display:block"></a><a href="https://www.youtube.com/@prouessia" style="display:inline-block;margin-right:8px;text-decoration:none"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/reseau-youtube.png" width="28" height="28" alt="Youtube" style="display:block"></a></div>
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
  pied text := E'\n\n—\nL''équipe Prouessia · prouessia.fr · contact@prouessia.fr · 06 05 87 45 21\nNe plus recevoir nos messages : ';
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

-- « Plan du jour » au nouveau design
create or replace function plan_du_jour()
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  jours text[] := array['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'];
  mois text[] := array['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];
  t timestamp := now() at time zone 'Europe/Paris';
  m_reel text := '<tr><td style="padding:0 0 14px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#E3E8FA;border-radius:26px"><tr><td style="padding:22px 24px">
<div style="font-size:15px;font-weight:600;color:#3556DB"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#3556DB;margin-right:8px;vertical-align:middle"></span>Reel · __QUAND__</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px"><tr>
<td style="vertical-align:top;width:104px"><img src="__COVER__" width="88" alt="Couverture" style="display:block;width:88px;border-radius:14px"></td>
<td style="vertical-align:top">
<div style="font-size:16px;font-weight:600;color:#1A2240;line-height:1.4">__HOOK__</div>
<div style="font-size:13px;color:#5D6478;margin-top:6px">Instagram · TikTok · YouTube</div>
<div style="margin-top:12px">
<a href="__VIDEO__" style="display:inline-block;background:#142445;color:#fff;font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">▶ Voir la vidéo</a>
<a href="__SOURCES__" style="display:inline-block;background:#fff;color:#1A2240;font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">Fiche sources</a>
<a href="https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?id=__ID__&d=non" style="display:inline-block;background:#fff;color:#D93B3B;font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">Refuser</a>
</div></td></tr></table>
</td></tr></table></td></tr>';
  m_carte text := '
<tr><td style="padding:0 0 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:22px">
<tr><td style="padding:20px 22px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="vertical-align:top;width:46px"><div style="width:36px;height:36px;border-radius:50%;background:#E3E8FA;color:#3556DB;font-weight:600;font-size:14px;line-height:36px;text-align:center">__I__</div></td>
<td style="vertical-align:top">
<div style="font-size:16px;font-weight:600;color:#1A2240">__NOM__</div>
<div style="font-size:13px;color:#5D6478;margin-top:1px">__DIRIGEANT__</div>
</td>
<td style="vertical-align:top;text-align:right;width:90px"><a href="https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?d=retire&p=__ID__" style="display:inline-block;font-size:13px;color:#D93B3B;text-decoration:none;font-weight:600;border:1px solid #F3C9C9;border-radius:999px;padding:5px 12px">Retirer</a></td>
</tr></table>
<div style="font-size:14px;color:#1A2240;margin-top:12px">__ADRESSE__</div>
<div style="margin-top:6px"><a href="__MAPS__" style="font-size:13px;color:#3556DB;font-weight:600;text-decoration:none">Voir sur Google Maps →</a></div>
__ALERTE__
<div style="margin-top:12px"><span style="display:inline-block;font-size:12px;font-weight:600;color:#2E6B2F;background:#E6F2DE;border-radius:999px;padding:4px 11px;margin:0 6px 6px 0">✓ Entreprise active</span><span style="display:inline-block;font-size:12px;font-weight:600;color:#2E6B2F;background:#E6F2DE;border-radius:999px;padding:4px 11px;margin:0 6px 6px 0">✓ Aucun site trouvé</span><a href="__SOURCE__" style="text-decoration:none"><span style="display:inline-block;font-size:12px;font-weight:600;color:#2E6B2F;background:#E6F2DE;border-radius:999px;padding:4px 11px;margin:0 6px 6px 0">✓ Adresse publiée par l’artisan</span></a></div>
<div style="background:#F2F3F7;border-radius:16px;padding:14px 16px;margin-top:6px">
<div style="font-size:12px;color:#5D6478">À <b style="color:#1A2240;font-weight:600">__EMAIL__</b> · Objet <b style="color:#1A2240;font-weight:600">__OBJET__</b></div>
<div style="font-size:14px;line-height:1.55;color:#1A2240;margin-top:6px">__MESSAGE__</div>
</div>
</td></tr></table></td></tr>';
  m_alerte text := '<div style="font-size:12px;color:#8A6200;background:#FBF1D3;border-radius:12px;padding:7px 12px;margin-top:8px">Adresse du siège au registre : __REGISTRE__</div>';
  nb_r integer; nb_p integer; reels text; cartes text; html text; quand timestamp;
begin
  update social_posts set status = 'en_attente' where status = 'a_valider';

  select count(*), coalesce(string_agg(
    replace(replace(replace(replace(replace(replace(m_reel,
      '__QUAND__', coalesce(jours[extract(isodow from scheduled_at at time zone 'Europe/Paris')::int] || ' '
                   || to_char(scheduled_at at time zone 'Europe/Paris', 'DD/MM "à" HH24" h "MI'), 'date à définir')),
      '__COVER__', coalesce(cover_path, '')),
      '__HOOK__', html_txt(hook)),
      '__VIDEO__', coalesce(video_path, '#')),
      '__SOURCES__', coalesce(sources_pdf_path, '#')),
      '__ID__', id::text),
    '' order by scheduled_at), '')
  into nb_r, reels
  from social_posts where status = 'en_attente';

  select count(*), coalesce(string_agg(
    replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(m_carte,
      '__I__', rn::text),
      '__NOM__', html_txt(nom)),
      '__DIRIGEANT__', html_txt(coalesce(split_part(dirigeant, ' (', 1), ''))),
      '__ADRESSE__', html_txt(coalesce(adresse, ville))),
      '__MAPS__', coalesce(maps, 'https://www.google.com/maps/search/?api=1&query=' || replace(coalesce(nom, '') || ' ' || coalesce(ville, ''), ' ', '+'))),
      '__ALERTE__', case when adresse_registre is not null then replace(m_alerte, '__REGISTRE__', html_txt(adresse_registre)) else '' end),
      '__SOURCE__', coalesce(email_source, '#')),
      '__EMAIL__', html_txt(email)),
      '__OBJET__', html_txt(objet)),
      '__MESSAGE__', html_txt(message)),
      '__ID__', id::text),
    '' order by rn), '')
  into nb_p, cartes
  from (select *, row_number() over (order by created_at) rn from prospects where statut = 'propose') p;

  html := replace(replace(replace('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plan du jour</title></head>
<body style="margin:0;padding:0;background:#F2F3F7">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F2F3F7"><tr><td align="center" style="padding:26px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;font-family:-apple-system,BlinkMacSystemFont,''Segoe UI'',Roboto,Helvetica,Arial,sans-serif;color:#1A2240">
<tr><td style="padding:0 4px 22px"><img src="https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/email/logo-prouessia.png" width="170" alt="Prouessia · Votre métier, en plus simple" style="display:block;width:170px;height:auto"></td></tr>
<tr><td style="padding:0 4px 18px"><div style="font-size:14px;color:#5D6478">__DATE__</div>
<div style="font-size:30px;font-weight:600;color:#1A2240;letter-spacing:-.01em;margin-top:2px">Le plan du jour</div></td></tr>
<tr><td style="padding:0 0 14px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#E6F2DE;border-radius:26px"><tr><td style="padding:24px 26px">
<div style="font-size:15px;font-weight:600;color:#2E6B2F"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#3F9A43;margin-right:8px;vertical-align:middle"></span>À valider aujourd’hui</div>
<div style="margin-top:12px"><span style="font-size:44px;font-weight:600;color:#1A2240;letter-spacing:-.02em">__NP__</span>
<span style="font-size:15px;color:#1A2240">&nbsp;e-mails de prospection · __NR__ Reel(s)</span></div>
<div style="font-size:14px;color:#5D6478;margin-top:8px;line-height:1.5">Un clic valide tout : le Reel part à l’heure prévue, les e-mails partent aussitôt (15 maximum par jour). Retirez d’abord ce que vous ne voulez pas. Sans clic, rien ne part.</div>
<div style="margin-top:18px"><a href="https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?d=plan" style="display:inline-block;background:#3556DB;color:#ffffff;font-weight:600;font-size:15px;text-decoration:none;padding:13px 22px;border-radius:999px;white-space:nowrap;margin:0 8px 8px 0">+&nbsp; Tout valider</a></div>
</td></tr></table></td></tr>',
            '__DATE__', initcap(jours[extract(isodow from t)::int]) || ' ' || extract(day from t)::int || ' ' || mois[extract(month from t)::int]),
            '__NP__', nb_p::text), '__NR__', nb_r::text)
       || reels
       || case when nb_p > 0 then replace(replace('<tr><td style="padding:12px 4px 12px">
<div style="font-size:20px;font-weight:600;color:#1A2240">Plombiers à contacter <span style="display:inline-block;background:#D93B3B;color:#fff;font-size:12px;font-weight:700;border-radius:999px;padding:2px 9px;vertical-align:middle">__NP__</span></div>
<div style="font-size:13px;color:#5D6478;margin-top:6px;line-height:1.5">Tous vérifiés : entreprise active au registre officiel, aucun site trouvé, adresse e-mail publiée par l’artisan lui-même (le badge ouvre la page).</div>
</td></tr>
<tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0">__CARTES__</table></td></tr>', '__NP__', nb_p::text), '__CARTES__', cartes) else '' end
       || '<tr><td style="padding:14px 0 6px;text-align:center"><a href="https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?d=plan" style="display:inline-block;background:#3556DB;color:#ffffff;font-weight:600;font-size:15px;text-decoration:none;padding:13px 22px;border-radius:999px;white-space:nowrap;margin:0 8px 8px 0">+&nbsp; Tout valider</a></td></tr>
<tr><td style="padding:16px 0;text-align:center;font-size:12px;color:#5D6478">Prouessia · rien ne part sans votre clic</td></tr>
</table></td></tr></table></body></html>';

  return jsonb_build_object('nb', nb_r + nb_p, 'nb_reels', nb_r, 'nb_prospects', nb_p, 'html', html,
    'sujet', 'Plan du jour : ' || nb_r || ' Reel, ' || nb_p || ' e-mails à valider');
end $$;

grant execute on function email_html(prospects, boolean), prospects_lot(integer), plan_du_jour() to service_role;
