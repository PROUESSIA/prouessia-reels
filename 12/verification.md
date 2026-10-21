# Reel 12 · Urgence de nuit (style E, mini-scène) · vérification du 21/10/2026

Accroche n° 5 de `faits/accroches-50.json` (statut V, source S1), adaptée en « 22 h, une fuite. Avant la caisse à outils : le devis. » Style E (rotation après A 18/10, B 19/10, C 20/10, D 21/10). Ton de voix : voix naturelle ElevenLabs (moins de 5 Reels mesurés, pas de test de ton). Sujet non publié dans `etat.json`.
Formule « vraies vidéos » (`essai/build.py`) : clips Pixabay déjà dans `videos/clips` (CDN Pixabay bloqué depuis la tâche), voix ElevenLabs « Anthony Sirius - Naturel et direct » (règle 8 : jamais la voix Gemini).

| Phrase dite | Fait | Source (fiche `faits/r01.json`, vérifiée le 12/10/2026) |
|---|---|---|
| Vingt-deux heures, une fuite chez un client | Mise en scène (étiquetée dans la fiche) | — |
| Chez un particulier, obligatoire dès le premier euro | Arrêté du 24/01/2017, art. 4 (aucun seuil) ; DGCCRF « dès le 1er euro » ; INC | Légifrance + economie.gouv.fr + inc-conso.fr |
| Remis avant l'intervention | Arrêté du 24/01/2017, art. 4 : remis avant l'exécution de la prestation | idem |
| Prouessia le relance tout seul, par e-mail | Fonction citable | AUTOMATION.md, règle 2 |
| « Écrivez DEVIS » (légende) | Automatisation Zernio active | AUTOMATION.md, mots-clés |

Aucun montant d'amende, aucun chiffre hors fiche, pas de « n°1 ». Pas de nouvelle lecture des pages officielles ce matin (WebFetch refusé en tâche automatique les jours précédents) : on s'appuie sur r01 vérifiée le 12/10.

## Contrôles vidéo
- Voix : une seule prise de 14,4 s ; transcription (caler.py) : les 6 phrases présentes, rien de lu en trop.
- Mouvement dès 0 s (panoramique sur vraie vidéo) ; différences entre images 0,1/0,5/1/2/3/4 s : 9,2 · 8,5 · 12,6 · 76,1 · 48,9 (seuil 2,0) → OK. Plans de 1,4 à 3,1 s, tous en mouvement.
- Écran plein 1080×1920 (vidéo plein cadre, aucune bande vide) ; texte entre 280 et 1 100 px, hors zones boutons.
- Accroche complète (appel client + « Avant la caisse à outils : le devis ») lisible dès l'image 0. Fin sur une question + « Dites-le en commentaire ».
- video.mp4 : 1080×1920, 16,2 s, 5,2 Mo. cover.png : image à 4,3 s. sources.pdf : 1 page, débordement 0.

## Mesures de voix (analyse_voix.py, 52 mots)
débit 4,28 mots/s · hauteur 176 Hz · variation 5,16 demi-tons · étendue 16,8 · dynamique 22,2 dB · attaque 0,2 dB · 6 pauses (0,18 s)
