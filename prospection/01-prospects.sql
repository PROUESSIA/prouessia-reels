-- Prouessia · prospection automatique
-- À coller une seule fois dans Supabase > SQL Editor > Run.

create table if not exists prospects (
  id uuid primary key default gen_random_uuid(),
  siren text unique,
  nom text,
  dirigeant text,
  ville text,
  code_postal text,
  departement text,
  date_creation date,
  est_ei boolean,
  effectif text,
  site_web text,
  email text,
  email_source text,          -- page publique où l'adresse a été trouvée
  statut text not null default 'nouveau',
  -- nouveau → pret → envoye_1 → envoye_2 → (repondu | client | desinscrit | ecarte)
  objet text,
  message text,
  envoye_1_at timestamptz,
  envoye_2_at timestamptz,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table prospects enable row level security;
grant select, insert, update, delete on prospects to service_role;

-- Import d'une page de l'API officielle recherche-entreprises.api.gouv.fr
create or replace function import_prospects(payload jsonb)
returns integer language plpgsql security definer set search_path = public as $$
declare n integer;
begin
  insert into prospects (siren, nom, dirigeant, ville, code_postal, departement, date_creation, est_ei, effectif)
  select r->>'siren',
         r->>'nom_complet',
         case when r->'dirigeants'->0->>'type_dirigeant' = 'personne physique'
              then initcap(coalesce(r->'dirigeants'->0->>'prenoms','')) || ' ' || initcap(coalesce(r->'dirigeants'->0->>'nom','')) end,
         coalesce(r->'matching_etablissements'->0->>'libelle_commune', r->'siege'->>'libelle_commune'),
         coalesce(r->'matching_etablissements'->0->>'code_postal', r->'siege'->>'code_postal'),
         left(coalesce(r->'matching_etablissements'->0->>'code_postal', r->'siege'->>'code_postal'), 2),
         nullif(r->>'date_creation','')::date,
         (r->'complements'->>'est_entrepreneur_individuel')::boolean,
         r->>'tranche_effectif_salarie'
  from jsonb_array_elements(payload->'results') r
  where r->>'etat_administratif' = 'A'
  on conflict (siren) do nothing;
  get diagnostics n = row_count;
  return n;
end $$;

-- Le lot d'e-mails du jour, au format de l'API Resend /emails/batch (jours ouvrés uniquement)
create or replace function prospects_lot(n integer default 15)
returns jsonb language plpgsql security definer set search_path = public as $$
declare lot jsonb; ids jsonb; deja integer;
  pied text := E'\n\n—\nL''équipe Prouessia · https://www.prouessia.fr\nVous ne souhaitez plus recevoir nos messages ? Un clic suffit : ';
  lien text := 'https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?d=stop&p=';
begin
  if extract(isodow from now() at time zone 'Europe/Paris') > 5 then
    return jsonb_build_object('nb', 0, 'batch_text', '[]', 'ids_text', '');
  end if;
  -- plafond par jour, même si le scénario tourne plusieurs fois
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
           'from', 'Prouessia <bonjour@prouessia.fr>',
           'to', jsonb_build_array(email),
           'reply_to', 'prouessia.contact@gmail.com',
           'subject', case when statut = 'pret' then objet else 'Re : ' || objet end,
           'text', case when statut = 'pret' then message
                   else E'Bonjour,\n\nJe me permets de revenir vers vous au sujet de mon message de la semaine dernière. '
                        || E'Si vous perdez parfois des devis restés sans réponse, on peut vous montrer en 10 minutes comment Prouessia les relance tout seul.\n\n'
                        || E'Si ce n''est pas le bon moment, aucun souci : un clic en bas de ce message et on ne vous écrit plus.' end
                   || pied || lien || id::text,
           'headers', jsonb_build_object('List-Unsubscribe', '<' || lien || id::text || '>')
         )), '[]'::jsonb),
         coalesce(jsonb_agg(id), '[]'::jsonb)
    into lot, ids
  from choix;
  return jsonb_build_object('nb', jsonb_array_length(lot), 'batch_text', lot::text,
                            'ids_text', (select coalesce(string_agg(x, ','), '') from jsonb_array_elements_text(ids) x));
end $$;

-- Marque le lot comme envoyé (appelé juste après l'envoi Resend)
create or replace function prospects_marquer(ids_text text)
returns integer language plpgsql security definer set search_path = public as $$
declare n integer;
begin
  update prospects set
    statut = case when statut = 'pret' then 'envoye_1' else 'envoye_2' end,
    envoye_1_at = case when statut = 'pret' then now() else envoye_1_at end,
    envoye_2_at = case when statut = 'envoye_1' then now() else envoye_2_at end,
    updated_at = now()
  where id::text = any (string_to_array(ids_text, ','));
  get diagnostics n = row_count;
  return n;
end $$;

grant execute on function import_prospects(jsonb), prospects_lot(integer), prospects_marquer(text) to service_role;

-- Les prospects à enrichir (recherche du site et de l'e-mail publics), les plus récents d'abord
create or replace function prospects_a_enrichir(n integer default 20)
returns text language plpgsql security definer set search_path = public as $$
declare res text;
begin
  with choix as (
    select id from prospects where statut = 'nouveau'
    order by est_ei desc nulls last, date_creation desc nulls last limit n
  ), maj as (
    update prospects p set statut = 'recherche', updated_at = now()
    from choix where p.id = choix.id
    returning p.id, p.nom, p.dirigeant, p.ville, p.code_postal, p.date_creation, p.est_ei, p.siren
  )
  select coalesce(jsonb_agg(to_jsonb(maj)), '[]'::jsonb)::text into res from maj;
  return res;
end $$;

-- Mise à jour en lot après recherche : [{id, site_web, email, email_source, objet, message, statut, notes}]
create or replace function prospects_maj(payload jsonb)
returns integer language plpgsql security definer set search_path = public as $$
declare n integer;
begin
  update prospects p set
    site_web = coalesce(e->>'site_web', p.site_web),
    email = coalesce(lower(e->>'email'), p.email),
    email_source = coalesce(e->>'email_source', p.email_source),
    objet = coalesce(e->>'objet', p.objet),
    message = coalesce(e->>'message', p.message),
    statut = coalesce(e->>'statut', p.statut),
    notes = coalesce(e->>'notes', p.notes),
    updated_at = now()
  from jsonb_array_elements(payload) e
  where p.id = (e->>'id')::uuid and p.statut not in ('desinscrit', 'client');
  get diagnostics n = row_count;
  return n;
end $$;

-- Bilan par statut (pour le tableau de bord du lundi)
create or replace function prospects_bilan()
returns text language sql security definer set search_path = public as $$
  select coalesce(jsonb_object_agg(statut, nb), '{}'::jsonb)::text
  from (select statut, count(*) nb from prospects group by statut) s;
$$;

grant execute on function prospects_a_enrichir(integer), prospects_maj(jsonb), prospects_bilan() to service_role;
