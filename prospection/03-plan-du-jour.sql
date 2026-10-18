-- Prouessia · plan du jour à valider (Reel + e-mails de prospection)
-- À coller dans Supabase > SQL Editor > Run.
-- Les prospects préparés passent au statut « propose ». Rien ne part tant que la fondatrice
-- n'a pas cliqué « Tout valider » dans l'e-mail du plan.

create or replace function html_txt(t text)
returns text language sql immutable as $$
  select replace(replace(replace(replace(coalesce(t, ''), '&', '&amp;'), '<', '&lt;'), '>', '&gt;'), E'\n', '<br>');
$$;

create or replace function plan_du_jour()
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  wh text := 'https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn';
  nb_r integer; nb_p integer; reels text; pros text; html text;
begin
  update social_posts set status = 'en_attente' where status = 'a_valider';

  select count(*), coalesce(string_agg(
    '<div style="border:2px solid #0B1B3A;border-radius:14px;padding:16px;margin:12px 0">'
    || '<p style="margin:0;font-size:13px;color:#5B6577">Reel · publication le '
    || coalesce(to_char(scheduled_at at time zone 'Europe/Paris', 'DD/MM à HH24"h"MI'), '?') || '</p>'
    || '<h3 style="margin:6px 0">' || html_txt(hook) || '</h3>'
    || '<p style="margin:4px 0"><a href="' || coalesce(video_path, '#') || '" style="color:#1E40AF;font-weight:bold">▶ Voir la vidéo</a>'
    || coalesce(' · <a href="' || sources_pdf_path || '" style="color:#1E40AF">Fiche sources</a>', '') || '</p>'
    || '<p style="font-size:13px;margin:8px 0">' || html_txt(caption) || '</p>'
    || '<p style="font-size:13px;margin:8px 0"><b>Commentaire :</b> ' || html_txt(pinned_comment) || '</p>'
    || '<p style="margin:8px 0"><a href="' || wh || '?id=' || id || '&d=non" style="color:#B42318">Refuser ce Reel</a></p></div>',
    '' order by scheduled_at), '')
  into nb_r, reels
  from social_posts where status = 'en_attente';

  select count(*), coalesce(string_agg(
    '<div style="border-top:1px solid #E5E2DA;padding:12px 0">'
    || '<p style="margin:0;font-size:13px;color:#5B6577">' || html_txt(nom) || ' · ' || html_txt(ville)
    || ' · <a href="' || coalesce(email_source, '#') || '" style="color:#5B6577">source de l''adresse</a></p>'
    || '<p style="margin:4px 0"><b>' || html_txt(objet) || '</b> → ' || html_txt(email) || '</p>'
    || '<p style="margin:4px 0;font-size:13px">' || html_txt(message) || '</p>'
    || '<p style="margin:4px 0"><a href="' || wh || '?d=retire&p=' || id || '" style="color:#B42318;font-size:13px">Retirer ce plombier</a></p></div>',
    '' order by created_at), '')
  into nb_p, pros
  from prospects where statut = 'propose';

  html := '<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#0B1B3A">'
    || '<h2 style="margin:0 0 4px">Le plan du jour</h2>'
    || '<p style="color:#5B6577;margin:0 0 16px">' || nb_r || ' Reel(s) à publier · ' || nb_p || ' e-mail(s) de prospection</p>'
    || '<p style="margin:20px 0"><a href="' || wh || '?d=plan" style="background:#1E40AF;color:#fff;padding:16px 28px;border-radius:12px;text-decoration:none;font-weight:bold;font-size:17px">Tout valider</a></p>'
    || '<p style="font-size:12px;color:#5B6577">Un clic valide le Reel (publié à l''heure prévue) et envoie tout de suite les e-mails (15 maximum par jour, la vidéo et la désinscription sont ajoutées). Retirez d''abord ce que vous ne voulez pas. Sans clic, rien ne part.</p>'
    || reels
    || case when nb_p > 0 then '<h3 style="margin:24px 0 4px">E-mails de prospection</h3>' || pros else '' end
    || '<p style="margin:24px 0"><a href="' || wh || '?d=plan" style="background:#1E40AF;color:#fff;padding:14px 26px;border-radius:12px;text-decoration:none;font-weight:bold">Tout valider</a></p>'
    || '</div>';

  return jsonb_build_object('nb', nb_r + nb_p, 'nb_reels', nb_r, 'nb_prospects', nb_p, 'html', html,
    'sujet', 'Plan du jour : ' || nb_r || ' Reel, ' || nb_p || ' e-mails à valider');
end $$;

create or replace function valider_plan()
returns jsonb language plpgsql security definer set search_path = public as $$
declare r integer; p integer;
begin
  update social_posts set status = 'valide' where status = 'en_attente';
  get diagnostics r = row_count;
  update prospects set statut = 'pret', updated_at = now() where statut = 'propose';
  get diagnostics p = row_count;
  return jsonb_build_object('reels', r, 'prospects', p);
end $$;

grant execute on function html_txt(text), plan_du_jour(), valider_plan() to service_role;
