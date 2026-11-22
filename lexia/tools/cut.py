from PIL import Image, ImageDraw, ImageFilter
import numpy as np, cv2, json
src=Image.open('src/img0.png').crop((0,0,512,512)).convert('RGBA')
A=np.array(src).astype(np.float32)
def mask(poly,feather=1.2):
    m=Image.new('L',(512,512),0); ImageDraw.Draw(m).polygon(poly,fill=255)
    if feather: m=m.filter(ImageFilter.GaussianBlur(feather))
    return np.array(m).astype(np.float32)/255
def part(m,name):
    P=A.copy(); P[...,3]*=m
    im=Image.fromarray(P.clip(0,255).astype(np.uint8))
    im.save(f'parts/{name}_full.png'); return im
armP=[(250,110),(272,116),(274,140),(264,175),(250,205),(236,238),(226,258),(220,280),(214,300),(205,310),(182,308),(176,292),(178,268),(195,250),(204,225),(216,190),(230,150),(236,122)]
farArmP=[(313,165),(330,180),(370,212),(400,225),(400,252),(372,252),(350,238),(318,226),(312,216),(311,195)]
thighP=[(265,205),(308,208),(320,255),(334,305),(344,352),(332,378),(304,378),(298,352),(282,322),(266,290),(258,250)]
shinP=[(298,335),(343,335),(354,400),(372,438),(378,460),(342,464),(326,432),(312,400)]
bootP=[(336,450),(378,444),(396,456),(424,456),(432,470),(422,484),(366,502),(350,498),(342,476)]
part(mask(armP),'arm'); part(mask(thighP),'thigh'); part(mask(shinP),'shin'); part(mask(bootP),'boot')
# body: everything above cut curve, minus arms
cut=Image.new('L',(512,512),0); d=ImageDraw.Draw(cut)
d.polygon([(0,0),(512,0),(512,262),(320,262),(300,268),(280,275),(258,282),(240,282),(200,262),(0,262)],fill=255)
cut=np.array(cut.filter(ImageFilter.GaussianBlur(3))).astype(np.float32)/255
B=A.copy()
rem=np.maximum(mask(armP,0),mask(farArmP,0))
remd=cv2.dilate((rem*255).astype(np.uint8),np.ones((5,5),np.uint8))
rgb=B[...,:3].astype(np.uint8); al=B[...,3].astype(np.uint8)
# premultiplied-ish: fill transparent area color with dark so inpaint ok
rgb=cv2.inpaint(np.ascontiguousarray(rgb),remd,6,cv2.INPAINT_TELEA)
al2=cv2.inpaint(al,remd,9,cv2.INPAINT_TELEA)
hard=np.where(al2>150,255,0).astype(np.uint8)
hard=cv2.morphologyEx(hard,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
hard=cv2.GaussianBlur(hard,(3,3),0)
al=np.where(remd>0,hard,al)
fa=(mask(farArmP,0.8)*255)
al=(al.astype(np.float32)*(1-fa/255)).astype(np.uint8)
B[...,:3]=rgb; B[...,3]=al.astype(np.float32)*cut
Image.fromarray(B.clip(0,255).astype(np.uint8)).save('parts/body_full.png')
