"""Folha de rostos dos cortes (07/11/2026). Regra da Núbia: o rosto fica sempre livre e bonito.
Nada de língua de fora, olho fechado, boca torta ou careta no começo ou no fim de um trecho.
O detector automático NÃO é confiável para isso (óculos e olhar para baixo enganam o modelo),
então a folha é para REVISÃO VISUAL obrigatória: abrir a imagem e olhar cada rosto.

Uso: python3 folha_rostos.py final.mp4 segs.json saida.jpg [--vel 1.1]
  segs.json: lista com t0/t1 de cada trecho na linha do corte (o mk.py já grava). Gera, para cada corte,
  o rosto em close no 1º, 2º, penúltimo e último quadro do trecho, com o tempo do vídeo final escrito embaixo.
Se um rosto estiver ruim: (1) trecho curto sem fala (< 0,5 s) sai; (2) senão, mova a borda 2 a 4 quadros
para dentro do silêncio ou para o quadro bom mais próximo; (3) se a careta está no meio da fala, troque
pela outra tentativa do bruto. Gere a folha de novo até todos os rostos passarem."""
import sys, json, subprocess, argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('segs'); ap.add_argument('out'); ap.add_argument('--vel', type=float, default=1.1)
a = ap.parse_args()
H = os.path.dirname(os.path.abspath(__file__))
try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision, BaseOptions
    DET = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=f'{H}/models/face_landmarker.task'), num_faces=1))
except Exception as e:
    print('sem detector de rosto (recorte fixo no terço de cima):', str(e)[:80]); DET = None
def frame(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t):.3f}', '-i', a.video, '-frames:v', '1', '-vf', 'scale=540:960', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(960, 540, 3) if len(raw) == 540 * 960 * 3 else None
def rosto(img):
    box = None
    if DET is not None:
        r = DET.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(img)))
        if r.face_landmarks:
            xs = [p.x for p in r.face_landmarks[0]]; ys = [p.y for p in r.face_landmarks[0]]
            cx, cy = (min(xs) + max(xs)) / 2 * 540, (min(ys) + max(ys)) / 2 * 960; s = max(max(xs) - min(xs), (max(ys) - min(ys)) * 0.56) * 540 * 1.5
            box = (int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2))
    if box is None: box = (120, 140, 420, 440)
    return Image.fromarray(img).crop(box).resize((200, 200))
segs = json.load(open(a.segs)); D = 1 / 30
pts = []
for i, s in enumerate(segs):
    t0, t1 = s['t0'] / a.vel, s['t1'] / a.vel
    pts += [(i, 'início', t0 + 0.5 * D), (i, '', t0 + 2 * D), (i, '', t1 - 2 * D), (i, 'fim', t1 - 0.6 * D)]
cols = 8; rows = (len(pts) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 200, rows * 228), (20, 14, 12)); dr = ImageDraw.Draw(sheet)
try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception: fnt = ImageFont.load_default()
for k, (i, lab, t) in enumerate(pts):
    img = frame(t); x, y = (k % cols) * 200, (k // cols) * 228
    if img is not None: sheet.paste(rosto(img), (x, y))
    dr.text((x + 6, y + 205), f'trecho {i + 1} {lab} {t:.2f}s', fill=(240, 195, 204), font=fnt)
sheet.save(a.out, quality=88); print(a.out, len(pts), 'rostos', 'em', len(segs), 'trechos')
