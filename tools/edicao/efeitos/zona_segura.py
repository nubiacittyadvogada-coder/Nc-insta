"""Zona do rosto (07/11/2026, regra da Núbia: NENHUM elemento pode tampar o rosto).
Lê a máscara da pessoa e grava safe.js com a posição do rosto a cada 0,25 s (linha do corte).
O fx_engine.html carrega safe.js e encaixa cada elemento acima ou abaixo do rosto (sobe, encolhe ou desce).
Uso: python3 zona_segura.py mask.mp4 PASTA_DO_FX/safe.js"""
import subprocess, sys, json
import numpy as np
mask, out = sys.argv[1], sys.argv[2]
W, H, S = 270, 480, 4  # amostra em 1/4 da resolução; S = fator para 1080x1920
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', mask, '-vf', f'fps=4,scale={W}:{H},format=gray', '-f', 'rawvideo', '-'])
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W) > 128
res = []
for m in fr:
    rows = np.where(m.sum(1) > 4)[0]
    if not len(rows): res.append(None); continue
    top = rows[0]; r = m[min(H - 1, top + 28)]  # linha da testa
    cols = np.where(r)[0]
    if not len(cols): res.append(None); continue
    xl, xr = cols[0], cols[-1]; w = xr - xl
    xl -= 0.2 * w; xr += 0.2 * w; bot = top + 1.5 * w
    res.append([round(float(xl * S)), round(float(top * S)), round(float(xr * S)), round(float(bot * S))])
open(out, 'w').write('window.ROSTO={dt:0.25,r:' + json.dumps(res) + '};')
v = [x for x in res if x]
print(out, len(res), 'amostras', 'topo min', min(x[1] for x in v), 'queixo max', max(x[3] for x in v))
