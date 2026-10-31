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
| lun. 2/11 | idée suivante (12) | POV | ép. 6 « L'aimant » (`anim/ep06/A-FAIRE.md` : voix + rendu ≈ 25 min à faire) | carte | style 5 |
| ensuite | | offre flash le 10/11, 20/11, 30/11 | ép. 7+ selon la bible (décors à créer) | |

## 7. Points ouverts à la passation (à traiter en priorité)

1. **YouTube refuse les envois (403) depuis le 30/10 vers 12 h** (31/10 : les envois YouTube refonctionnent, la vidéo de 9 h du 31/10 est sur YouTube ; 23 et 24 du 30/10 restent sans YouTube) : très probablement le quota quotidien de l'API YouTube (10 000 unités ; un envoi = 1 600, une recherche de la veille = 100). Les Reels 23 et 24 du 30/10 sont partis sur TikTok mais pas sur YouTube (statut `en_publication`). À surveiller le 31/10 au matin ; limiter la veille YouTube à 2 recherches par jour ; ne jamais relancer une publication déjà partie sur TikTok (doublon).
2. **« unknown » en description** : la fondatrice a vu le 30/10 deux vidéos publiées en même temps avec une description « unknown » (plateforme à confirmer avec elle). Les légendes en base sont complètes. À éclaircir avec sa capture.
3. **Lecture des commentaires reçus** : le mode `recus` renvoie 404 (YouTube). Le bilan du soir ne peut pas encore lister les commentaires : à réparer (YouTube `commentThreads` par vidéo, avec les `platform_ids`).
4. **Série** : épisodes 7 à 10 à écrire (décors à créer : chez la mère de Léa, entrepôt, maison de Mme Garnier) en respectant la bible et la logique.
5. **Prospection** : 2 prospects en réserve (adresse de domiciliation) ; département suivant à choisir (78, 92, 91, 94, 95, 93, 75, 77 déjà faits).
6. LinkedIn proposé (page entreprise à créer par la fondatrice), sans réponse.
7. **Relevé des vues (hub mode `stats`) en erreur le 30/10 au soir** : `getPostById` → `[400] Invalid post ID format` (exécution d45807fe…). Probablement un Reel lu sans identifiant TikTok valide (23 et 24 du 30/10, `platform_ids` vide). Le bilan du soir n'a donc pas de vues. À corriger dans une session avec la fondatrice (filtre « identifiant TikTok présent » dans la route stats de `make/build_hub.py`) ; les tâches de contrôle ne modifient pas les scénarios.

8. **Week-end et prospection (31/10)** : 13 prospects validés (`pret`) le 30/10 étaient encore `pret` à 09:50 le samedi 31/10 (prospection prévue du lundi au vendredi : à confirmer au contrôle). Aucun nouveau prospect proposé le samedi pour ne pas dépasser 15 envois par jour ; reprendre le lundi 2/11 (2 en réserve : CAREN, ABC PI ; département suivant à choisir).

9. **Instagram + Facebook automatiques arrêtés le 31/10 vers 09:40** (contrôle de 18 h 46) : Make a éteint le scénario 8274397 après 3 erreurs Zernio `[409] already scheduled`. Cause : la Story échoue, son gestionnaire `Ignore` coupe la branche avant l'écriture de `instagram` dans `platform_ids`, donc le Reel est renvoyé à chaque passage. Correction à faire en session avec la fondatrice : `Resume` au lieu d'`Ignore` sur la Story (et sur le 409 du Reel), marquer `instagram` sur les 4 Reels du 31/10, puis réactiver. Facebook 12 h 30 / 18 h / 20 h 30 du 31/10 non publiés (fondatrice prévenue par e-mail). Détails : `controles/2026-10-31.md`.

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
