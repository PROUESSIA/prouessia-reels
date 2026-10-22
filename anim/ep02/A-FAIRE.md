# Ép. 2 — à finir avant samedi 24/10 9 h 05

La dernière réplique (Vasseur, plan `vasseur`) est pour l'instant un sous-titre muet : le quota de voix Gemini était épuisé le 22/10.

1. Hub mode `voix`, `voice=Algenib`, `text` = « Vous êtes perdu, Monsieur Morel ? », style : voix d'homme de 50 ans, posée, mielleuse, presque amusée, calme inquiétant, `path=anim/ep02/vasseur-gemini.txt`.
2. Extraire le WAV → `anim/ep02/vasseur.wav`, couper les silences → `vasseur-court.wav`, ajouter `"vasseur": [[début, fin]]` dans `segments` et `"vasseur": ["Vous êtes perdu, Monsieur Morel ?"]` dans `textes`.
3. Dans le déroulé, remplacer le plan `"plan": "vasseur"` par `"qui": "vasseur", "n": 0` (garder décor, cam, cible, ev ; enlever `duree` et `soustitre` ; `"gras": 2`).
4. `python3 anim/film.py ep02 --sans3d --reutiliser`, vérifier, commit + push.
5. Hub mode `ajouter` avec le même `video_file=anim/ep02/film.mp4` (remplace la vidéo de l'ép. 2 déjà programmée), ou à défaut le noter dans `problemes/`.
6. Supprimer ce fichier.
