# Modèle « teaser télé-réalité » (montage/maroc/teaser)

Fichiers : `scripts/prepare_clips.py` (ancienne version à segments en dur), `scripts/build_index.py`.

Structure (≈ 75 s, 9:16) :
1. Accroche : 4 plans d'ambiance de 2 s avec textes League Gothic (« Ils pensaient partir en vacances… »).
2. Titre : gros mot jaune + bandeau rouge, impact grave, riser avant, léger tremblement.
3. Répliques rapides (2 à 5 s chacune) : sous-titre Montserrat 900 en capitales, contour noir, mots clés en jaune, flash blanc à chaque coupe, léger zoom avant, étiquette « CONFESSION » avec point rouge clignotant.
4. Respiration : 2 plans d'ambiance.
5. Montée dramatique : musique presque coupée, whoosh + impact.
6. Chute : deux personnes disent la même chose, puis écran de fin « QUI CACHE QUOI ? » et titre + « À SUIVRE… ».

Couleurs : noir, jaune #FFD60A, rouge #E10600. Étalonnage des confessionnaux sombres : `eq=brightness=0.05:contrast=1.15:saturation=1.1:gamma=1.08`.
Structure de données : liste `SEQ` de (id clip, type hook|title|conf|break, sous-titre, mots surlignés, texte superposé).
