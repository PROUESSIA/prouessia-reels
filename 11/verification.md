# Reel 11 · Validité du devis de dépannage (style D, l'oubli) · vérification du 20/10/2026

Accroche n° 4 de `faits/accroches-50.json` (statut V, source S1). Style D (rotation après A le 18/10, B le 19/10, C le 20/10). Ton de voix : promo (défaut ; moins de 5 Reels mesurés, pas de test de ton). Sujet non publié dans `etat.json`.

| Phrase dite | Fait | Source (fiche `faits/r01.json`, vérifiée le 12/10/2026) |
|---|---|---|
| Devis écrit obligatoire dès le premier euro chez un particulier | Arrêté du 24/01/2017, art. 4 (aucun seuil) ; DGCCRF « dès le 1er euro » | Légifrance + economie.gouv.fr (DGCCRF) |
| Mentions : date, client, lieu, réparations, prix, déplacement, durée de validité de l'offre | Arrêté du 24/01/2017, art. 4-I, liste reprise par la DGCCRF | idem |
| « Offre valable un mois » | Notre conseil (étiqueté), un mois = simple exemple | — |
| Prouessia relance tout seul par e-mail les devis sans réponse | Fonction citable | AUTOMATION.md, règle 2 |
| « Écrivez DEVIS en commentaire » | Automatisation Zernio active (mot-clé DEVIS → fiche à imprimer) | AUTOMATION.md, section mots-clés |

Aucun montant d'amende, aucun chiffre hors fiche, pas de « n°1 » ni « le meilleur ». Nuance art. 4-I / 4-II (signature chez le client) reprise dans « ce que la vidéo ne couvre pas » de la fiche sources.
Note : nouvelle lecture de la page DGCCRF tentée ce matin avec WebFetch, refusée (autorisation non accordée en tâche automatique) ; on s'appuie sur la fiche r01 vérifiée le 12/10.

## Contrôles vidéo
- Voix Gemini, une seule prise (39,8 s), 9 phrases présentes à la transcription (caler.py), rien de lu en trop.
- `debut=0.0` ; accroche complète (tag, titre, devis avec la ligne « Durée de validité ? ») lisible dès l'image 0 ; mouvement à 1,0 s (loupe) puis 1,3 s (cercle rouge).
- Élément animé (`w`/`drift`) dans chaque scène ; fond crème, logo en haut à gauche, signature en fin ; rien sous 1 500 px ; pas de sous-titres.
- video.mp4 : 1080×1920, 40,0 s, 2,0 Mo. cover.png : image à 5,2 s (juste après l'accroche). sources.pdf : 1 page, débordement 0.

## Mesures de voix (analyse_voix.py, 101 mots)
débit 3,96 mots/s · hauteur 132 Hz · variation 4,78 demi-tons · étendue 14,7 · dynamique 19,2 dB · attaque 7,0 dB · 26 pauses (0,48 s en moyenne)
