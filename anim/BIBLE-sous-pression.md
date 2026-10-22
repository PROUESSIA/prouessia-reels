# « Sous pression » — bible de la série (vidéos de 18 h)

Décision de la fondatrice (22/10/2026) : les vidéos de l'après-midi deviennent de **courts films animés** à suspense, en épisodes. Prouessia n'est **pas le sujet** : c'est le **sponsor** de la série, cité **une seule fois, au milieu** (« Sous pression, une série présentée par Prouessia, le partenaire des plombiers »). Le reste est de la fiction pure.

## Ce qui marche (veille du 22/10)
- Micro-dramas verticaux de 60 à 90 s, une saison de 5 à 10 épisodes, 1 épisode par jour, mêmes personnages.
- Accroche dans les 2 premières secondes (un téléphone qui sonne à 3 h 12, une fuite, une menace).
- Chaque épisode : mise en place → la tension monte → **cliffhanger** (on revient le lendemain pour la suite).
- Personnages attachants et constants → les gens commentent, devinent la suite, suivent le compte.
- Sous-titres mot à mot, mots-clés en jaune. Pas de musique (règle de la fondatrice), seulement les voix.
- Sources : [micro-dramas IA](https://blog.mulerun.com/p/how-to-make-ai-micro-dramas-for-tiktok-and-reels-2026/), [Fruit Love Island](https://en.wikipedia.org/wiki/Fruit_Love_Island), [tendances Reels 2026](https://www.anijam.ai/blog/instagram-reels-trends/), vidéo de référence de la fondatrice (@teo_8jours).

## Règles fixes
1. 50 à 80 s. Personnages low-poly **sans yeux ni bouche** (tête, nez, oreilles ; pas de lunettes : elles ressemblent à des yeux).
2. Le sponsor : une carte de 4 à 5 s au milieu (`"carte": "sponsor"`), dite par le narrateur (voix Charon). Jamais d'autre mention de Prouessia, jamais de démo de l'appli dans le film.
3. Fin : carte « Épisode N+1, demain 18 h » + « Histoire et personnages fictifs ». Toujours un cliffhanger juste avant.
4. Fiction : aucun vrai nom d'entreprise ni de personne. Le concurrent s'appelle **Vasseur Dépannage** (inventé). Les chiffres dits par les personnages sont de la fiction, pas des faits (la règle 1 d'AUTOMATION.md ne s'applique pas aux dialogues de fiction, mais rien de dangereux ni de faux conseil technique présenté comme vrai).
5. Vouvoiement non obligatoire entre personnages (c'est de la fiction) ; la voix de marque « on/nous » ne concerne que la carte sponsor.
6. Pas de musique. Voix Gemini : une voix par personnage (voir ci-dessous).

## Personnages
| Personnage | Rôle | Look | Voix Gemini |
|---|---|---|---|
| **Yanis Morel** | plombier indépendant, 35 ans, droit, têtu | barbe, veste bleue, badge jaune | Orus |
| **Léa** | sa compagne, infirmière, lucide et drôle | cheveux longs châtains, pull vert | Aoede |
| **Mme Lefèvre** | cliente de 80 ans, adorable, un peu naïve | chignon blanc, robe de chambre rose | Gacrux |
| **Bruno Vasseur** | patron de Vasseur Dépannage, charmeur, sans scrupules (apparaît ép. 3) | à créer : costume gris, cheveux gominés | Algenib |
| **Théo** | apprenti de Yanis, 19 ans, comique (apparaît ép. 4) | à créer : casquette, sweat orange | Puck |
| Narrateur | carte sponsor et fin | — | Charon |

## Arc de la saison 1 (10 épisodes)
1. **La fuite de 3 h 12** ✅ — Mme Lefèvre inondée ; robinet d'arrêt posé par Vasseur Dépannage, facturé 890 € ; menace par SMS.
2. **Cinq étoiles** — Yanis appelle les autres clients de Vasseur : tous des personnes âgées, tous la même pièce. Léa découvre que les avis 5 étoiles sont tous écrits le même jour. Cliffhanger : une camionnette blanche suit Yanis.
3. **La camionnette blanche** — face à face avec Bruno Vasseur sur un parking : charmant, menaçant. « Tu devrais penser à ta famille, Morel. » Cliffhanger : le lendemain, les pneus de Yanis sont crevés.
4. **L'apprenti** — Théo arrive, maladroit mais malin ; il filme tout. Ils trouvent le fournisseur des pièces défectueuses. Cliffhanger : le fournisseur est… le beau-frère de Vasseur.
5. **Le faux rendez-vous** — Théo se fait passer pour un client pour piéger Vasseur. Ça tourne mal. Cliffhanger : Théo ne répond plus.
6. **Sous l'évier** — Théo retrouvé enfermé dans une cave inondée ; course contre l'eau. Cliffhanger : la vidéo de Théo est effacée.
7. **La plainte** — Mme Lefèvre accepte de témoigner ; Vasseur lui rend visite avec des fleurs. Cliffhanger : elle retire son témoignage.
8. **L'immeuble** — gros dégât des eaux dans un immeuble entier, toutes les pièces viennent de Vasseur ; Yanis doit tout couper seul la nuit. Cliffhanger : quelqu'un a fermé la porte de la chaufferie à clé derrière lui.
9. **La preuve** — Léa a gardé le robinet de l'épisode 1 ; un expert confirme. Cliffhanger : Vasseur arrive chez Yanis.
10. **Pression maximale** — confrontation finale devant les voisins ; Vasseur démasqué ; Mme Lefèvre récupère son argent. Dernière image : le téléphone de Yanis sonne à 3 h 12… « Saison 2 ? »

## Production (moteur `anim/`)
- `anim/film.html` : décors (`chambre`, `camion` pluie, `cuisine_lefevre` inondée, `cuisine_jour`, `parking` nuit), personnages et poses (`debout`, `assis`, `volant`, `telephone`, `telephone_main`, `bras_croises`, `mains_levees`, `accroupi`, `allonge`, `assis_lit`), événements (`sonne`, `decroche`, `roule`, `torche`, `serre`, `coupe`, `debout`, `sms`). Ajouter un décor = une fonction `decorXxx(x0)` placée à un nouvel X (+20) et une couleur de fond dans `FONDS`.
- `anim/epNN/episode.json` : textes par personnage, voix, segments, **déroulé** (une ligne par plan : décor, caméra départ/fin, cible, événements, mots en jaune, incrustation d'heure, cartes sponsor/fin).
- Voix : hub mode `voix`, une prise par personnage (toutes ses répliques, une par ligne). Resserrer les silences (`silenceremove … stop_silence=0.2`), puis découper : idéalement transcription mot à mot (ElevenLabs Scribe, fichier `mots-<perso>.json` = une liste par réplique), sinon `segments` (début/fin de chaque réplique dans le fichier `-court.wav`).
- `python3 anim/apercu_film.py epNN planche.png` → une image par plan pour vérifier cadrages et lumière **avant** le rendu.
- `python3 anim/film.py epNN` → `anim/epNN/film.mp4` (rendu 3D ≈ 0,8 s par image : ≈ 20 à 25 min pour un épisode).
