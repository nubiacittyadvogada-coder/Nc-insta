#!/usr/bin/env bash
# Monta o Reel de 7s: recorta o vídeo gravado em 1080x1920, usa os 7 primeiros segundos,
# aplica o texto (PNG transparente) com entrada suave e remove o áudio original
# (a trilha é escolhida dentro do Instagram, onde é licenciada).
# Uso: tools/montar-reel7.sh video-gravado.mov texto-na-tela.png saida.mp4
set -euo pipefail
[ $# -eq 3 ] || { echo "uso: $0 <video> <texto.png> <saida.mp4>"; exit 1; }
ffmpeg -y -loglevel error -i "$1" -loop 1 -i "$2" -filter_complex \
  "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v];[1:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1[t];[v][t]overlay=0:0,format=yuv420p[o]" \
  -map "[o]" -t 7 -an -c:v libx264 -preset medium -crf 18 -movflags +faststart "$3"
echo "pronto: $3"
