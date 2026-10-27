# Ép. 6 « L'aimant » — à finir (écrit le 27/10 au soir)

Scénario, déroulé caméra, décor `rue` (événements `jour`, `glisse`, `boite1`, `cafe`, `au_cafe`, `enveloppe`, `retourne_imper`) prêts et vérifiés sur une planche. **Ne pas réécrire.** À faire le jeudi 29/10 pour le vendredi 30/10 18 h.

1. Voix : 4 prises (hub mode `voix`, `path` = `anim/ep06/voix-<perso>-gemini.txt`, `text` = les répliques du personnage, une par paragraphe séparées par une ligne vide). Maximum 3 prises par minute.

   - `theo` : voice `Puck`, style : « Voix de jeune homme français de 19 ans, apprenti plombier, au téléphone en filature : chuchoté, excité et tendu, débit rapide. Une vraie pause d'une seconde entre chaque réplique. »
   - `julien` : voice `Orus`, style : « Voix d'homme français de 44 ans, ancien pompier, au téléphone : calme, grave, protecteur, ferme à la deuxième réplique. Une vraie pause d'une seconde entre les deux répliques. »
   - `imper` : voice `Charon`, style : « Voix d'homme français d'une soixantaine d'années, sec, bas, froid, sans émotion ; la dernière réplique très lente, presque un murmure menaçant. Une vraie pause de deux secondes entre les deux répliques. »
   - `vasseur` : voice `Algenib`, style : « Voix d'homme français de 50 ans, charmeur mais cynique, satisfait, à voix basse au café. »

2. `python3 anim/voix_ep.py ep06 decoder`, pousser, attendre l'action « Transcrire une voix », `git pull`, `python3 anim/voix_ep.py ep06 mots`.
3. `cd anim && python3 film.py ep06 --prep`, planche, rendu en arrière-plan.
4. `cover.png`, pousser, `ajouter` pour le lendemain 18:00 Paris (17:00Z) ; hook « Sous pression · Épisode 6 — L'aimant » ; caption = « L'aimant » + « Épisode 6 · Sous pression » + « Théo suit l'homme en imperméable… jusqu'au café où l'attend Vasseur. » + « Histoire et personnages fictifs. » + 3 hashtags ; pinned_comment = « Selon vous, Théo doit-il s'enfuir ou continuer à filmer ? ». Cocher l'ép. 6 dans la bible.
