# Reel 14 · Idée n° 1 « Un devis en 2 minutes » · vérification du 22/10/2026

Sujet : 1re idée non faite de `idees/100-idees.json` (document « 100 idées de reels Prouessia », 22/10). Formule « vécu » (`moteur/vecu.py`), 13 phrases, 21,5 s. Prévu le 23/10/2026 à 9 h (Paris).

| Phrase dite | Nature | Source |
|---|---|---|
| Un devis en deux minutes, pas en deux heures (titre + 0 s) | Accroche de l'idée n° 1, mot pour mot | `idees/100-idees-reels.pdf` |
| Le client vous appelle… il a appelé un autre / c'est là qu'il vous choisit | Mise en situation (étiquetée dans la fiche) | — |
| Avec Prouessia, un devis en deux minutes. Depuis la camionnette, avant de repartir. | Avantage n° 1 (« Un devis en 2 minutes » ; images : plombier dans sa camionnette, téléphone en main) | `idees/100-idees.json` |
| Pas deux heures le soir | Reprise de l'accroche | idem |

Aucun chiffre officiel, aucune règle légale, aucun montant d'amende, pas de « n°1 ». Rien de la liste interdite (SMS, avant/après, avis, facturation électronique, stores, « prêt en 48 h »).

## Contrôles vidéo
- Voix Google AI Studio « Charon », style `STYLE` de `moteur/vecu.py`, une prise (25,6 s brute). Pas d'outil de transcription disponible (modèles bloqués par le proxy) : contrôle par découpage aux silences, 20 morceaux de parole répartis sur les 13 phrases dans l'ordre, durées cohérentes avec le texte ; pauses ramenées à 0,2 s entre phrases, 0,12 s dans une phrase. Débit ≈ 4,4 mots/s.
- Aucune musique : piste audio = voix seule.
- Mouvement : différences 0,1/0,5/1/2/3/4 s = 18,9 · 20,9 · 51,5 · 35,7 · 69,5 (seuil 2,0) → OK.
- 13 clips différents, aucun clip retiré ni déjà utilisé dans les 10 dernières vidéos (`videos/clips/utilises.json`), tous Pixabay (crédits dans `sources.json`).
- Écran plein 1080×1920, titre fixe en haut, phrase au centre, rien sous 1 670 px. cover.png = image à 1 s. sources.pdf : 1 page, débordement 0.

## Mesures de voix (analyse_voix.py)
Voir `voix-mesures.json` : hauteur 115 Hz · variation 5,26 demi-tons · 19 pauses (0,24 s).
