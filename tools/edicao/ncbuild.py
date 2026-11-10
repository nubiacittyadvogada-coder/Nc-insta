"""Montagem rápida NC: cortes por fala (energia), desfoque leve do fundo, zoom alternado, overlays PNG, legenda ASS, 1,1x, logo no fim.
Uso: python3 ncbuild.py cfg.json etapa(cut|blur|comp|all)"""
import json, subprocess, sys, os, wave, numpy as np
from PIL import Image, ImageDraw, ImageFont
cfg = json.load(open(sys.argv[1])); D = cfg['dir']; step = sys.argv[2] if len(sys.argv) > 2 else 'all'
os.chdir(D)
F = '/tmp/claude-0/-home-user/35e900c0-5567-55e2-9b5c-894faf2df1c8/scratchpad/juri/ed/fonts/'
FW = '/home/user/Nc-insta/modelos/fontes/'
W = json.load(open('w.json'))
A = np.frombuffer(wave.open('a.wav').readframes(10**9), np.int16).astype(np.float32)
def db(t, w=0.03):
    i = int(t * 16000); seg = A[max(0, i):i + int(w * 16000)]
    return 10 * np.log10(np.mean(seg ** 2) + 1) if len(seg) else 0
floor = np.percentile([db(t) for t in np.arange(0, len(A) / 16000 - 0.05, 0.05)], 15)
TH = floor + 12
def snap_start(s):
    t = s - 0.35
    while t < s + 0.15:
        if db(t, 0.02) > TH: return max(0, t - 0.04)
        t += 0.01
    return max(0, s - 0.06)
def snap_end(e, nxt=None):
    ws = [x[1] for x in W if abs(x[2] - e) < 0.011]; t = (ws[0] + 0.08) if ws else e - 0.3
    lim = min(e + 0.3, (nxt - 0.08) if nxt else e + 0.3); quiet = 0
    while t < lim:
        if db(t, 0.02) < TH: quiet += 1
        else: quiet = 0
        if quiet >= 12: return round(t - 0.12 + 0.06 + 0.01, 3)
        t += 0.01
    return lim
starts = sorted(x[1] for x in W)
def nxt_word(e):
    n = [s for s in starts if s > e + 0.01]; return n[0] if n else None
# pieces: [rawStart, rawEnd] given as word-start of first word and word-end of last word
P = []
for it in cfg['edl']:
    a, b = it[0], it[1]; lo = it[2] if len(it) > 2 else 0; hi = it[3] if len(it) > 3 else 1e9
    s = max(snap_start(a), lo); e = min(snap_end(b, nxt_word(b - 0.05)) + (it[4] if len(it) > 4 else 0), hi); P.append((round(s, 3), round(e, 3)))
json.dump(P, open('pieces.json', 'w'))
SRC = cfg['src']
if step in ('cut', 'all'):
    parts = []
    for i, (s, e) in enumerate(P):
        p = f'p{i:02d}.mp4'; parts.append(p)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-i', SRC, '-t', f'{e - s:.3f}', '-map', '0:v:0', '-map', '0:a:0',
                        '-vf', 'scale=1080:1920:flags=lanczos:out_color_matrix=bt709,fps=30,setsar=1,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '10', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', p], check=True)
    open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'cut.mp4'], check=True)
    for p in parts: os.remove(p)
