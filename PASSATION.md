# Passation de la communication Prouessia — dossier de relais

Rédigé le 30/10/2026 par l'équipe qui a monté la machine, pour l'équipe Claude Code qui en prend la responsabilité. Lire ce fichier en entier avant toute action, puis `AUTOMATION.md` (procédure détaillée, règles non négociables) qui reste la référence technique.

---

## 1. Le client

- **Prouessia** (prouessia.fr) : logiciel en ligne pour **plombiers indépendants en France**. Site vitrine fait pour le plombier, devis sur téléphone, signature au doigt, relances automatiques, fiches clients. **39 € par mois**, sans engagement, sans carte bancaire.
- **La fondatrice** gère tout seule : produit, technique, marketing, ventes. Elle parle français (et arabe), veut des échanges **directs, courts, sans allers-retours**, et des livraisons **complètes en une fois**. Si une info manque : la demander **une seule fois**, tout ensemble.
- **Voix publique : la marque** (« on / nous »), **jamais son prénom**, vouvoiement des plombiers.
- **Ce qu'elle fait elle-même** : cliquer « Tout valider » dans le Plan du jour ; coller les commentaires préparés ; répondre aux commentaires « DEVIS » / « SITE » hors Instagram.
- **Ce qu'elle ne veut jamais** : qu'on publie sans son clic ; qu'on commente ou écrive automatiquement chez d'autres comptes ; des appels/SMS automatiques ; acheter des listes ou deviner des e-mails ; voir une clé ou un mot de passe dans un message ou un fichier (elle les colle elle-même) ; de la musique dans les vidéos ; des faits non sourcés.

## 2. La mission

1. **Faire connaître Prouessia aux plombiers** avec 5 vidéos par jour (YouTube Shorts, TikTok, Instagram et Facebook, tout automatique depuis le 31/10).
2. **Créer des contacts** : appel « Écrivez DEVIS en commentaire » sur chaque Reel ; offre flash « maquette de site gratuite » tous les 10 jours.
3. **Prospecter** : jusqu'à 15 e-mails par jour à des plombiers sans site, vérifiés au registre officiel, envoyés seulement après validation.
4. **Fidéliser l'audience** avec la série animée « Sous pression » (un épisode par jour à 18 h, suspense, cliffhanger).
5. **Mesurer et ajuster** : stats, analyse des vidéos, bilan hebdomadaire.

## 3. Le planning d'une journée (heure de Paris)

| Heure | Qui | Quoi |
|---|---|---|
| 09:05 | Make, hub 8032025 (planifié) | Publie les vidéos validées du jour (TikTok + YouTube, chacune à son heure) **et** envoie les e-mails de prospection validés + relances J+5 |
| 09:10 | Claude Code, tâche « Machine à Reels Prouessia » | Fabrique les 5 vidéos du **lendemain**, prépare la prospection, envoie le **Plan du jour** (à valider) et l'e-mail **« 💬 Vos 20 min réseaux »** |
| dans la journée | La fondatrice | Clique « Tout valider » (c'est tout : Instagram et Facebook sont automatiques depuis le 31/10) |
| toutes les 30 min, 09:15-20:45 | Make, scénario 8273226 « publier (sans e-mails) » | Publie les vidéos validées tardivement (après 09:05) : tout de suite si l'heure est passée, sinon programmées à leur heure. Ne touche jamais aux e-mails |
| 09:45, 12:45, 18:45 | Claude Code, tâche « Contrôle des publications » | Vérifie que chaque vidéo prévue est bien partie ; relance si possible ; sinon e-mail court à la fondatrice |
| 20:45 | même tâche | Contrôle + **bilan du soir** par e-mail |

Les 5 créneaux vidéo : **9 h** vécu · **12 h 30** POV (ou offre flash) · **18 h** épisode de la série · **20 h 30** carte (règle officielle) · **22 h** style 5 « motion ».

**Règle « seulement le lendemain »** : on n'ajoute jamais au plan une vidéo ou un e-mail pour plus loin que le lendemain (préparer à l'avance des fichiers est permis).

