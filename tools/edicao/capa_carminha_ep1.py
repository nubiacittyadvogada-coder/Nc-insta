from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D='/tmp/claude-0/-home-user/35e900c0-5567-55e2-9b5c-894faf2df1c8/scratchpad/qc/cap/'
W,H=1080,1920
c=Image.new('RGB',(W,H),(14,12,12))
nov=Image.open(D+'n_12.8.png').convert('RGB').crop((0,30,1080,870))
nov=ImageEnhance.Contrast(nov).enhance(1.12)
c.paste(nov,(0,0))
me=Image.open(D+'p_6.png').convert('RGB').crop((0,430,1080,1250))
c.paste(me,(0,1100))
# gradients
g=Image.new('L',(1,H),0)
for y in range(H):
    a=0
    if 620<=y<840: a=int(255*(y-620)/220)
    elif 840<=y<1100: a=255
    elif 1100<=y<1260: a=int(255*(1-(y-1100)/160))
    elif y>1680: a=int(215*(y-1680)/240)
    g.putpixel((0,y),a)
g=g.resize((W,H))
c=Image.composite(Image.new('RGB',(W,H),(14,12,12)),c,g)
d=ImageDraw.Draw(c)
F=lambda p,s:ImageFont.truetype(p,s)
inter='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
interx='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
ser='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
seri='/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
pink=(236,170,180); red=(190,30,45)
# badge episodio
f=F(interx,40); t='EPISÓDIO 1'
bw=d.textlength(t,font=f)+60
d.rounded_rectangle((60,70,60+bw,140),radius=10,fill=red)
d.text((90,82),t,font=f,fill='white')
d.text((60,160),'ISSO DARIA CADEIA?',font=F(inter,30),fill=(255,255,255))
# credit
d.text((60,790),'AVENIDA BRASIL · TV GLOBO, 2012',font=F(inter,22),fill=(220,220,220))
# title band
def center(txt,font,y,fill):
    w=d.textlength(txt,font=font); d.text(((W-w)/2,y),txt,font=font,fill=fill)
center('A Carminha largou',F(ser,84),870,'white')
center('a Rita no lixão.',F(ser,84),960,'white')
center('Daria cadeia?',F(seri,110),1050,pink)
# arrow-ish divider
d.line((440,1185,640,1185),fill=pink,width=3)
center('A resposta vai irritar o Brasil',F(inter,38),1745,'white')
center('Núbia Citty · advogada criminalista',F(inter,26),1810,(200,200,200))
c.save('/home/user/Nc-insta/prontos-para-publicar/2026-11-11-carminha/capa-carminha-ep1.png')
c.resize((540,960)).save(D+'capa_prev.jpg',quality=85)
