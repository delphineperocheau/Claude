#!/bin/bash
# Planche contact : 4 vignettes par vidéo, une ligne par vidéo. Usage : contact_sheet.sh <dossier_videos> <sortie.jpg>
IN="$1"; OUT="$2"; T=$(mktemp -d)
for f in "$IN"/*.mp4 "$IN"/*.MP4 "$IN"/*.mov "$IN"/*.MOV; do
  [ -f "$f" ] || continue
  b=$(basename "${f%.*}"); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  ffmpeg -loglevel error -y -i "$f" -vf "fps=4/$d,scale=-2:240,drawtext=text='$b':fontcolor=yellow:fontsize=14:x=4:y=4,tile=4x1" -frames:v 1 "$T/$b.jpg"
done
ffmpeg -loglevel error -y -pattern_type glob -i "$T/*.jpg" -vf "scale=720:-2,tile=1x12" -frames:v 1 "$OUT"
rm -rf "$T"; echo "$OUT"
