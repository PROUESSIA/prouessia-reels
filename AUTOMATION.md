# Machine à Reels Prouessia : procédure quotidienne

Ce fichier est lu par la tâche programmée de Claude, chaque jour. Il décrit tout ce qu'elle doit faire, sans aide humaine, jusqu'à l'e-mail « À valider ». Rim (fondatrice) ne fait qu'une chose : cliquer **Valider** ou **Refuser** dans l'e-mail.

## Règles qui ne se discutent pas

1. **Faits vérifiés uniquement.** Chaque chiffre, date, délai ou règle dit à la voix ou écrit à l'écran doit venir de `faits/` (fiches `r0*.json`, journaux `*-verification.md`, `supplementaires.json`) et ne pas avoir dépassé `revoir_avant`. Un fait nouveau n'entre que s'il est confirmé sur une source officielle (service-public.gouv.fr, entreprendre.service-public.gouv.fr, economie.gouv.fr, impots.gouv.fr, legifrance si accessible) ouverte avec WebFetch ; on l'ajoute alors à `faits/supplementaires.json` avec l'URL et la date. Pas de source : on change de sujet. Jamais de montant d'amende, jamais « n°1 » ni « le meilleur ».
2. **Fonctions Prouessia citables** : liste des devis sans réponse, relance automatique du devis par e-mail. Rien d'autre (pas de SMS, pas d'appli mobile, pas d'avis clients).
3. **Voix de marque** : « on / nous », vouvoiement des plombiers, jamais le prénom de la fondatrice.
4. **Chaque vidéo a sa fiche sources PDF** (`moteur/fiche_sources.py`). Pas de fiche, pas de Reel.
5. **Rien n'est publié sans le clic Valider.** La procédure s'arrête à l'e-mail.

## Identifiants Make (équipe 3236251, zone eu1)

| Scénario | ID | État normal |
|---|---|---|
| 1 · Ajouter un Reel | 8031966 | éteint |
| 2 · Validation + Publication | 8032025 | **actif** (passe chaque jour à 09:05, heure de Paris) |
| 3 · Réponse Valider / Refuser | 8031972 | **actif** |
| 4 · Relever les stats | 8032365 | éteint |
| 5 · Exporter les stats vers GitHub | 8032370 | éteint |
| 6 · Générer la voix vers GitHub | 8032472 | éteint |
| 7 · Veille et analyse vidéo vers GitHub | 8032962 | éteint |
| Prospection · outils (vers GitHub) | 8038120 | éteint |

**Offre gratuite : 2 scénarios actifs maximum.** Pour lancer un scénario éteint : éteindre 8031972 → allumer le scénario → `scenarios_run` (responsive) → l'éteindre → **rallumer 8031972**. Toujours rallumer 8031972 à la fin, même après une erreur. En cas de « Too Many Requests », attendre 40 s et réessayer une fois.

**Budget : 1 000 crédits par mois.** Une journée normale ≈ 35 crédits avec la prospection ; le lundi ≈ 60 (veille : 3 recherches à 4 crédits + 3 analyses à 2 crédits). Ne pas relancer un scénario « pour voir ». Un seul Reel par jour.

## Mots-clés en commentaire (Instagram, via Zernio, connexion « Prouessia Zernio v2 » 12080150)

Automatisation active sur tout le compte Instagram : un commentaire qui est **exactement** « DEVIS » reçoit en message privé la fiche à imprimer `guides/DEVIS-fiche-a-imprimer.pdf` (et une réponse publique « envoyé en message privé »). Profil Zernio 6ad4b6cfee58f47508be0456, compte Instagram 6ad4e37eebbb709cd6908c42. Pour chaque Reel sur les devis, ajouter à la légende : « 👉 Écrivez DEVIS en commentaire : on vous envoie notre fiche à imprimer en message privé. » Ne jamais promettre un mot-clé qui n'a pas son automatisation (liste : `GET /comment-automations?profileId=…` avec le module Universal de Zernio). Un nouveau guide = une nouvelle automatisation, guide relu et sourcé d'abord.

## Leçons d'une vidéo virale (18/10/2026), à tester une par une

- Promesse + bénéfice dans la 1re seconde, puis 2 ou 3 bénéfices cochés un par un.
- Relance au milieu (vers 12-15 s) : écran plein « La plupart des plombiers s'arrêtent là… » puis la suite.
- Fin par un appel à commenter un mot-clé (voir ci-dessus).
- Tests possibles plus tard : sous-titres mot à mot, mascotte, démo de l'outil à l'écran.

## Procédure

