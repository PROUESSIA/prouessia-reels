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
2. Le sponsor : une carte **muette de 1,8 s** au milieu (`{"carte": "sponsor", "duree": 1.8}`) : « présenté par Prouessia », sans voix. Jamais d'autre mention de Prouessia, jamais de démo de l'appli dans le film.
2 bis. **Signature sonore** (sans musique, sons originaux de `anim/sons.py`) : la **sonnerie** de Julien (vibreur + trois « plic » de goutte) ouvre chaque épisode ou retentit dès qu'un téléphone sonne ; le **générique** (montée de pression, clac de vanne, goutte) accompagne la carte de fin. Champ `"son"` dans le déroulé.
3. Fin : carte muette « Épisode N+1, demain 18 h » + « Histoire et personnages fictifs » (3 s), avec le générique sonore. Toujours un cliffhanger juste avant.
4. Fiction : aucun vrai nom d'entreprise ni de personne. Le concurrent s'appelle **Vasseur Dépannage** (inventé). Les chiffres dits par les personnages sont de la fiction, pas des faits (la règle 1 d'AUTOMATION.md ne s'applique pas aux dialogues de fiction, mais rien de dangereux ni de faux conseil technique présenté comme vrai).
5. Vouvoiement non obligatoire entre personnages (c'est de la fiction) ; la voix de marque « on/nous » ne concerne que la carte sponsor.
6. **Rythme rapide** (demande du 22/10) : `"rythme": {"pauses": 0.4, "silences": 0.55, "vitesse": 1.12}` dans episode.json (pauses courtes, plans muets courts, voix accélérées de 12 % sans changer la hauteur). Viser 40 à 55 s.
7. **« Musique sans instrument »** (demande du 22/10) : fond de tension `anim/sons/tension.wav` (battements de cœur, tic-tac, gouttes, souffle grave, 96 BPM), baissé automatiquement sous les voix, coupé à la carte de fin où le générique prend le relais. Aucun instrument de musique. Voix Gemini : une voix par personnage.

## Personnages
| Personnage | Rôle | Look | Voix Gemini |
|---|---|---|---|
| **Julien Morel** | plombier indépendant, 44 ans, ancien pompier reconverti : calme, peu de mots, observe avant de parler, humour sec, ne lâche jamais une injustice | casquette bordeaux, tempes grises, veste gris-bleu, badge jaune, sans barbe | Orus |
| **Léa** | sa compagne, infirmière, lucide et drôle | cheveux longs châtains, pull vert | Aoede |
| **Mme Lefèvre** | cliente de 80 ans, adorable, un peu naïve | chignon blanc, robe de chambre rose | Gacrux |
| **Bruno Vasseur** | patron de Vasseur Dépannage, charmeur, sans scrupules (apparaît ép. 3) | à créer : costume gris, cheveux gominés | Algenib |
| **Théo** | apprenti de Yanis, 19 ans, comique (apparaît ép. 4) | à créer : casquette, sweat orange | Puck |
| Narrateur | carte sponsor et fin | — | Charon |

## Arc de la saison 1 (10 épisodes) — version « suspense » du 22/10
Chaque épisode finit sur un retournement : le spectateur doit se dire « non… » et revenir le lendemain.
1. **La fuite de 3 h 12** ✅ — Mme Lefèvre inondée ; robinet d'arrêt posé par Vasseur Dépannage, facturé 890 € ; SMS : « Occupe-toi de tes chantiers, Morel. »
2. **Elle ne répond plus** — Julien appelle les autres clients de Vasseur. Mme Rocher décroche en chuchotant : « Il est revenu… il est dans ma cuisine… » — la ligne coupe. Julien fonce sous la pluie. Porte entrouverte, eau qui coule sous la porte, cuisine inondée, personne. Sur la table : une facture Vasseur datée d'aujourd'hui, 23 h 10. Dans l'eau, le téléphone de Mme Rocher vibre : « appel entrant : Julien Morel ». Julien sort son propre téléphone : éteint. Une lampe s'allume derrière lui : « Vous êtes perdu, Monsieur Morel ? »
3. **L'homme à la lampe** — c'est Bruno Vasseur, souriant. Mme Rocher arrive derrière lui en pantoufles : « Bruno est un ange, il est venu réparer. » Julien passe pour un fou. Sirènes : la police arrive… pour Julien, entré chez une vieille dame en pleine nuit. Cliffhanger : les menottes.
4. **Garde à vue** — Léa vient le chercher, Mme Lefèvre témoigne pour lui. En sortant, Julien voit sur le bureau du policier un aimant « Vasseur Dépannage ». Cliffhanger : le policier est le beau-frère de Vasseur.
5. **Le numéro cloné** — Théo, l'apprenti (19 ans, malin), comprend : quelqu'un a copié la carte SIM de Julien. Les clients reçoivent des SMS « de Julien » qui les insultent. Cliffhanger : Mme Lefèvre en a reçu un… et ne répond plus à Julien.
6. **La cave** — Théo suit la camionnette blanche jusqu'à un entrepôt rempli de robinets défectueux. La porte se referme, la cave se remplit d'eau. Cliffhanger : le téléphone de Théo n'a plus de batterie.
7. **Course contre l'eau** — Julien et Léa retrouvent Théo de justesse ; il a filmé l'entrepôt. Cliffhanger : la vidéo a disparu du téléphone.
8. **L'immeuble** — un immeuble entier inondé en pleine nuit, toutes les pièces viennent de Vasseur ; Julien coupe tout seul dans la chaufferie. Cliffhanger : la porte se ferme à clé derrière lui.
9. **La preuve** — Léa a gardé le robinet de l'épisode 1 ; Théo a sauvegardé la vidéo dans le cloud. Cliffhanger : Vasseur sonne chez Julien et Léa.
10. **Pression maximale** — confrontation devant les voisins, Vasseur démasqué, Mme Lefèvre récupère son argent. Dernière image : le téléphone de Julien sonne à 3 h 12… « Saison 2 ? »

## Production (moteur `anim/`)
- `anim/film.html` : décors (`chambre`, `camion` pluie, `cuisine_lefevre` inondée, `cuisine_jour`, `parking` nuit), personnages et poses (`debout`, `assis`, `volant`, `telephone`, `telephone_main`, `bras_croises`, `mains_levees`, `accroupi`, `allonge`, `assis_lit`), événements (`sonne`, `decroche`, `roule`, `torche`, `serre`, `coupe`, `debout`, `sms`). Ajouter un décor = une fonction `decorXxx(x0)` placée à un nouvel X (+20) et une couleur de fond dans `FONDS`.
- `anim/epNN/episode.json` : textes par personnage, voix, segments, **déroulé** (une ligne par plan : décor, caméra départ/fin, cible, événements, mots en jaune, incrustation d'heure, cartes sponsor/fin).
- Voix : hub mode `voix`, une prise par personnage (toutes ses répliques, une par ligne). Resserrer les silences (`silenceremove … stop_silence=0.2`), puis découper : idéalement transcription mot à mot (ElevenLabs Scribe, fichier `mots-<perso>.json` = une liste par réplique), sinon `segments` (début/fin de chaque réplique dans le fichier `-court.wav`).
- `python3 anim/apercu_film.py epNN planche.png` → une image par plan pour vérifier cadrages et lumière **avant** le rendu.
- `python3 anim/film.py epNN` → `anim/epNN/film.mp4` (rendu 3D ≈ 0,8 s par image : ≈ 20 à 25 min pour un épisode).