## 4. Les formats

- **Vécu (9 h)** : idée suivante des 100 idées (`idees/100-idees.json`, champ `fait`), titre fixe = l'accroche, 10 à 16 phrases courtes lues mot pour mot (voix Gemini « Charon »), un plan différent par phrase, captures de l'appli nettes, question de débat, fin « Prouessia, le partenaire des plombiers ». Modèles : `16/`, `19/`, `22/`.
- **POV (12 h 30)** : « POV : … » en titre, scène à la 1re personne qui tourne mal (chute drôle), puis l'avantage. Modèles : `17/`, `20/`, `23/`.
- **Carte (20 h 30)** : carte d'appel client en ouverture, une règle officielle tirée de `faits/` avec sa source, puis un avantage. Gabarit `"gabarit": "carte"`. Modèles : `18/`, `21/`, `24/`.
- **Style 5 « motion » (22 h)**, validé le 30/10 : animation dessinée (grands mots qui rebondissent, fonds marine/jaune, vrais écrans de l'appli en carrousel, question, fin + DEVIS animé), aucun clip. `motion/faire.py`, modèle `m5test/motion.json`, publié pour la 1re fois : `28/` le 30/10 à 22 h.
- **Motion sur vécu, POV et carte** (30/10) : même style qu'avant, mais textes, surlignages, carte d'appel et appel DEVIS entrent en mouvement (automatique dans `moteur/vecu.py`). Pas dans la série.
- **Phrase de fin, sur tous les Reels sauf la série** (dans **son propre plan**, prouessia.fr en bas, depuis le 30/10) : « Vous voulez en savoir plus ? Écrivez « DEVIS » en commentaire. » (automatique dans `moteur/vecu.py`, voix commune `voix/cta-devis.wav`), et dans la légende : « 👉 Écrivez DEVIS en commentaire : on vous envoie notre fiche à imprimer en message privé. » Sur Instagram, « DEVIS » déclenche l'envoi automatique de la fiche (Zernio).
- **Offre flash, tous les 10 jours** (31/10, 10/11, 20/11, 30/11…) à 12 h 30 : « la maquette de votre site, gratuite, pour les 10 premiers commentaires « SITE » ». Modèle `25/` (`"cta": false`). La fondatrice répond elle-même.
- **Série « Sous pression » (18 h)** : bible `anim/BIBLE-sous-pression.md` (arc de 10 épisodes, personnages, logique de l'arnaque). Personnages sans yeux ni bouche, aucun texte d'explication à l'écran, carte sponsor muette de 1,8 s au milieu, histoire **logique et cohérente** avec les épisodes précédents, cliffhanger, pas de phrase DEVIS. Moteur `anim/film.py` + `anim/film.html`.

### Contrôles obligatoires avant d'ajouter une vidéo (vidéos refusées le 28/10)
1. **Captures de l'appli nettes, écran entier, jamais zoomées** : uniquement `"clip": "img:<nom>"` (images de `videos/app/` ou `videos/app/extras/`), jamais `app:`. Ouvrir une image de chaque plan d'appli en pleine taille.
2. **Aucune phrase muette ni coupée** : le calage doit afficher « phrases non reconnues : 0 » ; `vecu.py video` s'arrête si une phrase n'a pas de voix.
3. **Plans en rapport avec le sujet** (plomberie, chantier, téléphone, papiers) : pas de cuisine, d'animaux, de fond vert, d'animation.
4. Mouvement dès la 1re image, < 8 Mo, H.264 Main, 15 à 25 s, pas de musique.

## 5. Les outils (où est quoi)

- **Dépôt GitHub `PROUESSIA/prouessia-reels`** : tout le travail (scripts, vidéos, journaux). Toujours `git pull --rebase` avant de pousser ; ne jamais `git stash`/`pull` pendant un rendu.
- **Make** (organisation 9332564, équipe 3236251, offre Core 10 000 crédits/mois, remise à zéro le 27 du mois) :
  - **Hub 8032025** : lancé avec `scenarios_run` + `data.mode` (ajouter, voix, plan, lire, ecrire, pages, pixabay, test_mail, stats, veille, analyse…) ; sans mode = passage de 09:05. Liste des modes : `AUTOMATION.md`. Construit par `make/build_hub.py` (le bleu envoyé doit être complet).
  - **8273226 « publier (sans e-mails) »** : publication seule, toutes les 30 min de 09:15 à 20:45. Peut être lancé à la main avec `scenarios_run` sans données.
  - **8274397 « Instagram + Facebook (auto) »** (30/10) : toutes les 10 min dans 5 fenêtres après les créneaux ; Instagram (Reel + Story, Zernio) programmé à l'heure, Page Facebook publiée à l'heure. Détails : AUTOMATION.md.
  - **8031972** : liens de l'e-mail (Valider / Refuser / Tout valider / désinscription). Toujours actif.
  - Les tâches Claude Code ne modifient, n'activent ni ne désactivent aucun scénario ; seule une session de travail avec la fondatrice le fait.
- **Supabase** : tables `social_posts` (statuts `a_valider` → `en_attente` → `valide` → `en_publication` → `publie` ; `refuse`) et `prospects` (`propose` → `pret` → `envoye_1` → `envoye_2` → `repondu` / `client` / `desinscrit` ; réserve `a_proposer`, `plus_tard`, `ecarte`). Lecture/écriture par les modes `lire` / `ecrire` du hub.
- **Publication** : TikTok via Zernio ; YouTube direct (Shorts, commentaire épinglé automatique) ; Instagram (Zernio) + Page Facebook (module Reels Facebook) **automatiques** via le scénario 8274397 (décision du 30/10, remplace la publication à la main du 23/10).
- **Voix** : Gemini TTS via le hub (mode `voix`). **Quota : 10 prises par jour, 3 par minute**, remis à zéro vers 9 h. Une prise par personnage pour la série. Calage mot à mot : action GitHub « Transcrire une voix » (`voix/transcrire/`).
- **Clips libres de droits** : mode `pixabay` (requêtes en anglais) puis `videos/a_telecharger.txt` → action GitHub « Télécharger des clips ». Clips utilisés : `videos/clips/utilises.json` (interdits dans les 10 dernières vidéos).
- **E-mails** : Resend, depuis contact@prouessia.fr / reels@prouessia.fr, vers prouessia.contact@gmail.com. Les tests (`test_mail`) ne vont qu'aux deux boîtes de la fondatrice.

## 6. Calendrier en cours

| Date | 9 h | 12 h 30 | 18 h | 20 h 30 | 22 h |
|---|---|---|---|---|---|
| ven. 30/10 | 22 vécu (publié) | 23 POV (TikTok seul) | ép. 3 « Le piège » v2 | 24 carte TVA (TikTok seul) | 28 motion « La relance » |
| sam. 31/10 | 26 vécu idée 5 | **25 offre flash** | ép. 4 « Le contrat » | 27 carte devis payant | — (le style 5 commence le 1/11) |
| dim. 1/11 | 29 vécu idée 7 | 30 POV idée 9 | ép. 5 « La serrure » | 31 carte dépannage (idée 10) | 32 motion « Votre site, on le crée » (idée 11) |
| lun. 2/11 | 33 vécu idée 12 (logo) | 34 POV idée 13 (site sérieux) | ép. 6 « L'aimant » (rendu le 1/11) | 35 carte médiateur de la conso (idée 14) | 36 motion « Vos communes, affichées » (idée 15) |
| mar. 3/11 | 37 vécu idée 16 (services classés) | 38 POV idée 17 (formulaire) | ép. 7 « Chez maman » (écrit et rendu le 2/11) | 39 carte décennale (idée 18) | 40 motion « site rapide » (idée 19) |
| mer. 4/11 | 41 vécu idée 20 (adresse web) | 42 POV idée 22 (plus d'impression) | ép. 8 « La liste » (écrit et rendu le 3/11, décor entrepôt) | 43 carte devis accepté (r04, idée 23) | 44 motion « prévenu dès la signature » (idée 24) |
| jeu. 5/11 | **rien de fabriqué le 4/11** (3e jour sans validation, stock de 10 vidéos 37-44 + ép. 7-8 en attente) : idée 25 | POV (26) | ép. 9 seulement après la sortie des ép. 7 et 8 | carte (idée 27) | style 5 (idée 28) |
| ven. 6/11 | **rien de fabriqué le 5/11** (4e jour sans validation, même stock 37-44 + ép. 7-8) : idée 25 | POV (26) | ép. 9 après ép. 7 et 8 | carte (idée 27) | style 5 (idée 28) |
| sam. 7/11 | **rien de fabriqué le 6/11** (5e jour sans validation, même stock 37-44 + ép. 7-8) : idée 25 | POV (26) | ép. 9 après ép. 7 et 8 | carte (idée 27) | style 5 (idée 28) |
| dim. 8/11 | **rien de fabriqué le 7/11** (6e jour sans validation, même stock 37-44 + ép. 7-8) : idée 25 | POV (26) | ép. 9 après ép. 7 et 8 | carte (idée 27) | style 5 (idée 28) |
| lun. 9/11 | **rien de fabriqué le 8/11** (7e jour sans validation, même stock 37-44 + ép. 7-8) : idée 25 | POV (26) | ép. 9 après ép. 7 et 8 | carte (idée 27) | style 5 (idée 28) |
| ensuite | | offre flash le 10/11, 20/11, 30/11 | ép. 9-10 selon la bible (maison de Mme Garnier à créer) | |

## 7. Points ouverts à la passation (à traiter en priorité)

1. **YouTube refuse les envois (403) depuis le 30/10 vers 12 h** (31/10 : les envois YouTube refonctionnent, la vidéo de 9 h du 31/10 est sur YouTube ; 23 et 24 du 30/10 restent sans YouTube) : très probablement le quota quotidien de l'API YouTube (10 000 unités ; un envoi = 1 600, une recherche de la veille = 100). Les Reels 23 et 24 du 30/10 sont partis sur TikTok mais pas sur YouTube (statut `en_publication`). À surveiller le 31/10 au matin ; limiter la veille YouTube à 2 recherches par jour ; ne jamais relancer une publication déjà partie sur TikTok (doublon).
2. **« unknown » en description** : la fondatrice a vu le 30/10 deux vidéos publiées en même temps avec une description « unknown » (plateforme à confirmer avec elle). Les légendes en base sont complètes. À éclaircir avec sa capture.
3. **Lecture des commentaires reçus** : le mode `recus` renvoie 404 (YouTube). Le bilan du soir ne peut pas encore lister les commentaires : à réparer (YouTube `commentThreads` par vidéo, avec les `platform_ids`).
4. **Série** : épisodes 9 et 10 à écrire (décor à créer : maison de Mme Garnier) en respectant la bible et la logique. Ép. 7 fait le 2/11 (Mme Dumas, décors `cuisine_dumas` / `rue_dumas`), ép. 8 le 3/11 (décor `entrepot`, carte `liste` ; Mme Garnier = « 04/11 · 2e passage », donc ép. 9 = la nuit même).
5. **Prospection** : toute l'Île-de-France est faite ; le 2/11, Oise (60, Guide Artisan : `/picardie/oise/plombier`, anciennes régions) et Eure-et-Loir (28, `/centre/eure-et-loir/plombier`) : 15 `propose`, 6 `a_proposer` (recherche web à faire, 2 avec adresse de siège différente). Suivants possibles : Loiret (45, `/centre/loiret`), Eure (27, `/haute-normandie/eure`), Aisne (02) / Somme (80) (`/picardie/...`). Réserve ancienne : CAREN, ABC PI (domiciliation), HERVE RICARDO (siège en Gironde).
6. LinkedIn proposé (page entreprise à créer par la fondatrice), sans réponse.
7. **Relevé des vues (hub mode `stats`) en erreur le 30/10 au soir, de nouveau le 31/10 au soir (même erreur, exécution 9dc32c74…)** : `getPostById` → `[400] Invalid post ID format` (exécution d45807fe…). **1/11 au soir : 3e soir de suite, même erreur (exécution 3e2df6db…)** — toujours pas de vues dans le bilan. **2/11 au soir : `stats` réussit (exécution 2bc7437c…) mais `export_stats` ne contient aucune ligne de stats** → toujours pas de vues ; à examiner en session (lecture des stats écrites). Probablement un Reel lu sans identifiant TikTok valide (23 et 24 du 30/10, `platform_ids` vide). Le bilan du soir n'a donc pas de vues. À corriger dans une session avec la fondatrice (filtre « identifiant TikTok présent » dans la route stats de `make/build_hub.py`) ; les tâches de contrôle ne modifient pas les scénarios. **5/11 au soir : de nouveau `[400] Invalid post ID format` (exécution a57505c7…).** **6/11 au soir : idem (exécution bb9e174a…). 7/11 au soir : idem (exécution 3dc1705a…). 8/11 au soir : idem (exécution 8eb6c11b…).**

8. **Week-end et prospection (31/10)** : 13 prospects validés (`pret`) le 30/10 étaient encore `pret` à 09:50 le samedi 31/10 (prospection prévue du lundi au vendredi : à confirmer au contrôle). Aucun nouveau prospect proposé le samedi pour ne pas dépasser 15 envois par jour ; reprendre le lundi 2/11 (2 en réserve : CAREN, ABC PI ; département suivant à choisir). **1/11** : aucun nouveau prospect proposé : les 13 `pret` + 2 relances J+5 remplissent déjà les 15 envois du lundi 2/11 (plafond de `prospects_lot`). Recherche de nouveaux prospects (département suivant) le lundi 2/11, pour les envois du mardi 3/11. **3/11** : aucun nouveau prospect : les 15 `propose` du 2/11 (non validés) restent dans le Plan ; 9 en réserve `a_proposer` (6 de l'Oise/Eure-et-Loir à vérifier sur le web, CAREN, ABC PI, HERVE RICARDO).

9. **Instagram + Facebook automatiques arrêtés le 31/10 vers 09:40** (contrôle de 18 h 46) : Make a éteint le scénario 8274397 après 3 erreurs Zernio `[409] already scheduled`. Cause : la Story échoue, son gestionnaire `Ignore` coupe la branche avant l'écriture de `instagram` dans `platform_ids`, donc le Reel est renvoyé à chaque passage. Correction à faire en session avec la fondatrice : `Resume` au lieu d'`Ignore` sur la Story (et sur le 409 du Reel), marquer `instagram` sur les 4 Reels du 31/10, puis réactiver. Facebook 12 h 30 / 18 h / 20 h 30 du 31/10 non publiés (fondatrice prévenue par e-mail). Détails : `controles/2026-10-31.md`. Toujours éteint au contrôle de 20 h 46 : tant que ce n'est pas réparé, Instagram + Facebook du 1/11 ne partiront pas seuls (rappel Meta mis dans le bilan du soir). **1/11 à 09 h 47 : toujours éteint** (aucune exécution depuis le 31/10 08:40Z), vidéo de 9 h du 1/11 absente d'Instagram/Facebook ; fondatrice prévenue de nouveau par e-mail. Réparation urgente en session. **1/11, tâche de 09:10** : toujours éteint ; l'e-mail réseaux demande de publier à la main sur Instagram + Facebook les vidéos du 2/11 tant que ce n'est pas réparé. **1/11 à 20 h 47 : toujours éteint** ; aucune des 5 vidéos du 1/11 sur Instagram/Facebook. **2/11 : réparé et réactivé en session avec la fondatrice (07:06Z)** ; rattrapage des vidéos du 31/10 et du 1/11 non fait.

10. **3 vidéos refusées le 2/11** (33 vécu logo, 35 carte médiateur, 36 motion communes ; 34 POV et ép. 6 validés), sans motif noté. Hypothèse : trop de vidéos sur le site le même jour (idées 12 à 20 = thème « site »). Question posée une fois dans l'e-mail réseaux du 2/11 ; les 4 Reels du 3/11 sont aussi sur le site (idées 16 à 19, ordre des 100 idées). **2/11 : scénario modifié et réactivé à 07:06Z** (passages réussis dès 08:10Z) ; à confirmer sur la vidéo de 12 h 30 du 2/11. **3/11 à 08:30Z : aucune des 5 vidéos du 3/11 n'est validée (toutes `en_attente`, la vidéo de 9 h n'est donc pas partie) et les 15 prospects proposés le 2/11 sont toujours `propose`** : le Plan du 2/11 n'a pas été validé. Les 4 Reels du 4/11 changent de thème (idées 20 à 24 : site puis signature). Rappel dans l'e-mail réseaux du 3/11. **3/11 à 11:48Z : toujours rien de validé, 9 h et 12 h 30 non parties** (alerte déjà envoyée à 09 h 49, pas de relance). **3/11 à 19:52Z : journée entière perdue, aucune des 5 vidéos du 3/11 validée ni publiée ; les 5 du 4/11 et les 15 prospects toujours en attente** (2e jour sans validation : rappel dans le bilan du soir). Si rien n'est validé le 4/11 au matin, ne pas fabriquer d'autres vidéos en plus : le stock s'accumule. **4/11 à 08:14Z : toujours rien de validé (3e jour) ; aucune vidéo fabriquée pour le 5/11, Plan non renvoyé.** Attention : « Tout valider » ferait partir d'un coup toutes les vidéos en retard (pas de limite basse sur l'heure dans le passage de 30 min) ; proposé à la fondatrice de « décaler » le stock (une vidéo par créneau à partir du lendemain), à faire en session. Tant que rien n'est validé, ne rien fabriquer de plus. **4/11 à 08:48Z (contrôle) : 9 h du 4/11 non partie, les 5 vidéos du 4/11 `en_attente` ; alerte envoyée.** **4/11 à 11:48Z : toujours rien de validé, 9 h et 12 h 30 non parties** (pas de nouvelle alerte). **4/11 à 17:48Z : toujours rien de validé, 9 h, 12 h 30 et 18 h (ép. 8) non parties** (pas de nouvelle alerte ; rappel au bilan du soir). **4/11 à 19:48Z : journée entière perdue (3e jour), aucune vidéo prévue le 5/11 ; 15 relances J+5 parties le matin ; bilan envoyé avec l'avertissement « Tout valider = 10 vidéos d'un coup » et la proposition de répartir le stock.** **5/11 à 08:1xZ : 4e jour, toujours rien de validé (10 vidéos `en_attente`, 15 prospects `propose`) ; rien fabriqué pour le 6/11, Plan non renvoyé ; e-mail réseaux envoyé avec le même avertissement.** **5/11 à 11:47Z (contrôle) : inchangé, stock de 10 vidéos toujours `en_attente`, rien de prévu le 5/11 ni le 6/11.** **5/11 à 17:48Z : toujours inchangé.** **5/11 à 19:46Z : journée entière sans vidéo (4e jour), rien de prévu le 6/11 ; 13 relances J+5 parties le matin ; bilan envoyé avec le même avertissement.** **6/11 à 08:1xZ : 5e jour, toujours rien de validé (10 vidéos `en_attente`, 15 prospects `propose`) ; rien fabriqué pour le 7/11, Plan non renvoyé ; e-mail réseaux envoyé avec le même avertissement.** **6/11 à 11:46Z (contrôle) : inchangé.** **6/11 à 17:46Z : inchangé.** **6/11 à 19:46Z : journée entière sans vidéo (5e jour), rien de prévu le 7/11 ; aucun e-mail de prospection parti ; bilan envoyé avec le même avertissement.** **7/11 à 08:1xZ : 6e jour, toujours rien de validé (10 vidéos `en_attente`, 15 prospects `propose`) ; rien fabriqué pour le 8/11, Plan non renvoyé ; e-mail réseaux envoyé avec le même avertissement. Offre flash du 10/11 : à fabriquer le 9/11 seulement si la machine repart.** **7/11 à 08:46Z (contrôle) : inchangé.** **7/11 à 11:46Z : inchangé.** **7/11 à 17:46Z : inchangé.** **8/11 à 08:1xZ : 7e jour, toujours rien de validé (10 vidéos `en_attente`, 15 prospects `propose`) ; rien fabriqué pour le 9/11, Plan non renvoyé ; e-mail réseaux envoyé avec le même avertissement. Offre flash du 10/11 : à fabriquer le 9/11 seulement si la machine repart.** **8/11 à 11:46Z (contrôle) : inchangé, rien de prévu le 8/11.** **8/11 à 17:46Z : inchangé.** **8/11 à 19:46Z : journée entière sans vidéo (7e jour), rien de prévu le 9/11 ; aucun e-mail de prospection parti ; bilan envoyé avec le même avertissement.**

## 8. Décisions de la fondatrice (dans l'ordre)

- 20/10 : vraies images de plomberie, mouvement dès la 1re image, écran rempli.
- 22/10 : voix Charon, pas de musique, texte lu mot pour mot, jamais le même plan, 100 idées comme seule source des fonctions, série « Sous pression ».
- 22/10 : seulement le lendemain ; e-mails de prospection 15/jour, partent à 09:05 après validation.
- 23/10 : Instagram + Facebook à la main via Meta ; commentaires reçus : petit merci court sans question ; e-mail quotidien « Vos 20 min réseaux ».
- 26-27/10 : 4 vidéos par jour (vécu, POV, série, carte).
- 28/10 : captures nettes non zoomées et aucune phrase muette, à vérifier avant chaque envoi ; ép. 2 : Mme Rocher en panique ; ép. 3 : Vasseur a une excuse logique, seul Vasseur est renvoyé, il murmure la menace.
- 28/10 soir : série relancée depuis l'épisode 2.
- 29/10 : phrase « Écrivez DEVIS » à la fin de chaque prochaine vidéo, sauf la série ; offre flash maquette gratuite tous les 10 jours.
- 30/10 : Instagram + Facebook de nouveau automatiques (à partir des vidéos du 31/10) ; la phrase d'appel « Écrivez DEVIS » a son propre plan, avec prouessia.fr en bas.
- 30/10 : style 5 « motion » validé (5e vidéo, 22 h) ; motion aussi sur vécu/POV/carte en gardant leur style.
- 30/10 : publication même si la validation arrive après 09:05 ; contrôles dans la journée ; bilan du soir ; **la communication passe sous la responsabilité de Claude Code**.

## 9. Comment rendre compte à la fondatrice

- Un seul e-mail quand il faut agir, en 3 à 6 lignes : ce qui se passe, ce qu'on a déjà fait, ce qu'elle doit faire (ou rien).
- Jamais de jargon (« scénario », « API », « statut ») dans ses e-mails : dire « la vidéo de 12 h 30 n'est pas partie sur YouTube ».
- Ne pas la solliciter pour ce qu'on peut régler seul ; ne jamais lui demander une clé.
