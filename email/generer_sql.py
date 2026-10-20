"""Génère prospection/04-emails-design.sql à partir des maquettes validées (email/maquettes.py) :
- e-mail au plombier (1er envoi + relance J+5) en HTML, envoyé depuis contact@prouessia.fr
- « Plan du jour » au nouveau design (adresse + Google Maps + vérifications)
Les morceaux variables sont des repères __XXX__ remplacés en SQL par replace()."""
import os, re
import maquettes as M

D = os.path.dirname(os.path.abspath(__file__))
q = lambda s: "'" + s.replace("'", "''") + "'"   # littéral SQL

# ---------- e-mail au plombier ----------
M.UNIQUE = '__UNIQUE__'
mail = M.email_plombier({'objet': '__OBJET__', 'email': '__EMAIL__'})
corps = re.search(r'<p style="margin:0 0 14px">Bonjour,</p>.*?Répondez simplement\.</p>', mail, re.S).group(0)
mail = mail.replace(corps, '__CORPS__').replace('?d=stop&p=ID', '?d=stop&p=__ID__')
mail = re.sub(r'\n\s*', '\n', mail)
P1 = '<p style="margin:0 0 14px">'
P_FIN = '<p style="margin:0 0 20px">'
relance = (P1 + 'Bonjour,</p>' + P1 + 'On revient vers vous&nbsp;: en 45 secondes, voyez comment Prouessia relance vos devis sans réponse, '
           'pendant que vous êtes sur le chantier.</p>' + P_FIN + 'Pas le bon moment&nbsp;? Un clic en bas, et on arrête.</p>')

# ---------- plan du jour ----------
W = M.HOOK
reel = f'''<tr><td style="padding:0 0 14px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{M.LAV_F};border-radius:26px"><tr><td style="padding:22px 24px">
<div style="font-size:15px;font-weight:600;color:{M.LAV_T}">{M.point(M.LAV_T)}Reel · __QUAND__</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px"><tr>
<td style="vertical-align:top;width:104px"><img src="__COVER__" width="88" alt="Couverture" style="display:block;width:88px;border-radius:14px"></td>
<td style="vertical-align:top">
<div style="font-size:16px;font-weight:600;color:{M.TEXTE};line-height:1.4">__HOOK__</div>
<div style="font-size:13px;color:{M.GRIS};margin-top:6px">Instagram · TikTok · YouTube</div>
<div style="margin-top:12px">
<a href="__VIDEO__" style="display:inline-block;background:{M.NUIT};color:#fff;font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">▶ Voir la vidéo</a>
<a href="__SOURCES__" style="display:inline-block;background:#fff;color:{M.TEXTE};font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">Fiche sources</a>
<a href="{W}?id=__ID__&d=non" style="display:inline-block;background:#fff;color:{M.ROUGE};font-size:13px;font-weight:600;text-decoration:none;padding:8px 16px;border-radius:999px;margin:0 6px 6px 0">Refuser</a>
</div></td></tr></table>
</td></tr></table></td></tr>'''

carte = M.carte_prospect('__I__', {'adresse': 'x', 'adresse_registre': 'x', 'dirigeant': '__DIRIGEANT__', 'nom': '__NOM__',
                                     'maps': '__MAPS__', 'email_source': '__SOURCE__', 'email': '__EMAIL__', 'objet': '__OBJET__', 'message': '__MESSAGE__'})
carte = carte.replace(f'{W}?d=retire&p=ID', f'{W}?d=retire&p=__ID__')
carte = carte.replace('<div style="font-size:14px;color:#1A2240;margin-top:12px">x</div>', '<div style="font-size:14px;color:#1A2240;margin-top:12px">__ADRESSE__</div>')
carte = re.sub(r'(<a href="__MAPS__"[^>]*>Voir sur Google Maps →</a></div>)\n\s*\n', r'\1\n__ALERTE__\n', carte)
assert '__ALERTE__' in carte and '__ADRESSE__' in carte
alerte = (f'<div style="font-size:12px;color:{M.CREME_T};background:{M.CREME_F};border-radius:12px;padding:7px 12px;margin-top:8px">'
          'Adresse du siège au registre : __REGISTRE__</div>')

