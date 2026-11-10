"""Assinatura final com a logo do NC.

Uso: python3 endcard.py entrada.mp4 saida.mp4 [segundos=1.8]

Acrescenta ao fim do vídeo um cartão escuro liso com a logo completa (tools/edicao/marca/nc-logo-completa-branca.png) entrando em
fade. O áudio termina em fade e o cartão fica em silêncio.
Padrão de 05/11/2026: vale para TODOS os vídeos do NC Advogados.
"""
import subprocess, sys, os, json

src, out = sys.argv[1], sys.argv[2]
dur = float(sys.argv[3]) if len(sys.argv) > 3 else 1.8
here = os.path.dirname(os.path.abspath(__file__))
logo = os.path.join(here, 'marca', 'nc-logo-completa-branca.png')

info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', src]))
T = float(info['format']['duration'])
v = [s for s in info['streams'] if s['codec_type'] == 'video'][0]
W, H = v['width'], v['height']
has_a = any(s['codec_type'] == 'audio' for s in info['streams'])
lw = int(W * 0.46) // 2 * 2
br = int(os.path.getsize(src) * 8 / T * 0.95)
# teto para o arquivo final ficar abaixo de ~19 MiB (limite de 20 MiB do app)
br = min(br, int(19 * 2**20 * 8 / (T + dur)) - 160_000)

fc = (
    f"[0:v]fps=30,setsar=1,format=yuv420p[main];"
    f"color=c=0x0F0D0C:s={W}x{H}:r=30:d={dur},format=yuv420p,setsar=1[bg];"
    f"[1:v]scale={lw}:-1,format=rgba,fade=t=in:st=0.15:d=0.5:alpha=1[lg];"
    f"[bg][lg]overlay=(W-w)/2:(H-h)/2-40:shortest=1,format=yuv420p[card];"
    f"[main][card]concat=n=2:v=1:a=0[vo]"
)
cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src, '-loop', '1', '-t', str(dur), '-i', logo]
if has_a:
    fc += (f";[0:a]afade=t=out:st={max(0, T - 0.35):.3f}:d=0.35,aresample=48000[a0];"
           f"anullsrc=r=48000:cl=stereo,atrim=duration={dur}[a1];[a0][a1]concat=n=2:v=0:a=1[ao]")
    cmd += ['-filter_complex', fc, '-map', '[vo]', '-map', '[ao]', '-c:a', 'aac', '-b:a', '128k']
else:
    cmd += ['-filter_complex', fc, '-map', '[vo]']
# qualidade (10/11/2026): CRF 18 com teto de 8 Mbps e cor marcada como BT.709; o limite antigo de 3,4 Mbps borrava e o arquivo sem marcação de cor saía com tom errado no Instagram
cmd += ['-c:v', 'libx264', '-crf', '18', '-maxrate', '8M', '-bufsize', '16M', '-profile:v', 'high',
        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
        '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True)
print(out, round(os.path.getsize(out) / 2**20, 1), 'MiB')
