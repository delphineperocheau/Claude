---
name: montage-video
description: Monter une vidéo (Reel, teaser, promo) à partir de rushes et d'images fournis par Delphine via un dossier Google Drive, un album Google Photos partagé ou des fichiers déposés dans le dépôt, avec HyperFrames. Transcription, choix des phrases, découpe, sous-titres, charte couleur, musique, rendu MP4 vertical. À déclencher dès qu'elle demande une vidéo, un montage, un reel, un teaser ou « une nouvelle vidéo pour <client> ».
---

# Montage vidéo (méthode Delphine / HyperFrames)

Méthode éprouvée sur deux projets du dépôt :
- `montage/maroc/teaser/` : teaser façon télé-réalité, 17 rushes, phrases choc, confessionnal.
- `montage/carole-roig/reel/` : Reel de marque pour une cliente (opticienne), 1 vidéo + 3 photos + logo, charte couleur.

Chaque projet a un `scripts/build_index.py` qui génère la composition : **partir du modèle le plus proche et l'adapter**, ne pas réécrire de zéro. Troisième modèle : `montage/weroad-far-west/recap/` (récap de voyage : photos et vidéos d'un album, ordre chronologique, étiquettes de lieu, charte de marque). Détails dans `references/modele-teaser.md`, `references/modele-reel-marque.md` et `references/modele-recap-voyage.md`.

Charger aussi `/hyperframes` puis `/general-video` (règles de composition). Ne pas relancer leur entretien d'intention : le brief vient d'ici.

## 0. Préparer l'environnement

Le hook de session installe ffmpeg, le navigateur de rendu et la CLI HeyGen (`scripts/setup-hyperframes.sh`). Vérifier : `npx hyperframes doctor` (Chrome et FFmpeg doivent être OK ; whisper est géré par `transcribe.sh`).

## 1. Récupérer les médias

Dossier projet : `montage/<client-ou-sujet>/` avec `rushes/` (ignoré par git, trop lourd).

| Source | Méthode |
| --- | --- |
| Dossier Google Drive | Connecteur Google Drive : `search_files` (titre du dossier, puis `parentId = '<id>'`) pour lister. Télécharger avec `scripts/drive_download.sh` (lignes `<id> <nom>`). Ne pas utiliser `download_file_content` pour les vidéos (base64 dans le contexte). |
| Album Google Photos partagé | `python3 scripts/photos_download.py <lien> rushes/` (récupère tout l'album : la page publique n'affiche que ~300 médias, la suite est paginée ; testé sur 704 médias ; `manifest.json` donne l'horodatage UTC de chaque média, à utiliser pour l'ordre chronologique). Les photos iPhone/Pixel arrivent en HEIC : `pip install pillow-heif` puis `pillow_heif.register_heif_opener()` pour les ouvrir. Les « vidéos » de 2-3 s sont des photos animées (Motion Photos), utiles comme plans vivants. |
| Fichiers dans le dépôt | Déjà là. |

Drive et Photos : les fichiers doivent être partagés « tous les utilisateurs disposant du lien ». Si `drive_download.sh` signale PRIVÉ, demander de partager le dossier (clic droit > Partager > Accès général > Tous les utilisateurs disposant du lien) et rappeler à la fin qu'elle peut le repasser en privé.

## 2. Analyser

1. `ffprobe` : durée, dimensions, rotation (les vidéos téléphone 1920x1080 avec rotation -90 sont verticales).
2. Planche contact : `scripts/contact_sheet.sh rushes/ work/planche.jpg`, puis la lire (Read) pour voir le contenu.
3. Transcription : `scripts/transcribe.sh rushes/ work/tr` en arrière-plan (≈ 2 min par minute de son), puis `python3 scripts/words.py work/tr`.
4. Couleurs de marque : échantillonner le logo avec PIL (couleurs les plus fréquentes des pixels opaques).

Beaucoup de médias (album de voyage) : inventaire trié par l'horodatage de `manifest.json` (plus fiable que l'EXIF), puis planches numérotées de 40 vignettes à lire une par une. Méthode détaillée dans `references/modele-recap-voyage.md`.

## 3. Brief (court)

