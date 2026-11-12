from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, json, math, sys
W,H=1080,1350
LT,LS=120,90
def row(i): return LT+LS*i
F5='cedarville-cursive.ttf'; F7='cedarville-cursive.ttf'
INK=(22,28,62)
def paper(seed=1):
    random.seed(seed)
    im=Image.new('RGB',(W,H),(244,242,236))
    px=im.load()
    n=Image.effect_noise((W,H),10).convert('L')
    im=Image.blend(im,Image.merge('RGB',(n,n,n)).point(lambda v:v*0+v),0.04)
    d=ImageDraw.Draw(im)
    for y in range(LT,H,LS): d.line((0,y,W,y),fill=(150,175,215),width=2)
    d.line((110,0,110,H),fill=(214,120,120),width=3)
    im=im.convert('RGBA'); CANVAS[0]=im
    return im
def wobble_line(d,x1,y,x2,w=4,amp=3,seed=0):
    random.seed(seed); pts=[]
    for i in range(0,41):
        x=x1+(x2-x1)*i/40; pts.append((x,y+amp*math.sin(i/6+seed)+random.uniform(-0.8,0.8)))
    d.line(pts,fill=INK,width=w,joint='curve')
CANVAS=[None]
def text(d,xy,s,size,bold=False,fill=INK,maxw=None):
    maxw=maxw or (W-60-xy[0])
    f=ImageFont.truetype(F5,size)
    while f.getlength(s)>maxw and size>30: size-=2; f=ImageFont.truetype(F5,size)
    L=f.getlength(s); h=int(size*1.6)
    lay=Image.new('RGBA',(int(L)+40,h+40),(0,0,0,0)); ld=ImageDraw.Draw(lay)
    ld.text((20,20),s,font=f,fill=fill+(235,),stroke_width=(1 if bold else 0),stroke_fill=fill+(235,))
    lay=lay.rotate(random.uniform(-0.35,0.35),resample=Image.BICUBIC,expand=False)
    lay=lay.filter(ImageFilter.GaussianBlur(0.35))
    asc=f.getmetrics()[0]
    CANVAS[0].alpha_composite(lay,(int(xy[0])-20,int(xy[1]-asc)-20+int(random.uniform(-1,1))))
    return L
def sign(d): 
    f=ImageFont.truetype(F5,40); s='@nubiacitty'; d.text((W-60-f.getlength(s),45),s,font=f,fill=(90,90,110))
def finish(im):
    im=CANVAS[0].convert('RGB')
    # luz de foto: leve vinheta e gradiente
    g=Image.new('L',(W,H),0); gd=ImageDraw.Draw(g)
    for i in range(0,60): gd.rectangle((i*6,i*6,W-i*6,H-i*6),outline=int(i*1.2))
    g=g.filter(ImageFilter.GaussianBlur(40))
    dark=Image.new('RGB',(W,H),(205,200,190))
    return Image.composite(im,dark,g.point(lambda v:min(255,185+v)))
def cover(title,items,out,seed):
    im=paper(seed); d=ImageDraw.Draw(im); r=1
    for k,line in enumerate(title):
        L=text(d,(150,row(r)),line,88,True)
        if k==len(title)-1: wobble_line(d,150,row(r)+18,150+L,4,2,seed); wobble_line(d,165,row(r)+30,150+L-15,3,2,seed+2)
        r+=1
    r+=1
    for it in items:
        lines=it if isinstance(it,list) else [it]
        d.ellipse((140,row(r)-34,158,row(r)),fill=INK)
        for l in lines: text(d,(185,row(r)),l,76); r+=1
    r=max(r+1,12)
    L=text(d,(W-500,row(r)),'passe pro lado',70)
    yy=row(r)-22
    d.line((W-600,yy,W-520,yy),fill=INK,width=5); d.line((W-538,yy-14,W-518,yy),fill=INK,width=5); d.line((W-538,yy+14,W-518,yy),fill=INK,width=5)
    wobble_line(d,W-500,row(r)+16,W-500+L,3,2,seed+5)
    sign(d); finish(im).save(out,quality=95)
def explain(blocks,out,seed):
    im=paper(seed); d=ImageDraw.Draw(im); r=1
    for head,body in blocks:
        L=text(d,(150,row(r)),head,76,True); wobble_line(d,150,row(r)+16,150+L,3,2,seed); r+=1
        for l in body: text(d,(150,row(r)),l,62); r+=1
        r+=0.0
    sign(d); finish(im).save(out,quality=95)
def final(lines,out,seed,photo='/home/user/Nc-insta/links/foto.png'):
    im=paper(seed); d=ImageDraw.Draw(im)
    p=Image.open(photo).convert('RGB'); s=min(p.size); p=p.crop(((p.width-s)//2,0,(p.width-s)//2+s,s)).resize((380,380))
    m=Image.new('L',(380,380),0); ImageDraw.Draw(m).ellipse((0,0,380,380),fill=255)
    im.paste(p,((W-380)//2,140),m); d.ellipse(((W-380)//2-6,134,(W+380)//2+6,526),outline=INK,width=4)
    for i,(l,sz,b) in enumerate(lines):
        f=ImageFont.truetype(F5,sz); x=(W-f.getlength(l))/2; text(d,(x,row(6+i)),l,sz,b)
    sign(d); finish(im).save(out,quality=95)
spec=json.load(open(sys.argv[1]))
for c in spec:
    cover(c['title'],c['items'],c['id']+'-1.jpg',c['seed'])
    explain(c['blocks'],c['id']+'-2.jpg',c['seed']+1)
    final(c['final'],c['id']+'-3.jpg',c['seed']+2)
print('ok')
