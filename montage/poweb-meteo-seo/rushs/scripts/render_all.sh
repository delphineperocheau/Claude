#!/bin/bash
# Construit, vérifie et rend chaque rush, puis crée une version légère à envoyer.
# Usage : scripts/render_all.sh [id ...]   (depuis rushs/ ; sans argument : tous)
set -e
ids="$*"
[ -z "$ids" ] && ids=$(python3 -c "import sys;sys.path.insert(0,'scripts');from rushes import RUSHES;print(' '.join(RUSHES))")
mkdir -p renders ../livrables
for id in $ids; do
  python3 scripts/build_index.py "$id" > /dev/null || { echo "BUILD KO $id"; continue; }
  npx hyperframes check 2>&1 | grep -q "Check passed" || { echo "CHECK KO $id"; continue; }
  npx hyperframes render --output "renders/$id.mp4" > /dev/null 2>&1 || { echo "RENDU KO $id"; continue; }
  ffmpeg -loglevel error -y -i "renders/$id.mp4" -c:v libx264 -preset slow -b:v 3500k -maxrate 4000k -bufsize 8000k \
    -c:a aac -b:a 160k -af loudnorm=I=-14:TP=-1 -movflags +faststart "../livrables/poweb-meteo-seo-$id.mp4"
  echo "rendu $id"
done