tete = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plan du jour</title></head>
<body style="margin:0;padding:0;background:{M.FOND}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{M.FOND}"><tr><td align="center" style="padding:26px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;font-family:{M.FONT};color:{M.TEXTE}">
<tr><td style="padding:0 4px 22px"><img src="{M.RAW}logo-prouessia.png" width="170" alt="Prouessia · Votre métier, en plus simple" style="display:block;width:170px;height:auto"></td></tr>
<tr><td style="padding:0 4px 18px"><div style="font-size:14px;color:{M.GRIS}">__DATE__</div>
<div style="font-size:30px;font-weight:600;color:{M.TEXTE};letter-spacing:-.01em;margin-top:2px">Le plan du jour</div></td></tr>
<tr><td style="padding:0 0 14px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{M.VERT_F};border-radius:26px"><tr><td style="padding:24px 26px">
<div style="font-size:15px;font-weight:600;color:{M.VERT_T}">{M.point("#3F9A43")}À valider aujourd’hui</div>
<div style="margin-top:12px"><span style="font-size:44px;font-weight:600;color:{M.TEXTE};letter-spacing:-.02em">__NP__</span>
<span style="font-size:15px;color:{M.TEXTE}">&nbsp;e-mails de prospection · __NR__ Reel(s)</span></div>
<div style="font-size:14px;color:{M.GRIS};margin-top:8px;line-height:1.5">Un clic valide tout : le Reel part à l’heure prévue, les e-mails partent aussitôt (15 maximum par jour). Retirez d’abord ce que vous ne voulez pas. Sans clic, rien ne part.</div>
<div style="margin-top:18px">{M.pilule("+&nbsp; Tout valider", W + "?d=plan")}</div>
</td></tr></table></td></tr>'''
titre_pros = f'''<tr><td style="padding:12px 4px 12px">
<div style="font-size:20px;font-weight:600;color:{M.TEXTE}">Plombiers à contacter <span style="display:inline-block;background:{M.ROUGE};color:#fff;font-size:12px;font-weight:700;border-radius:999px;padding:2px 9px;vertical-align:middle">__NP__</span></div>
<div style="font-size:13px;color:{M.GRIS};margin-top:6px;line-height:1.5">Tous vérifiés : entreprise active au registre officiel, aucun site trouvé, adresse e-mail publiée par l’artisan lui-même (le badge ouvre la page).</div>
</td></tr>
<tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0">__CARTES__</table></td></tr>'''
pied = f'''<tr><td style="padding:14px 0 6px;text-align:center">{M.pilule("+&nbsp; Tout valider", W + "?d=plan")}</td></tr>
<tr><td style="padding:16px 0;text-align:center;font-size:12px;color:{M.GRIS}">Prouessia · rien ne part sans votre clic</td></tr>
</table></td></tr></table></body></html>'''
nl = lambda s: re.sub(r'\n\s*', '\n', s)

sql = f"""-- Prouessia · e-mails au nouveau design (validé le 20/10/2026)
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
  modele text := {q(mail)};
  corps text;
  suite text;
begin
  if relance then
    corps := {q(relance)};
  else
    suite := regexp_replace(coalesce(p.message, ''), '^Bonjour,\\s*', '');
    corps := {q(P1)} || 'Bonjour,</p>' || {q(P_FIN)} || html_txt(upper(left(suite, 1)) || substr(suite, 2)) || '</p>';
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
  lien text := '{W}?d=stop&p=';
  pied text := E'\\n\\n—\\nL''équipe Prouessia · prouessia.fr · contact@prouessia.fr · 07 49 49 17 77\\nNe plus recevoir nos messages : ';
  video text := E'\\n\\nLa vidéo (45 s) : https://www.prouessia.fr/#video';
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
                   else E'Bonjour, on revient vers vous : en 45 secondes, voyez comment Prouessia relance vos devis sans réponse, pendant que vous êtes sur le chantier.\\n\\nPas le bon moment ? Un clic en bas, et on arrête.' end
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
  m_reel text := {q(nl(reel))};
  m_carte text := {q(nl(carte))};
  m_alerte text := {q(alerte)};
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

  html := replace(replace(replace({q(nl(tete))},
            '__DATE__', initcap(jours[extract(isodow from t)::int]) || ' ' || extract(day from t)::int || ' ' || mois[extract(month from t)::int]),
            '__NP__', nb_p::text), '__NR__', nb_r::text)
       || reels
       || case when nb_p > 0 then replace(replace({q(nl(titre_pros))}, '__NP__', nb_p::text), '__CARTES__', cartes) else '' end
       || {q(nl(pied))};

  return jsonb_build_object('nb', nb_r + nb_p, 'nb_reels', nb_r, 'nb_prospects', nb_p, 'html', html,
    'sujet', 'Plan du jour : ' || nb_r || ' Reel, ' || nb_p || ' e-mails à valider');
end $$;

grant execute on function email_html(prospects, boolean), prospects_lot(integer), plan_du_jour() to service_role;
"""
out = os.path.join(D, '..', 'prospection', '04-emails-design.sql')
open(out, 'w').write(sql)
print(out, len(sql))