Demander seulement ce qui manque, en une fois : format (défaut : vertical 9:16 « format réel »), durée, style, textes imposés (titre, accroches), son (voix d'origine + musique, défaut), couleurs. Consigner dans `montage/<projet>/BRIEF.md`.

## 4. Choisir et caler les coupes

- Garder les phrases qui portent le message (ou « phrases choc » pour un teaser). Couper les consignes de tournage (« vas-y », « je te filme »).
- Les horodatages whisper sont en retard de 0,5 à 1 s : caler début et fin sur les silences affichés par `words.py`.
- Corriger les noms propres et les mots mal transcrits dans les sous-titres, et **signaler chaque correction incertaine** dans le message final.

## 5. Préparer les clips

Écrire `segments.json` puis `python3 .claude/skills/montage-video/scripts/prepare_clips.py segments.json` depuis le dossier HyperFrames. Redressement, recadrage 1080x1920, étalonnage, son normalisé. Une vidéo paysage dans un format vertical est posée sur fond flouté, jamais recadrée. Le dossier `media/` est ignoré par git.

## 6. Composer

```bash
cd montage/<projet>
HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init <nom> --non-interactive --example=blank --skill=general-video --resolution=portrait
```
Copier le `build_index.py` du modèle le plus proche dans `<nom>/scripts/`, adapter séquence, textes, couleurs, puis `python3 scripts/build_index.py`.

Règles apprises (éviter les erreurs déjà rencontrées) :
- **GSAP en local** : `assets/gsap.min.js` (copier depuis un projet existant). Le CDN échoue dans le navigateur de rendu (certificat du proxy).
- Polices sûres (embarquées) : Montserrat, League Gothic, Oswald, Archivo Black.
- Pas d'animation de `letterSpacing` (erreur lint) ; utiliser scale/opacity/x/y.
- Élément animé plusieurs fois (flash) : `tl.set(...).to(...)`, pas plusieurs `fromTo`.
- Pas de `<br>` : des `<span style="display:block">`.
- Chaque `<audio>` a un `id` et une `data-duration` ; un effet sonore par piste (`data-track-index` unique).
- Musique : piste unique avec `data-automation` (volume haut sur les plans sans parole, ~0,12 à 0,22 sous la voix).
- Texte blanc sur orange ou jaune : contraste insuffisant, mettre le texte en foncé.
- Mots surlignés : `white-space: nowrap` (sinon « JEAN-PAUL » se coupe).
- Superpositions volontaires (écran de fin) : `data-layout-allow-overlap`.

## 7. Vérifier puis rendre

1. `npx hyperframes lint` puis `npx hyperframes check` (0 erreur ; les avertissements `nested_structure_needs_subcomposition` et `timeline_track_too_dense` sont acceptables).
2. `npx hyperframes snapshot --at <t1>,<t2>,...` aux moments clés, assembler en une bande (ffmpeg `tile`), la regarder. Une image noire pile sur une coupe est un artefact de capture, vérifier à ±0,3 s.
3. `npx hyperframes render --output renders/<nom>.mp4` en arrière-plan (≈ 4 à 5 s de calcul par seconde de vidéo).
4. `scripts/share_version.sh renders/<nom>.mp4 montage/<projet>/<Nom-lisible>.mp4` (plus léger, -14 LUFS pour les réseaux).
5. Contrôler : `ffprobe` (1080x1920, piste audio), puis envoyer avec SendUserFile (display render). Limite d'envoi 30 Mo : au-delà, réencoder en débit fixe (`-b:v 2800k -maxrate 3200k`, ~26 Mo pour 73 s).

## 8. Musique

Sans compte HeyGen (variable `HEYGEN_API_KEY`), `media-use resolve --type bgm` échoue. Alors, par ordre de préférence :
1. un morceau fourni par Delphine (libre de droits) ;
2. une musique pop entraînante 120 BPM : `python3 scripts/music_pop.py <durée> out.wav` (numpy, intro sans batterie 4 s, outro 4,5 s), ou une musique synthétisée avec ffmpeg `aevalsrc` (exemples dans `montage/maroc/teaser/assets/` : suspense ; `montage/carole-roig/reel/assets/` : douce).
Effets sonores intégrés : `/root/.claude/skills/media-use/audio/assets/sfx/` (whoosh, riser, impact-bass, glitch, pop, chime, sparkle).

## 9. Livrer

- Commit + push des scripts, de `index.html` et des assets légers (jamais les rushes, `media/`, `renders/`, ni les `.mp4`).
- Message final en français, style de Delphine : phrases courtes, pas de formules. Contenu : durée et format, déroulé en quelques lignes, points à valider (corrections de transcription incertaines, choix supposés, musique de remplacement), infos manquantes utiles (contact sur l'écran de fin), rappel de repasser le dossier en privé.
