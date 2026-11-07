// Lê o fx.js do vídeo e devolve a lista de sons (tempo na linha do corte, antes do 1,1x). Uso: node sfx_cues.js fx.js
const fs=require('fs');const window={};eval(fs.readFileSync(process.argv[2],'utf8'));
const ev=(window.FX||{events:[]}).events;const C=[];const add=(t,s,g=1)=>{if(t!=null&&!isNaN(t))C.push({t:+t.toFixed(3),s,g})};
let k=0;const tec=()=>'tecla'+(k++%4);
ev.forEach(e=>{if(e.sfx===false)return;if(typeof e.sfx==='string'){add(e.t0,e.sfx);return}
 switch(e.type){
 case 'prompt':{const at=e.at??e.t0+0.3,cps=e.cps||18,n=e.text.length;for(let i=0;i<n;i++)if(e.text[i]!==' ')add(at+i/cps,tec(),0.8);const done=at+n/cps;add(e.okAt??done+0.4,'check');break}
 case 'passos':e.items.forEach((it,j)=>{add(it.at,'clique');add(it.okAt??(e.items[j+1]?e.items[j+1].at:it.at+1.2),'check',0.8)});break
 case 'painel':add(e.t0,'whoosh');add(e.iconAt??e.t0+0.35,'pop_grave');break
 case 'lousa':add(e.t0,'whoosh_curto',0.7);e.linhas.forEach(l=>{const d=l.dur||Math.max(0.5,l.txt.length*0.045);for(let x=0;x<d;x+=0.95)add(l.at+x,'giz:'+Math.min(0.95,d-x).toFixed(2));if(l.marca)add(l.marcaAt??l.at+d+0.3,'marcador')});break
 case 'fluxo':add(e.t0,'whoosh_curto',0.7);e.nos.forEach(n=>{add(n.at,'pop');if(n.lado)add(n.at+0.12,'pop',0.8)});break
 case 'objeto':add(e.t0,'pop_grave');break
 case 'cta':add(e.t0,'pop');add(e.clickAt??e.t0+0.9,'clique');break
 case 'conversa':e.items.forEach(it=>add(it.at,'bolha'));break
 case 'lei':add(e.t0,'pagina');add(e.marcaAt??e.t0+1.2,'marcador');break
 case 'vertigem':add(e.t0,'tensao:'+(e.t1-e.t0).toFixed(2));break
 case 'som':add(e.t0,e.som,e.g||1);break
 case 'text':case 'cover':add(e.t0,'whoosh_curto',0.6);break
 case 'img':add(e.t0,'whoosh',0.6);break
 case 'strike':add(e.at,'marcador');break
 case 'list':e.items.forEach(it=>add(it.at,'clique',0.8));break
 case 'comments':e.items.forEach(it=>{add(it.at,'bolha',0.8);if(it.strikeAt)add(it.strikeAt,'marcador')});break
 case 'compare':e.rows.forEach(r=>r.at.forEach(a=>add(a,'check',0.6)));break
 }});
process.stdout.write(JSON.stringify(C.sort((a,b)=>a.t-b.t)));
