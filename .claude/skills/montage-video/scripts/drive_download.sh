#!/bin/bash
# Télécharge des fichiers Drive partagés « tous les utilisateurs disposant du lien ».
# Usage : drive_download.sh <dossier_sortie> < liste   (lignes : "<fileId> <nom_fichier>")
set -e
OUT="$1"; mkdir -p "$OUT"
while read -r id name; do
  [ -z "$id" ] && continue
  curl -sSL -o "$OUT/$name" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t" &
done
wait
bad=0
for f in "$OUT"/*; do
  if file "$f" | grep -q "HTML document"; then echo "PRIVÉ : $f (le dossier n'est pas partagé par lien)"; rm -f "$f"; bad=1; fi
done
exit $bad
