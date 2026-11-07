"""Biblioteca de efeitos sonoros próprios (07/11/2026). Sintetizados do zero: sem direitos de terceiros.
Uso: python3 gerar_sons.py  (gera os .wav nesta pasta, 48 kHz mono)."""
import numpy as np, wave, os
SR = 48000
D = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)

def save(n, x, g=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * g
    with wave.open(os.path.join(D, n + '.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())

def t(d): return np.arange(int(SR * d)) / SR
def env(n, a, r):  # ataque/decay exponencial
    e = np.ones(n); na = max(1, int(SR * a)); e[:na] = np.linspace(0, 1, na)
    e[na:] = np.exp(-np.arange(n - na) / (SR * r)); return e
def lp(x, fc):  # passa-baixa 1 polo (fc pode variar no tempo)
    fc = np.broadcast_to(np.asarray(fc, float), x.shape); y = np.zeros_like(x); s = 0.0
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y

# whoosh: ruído com filtro varrendo, envelope em sino
def whoosh(d=0.55, f0=300, f1=4200):
    tt = t(d); n = rng.standard_normal(len(tt)); p = tt / d
    fc = f0 + (f1 - f0) * np.sin(np.pi * p) ** 2
    y = lp(n, fc) - lp(n, fc * 0.35); e = np.sin(np.pi * p) ** 1.6
    return y * e
save('whoosh', whoosh(), 0.7)
save('whoosh_curto', whoosh(0.3, 500, 5000), 0.6)
# subida de tensão (vertigem): ruído + tom grave subindo
tt = t(1.8); p = tt / 1.8
y = (lp(rng.standard_normal(len(tt)), 200 + 3500 * p ** 2) * p ** 2) * 0.8 + np.sin(2 * np.pi * np.cumsum(55 + 90 * p ** 2) / SR) * p ** 1.5 * 0.6
y[-int(SR * 0.04):] *= np.linspace(1, 0, int(SR * 0.04))
save('tensao', y, 0.75)
# pop: seno com queda de afinação
def pop(f=900, d=0.12):
    tt = t(d); fr = f * np.exp(-tt * 18) + f * 0.4
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(len(tt), 0.002, 0.03)
save('pop', pop(), 0.6); save('pop_grave', pop(520, 0.16), 0.65)
# bolha (mensagem): dois pops rápidos
b = np.concatenate([pop(1100, 0.07), np.zeros(int(SR * 0.025)), pop(1500, 0.09)]); save('bolha', b, 0.5)
# clique (mouse/botão)
tt = t(0.05); c = rng.standard_normal(len(tt)) * env(len(tt), 0.0005, 0.004) + np.sin(2 * np.pi * 3200 * tt) * env(len(tt), 0.0005, 0.006) * 0.6
save('clique', lp(c, 7000), 0.6)
# tecla (para digitação): clique curto mais grave, com variação
def tecla(k):
    tt = t(0.045); f = 1800 + 500 * k
    x = rng.standard_normal(len(tt)) * env(len(tt), 0.0004, 0.003) * 0.9 + np.sin(2 * np.pi * f * tt) * env(len(tt), 0.0005, 0.005) * 0.4
    return lp(x, 5000)
for k in range(4): save(f'tecla{k}', tecla(k), 0.45)
# check / confirmação: dois tons suaves (quinta)
tt = t(0.32)
ck = (np.sin(2 * np.pi * 880 * tt) * env(len(tt), 0.004, 0.08) + np.sin(2 * np.pi * 1320 * tt) * np.r_[np.zeros(int(SR * 0.07)), env(len(tt) - int(SR * 0.07), 0.004, 0.1)] * 0.8)
save('check', ck, 0.45)
# giz: ruído granulado em rajadas
tt = t(1.0); g = np.zeros(len(tt)); i = 0
while i < len(tt):
    ln = int(SR * rng.uniform(0.03, 0.09)); seg = rng.standard_normal(min(ln, len(tt) - i)) * rng.uniform(0.5, 1)
    seg *= np.hanning(len(seg)); g[i:i + len(seg)] += seg; i += ln + int(SR * rng.uniform(0.005, 0.03))
g = lp(g, 6000) - lp(g, 1800); save('giz', g, 0.35)
# marca-texto / risco: swish curto agudo
tt = t(0.35); p = tt / 0.35; m = rng.standard_normal(len(tt)); m = (lp(m, 2500 + 4000 * p) - lp(m, 1500)) * np.sin(np.pi * p) ** 0.8
save('marcador', m, 0.4)
# impacto (palavra forte): grave com corpo
tt = t(0.7); imp = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-tt * 6) + 38) / SR) * env(len(tt), 0.002, 0.22) + lp(rng.standard_normal(len(tt)), 900) * env(len(tt), 0.001, 0.03) * 0.8
save('impacto', imp, 0.85)
# carimbo: batida seca de madeira
tt = t(0.25); cb = lp(rng.standard_normal(len(tt)), 2200) * env(len(tt), 0.0008, 0.018) + np.sin(2 * np.pi * 180 * tt) * env(len(tt), 0.001, 0.05) * 0.8
save('carimbo', cb, 0.8)
# página virando
tt = t(0.45); p = tt / 0.45; pg = rng.standard_normal(len(tt)); pg = (lp(pg, 1500 + 5000 * p) - lp(pg, 700)) * (np.sin(np.pi * p) ** 2) * (1 + 0.6 * np.sin(2 * np.pi * 22 * tt))
save('pagina', pg, 0.5)
print('ok', sorted(f for f in os.listdir(D) if f.endswith('.wav')))
