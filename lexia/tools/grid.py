from PIL import Image, ImageDraw
import sys
im=Image.open(sys.argv[1])
def g(box,name,s=4,step=10):
  c=im.crop(box)
  bg=Image.new('RGBA',c.size,(200,230,200,255)); bg.alpha_composite(c)
  bg=bg.resize((c.size[0]*s,c.size[1]*s),Image.NEAREST); d=ImageDraw.Draw(bg)
  for x in range(box[0]-box[0]%step,box[2],step):
    X=(x-box[0])*s; d.line([(X,0),(X,bg.size[1])],fill=(255,0,0,255) if x%50==0 else (255,0,0,70))
    if x%50==0: d.text((X+2,2),str(x),fill=(0,0,0))
  for y in range(box[1]-box[1]%step,box[3],step):
    Y=(y-box[1])*s; d.line([(0,Y),(bg.size[0],Y)],fill=(0,0,255,255) if y%50==0 else (0,0,255,70))
    if y%50==0: d.text((2,Y+2),str(y),fill=(0,0,0))
  bg.save(name)
b=list(map(int,sys.argv[2].split(','))); g(b,sys.argv[3],int(sys.argv[4]))
