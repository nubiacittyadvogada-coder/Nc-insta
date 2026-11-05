// Gera os quadros (PNG transparentes) de cada animação atrás da pessoa.
// Uso: node render_atras.js /caminho/atras-da-pessoa.html pasta_saida "e1:3.9,e2:6.8,e3:4.9"
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(700);
const ev=(process.argv[4]||'e1:3.9,e2:6.8,e3:4.9').split(',').map(x=>x.split(':'));
for(const [k,dur] of ev){await p.evaluate(k=>setE(k),k);fs.mkdirSync(process.argv[3]+'/'+k,{recursive:true});
 for(let i=0;i<Math.round(+dur*30);i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:`${process.argv[3]}/${k}/f${String(i).padStart(4,'0')}.png`,omitBackground:true});}}
await b.close()})()
