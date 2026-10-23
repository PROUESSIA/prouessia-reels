# Ép. 2 (nouvelle version validée le 23/10) — à finir le vendredi 23/10, pour samedi 24/10 18 h

Le script est déjà dans `anim/ep02/episode.json` (textes, voix, déroulé). Il ne manque que les voix, puis le rendu.

1. **3 prises de voix** (hub mode `voix`, une par personnage, `text` = les répliques de `textes.<perso>`, une par ligne) :
   - `julien` : voice=Orus, style = « homme de 44 ans, ancien pompier, calme mais tendu, voix basse, phrases courtes, chuchoté pour « La clé est sur la porte… » et « Vasseur… » », `path=anim/ep02/voix-julien-gemini.txt`
   - `rocher` : voice=Vindemiatrix, style = « dame de 80 ans qui chuchote, terrifiée, souffle court, petites pauses », `path=anim/ep02/voix-rocher-gemini.txt`
   - `vasseur` : voice=Algenib, style = « homme de 50 ans, posé, mielleux, presque amusé, calme inquiétant », `path=anim/ep02/voix-vasseur-gemini.txt`
2. Pour chaque fichier : extraire le WAV (champ base64 avant le « | »), vérifier la durée et que le texte n'est pas lu deux fois ni les consignes lues ; couper les silences → `anim/ep02/<perso>-court.wav` (`silenceremove=stop_periods=-1:stop_duration=0.35:stop_threshold=-40dB`, garder 0,2 s) ; écrire `segments.<perso>` = [début, fin] de chaque réplique dans le fichier court (une réplique par ligne de `textes`, dans l'ordre ; silencedetect pour trouver les coupures). Si ElevenLabs Scribe répond, `mots-<perso>.json` (une liste par réplique) est mieux.
3. `rm -rf anim/ep02/frames anim/ep02/st anim/ep02/parts` puis `python3 anim/film.py ep02 --prep` (vérifier les durées), `python3 anim/apercu_film.py ep02 planche.png` (aucun plan noir), puis `python3 anim/film.py ep02` en arrière-plan (≈ 10 min).
4. Vérifier une planche d'images de `film.mp4` (sous-titres, clé, caisse à outils « VASSEUR » lisible, lampe), < 8 Mo. `cp anim/ep02/items.json anim/ep02/items-rendu.json`, cover.png (image de la caisse à outils), commit + push.
5. Hub mode `ajouter` avec seulement `video_file=anim/ep02/film.mp4` (remplace la vidéo déjà programmée, qui est en attente de validation). Le Plan du jour la montrera à valider.
6. Supprimer ce fichier.

**Règle de la fondatrice (23/10) : aucun texte d'explication à l'écran** (pas de carte « Précédemment », pas de sous-titre de narrateur). Seulement les sous-titres des dialogues, l'heure en incrustation et les cartes sponsor et fin.
