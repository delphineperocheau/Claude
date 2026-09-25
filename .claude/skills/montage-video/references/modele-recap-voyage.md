# Modèle : récap de voyage (WeRoad Far West 360°)

Projet : `montage/weroad-far-west/recap/`. Source : album Google Photos partagé (300 médias, HEIC + Motion Photos).

## Méthode
1. `photos_download.py`, puis inventaire daté et tri chronologique (photos EXIF en heure locale, +7 h pour la côte ouest US l'été ; vidéos en UTC).
2. Planches de 40 vignettes numérotées ; présélection ; planches grand format des candidats.
3. Sélection : paysages forts, moments de groupe, selfies souriants, une ou deux scènes drôles. Écarter plats, boutiques, flous, panneaux.
4. `scripts/shots.py` : liste `(index, durée, étiquette de lieu ou None)`. Durées multiples de 0,5 s (musique 120 BPM). Environ 1,5 à 2,5 s par plan.
5. `scripts/prep_media.py` : vidéos recadrées 1080x1920 muettes, photos redimensionnées (paysage : hauteur 2000 pour un panoramique horizontal).
6. `scripts/music.py <durée>` : musique pop synthétisée.
7. `scripts/build_index.py` : plans en coupe franche, zoom lent alterné (photos portrait, vidéos), panoramique gauche/droite (photos paysage), étiquette de lieu en pastille, balayage couleur de marque à chaque changement de lieu, logo en filigrane, intro titre + dates, écran de fin logo + titre + dates + mot de fin.

## Charte WeRoad
Corail `#FF4758`, encre `#171717`, crème `#FFF9EB`. Logo SVG extrait du site weroad.fr (« We » corail, « Road » `#4D4D4D`, passé en blanc sur image). Police : Montserrat 900.
