#!/bin/bash
# Prépare l'environnement HyperFrames (sessions Claude Code web)
set -e
if ! command -v ffmpeg >/dev/null; then
  (apt-get install -y ffmpeg || (apt-get update && apt-get install -y ffmpeg)) >/dev/null 2>&1
fi
npx -y hyperframes browser ensure >/dev/null 2>&1 || true
