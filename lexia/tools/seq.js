// foglio di fotogrammi della sequenza reale: node seq.js file.html t0 t1 n out.png [width]
const {chromium}=require('playwright');
(async()=>{const [f,t0,t1,n,out,w]=process.argv.slice(2);const b=await chromium.launch();
const c=await b.newContext({viewport:{width:+(w||700),height:330},deviceScaleFactor:1});const p=await c.newPage();
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+f);await p.waitForFunction(()=>window.__lexia&&window.__lexia.plan);
await p.addStyleTag({content:'main{display:none}.lexia-bubble{transition:none}:root{--size:230px!important}'});
await p.evaluate(()=>dispatchEvent(new Event('resize')));
const pl=await p.evaluate(()=>window.__lexia.plan);console.log(JSON.stringify(pl.ts.map(v=>+v.toFixed(2))),pl.total.toFixed(2));
const el=await p.$('.lexia-track');const fs=require('fs');fs.mkdirSync('sq',{recursive:true});
for(let i=0;i<+n;i++){const t=+t0+(+t1-+t0)*i/(+n-1);await p.evaluate(t=>window.__lexia.seek(t),t);await el.screenshot({path:`sq/${String(i).padStart(3,'0')}.png`});}
await b.close();
require('child_process').execSync(`python3 - <<'P'
from PIL import Image
import glob
fs=sorted(glob.glob('sq/*.png'))[:${n}]; ims=[Image.open(f) for f in fs]
cols=2; W,H=ims[0].size; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(W*cols,H*rows),(246,242,248))
for i,im in enumerate(ims): sh.paste(im,((i%cols)*W,(i//cols)*H))
sh.save('${out}')
P`);})();
