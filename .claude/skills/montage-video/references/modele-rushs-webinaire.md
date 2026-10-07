# Modèle : rushs courts tirés d'un webinaire (`montage/poweb-meteo-seo/rushs/`)

Cas d'origine : « La météo du SEO » (mars 2025), live Restream de 1 h 09 avec Camille Dufossez (École du SEO) et Delphine. 13 rushs verticaux de 25 à 60 s aux couleurs de poweb.

## Repérer les plages utilisables

- Planche contact à une image par minute (`fps=1/60,tile=6x12`) pour voir les mises en page.
- Restream alterne « diapo plein écran + vignettes minuscules » et « caméras en grand + diapo ». Seules les plages caméras donnent de bons rushs. Les détecter en lisant un pixel caractéristique (la barre bleue de l'étiquette de nom, `crop=8:30:0:325`, b > 150 et r < 120) toutes les 2 s.
- Transcrire uniquement ces plages : whisper `small` sur 4 cœurs ≈ 0,5× temps réel ; `medium` est trop lent pour 1 h.

## Qui parle ?

Pas de diarisation dans whisper. Méthode qui marche : différence d'image moyenne sur la zone visage de chaque webcam (fenêtres de 0,5 s, moyenne glissante 2 s, hystérésis ×1,35, plans de 1,5 s minimum).
Piège : la personne qui écoute bouge aussi (s'étire, hoche la tête). Vérifier les passages douteux avec des bandes de 6 images (`fps=5,tile=6x1`) des deux webcams et imposer les plans dans `rushes.py` (`"speakers": [(0.0, "delphine")]`).

## Coupes et sous-titres

- Choisir les extraits sur la transcription par segments, caler début et fin sur `silencedetect` (`n=-35dB:d=0.25`).
- `prep_rush.py` retranscrit chaque rush seul avec `--dtw small` et un `--prompt` (noms propres, jargon) : horodatages au mot fiables, contrairement à la passe longue (horodatages regroupés toutes les 2 s).
- Après la passe DTW, relire début et fin : un mot coupé ou une phrase tronquée se corrige en décalant la plage (le premier ou le dernier mot dit tout).
- Corrections de transcription par suite de mots exacte (ponctuation comprise) dans `"fix"` ; le script s'arrête si une correction ne trouve rien. Une nouvelle passe DTW peut changer les mots : revérifier les corrections après chaque re-préparation.
- Retirer une digression : plusieurs plages dans `"ranges"`, concaténées.

## Mise en page (charte poweb, direction visuelle du 07/10/2026)

- Fond quasi-noir #14110E, corail #E97458, blanc. Police Cabinet Grotesk (Fontshare : `api.fontshare.com/v2/css?f[]=cabinet-grotesk@800,700,500`, fichiers woff2 copiés dans `assets/`).
- Étiquettes collées de travers : petite « la météo du SEO ☀️ » blanche, question du rush en corail (texte noir), nom de la personne en noir à la première prise de parole.
- Locutrice active en grand (1080 de large), l'autre dans un polaroïd incliné en haut à droite. Recadrer les webcams sans les étiquettes de nom Restream.
- Sous-titres : étiquettes blanches, 4 mots max, légèrement inclinées, en bas de l'image vidéo.
- Pied « poweb  poweb85.fr » en minuscules, au-dessus des 250 px du bas. Écran de fin corail de 3,4 s.
- Lint : une `<video>` minutée ne doit pas être dans un conteneur minuté (polaroïd = div non minutée) ; deux vidéos avec la même source, le même début et la même durée sont refusées (fichier `-pola.mp4` réduit pour la vignette).

## Production

`scripts/render_all.sh [id…]` : construit `index.html`, `check`, rendu, puis version légère (3,5 Mb/s, -14 LUFS) dans `livrables/`. Un seul `index.html` pour tous les rushs : ne jamais lancer `build_index.py` pendant un rendu (utiliser `DRY=1` pour relire les sous-titres).
Temps : préparation ≈ 5 min par rush (dont whisper), rendu ≈ 6 min pour 50 s.
