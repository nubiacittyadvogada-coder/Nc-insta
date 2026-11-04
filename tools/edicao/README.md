# Padrão de edição "cinema" (aprovado pela Núbia em 04/11/2026)

1. Recorte da pessoa (modelo selfie_multiclass_256x256 do MediaPipe, rodado com ai-edge-litert):
   `python3 recorte_fundo.py VIDEO INICIO DURACAO selfie_multiclass_256x256.tflite mascara.mp4`
   Modelo: https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite (não versionar).
2. Animações: `node render_overlay.js overlay-editorial.html PASTA_FRAMES "#fume"` (150 PNGs a 30 fps). Variante "#claro" para fundo escuro. Padrão: fumê.
3. Composição (ffmpeg):
   - Cor A: `format=rgb24,colorbalance=rs=0.015:bs=-0.02:rm=0.025:bm=-0.025:rh=0.01:bh=-0.01,eq=contrast=1.08:brightness=0.015:saturation=1.04,curves=all='0/0.035 0.5/0.51 1/0.975'`
   - Fundo: `gblur=sigma=11,eq=brightness=-0.03:saturation=0.85` e `maskedmerge` com a máscara (tudo em gbrp).
   - Acabamento: brilho leve (screen 8% de um gblur 24), `vignette=PI/4.6`, `noise=alls=5:allf=t`.
   - Cartão de vidro: recorte da área, `gblur=sigma=30`, máscara arredondada (raio 44), entra com fade e sobe 60 px.
4. Tipografia: Archivo 700 (palavra grande, letter-spacing -11px), Bodoni Moda itálico 400 sobreposto, Archivo 600 em maiúsculas espaçadas (.42em) como subtítulo. Entrada letra a letra saindo do desfoque.
5. Regras: nunca número, resultado ou depoimento que não seja real; texto fora do rosto (terço de cima ou de baixo).
