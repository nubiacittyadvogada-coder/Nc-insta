from PIL import Image, ImageDraw, ImageFont
import numpy as np
im=Image.open('/root/.claude/uploads/35e900c0-5567-55e2-9b5c-894faf2df1c8/78c3ad72-image.png').convert('RGB')
a=np.asarray(im).astype(float)
# erase top text rows 50..165 by vertical interpolation between row 45 and row 172
r0,r1=44,172
for y in range(r0+1,r1):
    t=(y-r0)/(r1-r0); a[y]=a[r0]*(1-t)+a[r1]*t
H,W=a.shape[:2]
# bottom darkening
dark=np.array([13,12,12],float)
for y in range(690,H):
    al=min(1,max(0,(y-690)/180))
    if y>=870: al=1
    a[y]=a[y]*(1-al)+dark*al
im=Image.fromarray(a.clip(0,255).astype('uint8'))
d=ImageDraw.Draw(im)
B='bodoni-moda-latin-600-normal.ttf'; BI='bodoni-moda-latin-600-italic.ttf'
I='/usr/share/fonts/opentype/inter/Inter-Bold.otf'; IR='/usr/share/fonts/opentype/inter/Inter-Regular.otf'; IS='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
F=ImageFont.truetype
gold=(232,196,130); white=(245,242,238); grey=(205,200,195)
# badge
f=F(I,30); t='WORKSHOP HÍBRIDO · 8 E 9/12'
tw=d.textlength(t,font=f)
d.rounded_rectangle((84,64,84+tw+96+len(t)*2.2,116),radius=26,fill=(28,26,26))
d.ellipse((104,79,126,101),fill=(214,60,60))
# letterspacing
x=140
for ch in t:
    d.text((x,72),ch,font=f,fill=gold); x+=d.textlength(ch,font=f)+2.2
fn=F(B,42); d.text((996-d.textlength('Núbia Citty',font=fn),66),'Núbia Citty',font=fn,fill=white)
fh=F(IR,22); d.text((996-d.textlength('@nubiacitty',font=fh),122),'@nubiacitty',font=fh,fill=grey)
# title
d.text((84,790),'Crie o seu primeiro',font=F(B,74),fill=white)
d.text((84,872),'sistema com IA.',font=F(BI,96),fill=gold)
d.text((84,1000),'Comigo, do zero até funcionando. Você sai com o',font=F(IR,29),fill=white)
d.text((84,1040),'sistema pronto para usar e a aula fica gravada.',font=F(IR,29),fill=white)
# prices
def box(x,y,w,h,top,price,sub,hl=False):
    d.rounded_rectangle((x,y,x+w,y+h),radius=22,fill=(232,196,130) if hl else (30,28,28),outline=None if hl else (90,80,70),width=2)
    c=(20,18,18) if hl else white; c2=(60,50,40) if hl else grey
    d.text((x+28,y+20),top,font=F(I,22),fill=c2)
    d.text((x+28,y+50),price,font=F(B,62),fill=c)
    d.text((x+28,y+128),sub,font=F(IS,21),fill=c2)
box(84,1110,430,170,'ONLINE AO VIVO','R$ 497','em até 12x no cartão')
box(540,1110,456,170,'PRESENCIAL EM ITABIRA','R$ 997','só 10 vagas · café e networking',hl=True)
d.text((84,1300),'8 e 9 de dezembro',font=F(IS,24),fill=gold)
d.text((996-d.textlength('Responda ONLINE ou PRESENCIAL',font=F(IS,24)),1300),'Responda ONLINE ou PRESENCIAL',font=F(IS,24),fill=white)
im.save('workshop-arte.jpg',quality=93)
im.resize((540,675)).save('prev.jpg')
