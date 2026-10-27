# Ép. 5 « La serrure » — à finir (écrit le 27/10 au soir)

Le scénario, le déroulé caméra, les décors (`parking` avec Théo et Léa, `cuisine_lefevre` + événement `soir`, nouveau décor `rue`) et la carte `enregistrement` sont prêts et vérifiés sur une planche. **Ne pas réécrire.**

1. Voix : 5 prises (hub mode `voix`, `path` = `anim/ep05/voix-<perso>-gemini.txt`, `text` = les répliques du personnage dans `episode.json`, une par paragraphe, séparées par une ligne vide). Maximum 3 prises par minute : attendre 60 s après la 3e.

   - `theo` : voice `Puck`, style : « Voix de jeune homme français de 19 ans, apprenti plombier, malin et drôle, un peu moqueur au début, puis sérieux et chuchoté quand il montre la photo. Naturel, pas théâtral. Une vraie pause d'une seconde entre chaque réplique. »
   - `julien` : voice `Orus`, style : « Voix d'homme français de 44 ans, ancien pompier : calme, grave, peu de mots, humour sec. Ton de série policière, posé et tendu. Une vraie pause d'une seconde entre chaque réplique. »
   - `lea` : voice `Aoede`, style : « Voix de femme française d'une quarantaine d'années, infirmière : chaleureuse avec la vieille dame, puis sèche et méfiante avec le dépanneur, puis essoufflée et fière, et enfin glacée, presque un murmure, à la dernière réplique. Une vraie pause d'une seconde entre chaque réplique. »
   - `lefevre` : voice `Gacrux`, style : « Voix de femme française de 80 ans, douce, un peu naïve, contente de voir l'infirmière. »
   - `vasseur` : voice `Algenib`, style : « Voix d'homme français de 50 ans, commercial charmeur et mielleux, faussement rassurant ; à la dernière réplique, une menace douce, lente, presque souriante. Une vraie pause d'une seconde entre chaque réplique. »

2. `python3 anim/voix_ep.py ep05 decoder`, pousser (`voix/transcrire/ep05-*.wav`), attendre l'action « Transcrire une voix » (≈ 3 à 5 min), `git pull`, puis `python3 anim/voix_ep.py ep05 mots` (segments + `mots-<perso>.json`). Écouter/vérifier : « non reconnues 0 » pour chaque personnage.
3. `cd anim && python3 film.py ep05 --prep` puis `python3 apercu_film.py ep05 planche.png` (vérifier les 18 plans), puis le rendu `python3 film.py ep05` en arrière-plan (≈ 25 min).
4. `cover.png` (une image du plan de Vasseur), pousser, `ajouter` pour le lendemain 18:00 Paris (17:00Z) ; hook « Sous pression · Épisode 5 — La serrure » ; caption = « La serrure » + « Épisode 5 · Sous pression » + « Vasseur change la serrure de Mme Lefèvre… et Léa enregistre tout. » + « Histoire et personnages fictifs. » + 3 hashtags ; pinned_comment = « Selon vous, que fait l'homme en imperméable chez la mère de Léa ? ». Cocher l'ép. 5 dans la bible.
