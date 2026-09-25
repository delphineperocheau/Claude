# Modèle « Reel de marque » (montage/carole-roig/reel)

Fichier : `scripts/build_index.py` (sous-titres générés automatiquement depuis le JSON whisper).

Structure (≈ 45 s, 9:16) :
1. Intro 3,4 s : photo métier plein cadre (effet Ken Burns), dégradé foncé, motif graphique tiré du logo, nom en Montserrat 900, métier sur bandeau couleur de marque, zone géographique.
2. Vidéo face caméra : logo sur pastille blanche en haut à gauche, sous-titres par blocs de 5 mots max (découpe par phrase), questions hors champ en couleur d'accent avec étiquette « Question de cliente », réponses en couleur foncée avec liseré accent.
3. Promesses : une scène de 2,1 s par promesse (photo + gros mot blanc + complément en couleur d'accent). Photo carrée ou petite : cadre à bordure accent sur fond foncé, pas d'agrandissement plein écran.
4. Fin : fond blanc, logo, trait accent, nom, métier, liste des services. Ajouter contact (téléphone, site, Instagram) s'il est fourni.

Paramètres en tête de script : `TR` (JSON whisper), `CUT_IN`/`VID_DUR` (coupe du début), `FIX` (corrections), `QUESTIONS` (plages hors champ), `OUT_SCENES` (promesses), couleurs dans `:root` (`--char`, `--orange`).
Le chemin `TR` pointe vers le brouillon de session : le remplacer par `work/tr/<nom>.json` dans un nouveau projet.
