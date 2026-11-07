/* BIBLIOTECA DE MÓDULOS (07/11/2026). Identidade Núbia Citty: creme #F4EDE6, rosé #F0C3CC, vinho #8E2A3E, fundo #140E0C.
   Cada módulo é um "type" usado no fx.js do vídeo, igual aos efeitos antigos. Todos ficam na camada da frente (fg),
   a não ser que o evento diga layer:'bg'. Tempos em segundos na linha do corte (antes do 1,1x).
   Catálogo e regras de uso: CATALOGO-MODULOS.md (mesma pasta). */
(function(){
const F='file:///home/user/Nc-insta/modelos/fontes/';
const css=`@font-face{font-family:M;font-weight:500;src:url("${F}caveat-latin-500-normal.woff2")}
@font-face{font-family:M;font-weight:700;src:url("${F}caveat-latin-700-normal.woff2")}
@font-face{font-family:A;font-weight:700;src:url("${F}archivo-latin-700-normal.woff2")}
.m-box{position:absolute;left:60px;right:60px;background:rgba(20,14,12,.86);border:1px solid rgba(244,237,230,.22);border-radius:28px;box-shadow:0 20px 60px rgba(0,0,0,.45)}
.m-k{font-family:A;font-weight:600;font-size:24px;letter-spacing:.3em;color:#F0C3CC}
.m-pr{display:flex;align-items:center;gap:20px;padding:26px 30px;font-family:A;font-weight:500;font-size:38px;color:#F4EDE6}
.m-pr .ic{width:54px;height:54px;border-radius:16px;background:#8E2A3E;display:flex;align-items:center;justify-content:center;flex:none}
.m-pr .tx{flex:1;white-space:nowrap;overflow:hidden}.m-pr .cr{display:inline-block;width:3px;height:40px;background:#F0C3CC;vertical-align:-6px;margin-left:4px}
.m-ok{font-family:A;font-weight:600;font-size:24px;letter-spacing:.12em;color:#140E0C;background:#F0C3CC;border-radius:40px;padding:10px 18px;opacity:0;flex:none}
.m-row{display:flex;align-items:center;gap:26px;font-family:A;font-weight:500;font-size:42px;color:rgba(244,237,230,.38);padding:16px 0}
.m-row .n{width:70px;height:70px;border-radius:50%;border:2.5px solid rgba(244,237,230,.3);display:flex;align-items:center;justify-content:center;font-family:S;font-size:40px;flex:none;position:relative}
.m-row .n svg{position:absolute;inset:-3px;opacity:0}
.m-pn{position:absolute;left:0;right:0;top:0;background:linear-gradient(#1c1412,#140E0C);border-bottom:1px solid rgba(244,237,230,.18);border-radius:0 0 46px 46px;box-shadow:0 30px 80px rgba(0,0,0,.5);overflow:hidden}
.m-ttl{font-family:S;font-size:96px;line-height:1.02;color:#F4EDE6}.m-ttl i{font-style:italic;color:#F0C3CC}
.m-lz{position:absolute;left:50px;right:50px;border-radius:26px;background:#1d2420;border:12px solid #4a3426;box-shadow:inset 0 0 80px rgba(0,0,0,.55),0 24px 60px rgba(0,0,0,.45);padding:40px 46px}
.m-lz .ln{font-family:M;font-weight:700;font-size:74px;line-height:1.12;color:#EEF0E6;position:relative;display:inline-block;clip-path:inset(0 100% 0 0)}
.m-lz .ln.r{color:#F0C3CC}
.m-nd{position:absolute;background:rgba(20,14,12,.9);border:2px solid rgba(244,237,230,.35);border-radius:24px;padding:22px 26px;text-align:center;font-family:A;font-weight:600;font-size:38px;color:#F4EDE6;box-shadow:0 14px 40px rgba(0,0,0,.4)}
.m-nd.hi{border-color:#F0C3CC;background:#8E2A3E}.m-nd small{display:block;font-weight:500;font-size:24px;letter-spacing:.14em;color:#F0C3CC;margin-top:6px}.m-nd.hi small{color:#F4EDE6}
.m-cta{display:inline-flex;align-items:center;gap:18px;background:#F0C3CC;color:#140E0C;font-family:A;font-weight:700;font-size:46px;border-radius:70px;padding:30px 54px;box-shadow:0 16px 50px rgba(0,0,0,.45)}
.m-bl{position:absolute;max-width:700px;padding:22px 28px;border-radius:30px;font-family:A;font-weight:500;font-size:36px;line-height:1.25;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.m-bl.e{left:70px;background:#F4EDE6;color:#140E0C;border-bottom-left-radius:8px}.m-bl.d{right:70px;background:#8E2A3E;color:#F4EDE6;border-bottom-right-radius:8px}
.m-pill{display:inline-block;font-family:A;font-weight:600;font-size:24px;letter-spacing:.26em;color:#F0C3CC;background:rgba(20,14,12,.82);border:1px solid rgba(240,195,204,.45);border-radius:40px;padding:12px 22px}
.m-sim{font-family:A;font-weight:600;font-size:20px;letter-spacing:.24em;color:rgba(244,237,230,.7)}`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
const E=t=>{t=Math.max(0,Math.min(1,t));return 1-Math.pow(1-t,3)};
const B=t=>{t=Math.max(0,Math.min(1,t));const c=1.70158*1.4;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)}; /* com mola */
const H=h=>{const d=document.createElement('div');d.innerHTML=h.trim();return d.firstElementChild};
const cl=(a,b,c)=>Math.max(b,Math.min(c,a));

/* ÍCONES próprios (traço creme e rosé). Nada de imagem de terceiros. */
const I={
algema:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linecap="round"><circle cx="62" cy="120" r="38"/><circle cx="158" cy="120" r="38"/><path d="M62 82V62M158 82V62" /><path d="M62 62q48 -34 96 0" stroke="#F0C3CC" stroke-dasharray="10 9"/></g>`,
martelo:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><rect x="58" y="40" width="96" height="46" rx="8" transform="rotate(-35 106 63)"/><path d="M118 82l58 74"/><path d="M40 186h96" stroke="#F0C3CC"/></g>`,
balanca:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M110 34v150M70 184h80M40 70h140"/><path d="M40 70l-26 60h52zM180 70l-26 60h52z" stroke="#F0C3CC"/><path d="M14 130q26 26 52 0M154 130q26 26 52 0"/></g>`,
relogio:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linecap="round"><circle cx="110" cy="114" r="76"/><path d="M110 70v46l30 20" stroke="#F0C3CC"/><path d="M84 24h52"/></g>`,
documento:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><path d="M56 24h76l40 40v134H56z"/><path d="M132 24v40h40"/><path d="M80 104h66M80 132h66M80 160h40" stroke="#F0C3CC"/></g>`,
celular:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><rect x="62" y="20" width="96" height="180" rx="18"/><path d="M96 40h28"/><path d="M84 92h52M84 116h40" stroke="#F0C3CC"/></g>`,
cadeado:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><rect x="46" y="96" width="128" height="100" rx="16"/><path d="M74 96V70a36 36 0 0 1 72 0v26"/><path d="M110 132v28" stroke="#F0C3CC"/></g>`,
alerta:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><path d="M110 28l90 160H20z"/><path d="M110 86v50M110 160v4" stroke="#F0C3CC"/></g>`,
grade:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linecap="round"><rect x="30" y="30" width="160" height="160" rx="10"/><path d="M70 30v160M110 30v160M150 30v160" stroke="#F0C3CC"/></g>`,
escudo:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><path d="M110 22l72 26v56c0 46-32 80-72 96-40-16-72-50-72-96V48z"/><path d="M78 110l22 22 44-48" stroke="#F0C3CC"/></g>`,
dinheiro:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linecap="round"><rect x="20" y="62" width="180" height="100" rx="14"/><circle cx="110" cy="112" r="26" stroke="#F0C3CC"/><path d="M46 88v48M174 88v48"/></g>`,
ia:`<g fill="none" stroke="#F4EDE6" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><rect x="50" y="50" width="120" height="120" rx="20"/><path d="M80 50V24M110 50V24M140 50V24M80 196v-26M110 196v-26M140 196v-26M50 80H24M50 140H24M196 80h-26M196 140h-26"/><path d="M84 138l18-56 18 56M90 120h24M140 82v56" stroke="#F0C3CC"/></g>`
};
const ico=(n,s)=>`<svg width="${s}" height="${s}" viewBox="0 0 220 220">${I[n]||''}</svg>`;
const chk=`<svg width="76" height="76" viewBox="0 0 76 76"><circle cx="38" cy="38" r="36" fill="#F0C3CC"/><path d="M22 39l11 11 21-23" fill="none" stroke="#140E0C" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

const M={};
/* 1. PROMPT: caixa de comando sendo digitada. {text, at, cps=18, okAt, top, label} */
M.prompt=e=>{const el=H(`<div class="m-box" style="top:${e.top||190}px">${e.label?`<div class="m-k" style="padding:22px 30px 0">${e.label}</div>`:''}<div class="m-pr"><div class="ic">${ico('ia',40)}</div><div class="tx"><span class="t"></span><span class="cr"></span></div><div class="m-ok">✓ ${e.ok||'FEITO'}</div></div></div>`);
 const t=el.querySelector('.t'),cr=el.querySelector('.cr'),ok=el.querySelector('.m-ok');const at=e.at??e.t0+0.3,cps=e.cps||18;const done=at+e.text.length/cps;const okAt=e.okAt??done+0.4;
 return {el,up:s=>{t.textContent=e.text.slice(0,cl(Math.floor((s-at)*cps),0,e.text.length));cr.style.opacity=(s<done+0.1)?1:(Math.floor(s*2.4)%2);const q=B((s-okAt)/0.35);ok.style.opacity=s<okAt?0:1;ok.style.transform=`scale(${s<okAt?0.5:0.5+0.5*q})`}}};

/* 2. PASSOS: lista numerada que acende e ganha check. {k, items:[{txt,at,okAt?}], top} */
M.passos=e=>{const el=H(`<div class="m-box" style="top:${e.top||180}px;padding:34px 44px">${e.k?`<div class="m-k" style="margin-bottom:10px">${e.k}</div>`:''}${e.items.map((it,j)=>`<div class="m-row"><div class="n">${j+1}${chk.replace('<svg','<svg class="c"')}</div><div>${it.txt}</div></div>`).join('')}</div>`);
 const rows=[...el.querySelectorAll('.m-row')];
 return {el,up:s=>{rows.forEach((r,j)=>{const it=e.items[j];const on=E((s-it.at)/0.3);r.style.color=`rgba(244,237,230,${0.38+0.62*on})`;r.style.transform=`translateX(${on*8}px)`;const n=r.querySelector('.n');n.style.borderColor=on>0.5?'#F0C3CC':'rgba(244,237,230,.3)';const okAt=it.okAt??(e.items[j+1]?e.items[j+1].at:it.at+1.2);const c=r.querySelector('.c');const q=B((s-okAt)/0.3);c.style.opacity=s<okAt?0:1;c.style.transform=`scale(${q})`})}}};

/* 3. PAINEL: metade de cima vira um quadro com título e ícone/imagem; a pessoa continua embaixo.
   {k, ttl, icon|src, h=860, iconAt} */
M.painel=e=>{const h=e.h||860;const el=H(`<div class="m-pn" style="height:${h}px"><div style="position:absolute;left:70px;right:70px;top:150px">${e.k?`<div class="m-k">${e.k}</div>`:''}<div class="m-ttl" style="margin-top:18px;font-size:${e.size||96}px">${e.ttl||''}</div></div><div class="ob" style="position:absolute;right:${e.icRight??80}px;bottom:${e.icBottom??70}px">${e.src?`<img src="${e.src}" style="width:${e.icSize||330}px;display:block">`:ico(e.icon||'balanca',e.icSize||300)}</div></div>`);
 const ob=el.querySelector('.ob');const at=e.iconAt??e.t0+0.35;
 return {el,own:1,up:s=>{const q=E((s-e.t0)/0.45);const out=E((s-(e.t1-0.35))/0.35);el.style.transform=`translateY(${-(1-q)*h + -out*h}px)`;const p=B((s-at)/0.5);ob.style.opacity=s<at?0:1;ob.style.transform=`scale(${s<at?0.3:0.3+0.7*p}) rotate(${Math.sin((s-at)*1.6)*3}deg) translateY(${Math.sin((s-at)*2)*6}px)`}}};

/* 4. LOUSA: quadro com frases escritas à mão, uma de cada vez, e marcas (sublinha, circula, risca, seta).
   {k, linhas:[{txt, at, dur?, marca?:'sublinha'|'circula'|'risca', marcaAt?, r?:true}], top, seta?:[i,j,at]} */
M.lousa=e=>{const el=H(`<div class="m-lz" style="top:${e.top||150}px">${e.k?`<div class="m-k" style="color:#d9cdb8;margin-bottom:14px">${e.k}</div>`:''}${e.linhas.map(l=>`<div style="position:relative;margin:${l.gap??6}px 0 0 ${l.x||0}px"><span class="ln${l.r?' r':''}">${l.txt}</span><svg class="mk" style="position:absolute;left:-20px;top:-14px;overflow:visible" width="10" height="10"></svg></div>`).join('')}</div>`);
 document.body.appendChild(el);const lns=[...el.querySelectorAll('.ln')];const mks=[...el.querySelectorAll('.mk')];const paths=[];
 lns.forEach((ln,j)=>{const l=e.linhas[j];if(!l.marca)return paths.push(null);const w=ln.offsetWidth+40,h=ln.offsetHeight+28;let d;
  if(l.marca==='sublinha')d=`M10 ${h-4} q ${w/2} 14 ${w-10} -4`;else if(l.marca==='risca')d=`M6 ${h/2+6} L ${w-6} ${h/2-4}`;else d=`M${w/2} 4 C ${w+20} 0, ${w+30} ${h}, ${w/2} ${h+4} C -20 ${h+6}, -26 4, ${w/2+30} 2`;
  const svg=mks[j];svg.setAttribute('width',w);svg.setAttribute('height',h);svg.innerHTML=`<path d="${d}" fill="none" stroke="${l.marca==='risca'?'#E0707F':'#F0C3CC'}" stroke-width="7" stroke-linecap="round"/>`;const p=svg.firstChild;const L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L;paths.push([p,L])});
 el.remove();
 return {el,up:s=>{lns.forEach((ln,j)=>{const l=e.linhas[j];const q=cl((s-l.at)/(l.dur||Math.max(0.5,l.txt.length*0.045)),0,1);ln.style.clipPath=`inset(-20px ${100-q*100}% -20px -10px)`;const pp=paths[j];if(pp){const ma=l.marcaAt??l.at+(l.dur||l.txt.length*0.045)+0.3;pp[0].style.strokeDashoffset=pp[1]*(1-E((s-ma)/0.45))}})}}};

/* 5. FLUXO: explicação em caixas ligadas por setas, de cima para baixo; um nível pode ter 2 caminhos.
   {k, top, nos:[{txt, sub?, at, hi?} | {lado:[{txt,sub,hi},{txt,sub,hi}], at}]} */
M.fluxo=e=>{const top=e.top||170;const gap=e.gap||220;const el=H(`<div style="position:absolute;inset:0"></div>`);let y=top+(e.k?90:0);
 if(e.k)el.appendChild(H(`<div style="position:absolute;left:0;right:0;top:${top-10}px;text-align:center"><span class="m-pill">${e.k}</span></div>`));
 const svg=H(`<svg style="position:absolute;inset:0;overflow:visible" width="1080" height="1920"></svg>`);el.appendChild(svg);
 const lv=e.nos.map(n=>{const boxes=n.lado?n.lado.map((b,k)=>({...b,cx:k?775:305,w:430})):[{...n,cx:540,w:e.w||660}];
  const els=boxes.map(b=>{const d=H(`<div class="m-nd${b.hi?' hi':''}" style="left:${b.cx-b.w/2}px;width:${b.w}px;top:${y}px;box-sizing:border-box">${b.txt}${b.sub?`<small>${b.sub}</small>`:''}</div>`);el.appendChild(d);return d});
  const r={boxes,els,at:n.at,y,arrows:[]};y+=gap;return r});
 const mk=(d)=>{const p=document.createElementNS('http://www.w3.org/2000/svg','path');p.setAttribute('d',d);p.setAttribute('fill','none');p.setAttribute('stroke','#F0C3CC');p.setAttribute('stroke-width','6');p.setAttribute('stroke-linecap','round');p.setAttribute('stroke-linejoin','round');svg.appendChild(p);return p};
 let ready=false;
 const build=()=>{lv.forEach((l,i)=>{if(!i)return;const pv=lv[i-1];const ph=Math.max(...pv.els.map(d=>d.offsetHeight));const y0=pv.y+ph+12,y1=l.y-14;
   const pairs=[];if(pv.boxes.length===l.boxes.length)pv.boxes.forEach((b,k)=>pairs.push([b.cx,l.boxes[k].cx]));else if(pv.boxes.length===1)l.boxes.forEach(b=>pairs.push([pv.boxes[0].cx,b.cx]));else pv.boxes.forEach(b=>pairs.push([b.cx,l.boxes[0].cx]));
   pairs.forEach(([a,c])=>{const ln=mk(`M${a} ${y0} C ${a} ${(y0+y1)/2}, ${c} ${(y0+y1)/2}, ${c} ${y1}`);const hd=mk(`M${c-16} ${y1-18} L${c} ${y1} L${c+16} ${y1-18}`);const L=ln.getTotalLength();ln.style.strokeDasharray=L;l.arrows.push([ln,hd,L])})});ready=true};
 return {el,up:s=>{if(!ready)build();lv.forEach(l=>{const aq=E((s-(l.at-0.35))/0.35);l.arrows.forEach(([ln,hd,L])=>{ln.style.strokeDashoffset=L*(1-aq);hd.style.opacity=aq>0.95?1:0});l.els.forEach((d,k)=>{const t=l.at+k*0.12;const q=B((s-t)/0.4);d.style.opacity=s<t?0:1;d.style.transform=`scale(${0.6+0.4*q})`})})}}};

/* 6. OBJETO: ícone próprio (ou PNG com fundo transparente) que entra com mola e flutua. {icon|src, x, y, size, label?, from?:'baixo'|'lado'} */
M.objeto=e=>{const sz=e.size||260;const el=H(`<div style="position:absolute;left:${e.x??720}px;top:${e.y??380}px;width:${sz}px;text-align:center"><div class="o" style="filter:drop-shadow(0 14px 30px rgba(0,0,0,.55))">${e.src?`<img src="${e.src}" style="width:${sz}px;display:block">`:`<div style="width:${sz}px;height:${sz}px;border-radius:50%;background:radial-gradient(#2a1d1a,#140E0C);border:2px solid rgba(240,195,204,.5);display:flex;align-items:center;justify-content:center">${ico(e.icon,sz*0.66)}</div>`}</div>${e.label?`<div style="margin-top:16px"><span class="m-pill">${e.label}</span></div>`:''}</div>`);
 const o=el.querySelector('.o');
 return {el,own:1,up:s=>{const q=B((s-e.t0)/0.5);const fl=Math.sin((s-e.t0)*2.2)*8;o.style.transform=`translateY(${(e.from==='baixo'?(1-q)*300:0)+fl}px) scale(${e.from==='baixo'?1:Math.max(0,q)}) rotate(${(1-Math.min(q,1))*-14+Math.sin((s-e.t0)*1.3)*2}deg)`}}};

/* 7. CTA: botão com cursor que entra e "clica". {txt, top, clickAt, sub?} */
M.cta=e=>{const el=H(`<div style="position:absolute;left:0;right:0;top:${e.top||1380}px;text-align:center">${e.sub?`<div style="margin-bottom:24px"><span class="m-pill">${e.sub}</span></div>`:''}<div class="m-cta b">${e.txt}</div><svg class="cu" style="position:absolute;left:640px;top:${e.sub?120:80}px" width="90" height="90" viewBox="0 0 24 24"><path d="M5 3l14 8-6 1.6L10 19z" fill="#F4EDE6" stroke="#140E0C" stroke-width="1.3" stroke-linejoin="round"/></svg></div>`);
 const b=el.querySelector('.b'),cu=el.querySelector('.cu');const ck=e.clickAt??e.t0+0.9;
 return {el,own:1,up:s=>{const pb=B((s-e.t0)/0.45);b.style.transform=`scale(${Math.max(0,pb)*(1-0.08*Math.max(0,1-Math.abs(s-ck)/0.12))})`;const cq=E((s-(ck-0.6))/0.5);cu.style.opacity=s<ck-0.6?0:1;cu.style.transform=`translate(${(1-cq)*220}px,${(1-cq)*160}px) scale(${1-0.12*Math.max(0,1-Math.abs(s-ck)/0.12)})`}}};

/* 8. CONVERSA: balões entrando um a um. SEMPRE mostra "SIMULAÇÃO" se não for print real autorizado. {items:[{txt,lado:'e'|'d',at}], top, real?:false} */
M.conversa=e=>{const el=H(`<div style="position:absolute;inset:0">${e.real?'':`<div style="position:absolute;left:0;right:0;top:${(e.top||220)-80}px;text-align:center"><span class="m-pill" style="font-size:20px">SIMULAÇÃO</span></div>`}</div>`);let y=e.top||220;
 const bs=e.items.map(it=>{const d=H(`<div class="m-bl ${it.lado||'e'}" style="top:${y}px">${it.txt}</div>`);el.appendChild(d);y+=it.h||(Math.ceil(it.txt.length/30)*46+60);return d});
 return {el,up:s=>bs.forEach((d,j)=>{const at=e.items[j].at;const q=B((s-at)/0.35);d.style.opacity=s<at?0:1;d.style.transform=`translateY(${(1-Math.min(1,q))*30}px) scale(${0.85+0.15*q})`;d.style.transformOrigin=e.items[j].lado==='d'?'right bottom':'left bottom'})}};

window.FXMOD={M,ico,ICONES:Object.keys(I)};
})();
