#!/usr/bin/env python3
"""JARVIS AI — Variations B & C + 8K Upscale of all 3 posters."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont, ImageOps
import math, os, time

MIDNIGHT=(11,20,33); CHARCOAL=(26,29,36); SURFACE2=(22,27,38)
GOLD=(232,197,74); GOLD_DEEP=(212,175,55); GOLD_WARM=(200,170,60)
NEON=(255,0,51); CYAN=(30,200,230); CYAN_DEEP=(10,58,74)
TEXT=(234,246,248); MUTED=(138,160,176)

W,H=3840,2160; RAW_W,RAW_H=7680,4320
OUT="/data/data/com.termux/files/home/jarvis-reconstruct/posters"

def F(s): 
    try: return ImageFont.truetype("/system/fonts/DroidSans-Bold.ttf", s)
    except: return ImageFont.load_default()
def FR(s):
    try: return ImageFont.truetype("/system/fonts/DroidSans.ttf", s)
    except: return ImageFont.load_default()

FB= lambda s: F(int(H*s)); FRl= lambda s: FR(int(H*s))

def radial_bg(cc,ce,p=1.3):
    sw,sh=max(12,W//32),max(12,H//32)
    sm=Image.new("RGB",(sw,sh),ce); d=ImageDraw.Draw(sm)
    cx,cy=sw/2,sh/2; md=math.hypot(cx,cy)
    for i in range(80,0,-1):
        t=i/80; r=md*t; k=t**p
        c=tuple(int(cc[j]*(1-k)+ce[j]*k) for j in range(3))
        d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=c,width=2)
    return sm.resize((W,H),Image.LANCZOS)

def glow(w,h,cx,cy,r,col,a=40,b=60):
    l=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(l)
    for ri in range(r,0,-max(1,r//30)):
        al=int(a*(ri/r)**2); d.ellipse([cx-ri,cy-ri,cx+ri,cy+ri],fill=(*col,al))
    return l.filter(ImageFilter.GaussianBlur(b))

def vig(img,s=0.6,inn=0.35):
    v=Image.new("L",(W,H),0); vd=ImageDraw.Draw(v)
    cx,cy=W/2,H/2; md=math.hypot(cx,cy)
    for i in range(60,0,-1):
        t=i/60; r=md*t
        al=int(255*s*((t-inn)/(1-inn))**2) if t>inn else 0
        vd.ellipse([cx-r,cy-r,cx+r,cy+r],outline=al,width=2)
    v=v.resize((W,H),Image.LANCZOS)
    dk=Image.new("RGB",(W,H),(4,4,6))
    return Image.composite(dk,img.convert("RGB"),v)

def grain(img,sig=12):
    g=Image.effect_noise((W,H),sig).convert("RGB"); g=ImageOps.autocontrast(g)
    return Image.blend(img,ImageChops.multiply(img,g),0.04)

def centered(d,txt,fnt,cy,col,gc=None,gr=0):
    bb=d.textbbox((0,0),txt,font=fnt); tw=bb[2]-bb[0]
    tx=(W-tw)//2; ty=cy-(bb[3]+bb[1])//2
    if gc and gr:
        for o in range(gr,0,-1):
            al=int(100*(o/gr)**2)
            for dx,dy in((o,0),(-o,0),(0,o),(0,-o)):
                d.text((tx+dx,ty+dy),txt,font=fnt,fill=(*gc,al))
    d.text((tx,ty),txt,font=fnt,fill=col)

def reactor(d,cx,cy,R):
    for rm,col,w in[(1.00,GOLD,5),(0.86,GOLD_DEEP,4),(0.72,GOLD,3),
                     (0.58,NEON,2),(0.44,CYAN,2),(0.30,GOLD,2),(0.16,NEON,1)]:
        r=int(R*rm); d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col,width=w)
    for i in range(16):
        a=i*2*math.pi/16-math.pi/2
        d.line([cx+int(math.cos(a)*R*0.35),cy+int(math.sin(a)*R*0.35),
                cx+int(math.cos(a)*R*0.95),cy+int(math.sin(a)*R*0.95)],fill=GOLD,width=2)
    cr=int(R*0.11); d.ellipse([cx-cr,cy-cr,cx+cr,cy+cr],fill=GOLD)
    cr2=int(R*0.04); d.ellipse([cx-cr2,cy-cr2,cx+cr2,cy+cr2],fill=(255,250,220))

def huds(d,m=None,b=None,a=220):
    if m is None:m=int(min(W,H)*0.045)
    if b is None:b=int(min(W,H)*0.075)
    bw=max(2,int(min(W,H)*0.0012))
    for cx,cy in[(m,m),(W-m,m),(m,H-m),(W-m,H-m)]:
        dx=1 if cx<W//2 else -1; dy=1 if cy<H//2 else -1
        d.line([cx,cy,cx+dx*b,cy],fill=(*GOLD,a),width=bw)
        d.line([cx,cy,cx,cy+dy*b],fill=(*GOLD,a),width=bw)
        tl=int(b*0.18)
        d.line([cx+dx*b,cy,cx+dx*b,cy+dy*tl],fill=(*GOLD,int(a*0.8)),width=bw)
        d.line([cx,cy+dy*b,cx+dx*tl,cy+dy*b],fill=(*GOLD,int(a*0.8)),width=bw)

t0=time.time()

# ════════════ VAR B: DARK MINIMAL ════════════
print("[VAR-B] Dark Minimal...",flush=True)
img=radial_bg((18,30,48),(6,10,18),p=1.6).convert("RGBA")
ecx,ecy=W//2,int(H*0.44); R=int(H*0.28)
img=Image.alpha_composite(img,glow(W,H,ecx,ecy,int(R*1.5),GOLD,a=30,b=90))
img=Image.alpha_composite(img,glow(W,H,ecx,ecy,int(R*0.8),GOLD,a=45,b=40))
d=ImageDraw.Draw(img)
for i in range(20):
    rm=1.0-i*0.045
    if rm<0.12:break
    r=int(R*rm); col=[GOLD,GOLD_DEEP,GOLD_WARM,NEON][i%4]; w=max(1,5-i//4)
    d.ellipse([ecx-r,ecy-r,ecx+r,ecy+r],outline=col,width=w)
for i in range(64):
    a=i*2*math.pi/64
    if i%3==0:
        r1,r2=int(R*0.82),int(R*0.88)
        d.line([ecx+int(math.cos(a)*r1),ecy+int(math.sin(a)*r1),
                ecx+int(math.cos(a)*r2),ecy+int(math.sin(a)*r2)],fill=(*GOLD,200),width=3)
for i in range(24):
    a=i*2*math.pi/24-math.pi/2
    d.line([ecx+int(math.cos(a)*R*0.30),ecy+int(math.sin(a)*R*0.30),
            ecx+int(math.cos(a)*R*0.95),ecy+int(math.sin(a)*R*0.95)],
           fill=(GOLD if i%2==0 else GOLD_WARM),width=2)
cr=int(R*0.11)
img=Image.alpha_composite(img,glow(W,H,ecx,ecy,cr*3,GOLD,a=120,b=25))
d=ImageDraw.Draw(img)
d.ellipse([ecx-cr,ecy-cr,ecx+cr,ecy+cr],fill=(255,245,200),outline=(255,255,255),width=3)
ts=int(R*0.06)
d.polygon([(ecx,ecy-int(R*1.06)-ts),(ecx-ts,ecy-int(R*1.06)+ts),
           (ecx+ts,ecy-int(R*1.06)+ts)],fill=GOLD)
centered(d,"J A R V I S",FB(0.051),int(H*0.78),GOLD,gc=GOLD,gr=12)
centered(d,"A I   A S S I S T A N T",FRl(0.030),int(H*0.84),GOLD_DEEP)
centered(d,"jarvis-ai-3ba39.web.app",FRl(0.022),int(H*0.90),MUTED)
huds(d)
rgb=vig(img.convert("RGB"),s=0.50); rgb=grain(rgb,10)
rgb.save(f"{OUT}/jarvis_poster_B_dark_minimal.png",quality=100)
print(f"  saved B ({time.time()-t0:.0f}s)",flush=True)

# ════════════ VAR C: BLUEPRINT TECHNICAL ════════════
print("[VAR-C] Blueprint Technical...",flush=True)
img=radial_bg((15,24,40),(6,10,18),p=1.2).convert("RGBA")
ecx,ecy=W//2,int(H*0.42); R=int(H*0.22)
grid=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(grid)
for x in range(0,W,int(W*0.05)):
    gd.line([(x,0),(x,H)],fill=(*CYAN,12),width=1)
for y in range(0,H,int(H*0.05)):
    gd.line([(0,y),(W,y)],fill=(*CYAN,12),width=1)
for x in range(0,W,int(W*0.01)):
    gd.line([(x,0),(x,H)],fill=(*CYAN,4),width=1)
for y in range(0,H,int(H*0.01)):
    gd.line([(0,y),(W,y)],fill=(*CYAN,4),width=1)
gd.line([(ecx,0),(ecx,H)],fill=(*GOLD,30),width=2)
gd.line([(0,ecy),(W,ecy)],fill=(*GOLD,30),width=2)
for ang in[math.pi/4,-math.pi/4,3*math.pi/4,-3*math.pi/4]:
    x2=ecx+int(math.cos(ang)*max(W,H)); y2=ecy+int(math.sin(ang)*max(W,H))
    gd.line([(ecx,ecy),(x2,y2)],fill=(*GOLD,12),width=1)
img=Image.alpha_composite(img,grid)
img=Image.alpha_composite(img,glow(W,H,ecx,ecy,int(R*1.5),GOLD,a=25,b=70))
img=Image.alpha_composite(img,glow(W,H,ecx,ecy,int(R*0.6),GOLD,a=40,b=30))
d=ImageDraw.Draw(img)
reactor(d,ecx,ecy,R)
for i in range(72):
    a=i*2*math.pi/72
    r1=R*1.02; r2=R*1.05 if i%9==0 else R*1.035 if i%3==0 else R*1.025
    d.line([ecx+int(math.cos(a)*r1),ecy+int(math.sin(a)*r1),
            ecx+int(math.cos(a)*r2),ecy+int(math.sin(a)*r2)],fill=(*GOLD,160),width=1)
for i in range(8):
    a=i*math.pi/4; r=R*1.10
    bx=ecx+int(math.cos(a)*r)-10; by=ecy+int(math.sin(a)*r)-6
    d.text((bx,by),f"{i*45}\u00B0",font=FRl(0.011),fill=(*CYAN,140))
for rm,label in[(1.00,"R"),(0.58,"R\u00BD"),(0.30,"R\u00BC")]:
    r=int(R*rm)
    d.line([ecx,ecy,ecx+r,ecy],fill=(*CYAN,80),width=1)
    d.polygon([(ecx+r-6,ecy-4),(ecx+r,ecy),(ecx+r-6,ecy+4)],fill=(*CYAN,120))
    d.text((ecx+int(r*0.6),ecy-int(H*0.012)),label,font=FRl(0.011),fill=(*CYAN,140))
huds(d)
# annotations
f_mc=FRl(0.011); f_t=FRl(0.016)
annos=[
    (int(W*0.06),int(H*0.08),"SYSTEM ARCHITECTURE",f_mc,GOLD),
    (int(W*0.06),int(H*0.10),"CLASS: CINEMATIC POSTER v1.0",f_mc,CYAN),
    (int(W*0.06),int(H*0.12),f"RES: {RAW_W}\u00D7{RAW_H} (8K UHD)",f_mc,CYAN),
    (int(W*0.06),int(H*0.14),"ASP: 16:9 | RGB | 16-BIT PIPELINE",f_mc,MUTED),
    (W-int(W*0.22),int(H*0.08),"ENGINEER: MOKSHITH REDDY",f_mc,GOLD),
    (W-int(W*0.22),int(H*0.10),"BACKEND: CLOUDFLARE + GROQ",f_mc,CYAN),
    (W-int(W*0.22),int(H*0.12),"AUTH: FIREBASE GOOGLE SIGN-IN",f_mc,MUTED),
    (W-int(W*0.22),int(H*0.14),"HOSTING: FIREBASE (STATIC EXPORT)",f_mc,MUTED),
]
for x,y,txt,f,c in annos:
    d.text((x,y),txt,font=f,fill=(*c,160))
# title
centered(d,"JARVIS",FB(0.092),int(H*0.64),GOLD,gc=GOLD,gr=16)
centered(d,"CINEMATIC AI ARCHITECTURE",FRl(0.022),int(H*0.72),CYAN,gc=CYAN,gr=4)
centered(d,"jarvis-ai-3ba39.web.app",FRl(0.022),int(H*0.78),NEON,gc=NEON,gr=4)
centered(d,"YOUR INTELLIGENCE. AMPLIFIED.",FRl(0.022),int(H*0.84),MUTED)
# coord
d.text((int(W*0.04),H-int(H*0.06)),f"SEC-01:REACTOR  SEC-02:HUD  SEC-03:NEURAL  SEC-04:VIGNETTE  SEC-05:GRAIN  SEC-06:TYPO  SEC-07:BADGE",
       font=FRl(0.011),fill=(*CYAN,80))
rgb=vig(img.convert("RGB"),s=0.55); rgb=grain(rgb,14)
rgb.save(f"{OUT}/jarvis_poster_C_blueprint.png",quality=100)
print(f"  saved C ({time.time()-t0:.0f}s)",flush=True)

# ════════════ 8K UPSCALE ALL THREE ════════════
print("\n[8K UPSCALE] Running LANCZOS...",flush=True)
files=[
    ("jarvis_poster_HERO.png","jarvis_poster_HERO_8K.png"),
    ("jarvis_poster_B_dark_minimal.png","jarvis_poster_B_8K.png"),
    ("jarvis_poster_C_blueprint.png","jarvis_poster_C_8K.png"),
]
for src,dst in files:
    sp=f"{OUT}/{src}"; dp=f"{OUT}/{dst}"
    if not os.path.exists(sp): continue
    print(f"  Upscaling {src}...",flush=True)
    img=Image.open(sp)
    img=img.resize((RAW_W,RAW_H),Image.LANCZOS)
    img.save(dp,quality=100)
    sz=os.path.getsize(dp)
    print(f"  -> {dst} ({RAW_W}x{RAW_H}, {sz/1024/1024:.1f} MB)",flush=True)

print(f"\n{'='*60}")
print(f"  ALL POSTERS COMPLETE ({time.time()-t0:.0f}s)")
print(f"  4K base + 8K upscaled versions in {OUT}")
print(f"{'='*60}")
