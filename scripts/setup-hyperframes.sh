#!/bin/bash
# Prépare l'environnement HyperFrames (sessions Claude Code web)
set -e
if ! command -v ffmpeg >/dev/null; then
  (apt-get install -y ffmpeg || (apt-get update && apt-get install -y ffmpeg)) >/dev/null 2>&1
fi
npx -y hyperframes browser ensure >/dev/null 2>&1 || true
# CLI HeyGen (bibliothèque musicale, voix, images). Auth : variable HEYGEN_API_KEY
if ! command -v heygen >/dev/null && [ ! -x "$HOME/.local/bin/heygen" ]; then
  curl -fsSL https://static.heygen.ai/cli/install.sh | bash >/dev/null 2>&1 || true
fi
if [ -n "$CLAUDE_ENV_FILE" ]; then echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$CLAUDE_ENV_FILE"; fi
