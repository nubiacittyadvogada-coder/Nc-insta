const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(600);const N=+process.argv[4];
for(let i=0;i<N;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:process.argv[3]+'/f'+String(i).padStart(4,'0')+'.png',omitBackground:true});}
await b.close()})()
