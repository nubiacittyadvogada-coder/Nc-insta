from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, json, math, sys
W,H=1080,1350
LT,LS=120,90
def row(i): return LT+LS*i
F5='caveat500.ttf'; F7='caveat700.ttf'
INK=(28,30,44)
def paper(seed=1):
    random.seed(seed)
    im=Image.new('RGB',(W,H),(244,242,236))
    px=im.load()
    n=Image.effect_noise((W,H),10).convert('L')
    im=Image.blend(im,Image.merge('RGB',(n,n,n)).point(lambda v:v*0+v),0.04)
    d=ImageDraw.Draw(im)
    for y in range(LT,H,LS): d.line((0,y,W,y),fill=(150,175,215),width=2)
    d.line((110,0,110,H),fill=(214,120,120),width=3)
    return im
def wobble_line(d,x1,y,x2,w=4,amp=3,seed=0):
    random.seed(seed); pts=[]
    for i in range(0,41):
        x=x1+(x2-x1)*i/40; pts.append((x,y+amp*math.sin(i/6+seed)+random.uniform(-0.8,0.8)))
    d.line(pts,fill=INK,width=w,joint='curve')
def text(d,xy,s,size,bold=False,fill=INK):
    d.text(xy,s,font=ImageFont.truetype(F7 if bold else F5,size),fill=fill)
    return ImageFont.truetype(F7 if bold else F5,size).getlength(s)
def sign(d): 
    f=ImageFont.truetype(F5,40); s='@nubiacitty'; d.text((W-60-f.getlength(s),45),s,font=f,fill=(90,90,110))
def cover(title,items,out,seed):
    im=paper(seed); d=ImageDraw.Draw(im); r=1
    for k,line in enumerate(title):
        L=text(d,(150,row(r)-84),line,100,True)
        if k==len(title)-1: wobble_line(d,150,row(r)+12,150+L,4,2,seed); wobble_line(d,165,row(r)+24,150+L-15,3,2,seed+2)
        r+=1
    r+=1
    for it in items:
        lines=it if isinstance(it,list) else [it]
        d.ellipse((140,row(r)-34,158,row(r)-16),fill=INK)
        for l in lines: text(d,(185,row(r)-72),l,84); r+=1
    r=max(r+1,12)
    L=text(d,(W-500,row(r)-72),'passe pro lado',76)
    yy=row(r)-30
    d.line((W-600,yy,W-520,yy),fill=INK,width=5); d.line((W-538,yy-14,W-518,yy),fill=INK,width=5); d.line((W-538,yy+14,W-518,yy),fill=INK,width=5)
    wobble_line(d,W-500,row(r)+10,W-500+L,3,2,seed+5)
    sign(d); im.save(out,quality=95)
def explain(blocks,out,seed):
    im=paper(seed); d=ImageDraw.Draw(im); r=1
    for head,body in blocks:
        L=text(d,(150,row(r)-76),head,84,True); wobble_line(d,150,row(r)+8,150+L,3,2,seed); r+=1
        for l in body: text(d,(150,row(r)-62),l,66); r+=1
        r+=0.0
    sign(d); im.save(out,quality=95)
def final(lines,out,seed,photo='/home/user/Nc-insta/links/foto.png'):
    im=paper(seed); d=ImageDraw.Draw(im)
    p=Image.open(photo).convert('RGB'); s=min(p.size); p=p.crop(((p.width-s)//2,0,(p.width-s)//2+s,s)).resize((380,380))
    m=Image.new('L',(380,380),0); ImageDraw.Draw(m).ellipse((0,0,380,380),fill=255)
    im.paste(p,((W-380)//2,140),m); d.ellipse(((W-380)//2-6,134,(W+380)//2+6,526),outline=INK,width=4)
    y=row(6)-70
    for l,sz,b in lines:
        f=ImageFont.truetype(F7 if b else F5,sz); x=(W-f.getlength(l))/2; d.text((x,y),l,font=f,fill=INK); y+=LS
    sign(d); im.save(out,quality=95)
spec=json.load(open(sys.argv[1]))
for c in spec:
    cover(c['title'],c['items'],c['id']+'-1.jpg',c['seed'])
    explain(c['blocks'],c['id']+'-2.jpg',c['seed']+1)
    final(c['final'],c['id']+'-3.jpg',c['seed']+2)
print('ok')
