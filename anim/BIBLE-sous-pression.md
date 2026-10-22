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
| **Mme Rocher** | cliente de Vasseur, 80 ans, seule, peureuse puis naïve (ép. 2-3, 9-10) | cheveux blancs courts, gilet beige | Vindemiatrix |
| **Bruno Vasseur** | patron de Vasseur Dépannage, charmeur, sans scrupules (apparaît ép. 2) | costume gris, cheveux gominés | Algenib |
| **Théo** | apprenti de Julien, 19 ans, drôle et malin (apparaît ép. 5) | à créer : casquette, sweat orange | Puck |
| Narrateur | carte sponsor et fin | — | Charon |

## Arc de la saison 1 (10 épisodes) — version validée par la fondatrice le 22/10 au soir
Fil rouge : un plombier honnête contre un faux dépanneur qui arnaque les personnes âgées (arnaque réelle en France : aimants « urgence plomberie » dans les boîtes aux lettres, factures abusives). Le gentil est accusé à tort, le spectateur revient pour la revanche. **Rester simple et logique** : chaque rebondissement doit s'expliquer par ce qu'on a vu à l'écran (pas de policier complice, pas de carte SIM copiée, pas d'objet mystérieux jamais expliqué).
1. **La fuite de 3 h 12** ✅ — Mme Lefèvre (80 ans) inondée en pleine nuit ; robinet d'arrêt posé par Vasseur Dépannage, 890 € pour une pièce à 10 € ; Julien veut prévenir les autres clients. Fin : SMS anonyme « Occupe-toi de tes chantiers, Morel. »
2. **Elle ne répond plus** ✅ — 23 h, Julien appelle Mme Rocher, autre cliente de Vasseur. Elle chuchote, terrifiée : « Il est revenu… il est dans ma cuisine… » (Vasseur est entré avec la clé qu'elle cache sous son pot de fleurs : il l'avait vue la sortir la première fois). La ligne coupe. Julien fonce : pot renversé, clé dans la serrure, cuisine inondée, personne ; facture Vasseur datée de ce soir 23 h 10. Fin : une lampe s'allume dans son dos, « Vous êtes perdu, Monsieur Morel ? »
3. **Le piège** — retour 10 minutes en arrière : Vasseur entre avec la clé cachée sous le pot et fait couler l'eau lui-même (c'est le bruit qui a fait peur à Mme Rocher). Pendant qu'elle chuchote au téléphone avec Julien, il la surprend, lui prend le téléphone (la ligne coupe) et joue au sauveur : « Un voisin m'a appelé, il y avait de l'eau sous votre porte, je suis entré pour sauver votre cuisine. » Soulagée, elle le paie sur place (la facture « PAYÉ · 23 h 10 » de l'ép. 2). Puis il appelle la police : « Un inconnu harcèle ma cliente âgée au téléphone, il va venir chez elle. » Présent : Julien entre ; Vasseur glisse à Mme Rocher : « C'est lui, l'homme qui appelle les dames seules la nuit. » La police arrive ; Mme Rocher, qui n'a jamais vu Julien (il avait eu son numéro par son amie Mme Lefèvre), dit : « Je ne connais pas ce monsieur… » Julien est emmené. Fin : dans la voiture, le policier : « L'appel est arrivé à 23 h 14. » Julien : « Elle m'a parlé à 23 h 12… Il savait que j'arrivais. »
4. **Garde à vue** — nuit au poste ; Léa arrive, puis Mme Lefèvre en robe de chambre : « Ce monsieur m'a sauvée, l'autre m'a volée ! » Julien relâché au matin. Fin : sur sa camionnette, « ESCROC » à la peinture ; une vidéo de la camionnette circule dans le quartier.
5. **L'aimant** — Théo, l'apprenti (19 ans, drôle, malin), trouve le point commun : toutes les victimes ont appelé le numéro d'un aimant « Urgence plomberie 24 h/24 » glissé dans leur boîte, avec un faux logo de mairie. Fin : au dos de l'aimant de Mme Lefèvre, au stylo, son adresse et « 80 ans, seule » : les victimes étaient choisies à l'avance.
6. **L'entrepôt** — Théo suit la camionnette de Vasseur jusqu'à un entrepôt plein de cartons d'aimants et de robinets bas de gamme ; il prend des photos. Fin : la porte se referme, « T'es qui, toi ? »
7. **La fuite de Théo** — caché, batterie presque vide, il envoie sa position à Julien ; Julien et Léa arrivent, Théo s'échappe par le quai. Fin : ses photos sont floues, sauf une : une liste de 40 adresses.
8. **La liste** — tournée des adresses pour prévenir (« Ne rappelez pas ce numéro ») ; une dame leur claque la porte au nez (elle a vu la vidéo « ESCROC »). Fin : la dernière adresse est celle de la mère de Léa.
9. **La preuve** — Vasseur est déjà chez la mère de Léa ; Julien coupe l'eau, Léa filme Vasseur sortant une pièce abîmée de sa sacoche ; Mme Rocher, qui l'a reconnu à la télé locale, appelle Julien pour s'excuser. Fin : Vasseur voit le téléphone de Léa et sourit : « Tu crois que ça suffit ? »
10. **Pression maximale** — dans la rue, devant les voisins : le robinet de l'ép. 1 (gardé par Léa), la vidéo, la liste, les témoignages de Mme Rocher et Mme Lefèvre ; la police emmène Vasseur, Mme Lefèvre récupère ses 890 €. Dernière image : 3 h 12, le téléphone de Julien sonne… « Saison 2 ? »

**Rappel en ouverture (règle du 22/10)** : chaque épisode à partir du 2 commence par une carte muette `{"carte": "precedemment", "duree": 2.2, "son": "sonnerie", "volume": 0.5}` et un champ `"precedemment"` dans episode.json (1 ou 2 phrases simples, mots-clés en `<b>`), pour ceux qui arrivent en cours de série. Chaque épisode doit se comprendre seul ; quand un indice compte (clé, facture, heure), le montrer en gros plan avec un sous-titre court.

## Production (moteur `anim/`)
- `anim/film.html` : décors (`chambre`, `camion` pluie, `cuisine_lefevre` inondée, `cuisine_jour`, `parking` nuit), personnages et poses (`debout`, `assis`, `volant`, `telephone`, `telephone_main`, `bras_croises`, `mains_levees`, `accroupi`, `allonge`, `assis_lit`), événements (`sonne`, `decroche`, `roule`, `torche`, `serre`, `coupe`, `debout`, `sms`). Ajouter un décor = une fonction `decorXxx(x0)` placée à un nouvel X (+20) et une couleur de fond dans `FONDS`.
- `anim/epNN/episode.json` : textes par personnage, voix, segments, **déroulé** (une ligne par plan : décor, caméra départ/fin, cible, événements, mots en jaune, incrustation d'heure, cartes sponsor/fin).
- Voix : hub mode `voix`, une prise par personnage (toutes ses répliques, une par ligne). Resserrer les silences (`silenceremove … stop_silence=0.2`), puis découper : idéalement transcription mot à mot (ElevenLabs Scribe, fichier `mots-<perso>.json` = une liste par réplique), sinon `segments` (début/fin de chaque réplique dans le fichier `-court.wav`).
- `python3 anim/apercu_film.py epNN planche.png` → une image par plan pour vérifier cadrages et lumière **avant** le rendu.
- `python3 anim/film.py epNN` → `anim/epNN/film.mp4` (rendu 3D ≈ 0,8 s par image : ≈ 20 à 25 min pour un épisode).
