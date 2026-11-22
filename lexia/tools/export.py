from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json, base64, io
def b64(im):
    buf=io.BytesIO(); im.save(buf,'PNG',optimize=True); return 'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
arm=np.array(Image.open('parts/arm_full.png')).astype(np.float32)
# split arm at elbow along line perpendicular-ish (y ~ 212 on bone)
def ymask(y0,y1,up=True):
    m=np.zeros((512,512),np.float32); ys=np.arange(512)[:,None]
    t=np.clip((ys-y0)/(y1-y0),0,1); return np.broadcast_to(1-t if up else t,(512,512))
up=arm.copy(); up[...,3]*=ymask(214,220,True)
fo=arm.copy(); fo[...,3]*=ymask(200,206,False)
parts={'upperArm':up,'foreArm':fo}
for n in ['body','thigh','shin','boot']:
    parts[n]=np.array(Image.open(f'parts/{n}_full.png')).astype(np.float32)
pivots={'body':(288,238),'upperArm':(258,128),'foreArm':(224,212),'thigh':(288,238),'shin':(322,352),'boot':(364,463)}
out={}
for n,P in parts.items():
    im=Image.fromarray(P.clip(0,255).astype(np.uint8))
    bb=im.getchannel('A').point(lambda a:255 if a>3 else 0).getbbox()
    im=im.crop(bb); px,py=pivots[n]
    out[n]={'src':b64(im),'px':px-bb[0],'py':py-bb[1]}
fr=Image.open('src/img1.png'); bb=fr.getchannel('A').point(lambda a:255 if a>3 else 0).getbbox(); print('front bbox',bb)
fr=fr.crop(bb); H=560; fr=fr.resize((round(fr.width*H/fr.height),H),Image.LANCZOS)
out['front']={'src':b64(fr),'w':fr.width,'h':fr.height}
json.dump(out,open('rig.json','w'))
print({k:(v.get('px'),v.get('py')) for k,v in out.items()}, sum(len(v['src']) for v in out.values()))