dur_of = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode())
if step in ('blur', 'all'):
    import cv2
    from ai_edge_litert.interpreter import Interpreter
    it = Interpreter(model_path='/home/user/Nc-insta/tools/edicao/models/selfie_multiclass_256x256.tflite'); it.allocate_tensors()
    ii = it.get_input_details()[0]['index']; oi = it.get_output_details()[0]['index']
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', 'cut.mp4', '-vf', 'scale=in_color_matrix=bt709:in_range=tv,format=bgr24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    FB = 1080 * 1920 * 3
    class _C:
        def read(self):
            b = dec.stdout.read(FB)
            return (len(b) == FB, np.frombuffer(b, np.uint8).reshape(1920, 1080, 3) if len(b) == FB else None)
    cap = _C()
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1080x1920', '-r', '30', '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '10', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', 'v.mp4'], stdin=subprocess.PIPE)
    pm = None; k = 0; sk = cfg.get('segEvery', 3); bs = cfg.get('blur', 7)
    while True:
        ok, fr = cap.read()
        if not ok: break
        if k % sk == 0 or pm is None:
            x = cv2.resize(fr, (256, 256), interpolation=cv2.INTER_AREA)[:, :, ::-1].astype(np.float32)[None] / 255.0
            it.set_tensor(ii, x); it.invoke(); o = it.get_tensor(oi)[0]
            if not np.allclose(o.sum(-1), 1, atol=1e-2):
                e = np.exp(o - o.max(-1, keepdims=True)); o = e / e.sum(-1, keepdims=True)
            m = cv2.resize(1.0 - o[..., 0], (270, 480)); m = cv2.dilate((m > 0.4).astype(np.float32), np.ones((9, 9), np.uint8))
            m = cv2.GaussianBlur(m, (0, 0), 2)
            if pm is not None: m = 0.6 * m + 0.4 * pm
            pm = m; M = cv2.resize(m, (1080, 1920))[..., None]
        k += 1
        bg = cv2.resize(cv2.GaussianBlur(cv2.resize(fr, (270, 480), interpolation=cv2.INTER_AREA), (0, 0), bs / 4), (1080, 1920), interpolation=cv2.INTER_LINEAR)
        enc.stdin.write((fr * M + bg * (1 - M)).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
if step in ('comp', 'all'):
    L = dur_of('v.mp4')
    acc = []; t = 0
    for s, e in P: acc.append(t); t += e - s
    def m(raw, strict=False):
        for (s, e), a in zip(P, acc):
            if s - (0.12 if strict else 0.06) <= raw <= e + 0.02: return a + max(0, raw - s)
        for (s, e), a in zip(P, acc):
            if not strict and e < raw <= e + 0.6: return a + (e - s)
        return None
    # words
    fix = cfg.get('fix', {}); words = []
    for x, s, e in W:
        fs = m(s, True)
        if fs is None: continue
        key = f'{x}@{s}'; x2 = fix.get(key, fix.get(x, x))
        if x2 == '': continue
        words.append([x2, fs, fs + (e - s)])
    words.sort(key=lambda w: w[1])
    def ts(t):
        t = max(0, t); return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'
    chunks = []; cur = []
    for i, w in enumerate(words):
        cur.append(w); txt = ' '.join(c[0] for c in cur); nx = words[i + 1] if i + 1 < len(words) else None
        if len(cur) >= 4 or len(txt) >= 22 or w[0][-1] in '.,?!:' or nx is None or nx[1] - w[2] > 0.35:
            chunks.append(cur); cur = []
    ev = []
    nocap = cfg.get('nocap', [])
    for j, c in enumerate(chunks):
        s = c[0][1]; e = c[-1][2] + 0.15
        if j + 1 < len(chunks): e = max(min(e, chunks[j + 1][0][1]), s + 0.3)
        if any(a <= s < b for a, b in nocap): continue
        txt = ' '.join(x[0] for x in c).rstrip(',')
        for hw in cfg.get('hl', []):
            txt = txt.replace(hw, '{\\c&H00CCC3F0&}' + hw + '{\\c&H00FFFFFF&}')
        ev.append(f'Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{txt}')
    open('cap.ass', 'w').write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Archivo SemiBold,54,&H00FFFFFF,&H00FFFFFF,&H50000000,&H70000000,0,0,0,0,100,100,0,0,1,2.5,3,2,80,80,{cfg.get('capV', 430)},1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + '\n'.join(ev) + '\n')
    json.dump(dict(words=words, acc=acc, L=L), open('timeline.json', 'w'), ensure_ascii=False)
    # overlays
    sys.path.insert(0, "/tmp/claude-0/-home-user/35e900c0-5567-55e2-9b5c-894faf2df1c8/scratchpad"); import ov_nc
    OV = ov_nc.build(cfg, m, L, words)
    # zoom: alternate per piece (1.0 / Z)
    Z = cfg.get('zoom', 1.15); cy = cfg.get('zoomCY', 700)
    cw = int(1080 / Z) // 2 * 2; ch = int(1920 / Z) // 2 * 2; cx = (1080 - cw) // 2; y0 = int(min(max(cy - ch / 2, 0), 1920 - ch))
    zr = [(acc[i], acc[i] + (P[i][1] - P[i][0])) for i in range(len(P)) if i % 2 == 1 and i not in cfg.get('nozoom', [])]
    en = '+'.join(f'between(t,{a:.3f},{b:.3f})' for a, b in zr) or '0'
    inp = ['-i', 'v.mp4', '-i', 'cut.mp4']
    g = [f"[0:v]tpad=stop_mode=clone:stop_duration=1,split[w][zz];[zz]crop={cw}:{ch}:{cx}:{y0},scale=1080:1920:flags=lanczos[zm];[w][zm]overlay=enable='{en}'[b0]"]
    curv = 'b0'
    for i, (n, a, b) in enumerate(OV):
        inp += ['-loop', '1', '-framerate', '30', '-t', f'{L:.3f}', '-i', n]
        fo = max(a, b - 0.2)
        g.append(f'[{i + 2}:v]format=rgba,fade=t=in:st={a:.3f}:d=0.2:alpha=1,fade=t=out:st={fo:.3f}:d=0.2:alpha=1[o{i}]')
        g.append(f"[{curv}][o{i}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[c{i}]"); curv = f'c{i}'
    g.append(f'[{curv}]ass=cap.ass:fontsdir={F},setpts=PTS/1.1,fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[vo]')
    g.append('[1:a]highpass=f=80,afftdn=nf=-25,atempo=1.1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[ao]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(g), '-map', '[vo]', '-map', '[ao]', '-c:v', 'libx264', '-preset', 'medium', '-profile:v', 'high', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv'] + (['-b:v', cfg['vbr'], '-maxrate', '1500k', '-bufsize', '3000k'] if cfg.get('vbr') else (['-crf', '14'] if cfg.get('endcard', True) else ['-crf', '18', '-maxrate', '8M', '-bufsize', '16M'])) + ['-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', 'pre.mp4'], check=True)
    if cfg.get('endcard', True): subprocess.run(['python3', '/home/user/Nc-insta/tools/edicao/endcard.py', 'pre.mp4', cfg['out']], check=True)
    else: os.replace('pre.mp4', cfg['out'])
    print('ok', cfg['out'], round(dur_of(cfg['out']), 2))
