const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1100,height:420}});
 p.on('console',m=>console.log('console',m.text())); p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+process.argv[2]); await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
 // filmstrip: draw side pose at 8 phases into a separate canvas
 const cfg=JSON.parse(process.argv[3]||'{}');const data=await p.evaluate(({W0=1600,H0=300,SC=0.5,X0=100,DX=190,NF=8,OFF=0})=>{
   const c=document.querySelector('canvas'); const ctx=c.getContext('2d');
   c.width=W0;c.height=H0; ctx.setTransform(1,0,0,1,0,0); ctx.fillStyle='#e8f0e8';ctx.fillRect(0,0,W0,H0);
   for(let i=0;i<NF;i++){ ctx.setTransform(SC,0,0,SC,X0+i*DX,H0-12); 
     ctx.strokeStyle='#999'; ctx.beginPath(); ctx.moveTo(-200,0); ctx.lineTo(200,0); ctx.stroke();
     window.__lexia.drawSide(OFF+i/NF);} 
   return c.toDataURL();},cfg);
 require('fs').writeFileSync(process.argv[4]||'strip.png',Buffer.from(data.split(',')[1],'base64'));
 await b.close();})();
