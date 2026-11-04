import json,subprocess
R='/tmp/claude-0/-home-user/35e900c0-5567-55e2-9b5c-894faf2df1c8/scratchpad/'
d=json.load(open('jr-v2.json')); PY=[260,380,470]; BY={'lavoura':200,'certidao':600,'documentos':480}
GR="format=rgb24,colorbalance=rs=0.015:bs=-0.02:rm=0.025:bm=-0.025:rh=0.01:bh=-0.01,eq=contrast=1.08:brightness=0.015:saturation=1.04,curves=all='0/0.035 0.5/0.51 1/0.975',format=gbrp"
ins=['-i','cut.mp4','-i','mask.mp4','-framerate','30','-i','fr/f%04d.png']
n=len(d['splits'])
fc=[f"[0:v]{GR},split=2[sharp][b0]","[b0]gblur=sigma=6,eq=brightness=-0.03:saturation=0.88,format=gbrp[bg]","[1:v]format=gray,dilation,dilation,dilation,dilation,dilation,dilation,dilation,gblur=sigma=4,format=gbrp[mk]","[bg][sharp][mk]maskedmerge[dof]",f"[dof]vignette=PI/4.8,noise=alls=4:allf=t,format=yuv420p,split={n+1}[v0]"+''.join(f'[p{i}]' for i in range(n))]
cur='v0'
for i,(t0,t1,tag,name) in enumerate(d['splits']):
    ins+=['-i',R+f'broll/{name}.mp4']; e=f"enable='between(t,{t0},{t1})'"
    fc+= [f"[p{i}]crop=1080:960:0:{PY[i]}[top{i}]",f"[{3+i}:v]crop=1080:960:0:{BY[name]},setpts=PTS+{t0}/TB[br{i}]",f"[{cur}][top{i}]overlay=0:0:{e}[m{i}]",f"[m{i}][br{i}]overlay=0:960:eof_action=pass:{e}[s{i}]"]; cur=f's{i}'
fc.append(f"[{cur}][2:v]overlay=0:0:eof_action=pass,setpts=PTS/1.1,fps=30,format=yuv420p[o]");fc.append("[0:a]atempo=1.1[ao]")
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fc),'-map','[o]','-map','[ao]','-c:v','libx264','-crf','23','-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart','final.mp4'],check=True)
