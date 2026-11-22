const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const [name,opt] of [['desk',{viewport:{width:1280,height:720}}],['phone',{...devices['iPhone 13']}]]){
 const c=await b.newContext(opt); const p=await c.newPage(); p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+process.argv[2]); await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
 const ts=await p.evaluate(()=>window.__lexia.plan.ts); console.log(name,ts.map(x=>x.toFixed(2)).join(' '));
 const t0=ts[0]+ts[1];
 for (const [k,t] of [['walk',ts[0]*0.6],['turn',t0+ts[2]*0.5],['front',t0+ts[2]+1]]){
   await p.evaluate(t=>window.__lexia.seek(t),t); await p.waitForTimeout(350);
   await p.screenshot({path:`${name}-${k}.png`});
 }
 await c.close();}
await b.close();})();
