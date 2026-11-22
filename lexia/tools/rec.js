// fotogrammi per l'anteprima: node rec.js /percorso/Lexia-camminata.html  → frames/f0000.png … (30 fps)
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:640,height:330},deviceScaleFactor:2});
const p=await c.newPage();await p.goto('file://'+process.argv[2]);await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
await p.addStyleTag({content:'main{display:none}.lexia-bubble{transition:none}'});
await p.evaluate(()=>dispatchEvent(new Event('resize')));
const total=await p.evaluate(()=>window.__lexia.plan.total); const fps=30; const n=Math.round((total-1.0)*fps);
console.log(total,n);require('fs').mkdirSync('frames',{recursive:true});
const el=await p.$('.lexia-track');
for(let i=0;i<n;i++){await p.evaluate(t=>window.__lexia.seek(t),i/fps);await el.screenshot({path:`frames/f${String(i).padStart(4,'0')}.png`});}
await b.close();})();
