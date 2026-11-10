from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = '/tmp/claude-0/-home-user/35e900c0-5567-55e2-9b5c-894faf2df1c8/scratchpad/juri/ed/fonts/'
BOD = F + 'bodoni-moda-latin-400-normal.ttf'; BODI = F + 'bodoni-moda-latin-400-italic.ttf'
AR6 = F + 'archivo-latin-600-normal.ttf'; AR7 = F + 'archivo-latin-700-normal.ttf'
DARK = (17, 17, 17); SAND = (230, 218, 209); TAUPE = (216, 196, 182); WHITE = (255, 255, 255)

def font(p, s): return ImageFont.truetype(p, s)
def canvas(): return Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
def shadow_text(im, xy, txt, f, fill=WHITE, anchor='la'):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.text((xy[0], xy[1] + 3), txt, font=f, fill=(0, 0, 0, 150), anchor=anchor)
    sh = sh.filter(ImageFilter.GaussianBlur(7)); im.alpha_composite(sh)
    ImageDraw.Draw(im).text(xy, txt, font=f, fill=fill, anchor=anchor)

def rich_line(im, y, parts, size):
    """parts: list of (text, italic) centered"""
    fs = [font(BODI if it else BOD, size) for _, it in parts]
    d = ImageDraw.Draw(im); ws = [d.textlength(t, font=f) for (t, _), f in zip(parts, fs)]
    x = (1080 - sum(ws)) / 2
    for (t, it), f, w in zip(parts, fs, ws):
        shadow_text(im, (x, y), t, f); x += w

def backed(im, pad=30, alpha=205):
    bb = im.getbbox()
    if not bb: return im
    bg = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(bg)
    d.rounded_rectangle((bb[0] - pad, bb[1] - pad + 4, bb[2] + pad, bb[3] + pad - 4), radius=26, fill=(17, 17, 17, alpha))
    bg.alpha_composite(im); return bg

def parse(line):  # *italic* markup
    out = []; it = False
    for i, seg in enumerate(line.split('*')):
        if seg: out.append((seg, i % 2 == 1))
    return out

def build(cfg, m, L, words):
    OV = []; k = 0
    def save(im, a, b, back=True):
        nonlocal k
        if back: im = backed(im)
        n = f'ov{k:02d}.png'; im.save(n); OV.append((n, max(0, a), min(L, b))); k += 1
    # hook
    h = cfg.get('hook')
    if h:
        im = canvas(); y = h.get('y', 130)
        for ln in h['lines']:
            rich_line(im, y, parse(ln), h.get('size', 66)); y += int(h.get('size', 66) * 1.12)
        save(im, 0.05, h.get('end', 3.0))
    # serie card
    s = cfg.get('serie')
    if s:
        im = canvas(); d = ImageDraw.Draw(im); f = font(AR6, 20)
        txt = '  '.join(s['kicker']); w = d.textlength(txt, font=f)
        shadow_text(im, ((1080 - w) / 2, s.get('y', 150)), txt, f)
        y = s.get('y', 150) + 46
        for ln in s['lines']:
            rich_line(im, y, parse(ln), 52); y += 60
        a = m(s['raw'][0]); b = m(s['raw'][1]); save(im, a, b)
    # name chips
    for raw0, raw1, name, role in cfg.get('names', []):
        im = canvas(); y = cfg.get('nameY', 1580)
        shadow_text(im, (72, y), name, font(BOD, 46))
        d = ImageDraw.Draw(im); d.rectangle((72, y + 64, 128, y + 67), fill=TAUPE)
        shadow_text(im, (72, y + 80), '  '.join(role) if role.isupper() else role, font(AR6, 16))
        a = m(raw0); b = m(raw1)
        if a is not None and b is not None: save(im, a, b)
    # countdown timers
    for raw0, raw1 in cfg.get('timers', []):
        a = m(raw0); b = m(raw1)
        if a is None or b is None: continue
        for i in range(6):
            n = 5 - i; t0 = a + i; t1 = min(b, a + i + 1) if n > 0 else b
            if t0 >= b: break
            im = canvas(); d = ImageDraw.Draw(im); cx, cy, r = 940, 190, 74
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(17, 17, 17, 215) if n else (142, 42, 62, 235))
            # progress ring
            if n: d.arc((cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6), -90, -90 + 360 * n / 5, fill=SAND, width=6)
            f = font(AR7, 64); d.text((cx, cy - 4), str(n), font=f, fill=WHITE, anchor='mm')
            d.text((cx, cy + r + 22), 'SEGUNDOS' if n else 'ESTOUROU', font=font(AR6, 15), fill=WHITE, anchor='mm')
            save(im, t0, t1, False)
    # tags (PORÉM etc.)
    for raw, dur, txt in cfg.get('tags', []):
        a = m(raw)
        if a is None: continue
        im = canvas(); d = ImageDraw.Draw(im); f = font(AR7, 64); w = d.textlength(txt, font=f)
        y = cfg.get('tagY', 1240)
        d.rounded_rectangle(((1080 - w) / 2 - 34, y, (1080 + w) / 2 + 34, y + 104), radius=52, fill=(142, 42, 62, 240))
        d.text((540, y + 50), txt, font=f, fill=WHITE, anchor='mm')
        save(im, a, a + dur, False)
    # simple text card list (items accumulate)
    for blk in cfg.get('lists', []):
        items = blk['items']; times = [m(r) for r, _ in items]; end = m(blk['end'])
        for i in range(len(items)):
            im = canvas(); d = ImageDraw.Draw(im); y = blk.get('y', 1080)
            if blk.get('title'):
                f6 = font(AR6, 20); t6 = '  '.join(blk['title']); w6 = ImageDraw.Draw(im).textlength(t6, font=f6); shadow_text(im, ((1080 - w6) / 2, y), t6, f6); y += 48
            for j in range(i + 1):
                rich_line(im, y, parse(items[j][1]), 50); y += 66
            t1 = times[i + 1] if i + 1 < len(items) else end
            save(im, times[i], t1)
    # free text cards
    for raw0, raw1, lines, y in cfg.get('cards', []):
        a = m(raw0); b = m(raw1)
        if a is None or b is None: continue
        im = canvas(); yy = y
        for ln in lines:
            rich_line(im, yy, parse(ln), 56); yy += 64
        save(im, a, b)
    # cta
    c = cfg.get('cta')
    if c:
        im = canvas(); y = c.get('y', 150)
        for ln in c['lines']:
            rich_line(im, y, parse(ln), 58); y += 66
        f = font(AR6, 18); d = ImageDraw.Draw(im); txt = '  '.join('@NUBIACITTYADVOGADOS'); w = d.textlength(txt, font=f)
        shadow_text(im, ((1080 - w) / 2, y + 16), txt, f)
        save(im, m(c['raw']), L)
    return OV
