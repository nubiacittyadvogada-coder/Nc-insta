import subprocess,sys,json,textwrap
Q='/tmp/claude-0/-home-user/35e900c0-5567-55e2-9b5c-894faf2df1c8/scratchpad/qc/'
FONT='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
def build(src,segs,hook,out,hookdur=3.2):
    # segs: list of (start,end)
    fc=[];n=len(segs)
    for i,(a,b) in enumerate(segs):
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
        d=b-a
        fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={max(0,d-0.04)}:d=0.04[a{i}]")
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n))+f"concat=n={n}:v=1:a=1[vc][ac]")
    lines=hook.split('|')
    y0=105; draw=[]
    # dark box
    draw.append(f"drawbox=x=0:y=55:w=iw:h={len(lines)*72+110}:color=0x0E0C0C@0.93:t=fill:enable='lt(t,{hookdur})'")
    for j,l in enumerate(lines):
        l=l.replace("'", "’").replace(':','\\:')
        draw.append(f"drawtext=fontfile={FONT}:text='{l}':fontsize=56:fontcolor={'0xE8C482' if j==len(lines)-1 else 'white'}:x=(w-text_w)/2:y={y0+j*72}:enable='lt(t,{hookdur})'")
    fc.append('[vc]'+','.join(draw)+'[vo]')
    cmd=['ffmpeg','-v','error','-y','-i',Q+src,'-filter_complex',';'.join(fc),'-map','[vo]','-map','[ac]',
         '-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
         '-c:a','aac','-b:a','192k','-movflags','+faststart',out]
    subprocess.run(cmd,check=True)
J=json.loads(sys.argv[1])
build(**J)
