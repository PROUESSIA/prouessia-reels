# Captures de l’app Prouessia pour les Reels

Chaque capture = une image `NN-nom.png` (1170×2532 : fenêtre 390×844, zoom ×3) + une vidéo `NN-nom.mp4` (5 à 12 s, sans son, l’action se passe en direct). Le dossier `extras/` contient d’autres moments des mêmes scènes (images seules).

## Comment elles ont été faites (à lire)

- Les vraies pages de l’app tournent sur un serveur local, branché sur une copie de la base remplie **uniquement de données fictives** (Plomberie Démo, M. Martin, Mme Bernard, M. Petit… adresses et numéros inventés, SIRET de démo). Aucune donnée réelle, aucun accès à votre vraie base.
- Les e-mails (devis, relance, notification, demande) sont les vrais e-mails générés par l’app, affichés dans une page de lecture neutre (sans barre de notifications ni onglets).
- Les PDF sont les vrais PDF générés par l’app.
- La dictée vocale (15) utilise une voix simulée (texte écrit à l’avance).
- La vidéo est accélérée de façon légère quand le serveur de test est lent ; les saisies restent lisibles.
- Aucun écran ne montre de barre de notifications, d’onglet de navigateur ou d’adresse interne.

## Liste des 30 écrans

| Fichier | Idées de Reels | Ce que ça montre | Durée |
|---|---|---|---|
| 01-nouveau-devis | 1, 3, 4, 6, 7 | Un devis qui se remplit en direct : choix du client, titre, trois prestations ajoutées au toucher, total TTC calculé. | 12.0 s |
| 02-prestations | 3, 79 | Liste « Mes prestations » (prix prêts à l’emploi) : filtres Tout/Prestations/Fournitures, recherche « chauffe ». | 6.3 s |
| 03-client-prerempli | 7 | Le client choisi dans la liste, le devis enregistré en brouillon. ATTENTION : le formulaire de devis ne pré-remplit pas une fiche détaillée du client ; seul le choix du client existe (la fiche client est en 21). | 11.5 s |
| 04-apercu-devis | 5, 51, 52, 53, 58, 59 | Aperçu du devis côté plombier puis côté client : logo et couleur du plombier, lignes, totaux, PDF. Les couleurs du PDF sont fixes (pas de couleur choisie par le plombier sur le PDF). | 11.5 s |
| 05-envoyer-devis | 8 | Bouton « Envoyer au client », envoi, confirmation « Envoyé ». | 11.5 s |
| 06-mail-puis-devis | 9, 54, 83 | L’e-mail reçu par le client (vrai e-mail généré par l’app), clic sur le lien, saisie du code à 4 chiffres, ouverture du devis. | 11.5 s |
| 07-signature-doigt | 21, 26 | Le client accepte, tape son nom, signe au doigt, « Accepter et signer », devis accepté. | 11.5 s |
| 08-pdf-signe | 23, 25, 90 | PDF signé : signature sur le devis puis page « Preuve de signature électronique » (signataire, date/heure, adresse IP). L’app n’affiche pas le modèle d’appareil : ne pas le dire. | 7.7 s |
| 09-notification-signature | 24 | E-mail « devis accepté et signé » reçu par le plombier. Il n’existe pas de notification dans l’app (pas de push) : la notification est un e-mail. | 9.1 s |
| 10-contrat-signe | 28 | Contrat signé en ligne : formulaire, signature, confirmation. (Contrat Prouessia, SIRET fictif de démo.) | 11.5 s |
| 11-liste-devis | 10, 27, 37 | Liste des devis : taux de signature, recherche, filtres par statut (Envoyés, Acceptés, Refusés). | 11.5 s |
| 12-devis-sans-reponse | 32, 34, 35 | Page Relances : devis sans réponse, rappels envoyés/prévus. Le montant en attente se voit sur l’accueil (13). | 6.0 s |
| 13-tableau-de-bord | 36, 38 | Accueil : montant signé du mois, devis en attente, à faire aujourd’hui, défilement. | 5.9 s |
| 14-relance-auto | 31, 33, 39, 40 | Réglage « Relance automatique » (activée/désactivée) puis e-mail de relance reçu par le client. | 11.5 s |
| 15-dictee-vocale | 41, 42, 43, 88 | Micro dans les notes du devis : le texte dicté s’écrit tout seul. ATTENTION : la dictée utilise le moteur du navigateur ; pour l’enregistrement j’ai simulé la voix (texte prédéfini) car aucun micro n’existe ici. À refaire sur un vrai téléphone si vous voulez la voix réelle. | 11.5 s |
| 16-sans-reseau | 44, 45 | Bandeau « Pas de réseau » : on continue de préparer un devis, puis retour du réseau et enregistrement. ATTENTION (voir note en fin de fichier) : la promesse « devis créé tout seul au retour du réseau » ne fonctionne pas comme annoncé, donc la vidéo ne la montre pas. | 11.6 s |
| 17-brouillon-retrouve | 46 | Quitter l’écran du devis puis revenir : « Brouillon retrouvé ». | 11.5 s |
| 19-gros-boutons-erreur | 48, 49 | Gros boutons faciles à toucher, message d’erreur clair (« Choisissez un client. »). | 8.2 s |
| 20-interventions | 50, 76 | Interventions : liste avec statuts, fiche avec notes internes. ATTENTION : cette page n’est pas dans le menu de l’app (accessible par adresse seulement). L’historique par client = les devis liés dans la fiche client (21). | 11.5 s |
| 21-fiches-clients | 71, 72, 75, 77, 80 | Liste des clients, recherche à 2 lettres, fiche de M. Martin avec la note « Code portail 1234, chien gentil. » et ses devis. | 11.5 s |
| 22-nouvelle-demande | 73, 74, 78 | Un visiteur envoie une demande depuis le site vitrine, le plombier reçoit l’e-mail de notification, puis la demande dans « Demandes » (pastille sur l’onglet). Mail montré dans le format téléphone, pas en fenêtre d’ordinateur. | 11.5 s |
| 23-site-vitrine-mobile | 11 à 20, 56, 60 | Site vitrine de démonstration sur téléphone, tout en orange (photo d’accueil : plombier au travail, sans marque visible). | 9.8 s |
| 23-site-vitrine-ordi | 11 à 20, 56, 60 | Même site sur ordinateur (vidéo 1920×1080, image 1920×1080 : seul format non vertical). | 9.2 s |
| 24-logo-couleurs | 12, 51, 52 | « Créer mon logo » : choix du modèle, du symbole et de la couleur, aperçu en direct. | 11.5 s |
| 25-tarif | 61, 63, 64, 65, 66, 70 | Page tarif : 39 € TTC/mois, mise en place, paiement par virement programmé, remboursé 3 mois. | 6.7 s |
| 26-connexion | 85 | Mauvais mot de passe (erreur claire) puis connexion réussie. | 11.5 s |
| 26-mot-de-passe-oublie | 86 | Mot de passe oublié : saisie de l’e-mail, message « Vérifiez votre email ». | 11.5 s |
| 26-deconnexion | 87 | Mon compte puis « Se déconnecter », retour à la connexion. | 6.7 s |
| 27-mentions-legales | 89 | Mentions légales du site du plombier (fictives). Les pages légales de Prouessia ne sont PAS capturées : elles montrent votre identité et adresse réelles. | 7.3 s |
| 28-support | 92, 97 | Signaler un problème, message envoyé, réponse de l’équipe (réponse écrite pour la démo ; heure affichée = heure de la machine). | 11.6 s |
| 29-formulaire-contact | 94, 99 | Formulaire « Être recontacté » du site Prouessia rempli puis « C’est noté ! ». | 11.5 s |
| 18 | 47 | **N’existe pas dans l’app.** « Ajouter à l’écran d’accueil » se fait depuis le menu du navigateur du téléphone (l’app est installable, mais elle n’affiche aucune aide pour le faire). Pas de capture possible sans téléphone réel. | – |
| 30 | 95 | **N’existe pas.** Aucune démo de 90 s n’existe : les vidéos du dépôt font 26 s (relance), 49 s (présentation) et 5 courtes étapes. | – |

