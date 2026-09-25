#!/bin/bash
# Version légère pour envoi / réseaux sociaux (H.264, -14 LUFS). Usage : share_version.sh <rendu.mp4> <sortie.mp4>
ffmpeg -loglevel error -y -i "$1" -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart \
  -af "loudnorm=I=-14:TP=-1:LRA=11" -c:a aac -b:a 192k -ar 48000 "$2" && ls -la "$2"
