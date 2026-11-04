import json,sys
R='/tmp/claude-0/-home-user/35e900c0-5567-55e2-9b5c-894faf2df1c8/scratchpad/'
C={
'a':dict(js=R+'reed/a-v2.json',acc='#F0C3CC',bar='#8E2A3E',hook='Se prenderem alguém<br>da sua <i>família</i>',name='Núbia Citty',role='ADVOGADA CRIMINALISTA',cta='Salva e manda<br><i>para quem você ama</i>',at='@NUBIACITTY',serie=None),
'b':dict(js=R+'reed/b-v2.json',acc='#F0C3CC',bar='#8E2A3E',hook='A Constituição<br><i>só vale</i> pro seu primo?',name='Núbia Citty',role='ADVOGADA CRIMINALISTA',cta='Me conta<br><i>nos comentários</i>',at='@NUBIACITTY',serie=None),
'jr':dict(js=R+'jr/jr-v2.json',acc='#E3D2C3',bar='#D8C4B6',hook='Trabalhou na roça?<br>Esse tempo <i>pode contar</i>',name='José Matheus',role='ADVOGADO · NC ADVOGADOS',cta='Salve e mande<br><i>pra quem trabalhou na roça</i>',at='@NUBIACITTYADVOGADOS',nm=(7.0,10.2),serie=('PLANTÃO DO INSS','O que mexe na sua aposentadoria, explicado em um minuto.'))}
k=sys.argv[1];V=sys.argv[2] if len(sys.argv)>2 else 'A';c=C[k];D=json.load(open(c['js']))
D.setdefault('steps',[]);D.setdefault('flash',[])
F='file:///home/user/Nc-insta/modelos/fontes/'
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:A;font-weight:700;src:url("{F}archivo-latin-700-normal.woff2")}}
@font-face{{font-family:A;font-weight:600;src:url("{F}archivo-latin-600-normal.woff2")}}
@font-face{{font-family:S;font-weight:400;src:url("{F}bodoni-moda-latin-400-normal.woff2")}}@font-face{{font-family:S;font-style:italic;font-weight:400;src:url("{F}bodoni-moda-latin-400-italic.woff2")}}@font-face{{font-family:A;font-weight:500;src:url("{F}archivo-latin-500-normal.woff2")}}@font-face{{font-family:A;font-weight:400;src:url("{F}archivo-latin-400-normal.woff2")}}@font-face{{font-family:B;font-style:italic;font-weight:600;src:url("{F}bodoni-moda-latin-600-italic.woff2")}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:A;background:transparent}}
.g{{position:absolute;opacity:0}}
i{{font-family:B;font-style:italic;font-weight:600;color:{c['acc']};letter-spacing:0}}
.sh{{text-shadow:0 2px 6px rgba(0,0,0,.35),0 8px 30px rgba(0,0,0,.35)}}
#grad{{position:absolute;left:0;right:0;bottom:0;height:640px;background:linear-gradient(transparent,rgba(0,0,0,.32))}}
#hk{{left:90px;right:90px;top:250px;text-align:center;color:#fff;font-weight:700;font-size:62px;letter-spacing:-1.5px;line-height:1.08}}
#hk i{{font-size:70px}}
#se{{left:0;right:0;top:250px;text-align:center}}#se .k{{font-weight:600;font-size:20px;letter-spacing:.34em;color:#fff;opacity:.85}}#se .f{{margin:14px auto 0;width:760px;font-family:B;font-style:italic;font-weight:600;font-size:40px;line-height:1.15;color:#fff}}
#nm{{left:72px;top:1600px;color:#fff}}#nm .n{{font-weight:700;font-size:40px;letter-spacing:-.8px}}#nm .l{{width:56px;height:3px;background:{c['bar']};margin:12px 0 10px}}#nm .r{{font-weight:600;font-size:16px;letter-spacing:.3em;opacity:.85}}
#cap{{position:absolute;left:110px;right:110px;top:1360px;text-align:center;line-height:1.16}}
#cap .w{{display:inline-block;font-weight:600;font-size:54px;letter-spacing:-1px;color:rgba(255,255,255,.62);margin:0 5px}}
#cap .on{{color:#fff}}#cap .w i{{font-size:60px}}
#st{{left:72px;top:230px;display:flex;align-items:flex-end;gap:18px;color:#fff}}#st .n{{font-family:B;font-style:italic;font-weight:600;font-size:130px;line-height:.8;color:{c['acc']}}}
#st .k{{font-weight:600;font-size:17px;letter-spacing:.32em;opacity:.85}}#st .h{{font-weight:700;font-size:40px;letter-spacing:-1px;margin-top:6px}}#st .t{{padding-bottom:12px}}
#bar{{left:72px;top:400px;display:flex;gap:8px}}#bar i{{display:block;width:60px;height:3px;border-radius:2px;background:rgba(255,255,255,.35)}}#bar i.on{{background:#fff}}
#div{{left:0;top:958px;width:1080px;height:4px;background:{c['bar']}}}
#tag{{left:48px;top:996px;color:#fff;font-weight:600;font-size:18px;letter-spacing:.3em}}
#ct{{left:90px;right:90px;top:1330px;text-align:center;color:#fff;font-weight:700;font-size:54px;letter-spacing:-1.2px;line-height:1.12}}#ct i{{font-size:58px}}#ct .at{{margin-top:22px;font-weight:600;font-size:18px;letter-spacing:.32em;opacity:.9;font-family:A}}
#fl{{left:0;top:0;width:1080px;height:1920px;background:#fff}}
{{EXTRA}}</style></head><body><div id="grad"></div>
<div class="g sh" id="hk">{c['hook']}</div>
{'<div class="g sh" id="se"><div class="k">'+c['serie'][0]+'</div><div class="f">'+c['serie'][1]+'</div></div>' if c['serie'] else ''}
<div class="g sh" id="nm"><div class="n">{c['name']}</div><div class="l"></div><div class="r">{c['role']}</div></div>
<div class="g sh" id="st"><div class="n" id="stn"></div><div class="t"><div class="k" id="stk"></div><div class="h" id="sth"></div></div></div>
<div class="g" id="bar"><i></i><i></i><i></i></div>
<div class="g" id="div"></div><div class="g sh" id="tag"></div>
<div class="g sh" id="ct">{c['cta']}<div class="at">{c['at']}</div></div>
<div id="cap" class="sh"></div><div class="g" id="fl"></div>
<script>
const D={json.dumps(D,ensure_ascii=False)};const HK=3.0;const NM={json.dumps(list(c.get('nm',(3.1,6.2))))};
const $=id=>document.getElementById(id);const e3=t=>{{t=Math.min(1,Math.max(0,t));return 1-Math.pow(1-t,3)}};
function sh(id,s,a,b,dy){{const E=$(id);if(!E)return 0;const i=e3((s-a)/0.5),o=e3((s-(b-0.4))/0.4);const v=i*(1-o);E.style.opacity=v;E.style.transform=`translateY(${{(1-i)*dy}}px)`;return v}}
window.setT=(s)=>{{
 sh('hk',s,-1,HK,0);
 if(D.serie)sh('se',s,D.serie[0],D.serie[1],16);
 sh('nm',s,NM[0],NM[1],14);if(D.splits.some(x=>s>=x[0]-0.1&&s<x[1]+0.1))$('nm').style.opacity=0;
 sh('ct',s,D.cta,D.total+1,18);
 const st=D.steps.find(x=>s>=x[0]-0.1&&s<x[1]);
 if(st){{$('stn').textContent=st[2];$('stk').textContent=st[3];$('sth').textContent=st[4];sh('st',s,st[0],st[1],16);const B=$('bar');B.style.opacity=$('st').style.opacity;[...B.children].forEach((x,i)=>x.className=(i<+st[2])?'on':'');}}else{{$('st').style.opacity=0;$('bar').style.opacity=0;}}
 const sp=D.splits.find(x=>s>=x[0]&&s<x[1]);$('div').style.opacity=sp?1:0;const tg=$('tag');if(sp){{tg.textContent=sp[2];tg.style.opacity=Math.min(1,(s-sp[0])/0.25)}}else tg.style.opacity=0;
 let f=0;D.flash.forEach(t=>{{const d=s-t;if(d>=-0.03&&d<0.2)f=Math.max(f,d<0.03?0.3:0.3*(1-(d-0.03)/0.17))}});$('fl').style.opacity=f;
 const cap=$('cap');const pg=(s<HK||s>=D.cta-0.05)?null:D.pages.find(p=>s>=p.a-0.05&&s<p.b+0.1);
 cap.style.top=sp?'760px':'1360px';
 if(pg){{cap.innerHTML=pg.w.map(w=>{{const on=s>=w[1];const t=w[2]?`<i>${{w[0]}}</i>`:w[0];return `<span class="w${{on?' on':''}}">${{t}}</span>`}}).join(' ');cap.style.opacity=1}}else cap.style.opacity=0;
}};
</script></body></html>'''
EA='''#hk{font-family:S;font-weight:400;font-size:74px;letter-spacing:-1px;line-height:1.05}#hk i{font-family:S;font-weight:400;font-size:74px;color:#fff}
#ct{font-family:S;font-weight:400;font-size:62px;letter-spacing:-.5px}#ct i{font-family:S;font-weight:400;font-size:62px;color:#fff}
#se .f{font-family:S;font-weight:400}
#cap .w{font-family:A;font-weight:500;font-size:48px;letter-spacing:-.3px}#cap .w i{font-family:A;font-style:normal;font-weight:500;font-size:48px;color:inherit}
#nm .n{font-family:S;font-weight:400;font-size:46px;letter-spacing:0}#nm .r{font-family:A;font-weight:500;font-size:15px}
#st .n{font-family:S;font-style:italic;font-weight:400;font-size:120px;color:#fff}#st .h{font-family:S;font-weight:400;font-size:44px;letter-spacing:0}#st .k{font-family:A;font-weight:500}'''
EB='''#hk{font-family:A;font-weight:600;font-size:60px;letter-spacing:-1.5px}#hk i{font-family:A;font-style:normal;font-weight:400;font-size:60px;color:#fff;opacity:.85}
#ct{font-family:A;font-weight:600;font-size:52px}#ct i{font-family:A;font-style:normal;font-weight:400;font-size:52px;color:#fff;opacity:.85}
#se .f{font-family:A;font-style:normal;font-weight:500;font-size:34px}
#cap .w{font-family:A;font-weight:500;font-size:48px;letter-spacing:-.5px}#cap .w i{font-family:A;font-style:normal;font-weight:500;font-size:48px;color:inherit}
#nm .n{font-family:A;font-weight:600;font-size:40px}#nm .r{font-family:A;font-weight:500;font-size:15px}
#st .n{font-family:A;font-style:normal;font-weight:600;font-size:110px;color:#fff;letter-spacing:-4px}#st .h{font-family:A;font-weight:600;font-size:40px}'''
html=html.replace('{EXTRA}',EA if V=='A' else EB)
open(f'ov-{k}{"" if V=="A" else "-B"}.html','w').write(html)
