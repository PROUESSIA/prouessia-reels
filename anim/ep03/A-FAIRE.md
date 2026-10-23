# Ép. 3 « Le piège » — nouvelle version (23/10, logique corrigée) — à finir le samedi 24/10, pour dimanche 25/10 18 h

La fondatrice a refusé la version où Mme Rocher dit ne pas connaître Julien (elle l'a appelé à l'ép. 2). Nouvelle logique : la police (appelée par Julien) arrive ; Mme Rocher confirme qu'elle a appelé Julien et ne sait pas comment Vasseur est entré ; Vasseur montre un « contrat d'entretien » signé par elle (accès en cas d'urgence, clé sous le pot) ; le policier constate qu'il n'y a pas d'effraction et un contrat signé (litige, pas délit), conseille à Mme Rocher de porter plainte demain si elle conteste, et fait sortir tout le monde ; Vasseur, face à Julien : « La prochaine, c'est madame Lefèvre. »

Le déroulé est déjà dans `anim/ep03/episode.json`. Il manque 3 voix (4 répliques nouvelles). Les anciennes répliques restent dans `*-court.mp3`.

1. Convertir les voix existantes : pour julien, vasseur, rocher, policier : `ffmpeg -i anim/ep03/<p>-court.mp3 -ar 24000 -ac 1 anim/ep03/<p>-court.wav`.
2. 3 prises (hub mode `voix`, une réplique par ligne, MÊMES voix et styles que `voix-*-gemini.txt`) :
   - vasseur (Algenib, mielleux, calme inquiétant) : « Madame m'a confié sa clé, pour les urgences. C'est dans son contrat. » → `anim/ep03/voix-vasseur2-gemini.txt`
   - rocher (Vindemiatrix, dame de 80 ans perdue, voix tremblante) : « Monsieur Morel, oui, je l'ai appelé. Mais lui… je ne sais pas comment il est entré. » puis « J'ai signé… ça ? » → `anim/ep03/voix-rocher2-gemini.txt`
   - policier (Alnilam, ferme, sans émotion) : « Pas d'effraction, un contrat signé : c'est un litige, pas un délit. Madame, si vous contestez, venez porter plainte demain. Messieurs, tout le monde dehors. » → `anim/ep03/voix-policier2-gemini.txt`
3. Pour chacune : extraire le WAV, ajouter 0,4 s de silence puis la nouvelle prise À LA FIN de `<p>-court.wav`, et ajouter dans `segments.<p>` les [début, fin] des nouvelles répliques (dans le fichier allongé, silencedetect). Ordre des répliques = ordre de `textes.<p>` (vasseur n=5 ; rocher n=3 et 4 ; policier n=3).
4. `rm -rf anim/ep03/frames anim/ep03/st anim/ep03/parts`, `python3 anim/film.py ep03 --prep`, planche (`apercu_film.py`), puis `python3 anim/film.py ep03` (≈ 20 min). Vérifier la carte « contrat » (lisible) et la fin face à face. < 8 Mo (réencoder crf 25 si besoin), cover.png (image du contrat ou de la fin), mp3 des voix, commit + push.
5. Hub `ajouter` : video_file=anim/ep03/film.mp4, cover_file=anim/ep03/cover.png, scheduled_at=2026-10-25T16:00:00Z, hook « Sous pression · Épisode 3 — Le piège », caption = « Le piège\nÉpisode 3 · Sous pression\n\nLa police arrive enfin… mais Vasseur a un papier signé.\nHistoire et personnages fictifs. Épisode 4 demain à 18 h.\n\n#plombier #seriesuspense #animation », pinned_comment = « Ce contrat, vous l'auriez signé ? », sources_file=anim/BIBLE-sous-pression.md.
6. Supprimer ce fichier.
