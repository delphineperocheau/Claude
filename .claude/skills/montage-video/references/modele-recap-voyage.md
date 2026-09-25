# Modèle : récap de voyage (WeRoad Far West 360°)

Projet : `montage/weroad-far-west/recap/`. Source : album Google Photos partagé (300 médias, HEIC + Motion Photos).

## Méthode
1. `photos_download.py` (album complet, pagination), puis tri chronologique par l'horodatage de `manifest.json`.
2. Planches de 40 vignettes numérotées ; présélection ; planches grand format des candidats.
3. Sélection : paysages forts, moments de groupe, selfies souriants, une ou deux scènes drôles. Écarter plats, boutiques, flous, panneaux.
4. `scripts/shots.py` : liste `(index, durée, étiquette de lieu ou None)`. Durées multiples de 0,5 s (musique 120 BPM). Environ 1,5 à 2,5 s par plan.
5. `scripts/prep_media.py` : vidéos recadrées 1080x1920 muettes, photos redimensionnées (paysage : hauteur 2000 pour un panoramique horizontal).
6. `scripts/music.py <durée>` : musique pop synthétisée.
7. `scripts/build_index.py` : plans en coupe franche, zoom lent alterné (photos portrait, vidéos), panoramique gauche/droite (photos paysage), étiquette de lieu en pastille, balayage couleur de marque à chaque changement de lieu, logo en filigrane, intro titre + dates, écran de fin logo + titre + dates + mot de fin.

## Charte WeRoad
Corail `#FF4758`, encre `#171717`, crème `#FFF9EB`. Logo SVG extrait du site weroad.fr (« We » corail, « Road » `#4D4D4D`, passé en blanc sur image). Police : Montserrat 900.

## Trouver un moment précis dans une longue vidéo (ex. la baleine)
Un sujet lointain est invisible sur les vignettes. Recadrer une zone de la vidéo à pleine résolution sur plusieurs instants (`crop=640:300:x:y`) et les assembler en grille. Dans le plan final, zoomer dessus avec l'option `crop` de `shots.py` (ex. `480:853:x:y`, recadrage 9:16 agrandi).

## Variante « tous les médias sur une musique fournie » (`montage/weroad-far-west-2/recap/`)
- Durée = durée du MP3. Tempo et phase mesurés (autocorrélation de l'enveloppe d'énergie, puis recherche fine BPM/phase) : 129 BPM pour « Burgers ».
- `scripts/plan.py` : chaque plan dure un nombre entier de temps (photos 4, vidéos selon longueur et poids `w`), ajusté pour tomber pile sur l'écran de fin. Les coupes tombent sur les temps.
- Vidéos paysage : fond flouté + image entière (dans `prep_media.py`). Capture d'écran de story : option `crop` pour retirer l'interface.
- Fichiers Drive numérotés (000001…) : vérifier l'ordre avec l'EXIF, les vidéos exportées ont une date d'export, pas de prise de vue.
- Un MP3 fourni n'est pas versionné (droits, poids).
