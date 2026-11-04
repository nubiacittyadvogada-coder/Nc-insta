import json,subprocess
W=json.load(open('w.json'))
FIX={'Ela':'Você','NSS':'INSS','vaga.':'basta.','mante':'mande','Mateus,':'Matheus,','NCA':'NC','Devogado.':'Advogados.'}
CL=[(0.15,3.72),(4.3,7.1),(7.28,14.0),(14.2,17.8),(17.8,21.42),(21.9,30.85),(41.8,48.66),(49.05,52.62),(60.25,65.36),(65.6,68.8),(69.1,72.5)]
Z=[1.0,1.18,1.0,1.32]; CY=660
KW={'roça','aposentadoria.','1991','INSS','testemunha','documento','lavrador.','papéis.','roça.','sindicato','rural.'}
t=0;words=[];parts=[];mparts=[];vi=[];offs=[]
for j,(a,b) in enumerate(CL):
    z=Z[j%4];w=round(1080/z/2)*2;h=round(1920/z/2)*2;y=int(min(max(CY-h/2,0),1920-h));x=(1080-w)//2
    crop=f"trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps=30,crop={w}:{h}:{x}:{y},scale=1080:1920"
    parts.append(f"[0:v]{crop}[v{j}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{j}]");vi.append(f"[v{j}][a{j}]")
    mparts.append(f"[0:v]{crop}[m{j}]")
    occupied=False
    for wd,s,e in W:
        if s>=a-0.02 and s<b-0.05:
            wd=FIX.get(wd,wd)
            if wd=='produção' and s<50: wd='produção,'
            if wd=='NC' : pass
            words.append([wd,round(t+max(0,s-a),2),1 if wd in KW else 0])
    offs.append(t); t+=b-a
total=round(t,2)
# merge 'NC' 'Advogados.'
# pages: <=6 words, break at punctuation
pages=[];cur=[]
for i,wd in enumerate(words):
    cur.append(wd)
    nxt=words[i+1][1] if i+1<len(words) else total
    if len(cur)==6 or wd[0][-1] in '.?!' or (wd[0][-1] in ',:' and len(cur)>=2) or nxt-wd[1]>1.3 or i==len(words)-1:
        pages.append(dict(a=cur[0][1],b=round(min(nxt,wd[1]+1.2),2),w=cur));cur=[]
def ct(raw,j): return round(offs[j]+raw-CL[j][0],2)
splits=[[ct(7.58,2),ct(7.58,2)+1.6,'TRABALHO RURAL','lavoura'],[ct(24.48,5),ct(24.48,5)+1.6,'CERTIDÕES DA ÉPOCA','certidao'],[ct(51.12,7),ct(51.12,7)+1.6,'REÚNA OS PAPÉIS','documentos']]
D=dict(pages=pages,splits=splits,steps=[],flash=[],cta=ct(65.6,9),total=total,serie=[3.6,6.75])
json.dump(D,open('jr-v2.json','w'),ensure_ascii=False)
fc=';'.join(parts)+';'+''.join(vi)+f"concat=n={len(CL)}:v=1:a=1[vv][aa];[aa]loudnorm=I=-15:TP=-1.5:LRA=11[ao]"
subprocess.run(['ffmpeg','-v','error','-y','-i','raw.mp4','-filter_complex',fc,'-map','[vv]','-map','[ao]','-c:v','libx264','-crf','14','-preset','fast','-c:a','aac','-b:a','192k','cut.mp4'],check=True)
N=len(CL)
mfc="[0:v]format=gray[g0];[1:v]format=gray,fps=30[mk];[g0][mk]blend=all_mode=lighten,split=%d"%N+''.join(f'[i{j}]' for j in range(N))+';'+';'.join(p.replace('[0:v]',f'[i{j}]',1) for j,p in enumerate(mparts))+';'+''.join(f'[m{j}]' for j in range(N))+f"concat=n={N}:v=1:a=0,format=gray[mm]"
subprocess.run(['ffmpeg','-v','error','-y','-i','rawmask.mp4','-loop','1','-t','73','-i','/home/user/Nc-insta/tools/edicao/mascara-mesa.png','-filter_complex',mfc,'-map','[mm]','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','mask.mp4'],check=True)
print(total,splits,D['cta']);print([' '.join(x[0] for x in p['w']) for p in pages])
