# ritaglia coscia / tibia / stivale dalla gamba d'appoggio della posa 4 (src/p4.png), con calotte tonde ai giunti
from PIL import Image, ImageDraw
import numpy as np, json, base64, io, math
from legpoly import *
SS=4
src=Image.open('src/p4.png').convert('RGBA'); A=np.array(src).astype(np.float32)
def raster(draw):
    m=Image.new('L',(512*SS,512*SS),0); draw(ImageDraw.Draw(m)); return np.array(m.resize((512,512),Image.LANCZOS)).astype(np.float32)/255
sc=lambda pts:[(x*SS,y*SS) for x,y in pts]
def disc(c,r): return raster(lambda d:d.ellipse([(c[0]-r)*SS,(c[1]-r)*SS,(c[0]+r)*SS,(c[1]+r)*SS],fill=255))
leg=raster(lambda d:d.polygon(sc(front+back),fill=255))
ys,xs=np.mgrid[0:512,0:512].astype(np.float32)
# asse del ginocchio = bisettrice tra coscia e tibia
def unit(a,b): d=np.array([b[0]-a[0],b[1]-a[1]],float); return d/np.hypot(*d)
t=unit(HIP,KNEE)+unit(KNEE,ANK); t/=np.hypot(*t)
side=(xs-KNEE[0])*t[0]+(ys-KNEE[1])*t[1]
above=np.clip(0.5-side,0,1); below=np.clip(0.5+side,0,1)
kd=disc(KNEE,25.5)
# attorno al ginocchio la sagoma e' una capsula pulita lungo le ossa (via i resti di contorno dell'altra gamba)
def segdist(a,b):
    ax,ay=a; bx,by=b; vx,vy=bx-ax,by-ay; tt=np.clip(((xs-ax)*vx+(ys-ay)*vy)/(vx*vx+vy*vy),0,1)
    return np.hypot(xs-ax-tt*vx,ys-ay-tt*vy)
dk=np.hypot(xs-KNEE[0],ys-KNEE[1])
leg=leg*np.clip(22.2+np.maximum(0,dk-24)*0.45-np.minimum(segdist(HIP,KNEE),segdist(KNEE,ANK))+0.5,0,1)
# la natica resta al busto: sopra, la coscia e' limitata a una linea dritta dietro e a una calotta attorno all'anca
trim=raster(lambda d:d.polygon(sc([(221,236),(223,296),(205,296),(205,236)]),fill=255))
thigh=leg*np.maximum(above,kd)*(1-trim)
shin=leg*np.maximum(below,kd)
def save(mask,name,extra=None):
    P=A.copy(); P[...,3]*=mask
    if extra: extra(P)
    im=Image.fromarray(P.clip(0,255).astype(np.uint8)); im.save(f'parts/{name}_full.png'); return im
save(thigh,'thigh'); save(shin,'shin')
# stivale: tutto sotto l'orlo; gambale prolungato verso l'alto (resta sotto l'orlo quando la caviglia ruota)
bm=np.clip((ys-460.5),0,1)*(xs>226)
def ext(P):
    row=P[465].copy()
    for y in range(455,465):
        P[y]=row; P[y,:240,3]=0; P[y,271:,3]=0
        if y<458: P[y,:,3]*=(y-454)/4
save(bm,'boot',ext)
def b64(im):
    buf=io.BytesIO(); im.save(buf,'PNG',optimize=True); return 'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
rig=json.load(open('rig.json'))
for n,pv in (('thigh',HIP),('shin',KNEE),('boot',ANK)):
    im=Image.open(f'parts/{n}_full.png'); bb=im.getchannel('A').point(lambda a:255 if a>3 else 0).getbbox(); im=im.crop(bb)
    rig[n]={'src':b64(im),'px':pv[0]-bb[0],'py':pv[1]-bb[1]}; im.save(f'parts/{n}.png'); print(n,bb,im.size)
json.dump(rig,open('rig.json','w'))
ang=lambda a,b:math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
print('L1',math.dist(HIP,KNEE),'L2',math.dist(KNEE,ANK),'thigh0',ang(HIP,KNEE),'shin0',ang(KNEE,ANK))
