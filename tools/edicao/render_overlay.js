const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]+process.argv[4]);await p.waitForTimeout(500);
for(let i=0;i<150;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:process.argv[3]+'/f'+String(i).padStart(4,'0')+'.png',omitBackground:true});}
await b.close()})()
