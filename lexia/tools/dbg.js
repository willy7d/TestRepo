const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.argv[2]);await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
console.log(await p.evaluate(()=>{const L=window.__lexia;let o=['S '+L.S+' C '+L.C+' D0 '+L.D0.map(v=>v.toFixed(1))+' D1 '+L.D1.map(v=>v.toFixed(1))+' Pstop '+L.P_STOP.toFixed(3)+' Hstand '+L.H_STAND.toFixed(1),'ph   H     dx     y    pitch  knee(norm)  thigh(norm)'];
for(let i=0;i<40;i++){const ph=i/40;const h=L.hipH(ph);const l=L.legRel(ph);const k=L.ik([0,-h],[l.dx,l.y]);
o.push([ph.toFixed(3),h.toFixed(1),l.dx.toFixed(1),l.y.toFixed(1),(l.pitch*57.3).toFixed(0),((k.ta-k.sa)*57.3).toFixed(1)+'('+L.curve(L.KN,ph).toFixed(0)+')',(90-k.ta*57.3).toFixed(1)+'('+L.curve(L.TH,ph).toFixed(0)+')'].join('  '))}return o.join('\n')}));
await b.close();})();
