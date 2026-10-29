/* NC Render: motor de artes da Central Núbia Citty.
   Um único código desenha carrosséis, stories, posts, capas e textos de Reels,
   tanto no app (celular) quanto na produção automática no servidor.
   Ênfase no texto: *palavra* vira itálico/destaque. Quebra manual: \n */
(function (root) {
  const C = {
    vinho: '#6B1E2E', vinhoEsc: '#4A1220', vinhoClaro: '#8E3346',
    preto: '#0F0D0D', grafite: '#2A2426', branco: '#FFFFFF',
    off: '#F6F1EA', bege: '#E4D6C3', begeEsc: '#CDB89D', dourado: '#B08D57',
    cinza: '#8A7F7A', cinzaClaro: '#CFC6BE'
  };
  const F = {
    serif: '"Bodoni Moda", "Didot", "Bodoni 72", Georgia, serif',
    sans: '"Archivo", "Helvetica Neue", Arial, sans-serif',
    cond: '"Anton", "Impact", "Arial Narrow", sans-serif'
  };
  const FORMATS = {
    carrossel: { w: 1080, h: 1350, top: 96, bottom: 96 },
    estatico: { w: 1080, h: 1350, top: 96, bottom: 96 },
    story: { w: 1080, h: 1920, top: 250, bottom: 330 },
    capa: { w: 1080, h: 1920, top: 330, bottom: 330 },   // capa de Reel: texto dentro do recorte 1080x1350 do grid
    overlay: { w: 1080, h: 1920, top: 0, bottom: 0 }
  };
  const STYLES = ['editorial', 'lifestyle', 'colagem', 'jornalistico', 'minimal'];
  const HANDLE = '@nubiacitty';

  // ---------- utilidades ----------
  function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) { let s = seed || 1; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

  function parseRich(text) {
    const words = []; let em = false; let buf = '';
    const push = () => { if (buf) { words.push({ t: buf, em }); buf = ''; } };
    for (const ch of String(text || '')) {
      if (ch === '*') { push(); em = !em; continue; }
      if (ch === '\n') { push(); words.push({ br: true }); continue; }
      if (ch === ' ') { push(); words.push({ sp: true }); continue; }
      buf += ch;
    }
    push();
    // junta pedaços colados (ex.: *palavra*,)
    const out = []; let cur = [];
    for (const w of words) {
      if (w.sp || w.br) { if (cur.length) out.push(cur); cur = []; if (w.br) out.push('BR'); continue; }
      cur.push(w);
    }
    if (cur.length) out.push(cur);
    return out; // array de palavras (cada palavra = array de pedaços) ou 'BR'
  }

  function wrap(ctx, text, fontFn, size, maxW, upper) {
    const words = parseRich(upper ? String(text || '').toUpperCase() : text);
    const space = (() => { ctx.font = fontFn(size, false); return ctx.measureText(' ').width; })();
    const lines = []; let line = []; let lw = 0;
    const measure = (word) => word.reduce((a, p) => { ctx.font = fontFn(size, p.em); return a + ctx.measureText(p.t).width; }, 0);
    for (const w of words) {
      if (w === 'BR') { lines.push({ words: line, w: lw }); line = []; lw = 0; continue; }
      const ww = measure(w);
      const add = line.length ? space + ww : ww;
      if (line.length && lw + add > maxW) { lines.push({ words: line, w: lw }); line = [w]; lw = ww; }
      else { line.push(w); lw += add; }
    }
    if (line.length) lines.push({ words: line, w: lw });
    let widest = 0; lines.forEach(l => { widest = Math.max(widest, l.w); });
    return { lines, space, widest };
  }

  function fit(ctx, text, o) {
    let size = o.max;
    while (size > o.min) {
      const r = wrap(ctx, text, o.font, size, o.maxW, o.upper);
      if (r.lines.length * size * o.lh <= o.maxH && r.widest <= o.maxW) return Object.assign(r, { size, h: r.lines.length * size * o.lh });
      size -= 2;
    }
    const r = wrap(ctx, text, o.font, o.min, o.maxW, o.upper);
    return Object.assign(r, { size: o.min, h: r.lines.length * o.min * o.lh });
  }

  // desenha bloco já ajustado; y = topo do bloco
  function draw(ctx, block, o) {
    const { size } = block; const lh = size * o.lh;
    ctx.textBaseline = 'alphabetic';
    block.lines.forEach((ln, i) => {
      let x = o.x;
      if (o.align === 'center') x = o.x + (o.maxW - ln.w) / 2;
      if (o.align === 'right') x = o.x + o.maxW - ln.w;
      const baseY = o.y + i * lh + size * (o.ascent || 0.86);
      ln.words.forEach((word, wi) => {
        if (wi > 0) x += block.space;
        word.forEach(p => {
          ctx.font = o.font(size, p.em);
          const w = ctx.measureText(p.t).width;
          if (p.em && o.emBox) {
            const nextEm = wi < ln.words.length - 1 && ln.words[wi + 1][0].em && p === word[word.length - 1];
            ctx.fillStyle = o.emBox;
            ctx.fillRect(x - size * 0.08, baseY - size * 0.92, w + size * 0.16 + (nextEm ? block.space : 0), size * 1.08);
          }
          ctx.fillStyle = p.em ? (o.emColor || o.color) : o.color;
          ctx.fillText(p.t, x, baseY);
          x += w;
        });
      });
    });
  }

  function spaced(ctx, str, x, y, spacing, align) {
    const chars = [...String(str || '')];
    const total = chars.reduce((a, c) => a + ctx.measureText(c).width + spacing, 0) - spacing;
    let cx = align === 'right' ? x - total : align === 'center' ? x - total / 2 : x;
    chars.forEach(c => { ctx.fillText(c, cx, y); cx += ctx.measureText(c).width + spacing; });
    return total;
  }

  const grainCache = {};
  function grain(ctx, W, H, alpha, dark) {
    const key = dark ? 'd' : 'l';
    if (!grainCache[key]) {
      const g = document.createElement('canvas'); g.width = g.height = 160;
      const gx = g.getContext('2d'); const img = gx.createImageData(160, 160); const r = rng(7);
      for (let i = 0; i < img.data.length; i += 4) { const v = dark ? 255 : 0; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = r() * 255; }
      gx.putImageData(img, 0, 0); grainCache[key] = g;
    }
    ctx.save(); ctx.globalAlpha = alpha; ctx.fillStyle = ctx.createPattern(grainCache[key], 'repeat'); ctx.fillRect(0, 0, W, H); ctx.restore();
  }

  function cover(ctx, img, x, y, w, h) {
    const r = Math.max(w / img.width, h / img.height);
    const iw = img.width * r, ih = img.height * r;
    ctx.drawImage(img, x + (w - iw) / 2, y + (h - ih) / 2, iw, ih);
  }

  const big = (s) => s.format === 'story' || s.format === 'capa';
  const serif = (wt) => (s, em) => `${em ? 'italic ' : ''}${wt} ${s}px ${F.serif}`;
  const sans = (wt) => (s, em) => `${em ? 'italic ' : ''}${wt} ${s}px ${F.sans}`;
  const cond = () => (s) => `400 ${s}px ${F.cond}`;

  // título + corpo dentro de uma área; devolve altura usada
  function textStack(ctx, s, a) {
    const gap = s.body ? a.gap || 44 : 0;
    const titleMaxH = s.body ? a.h * (a.titleShare || 0.62) : a.h;
    const t = fit(ctx, s.title, { font: a.tFont, max: a.tMax, min: a.tMin || 40, lh: a.tLh, maxW: a.w, maxH: titleMaxH, upper: a.upper });
    let b = null;
    if (s.body) b = fit(ctx, s.body, { font: a.bFont, max: a.bMax || 40, min: 26, lh: a.bLh || 1.42, maxW: a.bw || a.w, maxH: a.h - t.h - gap });
    const total = t.h + (b ? gap + b.h : 0);
    let y = a.y;
    if (a.valign === 'bottom') y = a.y + a.h - total;
    if (a.valign === 'center') y = a.y + (a.h - total) / 2;
    draw(ctx, t, { x: a.x, y, maxW: a.w, lh: a.tLh, align: a.align, font: a.tFont, color: a.tColor, emColor: a.emColor, emBox: a.emBox, ascent: a.ascent });
    if (b) draw(ctx, b, { x: a.x, y: y + t.h + gap, maxW: a.bw || a.w, lh: a.bLh || 1.42, align: a.align, font: a.bFont, color: a.bColor, emColor: a.bEm || a.bColor });
    return { y, total };
  }

  function footer(ctx, W, H, s, f, color, accent, right) {
    const y = H - f.bottom - 18;
    ctx.fillStyle = accent; ctx.fillRect(96, y - 30, 56, 3);
    ctx.font = sans(600)(24); ctx.fillStyle = color; ctx.textAlign = 'left';
    spaced(ctx, HANDLE, 96, y + 6, 1.5, 'left');
    if (right) { ctx.font = sans(500)(24); spaced(ctx, right, W - 96, y + 6, 1.5, 'right'); }
  }

  function kickerRow(ctx, W, s, f, color, counterColor) {
    const y = f.top + 44;
    if (s.kicker) { ctx.font = sans(700)(23); ctx.fillStyle = color; spaced(ctx, String(s.kicker).toUpperCase(), 96, y, 4, 'left'); }
    if (s.total > 1) { ctx.font = sans(500)(23); ctx.fillStyle = counterColor || color; spaced(ctx, `${String(s.index).padStart(2, '0')} / ${String(s.total).padStart(2, '0')}`, W - 96, y, 3, 'right'); }
  }

  function contentBox(W, H, f, s, extraTop, extraBottom) {
    const top = f.top + (extraTop == null ? 150 : extraTop);
    const bottom = H - f.bottom - (extraBottom == null ? 130 : extraBottom) - (s.sticker ? 430 : 0);
    return { x: 96, y: top, w: W - 192, h: bottom - top };
  }

  // ---------- estilos ----------
  const draws = {
    editorial(ctx, W, H, s, f) {
      const v = s.variant || 'meio';
      const bg = v === 'capa' ? C.vinho : v === 'final' ? C.preto : (s.theme === 'escuro' ? C.preto : C.off);
      const dark = bg !== C.off;
      ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
      grain(ctx, W, H, dark ? 0.06 : 0.05, dark);
      ctx.strokeStyle = dark ? 'rgba(176,141,87,.55)' : 'rgba(107,30,46,.25)'; ctx.lineWidth = 2;
      ctx.strokeRect(40, 40, W - 80, H - 80);
      const ink = dark ? C.off : C.preto; const acc = dark ? C.dourado : C.vinho;
      kickerRow(ctx, W, s, f, acc, dark ? 'rgba(246,241,234,.7)' : C.cinza);
      const box = contentBox(W, H, f, s);
      if (v === 'capa') {
        ctx.font = `italic 400 ${Math.round(W * 0.5)}px ${F.serif}`; ctx.fillStyle = 'rgba(246,241,234,.06)'; ctx.textAlign = 'left';
        ctx.fillText('“', W - 420, f.top + 520);
      }
      textStack(ctx, s, Object.assign({}, box, {
        tFont: serif(v === 'meio' ? 600 : 700), tMax: v === 'capa' ? 128 : v === 'final' ? 100 : 96, tLh: 1.08,
        tColor: ink, emColor: v === 'capa' ? C.bege : acc, align: 'left',
        valign: v === 'capa' ? 'bottom' : 'center',
        bFont: sans(400), bColor: dark ? 'rgba(246,241,234,.86)' : '#3A3330', bEm: acc
      }));
      footer(ctx, W, H, s, f, dark ? C.off : C.preto, C.dourado, v === 'capa' ? 'ARRASTA  →' : s.footer || '');
    },

    jornalistico(ctx, W, H, s, f) {
      const claro = s.theme === 'claro';
      ctx.fillStyle = claro ? C.off : C.preto; ctx.fillRect(0, 0, W, H);
      grain(ctx, W, H, 0.07, !claro);
      const ink = claro ? C.preto : C.off;
      // selo
      const label = String(s.kicker || 'PAUTA').toUpperCase();
      ctx.font = cond()(44); const lw = ctx.measureText(label).width + 48;
      ctx.fillStyle = C.vinho; ctx.fillRect(96, f.top + 6, lw, 70);
      ctx.fillStyle = C.off; ctx.textAlign = 'left'; ctx.fillText(label, 120, f.top + 60);
      if (s.date) { ctx.font = sans(600)(22); ctx.fillStyle = claro ? C.cinza : C.cinzaClaro; spaced(ctx, String(s.date).toUpperCase(), 96 + lw + 24, f.top + 52, 3, 'left'); }
      if (s.total > 1) { ctx.font = sans(600)(22); ctx.fillStyle = claro ? C.cinza : C.cinzaClaro; spaced(ctx, `${s.index}/${s.total}`, W - 96, f.top + 52, 3, 'right'); }
      ctx.fillStyle = claro ? 'rgba(15,13,13,.85)' : 'rgba(246,241,234,.85)'; ctx.fillRect(96, f.top + 110, W - 192, 4);
      const box = contentBox(W, H, f, s, 170, 150);
      textStack(ctx, s, Object.assign({}, box, {
        tFont: cond(), tMax: 156, tMin: 48, tLh: 1.16, upper: true, ascent: 0.96,
        tColor: claro ? C.preto : C.off, emColor: C.off, emBox: C.vinho, align: 'left', valign: 'top', gap: 52,
        bFont: sans(500), bMax: 38, bColor: claro ? '#3A3330' : C.cinzaClaro, bEm: claro ? C.vinho : C.off
      }));
      const y = H - f.bottom - 40;
      ctx.fillStyle = claro ? 'rgba(15,13,13,.25)' : 'rgba(246,241,234,.25)'; ctx.fillRect(96, y - 46, W - 192, 2);
      ctx.font = sans(500)(22); ctx.fillStyle = claro ? C.cinza : C.cinzaClaro;
      if (s.source) spaced(ctx, ('FONTE: ' + s.source).toUpperCase(), 96, y, 1.5, 'left');
      ctx.font = sans(700)(24); ctx.fillStyle = ink; spaced(ctx, HANDLE, W - 96, y, 1.5, 'right');
    },

    minimal(ctx, W, H, s, f) {
      const escuro = s.theme === 'escuro' || s.variant === 'final';
      const bg = s.theme === 'vinho' ? C.vinho : escuro ? C.preto : C.bege;
      const dark = bg !== C.bege;
      ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
      grain(ctx, W, H, 0.05, dark);
      const ink = dark ? C.off : C.preto; const acc = dark ? C.dourado : C.vinho;
      if (s.kicker) { ctx.font = sans(600)(22); ctx.fillStyle = dark ? 'rgba(246,241,234,.7)' : 'rgba(15,13,13,.6)'; spaced(ctx, String(s.kicker).toUpperCase(), 96, f.top + 44, 5, 'left'); }
      if (s.total > 1) { ctx.font = sans(500)(22); ctx.fillStyle = dark ? 'rgba(246,241,234,.6)' : 'rgba(15,13,13,.5)'; spaced(ctx, `${s.index}/${s.total}`, W - 96, f.top + 44, 3, 'right'); }
      const box = contentBox(W, H, f, s, 200, 170);
      textStack(ctx, s, Object.assign({}, box, {
        tFont: serif(400), tMax: 112, tLh: 1.1, tColor: ink, emColor: acc, align: 'left', valign: 'center', titleShare: 0.66,
        bFont: sans(400), bMax: big(s) ? 48 : 36, bColor: dark ? 'rgba(246,241,234,.8)' : 'rgba(15,13,13,.75)', bEm: acc
      }));
      ctx.font = sans(600)(22); ctx.fillStyle = ink; spaced(ctx, HANDLE, 96, H - f.bottom - 18, 2, 'left');
    },

    colagem(ctx, W, H, s, f) {
      const r = rng(hash(String(s.title) + (s.index || 0)));
      ctx.fillStyle = C.bege; ctx.fillRect(0, 0, W, H);
      grain(ctx, W, H, 0.1, false);
      // círculo vinho
      ctx.fillStyle = C.vinho; ctx.beginPath(); ctx.arc(W * (0.82 + r() * 0.1), f.top + 120 + r() * 80, W * 0.36, 0, Math.PI * 2); ctx.fill();
      // faixa dourada
      ctx.save(); ctx.translate(0, H * 0.86); ctx.rotate(-0.05); ctx.fillStyle = 'rgba(176,141,87,.55)'; ctx.fillRect(-40, 0, W + 80, 54); ctx.restore();
      // papel rasgado
      const px = 70, pw = W - 140; const box0 = contentBox(W, H, f, s, 230, 190);
      const py = box0.y - 60, ph = box0.h + 120;
      const ang = (r() - 0.5) * 0.05;
      ctx.save(); ctx.translate(W / 2, py + ph / 2); ctx.rotate(ang); ctx.translate(-W / 2, -(py + ph / 2));
      ctx.shadowColor = 'rgba(0,0,0,.22)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 12;
      ctx.fillStyle = C.off; ctx.beginPath();
      const step = 26; ctx.moveTo(px, py);
      for (let x = px; x <= px + pw; x += step) ctx.lineTo(x, py + (r() - 0.5) * 12);
      ctx.lineTo(px + pw, py + ph);
      for (let x = px + pw; x >= px; x -= step) ctx.lineTo(x, py + ph + (r() - 0.5) * 16);
      ctx.closePath(); ctx.fill(); ctx.shadowColor = 'transparent';
      // fitas
      ctx.fillStyle = 'rgba(205,184,157,.75)';
      [[px + 40, py - 18, -0.3], [px + pw - 170, py - 14, 0.25]].forEach(([x, y, a]) => { ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.fillRect(0, 0, 150, 44); ctx.restore(); });
      const box = { x: px + 56, y: py + 70, w: pw - 112, h: ph - 140 };
      textStack(ctx, s, Object.assign({}, box, {
        tFont: serif(700), tMax: 104, tLh: 1.08, tColor: C.preto, emColor: C.vinho, align: 'left', valign: 'center',
        bFont: sans(400), bMax: big(s) ? 46 : 36, bColor: '#3A3330', bEm: C.vinho
      }));
      ctx.restore();
      // etiqueta recortada
      if (s.kicker) {
        ctx.save(); ctx.translate(96, f.top + 40); ctx.rotate(-0.04);
        ctx.font = cond()(40); const label = String(s.kicker).toUpperCase(); const lw = ctx.measureText(label).width + 44;
        ctx.fillStyle = C.preto; ctx.fillRect(0, 0, lw, 66); ctx.fillStyle = C.off; ctx.fillText(label, 22, 52); ctx.restore();
      }
      if (s.total > 1) { ctx.font = sans(700)(24); ctx.fillStyle = C.off; spaced(ctx, `${s.index}/${s.total}`, W - 96, f.top + 84, 3, 'right'); }
      ctx.font = sans(700)(24); ctx.fillStyle = C.preto; spaced(ctx, HANDLE, 96, H - f.bottom - 18, 2, 'left');
    },

    lifestyle(ctx, W, H, s, f) {
      if (s.photo) cover(ctx, s.photo, 0, 0, W, H);
      else {
        const g = ctx.createRadialGradient(W * 0.3, H * 0.25, 40, W * 0.5, H * 0.5, H * 0.8);
        g.addColorStop(0, C.vinhoClaro); g.addColorStop(0.55, C.vinhoEsc); g.addColorStop(1, C.preto);
        ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      }
      const gr = ctx.createLinearGradient(0, H * 0.35, 0, H);
      gr.addColorStop(0, 'rgba(15,13,13,0)'); gr.addColorStop(1, 'rgba(15,13,13,.88)');
      ctx.fillStyle = gr; ctx.fillRect(0, 0, W, H);
      grain(ctx, W, H, 0.07, true);
      kickerRow(ctx, W, s, f, C.dourado, 'rgba(246,241,234,.75)');
      const box = contentBox(W, H, f, s, 380);
      textStack(ctx, s, Object.assign({}, box, {
        tFont: serif(600), tMax: 100, tLh: 1.08, tColor: C.off, emColor: C.bege, align: 'left', valign: 'bottom',
        bFont: sans(400), bMax: big(s) ? 48 : 36, bColor: 'rgba(246,241,234,.88)', bEm: C.bege
      }));
      footer(ctx, W, H, s, f, C.off, C.dourado, s.variant === 'capa' ? 'ARRASTA  →' : '');
    },

    // texto para sobrepor ao vídeo do Reel de 7 segundos (fundo transparente)
    overlay(ctx, W, H, s) {
      const pos = s.textPos || 'topo';
      const maxW = W - 220;
      const st = s.overlayStyle || 'caixa';
      const font = st === 'serif' ? serif(600) : st === 'creme' ? serif(500) : sans(700);
      const block = fit(ctx, s.title, { font, max: st === 'serif' ? 76 : st === 'creme' ? 92 : 62, min: 36, lh: st === 'creme' ? 1.08 : 1.22, maxW: maxW - 96, maxH: 620 });
      const bw = block.widest + 96, bh = block.h + 76;
      const x = (W - bw) / 2;
      const y = pos === 'centro' ? (H - bh) / 2 - 80 : pos === 'base' ? H - 560 - bh : 300;
      if (st === 'creme') { ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 2; }
      else if (st !== 'sombra') {
        ctx.fillStyle = st === 'serif' ? 'rgba(107,30,46,.94)' : 'rgba(246,241,234,.96)';
        roundRect(ctx, x, y, bw, bh, 22); ctx.fill();
      } else { ctx.shadowColor = 'rgba(0,0,0,.65)'; ctx.shadowBlur = 18; }
      draw(ctx, block, { x: x + 48, y: y + 38, maxW: bw - 96, lh: st === 'creme' ? 1.08 : 1.22, align: 'center', font,
        color: st === 'caixa' ? C.preto : st === 'creme' ? '#F4E9C8' : C.off, emColor: st === 'caixa' ? C.vinho : st === 'creme' ? '#F4E9C8' : C.bege });
      ctx.shadowColor = 'transparent';
    }
  };

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }

  async function ready() {
    if (!root.document || !document.fonts) return;
    const specs = ['600 40px "Bodoni Moda"', 'italic 600 40px "Bodoni Moda"', '700 40px "Bodoni Moda"', 'italic 700 40px "Bodoni Moda"',
      '400 40px "Bodoni Moda"', 'italic 400 40px "Bodoni Moda"', '400 40px "Archivo"', '500 40px "Archivo"', '600 40px "Archivo"',
      '700 40px "Archivo"', 'italic 700 40px "Archivo"', 'italic 400 40px "Archivo"', '400 40px "Anton"'];
    await Promise.all(specs.map(sp => document.fonts.load(sp, 'ÁÉÍÓÚçãõ Aa').catch(() => null)));
  }

  function render(spec, canvas) {
    const f = FORMATS[spec.format] || FORMATS.carrossel;
    const cv = canvas || document.createElement('canvas');
    cv.width = f.w; cv.height = f.h;
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, f.w, f.h);
    ctx.textAlign = 'left';
    const style = spec.format === 'overlay' ? 'overlay' : (STYLES.includes(spec.style) ? spec.style : 'editorial');
    draws[style](ctx, f.w, f.h, spec, f);
    return cv;
  }

  function slug(t) { return String(t || 'conteudo').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40); }

  // transforma um conteúdo da Central na lista de artes a gerar
  function specsFor(c) {
    const p = c.payload || {}; const base = slug(c.slug || c.title); const style = c.style || 'editorial';
    const kicker = c.seriesName || p.kicker || '';
    if (c.type === 'carrossel') {
      const cards = p.cards || []; const n = cards.length;
      return cards.map((cd, i) => ({ name: `${base}-card-${String(i + 1).padStart(2, '0')}.png`, spec: {
        format: 'carrossel', style: cd.style || style, theme: cd.theme, variant: i === 0 ? 'capa' : i === n - 1 ? 'final' : 'meio',
        kicker: cd.kicker || kicker, title: cd.title, body: cd.body, index: i + 1, total: n, source: cd.source, date: cd.date } }));
    }
    if (c.type === 'stories') {
      const st = p.stories || []; const n = st.length;
      return st.map((s, i) => ({ name: `${base}-story-${String(i + 1).padStart(2, '0')}.png`, spec: {
        format: 'story', style: s.style || style, theme: s.theme, variant: s.variant || 'meio', kicker: s.kicker || '',
        title: s.texto, body: s.apoio, index: i + 1, total: n, sticker: !!(s.sticker && s.sticker.tipo) } }));
    }
    if (c.type === 'estatico') {
      const cd = p.card || {};
      return [{ name: `${base}-post.png`, spec: { format: 'estatico', style: cd.style || style, theme: cd.theme, variant: cd.variant || 'final',
        kicker: cd.kicker || kicker, title: cd.title, body: cd.body, source: cd.source, date: cd.date } }];
    }
    if (c.type === 'reel7') {
      return [{ name: `${base}-texto-na-tela.png`, spec: { format: 'overlay', title: p.frase, textPos: p.posicaoTexto || 'topo', overlayStyle: p.estiloTexto || 'caixa' } }];
    }
    if (c.type === 'reelFalado') {
      return [{ name: `${base}-capa.png`, spec: { format: 'capa', style, theme: p.temaCapa, variant: 'capa', kicker, title: p.textoCapa } }];
    }
    return [];
  }

  root.NCRender = { C, F, FORMATS, STYLES, ready, render, specsFor, slug };
})(typeof window !== 'undefined' ? window : globalThis);
