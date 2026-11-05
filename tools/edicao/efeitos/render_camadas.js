const {chromium}=require('playwright');(async()=>{const [html,layer,dir,N]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+html+'?'+layer);await p.waitForTimeout(900);
for(let i=0;i<+N;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:dir+'/f'+String(i).padStart(4,'0')+'.png',omitBackground:true});}
await b.close()})()
