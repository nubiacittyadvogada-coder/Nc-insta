#!/usr/bin/env bash
# Prepara o ambiente de edição (rodar no início de cada sessão nova).
set -e
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || { echo "ffmpeg ausente"; exit 1; }
python3 -c "import whisper" 2>/dev/null || pip install -q openai-whisper
python3 -c "import ai_edge_litert" 2>/dev/null || pip install -q ai-edge-litert
dpkg -s libegl1 >/dev/null 2>&1 || (apt-get install -y -q libegl1 libgles2 >/dev/null 2>&1 || true)
python3 -c "import mediapipe" 2>/dev/null || pip install -q mediapipe
mkdir -p models
[ -s models/face_landmarker.task ] || curl -sSL -o models/face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
[ -s models/selfie_multiclass_256x256.tflite ] || curl -sSL -o models/selfie_multiclass_256x256.tflite https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite
node -e "require('playwright')" && echo "ok: ffmpeg, whisper, recorte, playwright"
