const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:640,height:330},deviceScaleFactor:2});
const p=await c.newPage();await p.goto('file://'+process.argv[2]);await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
await p.addStyleTag({content:'main{display:none}.lexia-bubble{transition:none}'});
await p.evaluate(()=>dispatchEvent(new Event('resize')));
const total=await p.evaluate(()=>window.__lexia.plan.total); const fps=25; const n=Math.round((total-1.2)*fps);
console.log(total,n);
const el=await p.$('.lexia-track');
for(let i=0;i<n;i++){await p.evaluate(t=>window.__lexia.seek(t),i/fps);await el.screenshot({path:`frames/f${String(i).padStart(4,'0')}.png`});}
await b.close();})();
