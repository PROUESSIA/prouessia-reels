-- Prouessia · e-mails courts + vidéo. À coller dans Supabase > SQL Editor > Run (remplace la fonction prospects_lot).

-- Le lot d'e-mails du jour, au format de l'API Resend /emails/batch (jours ouvrés uniquement)
create or replace function prospects_lot(n integer default 15)
returns jsonb language plpgsql security definer set search_path = public as $$
declare lot jsonb; ids jsonb; deja integer;
  video text := E'\n\nLa vidéo (26 s) : https://qibubxxhvhghktlpvrls.supabase.co/storage/v1/object/public/reels/demo/prouessia-relance.mp4';
  pied text := E'\n\n—\nL''équipe Prouessia · www.prouessia.fr\nNe plus recevoir nos messages : ';
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
           'text', case when statut = 'pret' then message || video
                   else E'Bonjour, on revient vers vous : 26 secondes pour voir comment Prouessia relance vos devis sans réponse.'
                        || video || E'\n\nPas le bon moment ? Un clic en bas, et on arrête.' end
                   || pied || lien || id::text,
           'headers', jsonb_build_object('List-Unsubscribe', '<' || lien || id::text || '>')
         )), '[]'::jsonb),
         coalesce(jsonb_agg(id), '[]'::jsonb)
    into lot, ids
  from choix;
  return jsonb_build_object('nb', jsonb_array_length(lot), 'batch_text', lot::text,
                            'ids_text', (select coalesce(string_agg(x, ','), '') from jsonb_array_elements_text(ids) x));
end $$;
