# braccio superiore rifatto dalla posa 0 (src/p0.png) come capsula netta spalla→gomito (via i capelli e i bordi sfumati della v1)
from PIL import Image
import numpy as np, json, base64, io
SH=(258,128); EL=(224,212); R0,R1=16.6,15.2
A=np.array(Image.open('src/p0.png').convert('RGBA')).astype(np.float32)
ys,xs=np.mgrid[0:512,0:512].astype(np.float32)
vx,vy=EL[0]-SH[0],EL[1]-SH[1]
t=np.clip(((xs-SH[0])*vx+(ys-SH[1])*vy)/(vx*vx+vy*vy),0,1)
d=np.hypot(xs-SH[0]-t*vx,ys-SH[1]-t*vy)
A[...,3]*=np.clip(R0+(R1-R0)*t-d+0.5,0,1)
im=Image.fromarray(A.clip(0,255).astype(np.uint8))
bb=im.getchannel('A').point(lambda a:255 if a>3 else 0).getbbox(); im=im.crop(bb); im.save('parts/upperArm.png')
buf=io.BytesIO(); im.save(buf,'PNG',optimize=True)
rig=json.load(open('rig.json'))
rig['upperArm']={'src':'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode(),'px':SH[0]-bb[0],'py':SH[1]-bb[1]}
json.dump(rig,open('rig.json','w')); print(bb,im.size)
