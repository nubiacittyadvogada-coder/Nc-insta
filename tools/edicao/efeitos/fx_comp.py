"""Composição com o motor de efeitos (06/11/2026).

Uso: python3 fx_comp.py PASTA saida.mp4 [--paper 44,50.8] [--clip arquivo.mp4,inicio,ycorte,duracao] [--logo]
A PASTA precisa ter: cut.mp4 (cortado, sem 1,1x), mask.mp4, fxbg/ e fxfg/ (quadros do fx_engine.html),
fr/ (legendas e textos do overlay_min.py). Tempos na linha do corte (antes do 1,1x).
--paper: janelas de "recorte de papel" (contorno branco atrás da pessoa). Pode repetir.
--clip: vídeo na metade de cima (cena de referência), pessoa embaixo.
"""
import subprocess, sys, os, argparse
ap = argparse.ArgumentParser()
ap.add_argument('d'); ap.add_argument('out')
ap.add_argument('--paper', action='append', default=[])
ap.add_argument('--clip', default=None)
a = ap.parse_args(); D = a.d
GR = "format=rgb24,colorbalance=rs=0.015:bs=-0.02:rm=0.025:bm=-0.025:rh=0.01:bh=-0.01,eq=contrast=1.06:brightness=0.01:saturation=1.03,curves=all='0/0.03 0.5/0.505 1/0.975',format=gbrp"
ins = ['-i', f'{D}/cut.mp4', '-i', f'{D}/mask.mp4', '-framerate', '30', '-i', f'{D}/fxbg/f%04d.png', '-framerate', '30', '-i', f'{D}/fxfg/f%04d.png', '-framerate', '30', '-i', f'{D}/fr/f%04d.png']
T = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{D}/cut.mp4']))
fc = [f"[0:v]{GR},vignette=PI/4.8,split=2[sharp][b0]",
      "[b0]gblur=sigma=6,eq=brightness=-0.03:saturation=0.88,format=rgba[bgb]",
      "[bgb][2:v]overlay=0:0:eof_action=pass,format=rgba[bg1]",
      "[1:v]format=gray,split=2[m1][m2]",
      "[m1]dilation,dilation,dilation,dilation,dilation,dilation,dilation,gblur=sigma=4,format=gbrp[mk]"]
if a.paper:
    en = '+'.join(f"between(t,{p.split(',')[0]},{p.split(',')[1]})" for p in a.paper)
    fc += ["[m2]" + ",".join(["dilation"] * 16) + ",gblur=sigma=1.5[pm]", f"color=c=white:s=1080x1920:r=30:d={T + 1},format=rgba[wh]", "[wh][pm]alphamerge[paper]", f"[bg1][paper]overlay=0:0:enable='{en}',format=gbrp[bg]"]
else:
    fc += ["[m2]nullsink", "[bg1]format=gbrp[bg]"]
fc += ["[bg][sharp][mk]maskedmerge[dof]", "[dof]noise=alls=3:allf=t,format=rgba[v0]"]
cur = 'v0'
if a.clip:
    f, t0, yc, du = a.clip.split(','); t0, du = float(t0), float(du)
    ins += ['-i', f]; n = 5
    en = f"between(t,{t0},{t0 + du})"
    fc += [f"[{cur}]split=2[pa][pb]", f"[pb]crop=1080:960:0:{yc}[pbot]", f"[{n}:v]format=rgba,setpts=PTS+{t0}/TB[clp]",
           f"[pa][pbot]overlay=0:960:enable='{en}'[pm2]", f"[pm2][clp]overlay=0:0:eof_action=pass:enable='{en}'[vc]"]
    cur = 'vc'
fc += [f"[{cur}][3:v]overlay=0:0:eof_action=pass[v1]", "[v1][4:v]overlay=0:0:eof_action=pass,setpts=PTS/1.1,fps=30,format=yuv420p[o]"]
t = T / 1.1; br = min(int(19 * 2**20 * 8 / t) - 200000, 6_000_000)
# ERRO REAL 06/11/2026: atempo dentro do mesmo filter_complex deixava o áudio até 3 s atrasado.
# Agora: vídeo sem áudio, áudio acelerado à parte, e junção com -shortest.
vtmp, atmp = a.out + '.v.mp4', a.out + '.a.m4a'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-threads', '4'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[o]', '-an', '-c:v', 'libx264', '-b:v', str(br), '-maxrate', str(int(br * 1.3)), '-bufsize', str(br * 2), '-preset', 'medium', vtmp], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/cut.mp4', '-vn', '-filter:a', 'atempo=1.1', '-c:a', 'aac', '-b:a', '128k', atmp], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vtmp, '-i', atmp, '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', '-movflags', '+faststart', a.out], check=True)
os.remove(vtmp); os.remove(atmp)
print(a.out, round(os.path.getsize(a.out) / 2**20, 1), 'MiB')
