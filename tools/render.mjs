// Produção automática: lê um arquivo de conteúdos e gera as artes finais
// (PNG nas dimensões do Instagram), os textos de apoio e a prévia em MP4 do Reel de 7s.
// Uso: node tools/render.mjs conteudos/primeiro-teste.json prontos-para-publicar/2026-10-30-primeiro-teste
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const { chromium } = createRequire(import.meta.url)('playwright');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [, , input, outDir] = process.argv;
if (!input || !outDir) { console.error('uso: node tools/render.mjs <conteudos.json> <pasta-de-saida>'); process.exit(1); }
const contents = JSON.parse(fs.readFileSync(input, 'utf8'));
const OUT = path.resolve(outDir);
fs.mkdirSync(OUT, { recursive: true });

const faces = [
  ['Bodoni Moda', 400, 'normal', 'bodoni-moda-latin-400-normal'], ['Bodoni Moda', 400, 'italic', 'bodoni-moda-latin-400-italic'],
  ['Bodoni Moda', 600, 'normal', 'bodoni-moda-latin-600-normal'], ['Bodoni Moda', 600, 'italic', 'bodoni-moda-latin-600-italic'],
  ['Bodoni Moda', 700, 'normal', 'bodoni-moda-latin-700-normal'], ['Bodoni Moda', 700, 'italic', 'bodoni-moda-latin-700-italic'],
  ['Archivo', 400, 'normal', 'archivo-latin-400-normal'], ['Archivo', 400, 'italic', 'archivo-latin-400-italic'],
  ['Archivo', 500, 'normal', 'archivo-latin-500-normal'], ['Archivo', 600, 'normal', 'archivo-latin-600-normal'],
  ['Archivo', 700, 'normal', 'archivo-latin-700-normal'], ['Archivo', 700, 'italic', 'archivo-latin-700-italic'],
  ['Anton', 400, 'normal', 'anton-latin-400-normal']
];
const css = faces.map(([fam, w, st, file]) =>
  `@font-face{font-family:"${fam}";font-weight:${w};font-style:${st};src:url("file://${ROOT}/modelos/fontes/${file}.woff2") format("woff2")}`).join('\n');
const tmp = path.join(OUT, '.render.html');
fs.writeFileSync(tmp, `<!doctype html><meta charset="utf-8"><style>${css}</style><script src="file://${ROOT}/modelos/renderer.js"></script>`);

const clean = (t) => String(t || '').replace(/\*/g, '');
const ts = (s) => { const h = String(Math.floor(s / 3600)).padStart(2, '0'); const m = String(Math.floor(s / 60) % 60).padStart(2, '0'); const ss = String(Math.floor(s % 60)).padStart(2, '0'); return `${h}:${m}:${ss},000`; };

function textoDeApoio(c) {
  const p = c.payload; const L = [`# ${clean(c.title)}`, '', `Formato: ${c.type} · Objetivo: ${c.objective}${c.seriesName ? ` · Série: ${c.seriesName}` : ''}`, ''];
  if (c.validarOpiniao) L.push(`> Validar: ${c.validarOpiniao}`, '');
  if (c.perguntaPessoal) L.push(`> Preciso de você: ${c.perguntaPessoal}`, '');
  if (c.type === 'reel7') {
    L.push('## Frase na tela', clean(p.frase), '', '## Versões alternativas', ...p.alternativas.map(a => `- ${clean(a)}`), '',
      '## Cena para gravar', p.cena, '', '## Texto', `Posição: ${p.posicaoTexto}. ${p.estiloVisual}`, '', '## Trilha', p.trilha, '');
  }
  if (c.type === 'reelFalado') {
    L.push('## Gancho (3 primeiros segundos)', p.gancho, '', '## Roteiro', ...p.roteiro.map(b => `**${b.inicio}s a ${b.fim}s.** ${b.fala}`), '',
      '## Como gravar', ...p.orientacoes.map(o => `- ${o}`), '', '## Texto da capa', clean(p.textoCapa), '',
      '## Cortes sugeridos', ...p.cortes.map(o => `- ${o}`), '', '## Fundamentos conferidos', p.fundamentos, '');
  }
  if (c.type === 'carrossel') L.push('## Cards', ...p.cards.map((cd, i) => `${i + 1}. ${clean(cd.title)}${cd.body ? ` | ${clean(cd.body)}` : ''}`), '');
  if (c.type === 'stories') L.push('## Sequência', ...p.stories.map((s, i) => `${i + 1}. ${clean(s.texto)}${s.apoio ? ` | ${clean(s.apoio)}` : ''}\n   Figurinha: ${s.sticker?.tipo || 'nenhuma'}${s.sticker?.opcoes ? ` (${s.sticker.opcoes.join(' / ')})` : ''}${s.sticker?.pergunta ? `: "${s.sticker.pergunta}"` : ''}. ${s.orientacao || ''}`), '');
  if (p.legenda) L.push('## Legenda', clean(p.legenda), '');
  L.push('## CTA', p.cta, '', '## Objetivo estratégico', p.objetivoEstrategico, '');
  return L.join('\n');
}

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file://' + tmp);
await page.evaluate(() => NCRender.ready());
const report = [];

for (const [i, c] of contents.entries()) {
  const dir = path.join(OUT, `${String(i + 1).padStart(2, '0')}-${c.slug}`);
  fs.mkdirSync(dir, { recursive: true });
  const files = await page.evaluate((content) => NCRender.specsFor(content).map(({ name, spec }) => {
    const cv = NCRender.render(spec); return { name, w: cv.width, h: cv.height, data: cv.toDataURL('image/png') };
  }), c);
  for (const f of files) {
    fs.writeFileSync(path.join(dir, f.name), Buffer.from(f.data.split(',')[1], 'base64'));
    report.push(`${path.relative(OUT, path.join(dir, f.name))}  ${f.w}x${f.h}`);
  }
  fs.writeFileSync(path.join(dir, 'textos.md'), textoDeApoio(c));
  if (c.type === 'reelFalado') {
    const srt = c.payload.roteiro.map((b, k) => `${k + 1}\n${ts(b.inicio)} --> ${ts(b.fim)}\n${b.fala}\n`).join('\n');
    fs.writeFileSync(path.join(dir, 'legendas-revisaveis.srt'), srt);
  }
  if (c.type === 'reel7') {
    // prévia de montagem: cena provisória + texto, 7s, 1080x1920, sem áudio (trilha entra pelo Instagram)
    const scene = await page.evaluate(() => NCRender.render({ format: 'story', style: 'lifestyle', kicker: '', title: '' }).toDataURL('image/png'));
    const scenePath = path.join(dir, '.cena-provisoria.png');
    fs.writeFileSync(scenePath, Buffer.from(scene.split(',')[1], 'base64'));
    const overlay = path.join(dir, files[0].name);
    const mp4 = path.join(dir, `${c.slug}-previa.mp4`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-loop', '1', '-i', scenePath, '-loop', '1', '-i', overlay, '-filter_complex',
      "[0:v]scale=1188:2112,zoompan=z='min(zoom+0.0005,1.08)':d=210:s=1080x1920:fps=30[bg];[1:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1[tx];[bg][tx]overlay=0:0,format=yuv420p[v]",
      '-map', '[v]', '-t', String(c.payload.duracao || 7), '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-movflags', '+faststart', mp4]);
    fs.unlinkSync(scenePath);
    report.push(`${path.relative(OUT, mp4)}  vídeo`);
  }
}
await browser.close();
fs.unlinkSync(tmp);
console.log(report.join('\n'));
