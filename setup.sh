#!/usr/bin/env bash
# Prépare une session vierge : modèle de transcription (calage voix/image) + dépendances Python.
set -e
pip install --break-system-packages -q numpy scipy soundfile sherpa-onnx playwright >/dev/null 2>&1 || true
ASR="$HOME/asr/sherpa-onnx-whisper-small"
if [ ! -f "$ASR/small-encoder.int8.onnx" ]; then
  mkdir -p "$HOME/asr" && cd "$HOME/asr"
  curl -sL -o w.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2
  tar xjf w.tar.bz2 && rm w.tar.bz2
fi
echo "setup ok"
