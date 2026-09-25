#!/bin/bash
# Transcrit en français (whisper.cpp medium) chaque vidéo d'un dossier.
# Sortie : <work>/<nom>.json (tokens horodatés) + <nom>.srt
# Usage : transcribe.sh <dossier_videos> <dossier_travail>
set -e
IN="$1"; WORK="$2"; mkdir -p "$WORK"
WDIR=/root/.cache/hyperframes/whisper
BIN=$WDIR/whisper.cpp/build/bin/whisper-cli
MODEL=$WDIR/models/ggml-medium.bin
# 1er usage : hyperframes installe whisper.cpp + le modèle
if [ ! -x "$BIN" ] || [ ! -f "$MODEL" ]; then
  ffmpeg -loglevel error -y -f lavfi -i "sine=duration=2" "$WORK/_t.wav"
  npx -y hyperframes transcribe "$WORK/_t.wav" --model medium --language fr --dir "$WORK" >/dev/null 2>&1 || true
fi
# Le binaire compilé en -march=native plante si le conteneur change de machine : recompilation portable
ffmpeg -loglevel error -y -f lavfi -i "sine=duration=1" -ar 16000 -ac 1 "$WORK/_t.wav"
if ! "$BIN" -m "$MODEL" -l fr -t 1 "$WORK/_t.wav" >/dev/null 2>&1; then
  echo "Recompilation portable de whisper.cpp…"
  (cd $WDIR/whisper.cpp && rm -rf build && cmake -B build -DGGML_NATIVE=OFF -DGGML_AVX2=ON -DGGML_FMA=ON -DGGML_F16C=ON -DWHISPER_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release >/dev/null && cmake --build build -j"$(nproc)" --config Release >/dev/null)
fi
rm -f "$WORK/_t.wav"
for f in "$IN"/*.mp4 "$IN"/*.mov "$IN"/*.MOV "$IN"/*.MP4; do
  [ -f "$f" ] || continue
  b=$(basename "${f%.*}")
  ffmpeg -loglevel error -y -i "$f" -ac 1 -ar 16000 "$WORK/$b.wav"
  "$BIN" -m "$MODEL" -l fr -t "$(nproc)" -bs 2 -bo 2 -ojf -osrt -of "$WORK/$b" "$WORK/$b.wav" >/dev/null 2>&1
  echo "$b ok"
done