## À savoir avant de publier

1. **Sans réseau (16)** : quand le réseau est coupé, le bouton « Enregistrer » reste en attente (« On enregistre votre devis… ») au lieu de garder le devis sur le téléphone ; il se crée seulement au retour du réseau, et la file « créé tout seul » du code ne se déclenche pas. Le brouillon, lui, est bien conservé (17). Ne dites pas « le devis se crée tout seul sans réseau » tant que ce n’est pas corrigé.
2. **Compte de démo** : artisan installé depuis plus d’un an, 48 clients, 51 devis dont 46 signés (≈ 62 000 € TTC sur l’année), 42 demandes reçues, 25 interventions ; site et logo orange. Les chiffres sont inventés pour la démonstration : ne les présentez jamais comme ceux d’un vrai client.
3. **Pas de pré-remplissage détaillé du client** dans le devis (03) ; **pas de ligne « appareil »** sur la preuve de signature (08) ; **pas de notification dans l’app** (09, 22) : ce sont des e-mails.
4. **Interventions (20)** n’est pas dans le menu de l’app.
5. Les pages légales de Prouessia (mentions, confidentialité) affichent votre identité réelle : non capturées.
6. Dans l’espace de démonstration, les statuts d’interventions viennent d’une base reconstituée ; vérifiez sur votre vraie base que la page Interventions affiche bien « Terminée » / « Planifiée ».
