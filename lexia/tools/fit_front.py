# adatta la posa frontale (disegno con proporzioni diverse) a quelle della figura di profilo:
# rimappa le altezze di mento / spalle / cintura / orlo e ingrandisce la testa. Uso: python3 fit_front.py  (legge front_orig.png = src/posa-frontale-rig.png, aggiorna rig.json)
from PIL import Image
import numpy as np, cv2, json, base64, io, sys
SRC=[0, 80,107,200,502,560]      # altezze nel disegno frontale: cima, mento, spalle, cintura, orlo, suola
DST=[0, 94,114,232,521,560]      # le stesse nella figura di profilo (normalizzata a 560)
HEAD=1.17                        # la testa di profilo e' piu' grande
im=cv2.imread('front_orig.png',cv2.IMREAD_UNCHANGED).astype(np.float32)
H,W=im.shape[:2]; PAD=16; W2=W+2*PAD
im[...,:3]*=im[...,3:]/255                                   # premoltiplicato, per bordi puliti
yt=np.arange(H,dtype=np.float32)
ysrc=np.interp(yt,DST,SRC).astype(np.float32)
# lisciatura della mappa verticale (niente spigoli nei punti di raccordo)
k=np.ones(15,np.float32)/15; ysrc=np.convolve(np.pad(ysrc,7,mode='edge'),k,'valid').astype(np.float32)
sx=np.interp(yt,[0,DST[1],DST[2]+50,H],[HEAD,HEAD,1,1]).astype(np.float32)
cx=W/2-0.5
xt=np.arange(W2,dtype=np.float32)-PAD
mapx=(cx+(xt[None,:]-cx)/sx[:,None]).astype(np.float32); mapy=np.repeat(ysrc[:,None],W2,1)
out=cv2.remap(im,mapx,mapy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
a=out[...,3:].clip(0,255); out[...,:3]=np.where(a>0,out[...,:3]*255/np.maximum(a,1),0)
out=out.clip(0,255).astype(np.uint8)
res=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGRA2RGBA)); res.save('parts/front.png')
buf=io.BytesIO(); res.save(buf,'PNG',optimize=True)
rig=json.load(open('rig.json')); rig['front']={'src':'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode(),'w':res.width,'h':res.height}
json.dump(rig,open('rig.json','w')); print(res.size)
