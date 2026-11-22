const {chromium}=require('playwright');const {execSync}=require('child_process');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const S of [370,385,400,415]) for(const C of [74,80,86,92,98]){
 execSync(`python3 build.py t.html S=${S} C=${C}`);
 await p.goto('file://'+process.cwd()+'/t.html');await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
 const r=await p.evaluate(()=>{const L=window.__lexia;let ek=0,et=0,n=0,hmin=1e9,hmax=0;for(let i=0;i<100;i++){const ph=i/100;const h=L.hipH(ph);hmin=Math.min(hmin,h);hmax=Math.max(hmax,h);const l=L.legRel(ph);const k=L.ik([0,-h],[l.dx,l.y]);
  const kn=(k.ta-k.sa)*57.3*-1, th=90-k.ta*57.3; ek+=(Math.abs(kn)-L.curve(L.KN,ph))**2; et+=(th-L.curve(L.TH,ph))**2;n++}
  return 'knee rms '+Math.sqrt(ek/n).toFixed(1)+' thigh rms '+Math.sqrt(et/n).toFixed(1)+' bob '+(hmax-hmin).toFixed(1)+' D0 '+L.D0.map(v=>v.toFixed(0))+' D1 '+L.D1.map(v=>v.toFixed(0))});
 console.log(S,C,r);}
await b.close();})();
