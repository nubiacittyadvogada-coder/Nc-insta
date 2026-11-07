"""Trilha de efeitos sonoros do vídeo (07/11/2026). Uso: python3 sfx.py fx.js DURACAO saida.wav [--ganho 0.32]
Os sons saem da biblioteca sons/ (gerar_sons.py). A trilha fica na linha do corte e é misturada antes do 1,1x (fx_comp.py --sfx)."""
import json, subprocess, sys, os, wave, argparse
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); SR = 48000
ap = argparse.ArgumentParser(); ap.add_argument('fx'); ap.add_argument('dur', type=float); ap.add_argument('out'); ap.add_argument('--ganho', type=float, default=0.32)
a = ap.parse_args()
cues = json.loads(subprocess.check_output(['node', os.path.join(H, 'sfx_cues.js'), a.fx]))
def load(n):
    with wave.open(os.path.join(H, 'sons', n + '.wav')) as w: return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32767
cache = {}; out = np.zeros(int(SR * (a.dur + 2)), np.float32)
for c in cues:
    nome, _, lim = c['s'].partition(':')
    if nome not in cache: cache[nome] = load(nome)
    x = cache[nome]
    if lim:
        L = float(lim)
        if nome == 'tensao':  # estica ou corta para caber na janela, com fim suave
            n = int(SR * L); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
        else:
            x = x[:int(SR * L)].copy(); f = min(len(x), int(SR * 0.04)); x[-f:] *= np.linspace(1, 0, f)
    i = int(SR * c['t']); j = min(len(out), i + len(x))
    if i < len(out): out[i:j] += x[:j - i] * c['g']
out = out[:int(SR * a.dur)] * a.ganho
out = np.clip(out, -0.98, 0.98)
with wave.open(a.out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes())
print(a.out, len(cues), 'sons')