1. `cd` dans le dépôt, `git pull`, `bash setup.sh`.
2. **Stats** : lancer 4 (relever : vues, portée, partages, commentaires sur Instagram et TikTok via Zernio ; vues, likes, commentaires sur YouTube ; et, dès que le jeton Instagram est en place, taux de skip, durée moyenne de visionnage, enregistrements et repartages Instagram) puis, le lundi seulement, 5 (exporter). `git pull`, lire le dernier `stats/*.md`.
3. **Choisir le Reel du jour** dans `faits/accroches-50.json` :
   - priorité aux accroches au statut `V` (fait vérifié), jamais `A` ;
   - ne pas répéter un sujet publié dans `etat.json` ;
   - tourner les styles A → J ; dès que 2 styles ont au moins 5 Reels mesurés, appliquer la règle 70/30 (70 % style gagnant, 30 % test) ; gagnant = **le taux de skip Instagram le plus bas** (puis la durée moyenne de visionnage, puis les vues à 7 jours) quand le jeton Instagram est en place, sinon le plus de vues à 7 jours ;
   - lire aussi les dernières fiches `veille/analyses/` et `analyses/` : reprendre ce qui retient (type d'accroche, rythme des plans, ton de voix), jamais copier un concurrent, jamais reprendre un chiffre vu chez un concurrent sans le vérifier sur une source officielle ;
   - si un sujet a nettement plus de partages que la moyenne, proposer une suite (série) ;
   - **ton de voix** : par défaut le style « promo » (étape 5). Dès que 5 Reels sont mesurés, 1 Reel sur 3 teste une variante de ton (plus rapide, plus posé, plus complice…) en ne changeant QUE la voix, jamais le style d'accroche le même jour, pour savoir ce qui fait la différence.
4. **Script** : 6 à 10 lignes, une phrase par ligne, 25 à 40 s. Ligne 1 = l'accroche, qui commence par « Plombiers ! » quand c'est naturel. Dernière ligne, toujours : « Prouèssia : les règles du plombier, en trente secondes. » Écrire les nombres en lettres pour la voix.
5. **Voix** : lancer 6 avec `text` = le script, `style` = le texte ci-dessous, `path` = `NN/voix.txt` (NN = `prochain_numero_dossier` sur 2 chiffres). `git pull`. Le fichier contient du JSON suivi de `|200` : extraire le champ `"data"` (base64) avec une regex, décoder → WAV 24 kHz. Vérifier la transcription avec `moteur/caler.py` : toutes les phrases présentes, rien de lu en trop. Gemini répète parfois tout le texte deux fois : ne garder que la première prise (couper au silence qui suit la dernière phrase, avant le calage). S'il manque une phrase, relancer une seule fois. Puis **mesurer le ton** : `python3 moteur/analyse_voix.py NN/voix.wav <nombre de mots du script>` et garder le résultat (débit, hauteur, variation de hauteur, dynamique, attaque, pauses) pour `etat.json`.

   Style (ton « promo », validé par la fondatrice le 18/10/2026) : « Style promo énergique : voix d'homme enthousiaste et pleine d'entrain, léger accent du Sud-Ouest, débit vif et rythmé, grand sourire dans la voix. Attaque la première phrase avec punch, comme pour interpeller quelqu'un sur un chantier. Appuie fort sur les chiffres et les mots clés, intonation qui monte franchement sur les questions, courte pause dynamique entre chaque ligne. Reste naturel et complice, jamais criard ni vendeur de télé-achat. Dernière phrase dite avec un grand sourire. »
6. **Vidéo** : copier `moteur/exemple_reel03.py` en `NN/reel.py` et l'adapter (PH, BORNES via `caler.segments` + `caler.transcrire`, scènes). Obligatoire :
   - `debut=0.0` : la voix démarre à la première image ;
   - toute l'accroche est lisible dès l'image 0 (éléments `at < 1` visibles d'emblée) ;
   - du mouvement avant 1,5 s ;
   - pas d'image figée plus de 1,3 s ;
   - fond crème #F7F5EF, logo en haut à gauche, signature en fin ;
   - rien sous 1 500 px (zone de la légende Instagram), pas de sous-titres.

   Vérifier une planche d'images fixes avant le rendu final. Sortie : `NN/video.mp4` (< 50 Mo), `NN/cover.png` (image juste après l'accroche), `NN/sources.pdf`, `NN/verification.md`.
7. `git add NN && git commit && git push`.
8. **Ajouter** : lancer 1 avec `video_file=NN/video.mp4`, `cover_file=NN/cover.png`, `sources_file=NN/sources.pdf`, `scheduled_at` = **demain 09:00** heure de Paris convertie en UTC (07:00Z en heure d'été, 08:00Z en heure d'hiver ; passage à l'heure d'hiver le dernier dimanche d'octobre). Le Reel est préparé la veille : la fondatrice a toute la journée pour valider, et il part le lendemain matin au passage de 09:05, plus topic, hook, caption (légende + « Sources officielles : … » + « Information générale, pas un conseil personnalisé. » + 5 à 7 hashtags) et pinned_comment : **ce texte est publié automatiquement en commentaire** sous le Reel sur YouTube (et sur Instagram dès que la connexion Instagram existe dans Make ; TikTok n'a pas d'API de commentaire, la fondatrice le colle à la main). Une question courte aux plombiers liée au sujet, voix de marque, vouvoiement, 150 caractères max, pas de lien, pas de chiffre non vérifié.
9. Lancer 2 (déjà actif) pour envoyer l'e-mail « À valider » tout de suite.
10. Mettre à jour `etat.json` (n, style, sujet, date, dossier, `ton` = nom du style de voix, `voix_mesures` = sortie de `analyse_voix.py`) et incrémenter `prochain_numero_dossier`. Commit + push.
10 bis. **Commentaires du jour chez les autres** (le compte se fait remarquer en commentant, mais **jamais de commentaire publié automatiquement chez un autre compte** : Instagram, TikTok et YouTube traitent ça comme du spam et brident le compte). Lancer 7 avec `mode=recherche`, `after` = il y a 3 jours, sur « plombier » puis « plomberie ». Choisir 5 Shorts récents de plombiers ou d'artisans francophones (pas de concurrents logiciels, pas de vidéos polémiques). Pour chacun, écrire un commentaire **propre à la vidéo** (on parle de ce qu'on y voit), 1 ou 2 phrases, voix de marque, vouvoiement, utile ou chaleureux, **sans lien, sans pub, sans « allez voir notre compte »**, sans chiffre non vérifié. Écrire `commentaires/AAAA-MM-JJ.md` : pour chaque vidéo, le lien, la chaîne, le commentaire prêt à coller. Ajouter 3 idées de comptes Instagram ou TikTok à aller commenter dans la journée (ceux qui reviennent dans la veille). La fondatrice les colle à la main en 5 minutes ; le lien du fichier est dans l'e-mail « À valider ».
11. **Analyse de nos vidéos** : pour chaque Reel publié il y a 2 jours, lancer 7 avec `mode=analyse`, `video_url` = l'URL YouTube du Short (id YouTube dans `platform_ids`), `path=analyses/NN.json`. On obtient la même grille que pour les concurrents (accroche, plans, voix, musique, moments à risque de skip). À mettre en face du taux de skip réel.
12. **Le lundi, veille concurrents** : lancer 7 avec `mode=recherche`, `after` = il y a 90 jours (ISO, UTC), `path=veille/AAAA-MM-JJ-<mot>.txt`, pour 3 recherches : « plombier », « astuce plomberie », « artisan devis facture ». Le fichier donne, Short par Short (séparés par ` ## `) : id, titre, chaîne, vues, likes, commentaires, durée, date. Choisir les 3 Shorts en français avec le plus de vues par jour depuis leur publication, et lancer 7 en `mode=analyse` sur chacun (`path=veille/analyses/AAAA-MM-JJ-<id>.json`). Le fichier contient la réponse Gemini : le JSON d'analyse est le champ `text`. Seules des vidéos publiques sont analysées (aucune donnée client n'est envoyée à Gemini).
13. **Le lundi, bilan** : écrire `bilans/AAAA-MM-JJ.md` (ce qui a été testé, vues à 7 jours par style d'accroche ET par ton de voix, lien entre les mesures de voix (débit, variation de hauteur, attaque) et les vues, décision de la semaine) et le pousser.

## Prospection automatique (lundi au vendredi, après le Reel)

Table Supabase `prospects` (SQL : `prospection/01-prospects.sql`). Statuts : `nouveau` → `recherche` → `pret` | `sans_email` | `ecarte` → `envoye_1` → `envoye_2` → `repondu` | `client` | `desinscrit`. L'envoi part tout seul à 9 h 05 avec le scénario 2 (15 e-mails maximum par jour ouvré, une seule relance à J+5, puis plus rien). Lien de désinscription dans chaque e-mail (webhook `?d=stop&p=<id>`).

Le scénario « Prospection · outils » (8038120, à lancer en jonglant les créneaux comme les autres) a 4 modes, résultat écrit dans le fichier `path` du dépôt :
- `importer` : `departement`, `page` → 25 entreprises 43.22A actives du registre officiel (recherche-entreprises.api.gouv.fr). Le fichier donne `importes=<n>` et la fin du JSON avec `total_pages`.
- `exporter` : `n` → les prospects à rechercher (JSON), ils passent en `recherche`.
- `maj` : `payload` = tableau JSON `[{id, site_web, email, email_source, objet, message, statut, notes}]` (JSON valide sur une ligne, guillemets échappés).
- `bilan` : nombre de prospects par statut.
- `importer_json` : `payload` = `{"results":[{"siren","nom_complet","etat_administratif":"A","siege":{"libelle_commune","code_postal"},"complements":{"est_entrepreneur_individuel":true|false}}]}` pour ajouter des entreprises trouvées autrement (source B ci-dessous).

Constat du 19/10 : les artisans en nom propre du registre ont rarement un site ou un e-mail public (0 sur 6 au premier test). D'où deux sources :
- **Source A, le registre** : sert surtout la liste « à visiter » (ceux sans site sont la meilleure cible pour un site à leur nom).
- **Source B, le web** : chercher « plombier <ville> » pour les villes du département de la semaine, garder les plombiers qui ont un site avec un e-mail de contact, vérifier leur SIREN dans les mentions légales ou sur annuaire-entreprises.data.gouv.fr (activité 43.22A ou plomberie, entreprise active), puis `importer_json` et `maj`. Jamais d'annuaire payant ni de liste achetée.
- Une entreprise dont l'adresse est « [NON-DIFFUSIBLE] » au registre a demandé à ne pas être diffusée : statut `ecarte`, on ne la contacte pas.

Chaque jour :
1. **Le lundi** : `importer` 2 pages pour le département de la semaine (S1 : 78, S2 : 92, S3 : 91, S4 : 94, puis 75, 95, 93, 77), en reprenant à la page suivante de la dernière fois (noter la page dans `etat.json` → `prospection`).
2. `exporter` avec `n=20`, `path=prospection/a-rechercher/AAAA-MM-JJ.json`, `git pull`.
3. Pour chaque prospect, chercher avec WebSearch/WebFetch : son site officiel et une adresse e-mail **publiée par l'entreprise elle-même** (page contact, mentions légales, fiche officielle). Jamais d'adresse devinée (prenom.nom@…), jamais d'adresse personnelle trouvée ailleurs. `email_source` = l'URL de la page où l'adresse est écrite. Pas d'adresse : statut `sans_email` (liste pour les visites). Grosse entreprise, activité sans rapport avec la plomberie ou fermée : `ecarte`.
4. Pour ceux qui ont une adresse, écrire `objet` (moins de 50 caractères, ex. « Vos devis à <Ville> », pas de majuscules partout, pas de « gratuit », pas de point d'exclamation) et `message` : **30 mots maximum**, texte simple, sur ce modèle :
   « Bonjour[ Monsieur X], on a vu votre entreprise de plomberie à <Ville>. Un devis sans réponse, c'est un client perdu : Prouessia le relance tout seul.

   Ça vous intéresse ? Répondez simplement à ce mail. »
   On peut changer la 2e phrase selon le prospect (pas de site → « on crée aussi votre site à votre nom »), en restant à 30 mots et en ne citant que ce qui existe. Voix de marque (« on »), vouvoiement, jamais le prénom de la fondatrice, pas de prix, pas de pièce jointe. **Ne pas écrire** le lien de la vidéo de démo (26 s), la signature ni la désinscription : ils sont ajoutés automatiquement.
   Puis statut `pret`.
5. `maj` avec tout le lot, `path=prospection/maj/AAAA-MM-JJ.txt`. Vérifier que le fichier dit `maj=200`.
6. Écrire `prospection/a-visiter/AAAA-MM-JJ.md` : les `sans_email` des Yvelines et des Hauts-de-Seine, avec adresse (registre officiel) et site s'il existe, pour les visites et les comptoirs. Pas d'appel à froid sans accord (loi du 30 juin 2025, en vigueur depuis le 11/08/2026, doute pour les pros : on ne prend pas le risque).
7. Écrire `prospection/envoyes/AAAA-MM-JJ.md` : les prospects contactés la veille, avec pour chacun deux liens à cliquer par la fondatrice quand il répond : « A répondu » `https://hook.eu1.make.com/k5jcskqhsbvtd7wz7ijzea3ow1889ufn?d=repondu&p=<id>` et « Client » `…?d=client&p=<id>`.
8. **Le lundi** : `bilan` → ajouter les chiffres (importés, prêts, envoyés, réponses, clients, désinscrits) au bilan de la semaine.

Interdits : messages automatiques sur Instagram, TikTok, Facebook ou LinkedIn à des inconnus, appels ou SMS automatiques, achat de fichiers, plus de 15 e-mails par jour, relancer un `desinscrit` ou un `repondu`.

## En cas de problème

N'importe quelle étape échoue deux fois : on s'arrête, on rallume 8031972 si besoin, et on écrit `problemes/AAAA-MM-JJ.md` avec l'étape, le message d'erreur et ce qui a été tenté. On ne publie jamais un Reel incomplet.
