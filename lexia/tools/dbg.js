const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[2]);await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
console.log(await p.evaluate(()=>{const L=window.__lexia;let o=[];for(let i=0;i<20;i++){const ph=i/20;const h=L.hipH(ph);const l=L.legRel(ph);const k=L.ik([0,-h],[l.dx,l.y]);o.push([ph.toFixed(2),h.toFixed(1),l.dx.toFixed(1),l.y.toFixed(1),(Math.hypot(l.dx,l.y+h)).toFixed(1),((k.sa-k.ta)*57.3).toFixed(1)].join(' '))}return o.join('\n')}));
await b.close();})();
