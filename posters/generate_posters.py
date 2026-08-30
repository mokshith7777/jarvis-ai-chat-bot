#!/usr/bin/env python3
"""Generate 3 cinematic JARVIS AI posters (4K UHD = 3840x2160)."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import math, random, os, time

# ---- JARVIS Brand Colors ----
GOLD      = (232, 197, 74)
GOLD_DEEP = (212, 175, 55)
NEON      = (255, 0, 51)
CYAN      = (30, 200, 230)
MIDNIGHT  = (11, 20, 33)
CHARCOAL  = (26, 29, 36)
SURFACE2  = (22, 27, 38)
MUTED     = (138, 160, 176)

W, H = 3840, 2160
OUT = "/data/data/com.termux/files/home/jarvis-reconstruct/posters"
os.makedirs(OUT, exist_ok=True)

# ---- Fonts ----
def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

FB = lambda s: load_font("/system/fonts/DroidSans-Bold.ttf", s)
FR = lambda s: load_font("/system/fonts/DroidSans.ttf", s)
# keep one instance per size to reduce font loading cost
F_HERO  = FB(200)   # JARVIS main
F_BIG   = FB(110)   # section titles
F_MED   = FB(64)    # subtitles
F_SM    = FR(48)    # url/tagline
F_TINY  = FR(34)    # HUD labels

# ---- Fast helpers (all C-level, no per-pixel python loops) ----

def radial_bg(w, h, c_center, c_edge, power=1.6, scale=6):
    """Smooth radial gradient background via small canvas + upscale."""
    sw, sh = max(8, w // scale), max(8, h // scale)
    small = Image.new("RGB", (sw, sh), c_edge)
    sd = ImageDraw.Draw(small)
    cx, cy = sw / 2, sh / 2
    maxd = math.hypot(cx, cy)
    steps = 96
    for i in range(steps, 0, -1):
        t = i / steps
        r = maxd * t
        k = t ** power
        col = tuple(int(c_center[j] * (1 - k) + c_edge[j] * k) for j in range(3))
        sd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    return small.resize((w, h), Image.BILINEAR)

def vignette(img, strength=0.55, color=MIDNIGHT, scale=4):
    """Radial vignette mask, composited at small scale then upscaled."""
    sw, sh = img.width // scale, img.height // scale
    mask = Image.new("L", (sw, sh), 0)
    md = ImageDraw.Draw(mask)
    cx, cy = sw / 2, sh / 2
    maxd = math.hypot(cx, cy)
    steps = 64
    for i in range(steps, 0, -1):
        t = i / steps
        r = maxd * t
        alpha = int(255 * ((1 - t) ** 2) * strength)
        md.ellipse([cx - r, cy - r, cx + r, cy + r], outline=alpha, width=2)
    mask = mask.resize(img.size, Image.BILINEAR)
    dark = Image.new("RGB", img.size, color)
    return Image.composite(dark, img, mask)

def film_grain(img, sigma=14, alpha=0.05):
    """Grain using Image.effect_noise (C-level) blended softly."""
    noise = Image.effect_noise(img.size, sigma).convert("L")
    noise_img = Image.new("RGB", img.size, (0, 0, 0))
    noise_img = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, ImageChops.multiply(img, noise_img), alpha)

def glow_layer(size, draw_fn, blur=60):
    """Draw on transparent layer, blur it, return RGBA layer."""
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay))
    return lay.filter(ImageFilter.GaussianBlur(blur))

def center_text(draw, text, font, cy, color, glow=None, glow_rad=0, spacing=0):
    """Draw horizontally centered text at vertical center cy, with optional glow."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = cy - (bbox[3] + bbox[1]) // 2
    if glow and glow_rad:
        gl = glow if isinstance(glow, tuple) else color
        for o in range(glow_rad, 0, -1):
            a = int(90 * (o / glow_rad) ** 2)
            for dx, dy in ((o, 0), (-o, 0), (0, o), (0, -o)):
                draw.text((tx + dx, ty + dy), text, font=font, fill=(*gl, a))
    return draw.text((tx, ty), text, font=font, fill=color)

def arc_reactor(draw, cx, cy, R, colors_widths, spokes=16, core_frac=0.2):
    """Draw an arc-reactor style emblem: rings + spokes + bright core."""
    for rm, color, width in colors_widths:
        r = int(R * rm)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    for i in range(spokes):
        a = i * 2 * math.pi / spokes - math.pi / 2
        x1 = cx + int(math.cos(a) * R * 0.35)
        y1 = cy + int(math.sin(a) * R * 0.35)
        x2 = cx + int(math.cos(a) * R * 0.92)
        y2 = cy + int(math.sin(a) * R * 0.92)
        draw.line([x1, y1, x2, y2], fill=GOLD, width=2)
    cr = int(R * core_frac)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=GOLD)

def starfield(size, n=260, seed=7):
    """Subtle starfield overlay."""
    rng = random.Random(seed)
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y = rng.randint(0, size[0]), rng.randint(0, size[1])
        s = rng.randint(1, 3)
        a = rng.randint(30, 120)
        col = GOLD if rng.random() < 0.6 else CYAN
        d.ellipse([x - s, y - s, x + s, y + s], fill=(*col, a))
    return lay

def hud_corners(draw, m=0.05, size=0.07, width=6, color=GOLD, alpha=200):
    """HUD corner brackets."""
    bx = int(W * size)
    pts = [(int(W*m), int(H*m)), (W-int(W*m), int(H*m)),
           (int(W*m), H-int(H*m)), (W-int(W*m), H-int(H*m))]
    for cx, cy in pts:
        s = 1 if (cx < W//2) != (cy < H//2) else 1
        # draw an L bracket opening toward the far corner
        hx = 1 if cx < W//2 else -1
        hy = 1 if cy < H//2 else -1
        draw.line([cx, cy, cx + hx*bx, cy], fill=(*color, alpha), width=width)
        draw.line([cx, cy, cx, cy + hy*bx], fill=(*color, alpha), width=width)
        draw.line([cx + hx*bx, cy, cx + hx*bx, cy + hy*int(bx*0.18)], fill=(*color, alpha), width=width)
        draw.line([cx, cy + hy*bx, cx + hx*int(bx*0.18), cy + hy*bx], fill=(*color, alpha), width=width)

t0 = time.time()

# ============================================================
# POSTER 1 — "NEON GENESIS" (cinematic cyberpunk glow, hero centered)
# ============================================================
print("Poster 1: Neon Genesis ...", flush=True)
img = radial_bg(W, H, (24, 38, 58), MIDNIGHT, power=1.4)

# gold center bloom
img = Image.alpha_composite(img.convert("RGBA"), glow_layer(img.size,
        lambda d: d.ellipse([W//2-900, H//2-900, W//2+900, H//2+900], fill=(*GOLD, 26)), 200)).convert("RGB")
img = Image.alpha_composite(img.convert("RGBA"), glow_layer(img.size,
        lambda d: d.ellipse([W//2-520, H//2-520, W//2+520, H//2+520], fill=(*GOLD, 40)), 140)).convert("RGB")
# cyan accents corners
img = Image.alpha_composite(img.convert("RGBA"), glow_layer(img.size,
        lambda d: d.ellipse([int(W*.85)-500, int(H*.13)-500, int(W*.85)+500, int(H*.13)+500], fill=(*CYAN, 34)), 260)).convert("RGB")
img = Image.alpha_composite(img.convert("RGBA"), glow_layer(img.size,
        lambda d: d.ellipse([int(W*.14)-500, int(H*.86)-500, int(W*.14)+500, int(H*.86)+500], fill=(*NEON, 28)), 260)).convert("RGB")

d = ImageDraw.Draw(img)

# hex grid (subtle)
rng = random.Random(3)
for row in range(-1, H // 150 + 3):
    for col in range(-1, W // 260 + 3):
        cx = col * 260 + (row % 2) * 130
        cy = row * 150
        if -150 < cx < W + 150 and -150 < cy < H + 150:
            pts = [(cx + 70 * math.cos(i * math.pi/3), cy + 70 * math.sin(i * math.pi/3)) for i in range(6)]
            d.polygon(pts, outline=(*GOLD, 12))

# arc reactor emblem — upper area
ecx, ecy = W // 2, int(H * 0.40)
R = int(H * 0.20)
arc_reactor(d, ecx, ecy, R, [
    (1.0, GOLD, 5), (0.86, GOLD_DEEP, 4), (0.72, GOLD, 3),
    (0.58, NEON, 2), (0.44, CYAN, 2), (0.30, GOLD, 2), (0.16, NEON, 1),
], spokes=16, core_frac=0.16)

# text block
center_text(d, "JARVIS", F_HERO, int(H * 0.62), GOLD, glow=GOLD, glow_rad=18)
center_text(d, "A I   A S S I S T A N T", F_MED, int(H * 0.68), MUTED)
center_text(d, "jarvis-ai-3ba39.web.app", F_SM, int(H * 0.80), NEON, glow=NEON, glow_rad=6)
center_text(d, "YOUR INTELLIGENCE. AMPLIFIED.", F_SM, int(H * 0.86), CYAN, glow=CYAN, glow_rad=6)

img = Image.alpha_composite(img.convert("RGBA"), starfield(img.size, 200, seed=7)).convert("RGB")
img = vignette(img, 0.5)
img = film_grain(img, 12, 0.04)
img.save(f"{OUT}/jarvis_poster_1_neon_genesis.png", quality=95)
print(f"  saved poster 1  ({time.time()-t0:.0f}s)", flush=True)

# ============================================================
# POSTER 2 — "ARC REACTOR / PALLADIUM" (minimal, logo-dominant, Stark vibes)
# ============================================================
print("Poster 2: Arc Reactor ...", flush=True)
img = radial_bg(W, H, (18, 30, 48), (7, 12, 22), power=1.7)
d = ImageDraw.Draw(img)

R = int(H * 0.30)
ecx, ecy = W // 2, H // 2
# soft outer bloom
img = Image.alpha_composite(img.convert("RGBA"), glow_layer(img.size,
        lambda dd: dd.ellipse([ecx-R-100, ecy-R-100, ecx+R+100, ecy+R+100], fill=(*GOLD, 22)), 220)).convert("RGB")
d = ImageDraw.Draw(img)

# reactor: many fine rings, dashed ring, spokes
rings = [(1.0, GOLD, 7), (0.94, GOLD_DEEP, 4), (0.88, GOLD, 2),
         (0.80, (200, 172, 70), 2), (0.74, NEON, 2), (0.66, CYAN, 1),
         (0.56, GOLD, 2), (0.50, GOLD_DEEP, 1), (0.44, GOLD, 2),
         (0.36, NEON, 1), (0.28, CYAN, 1), (0.20, GOLD, 1)]
for rm, color, width in rings:
    r = int(R * rm)
    d.ellipse([ecx - r, ecy - r, ecx + r, ecy + r], outline=color, width=width)

# dashed mid ring
for i in range(48):
    a = i * 2 * math.pi / 48
    if i % 3 == 0:
        r1, r2 = R * 0.83, R * 0.92
        x1 = ecx + int(math.cos(a) * r1); y1 = ecy + int(math.sin(a) * r1)
        x2 = ecx + int(math.cos(a) * r2); y2 = ecy + int(math.sin(a) * r2)
        d.line([x1, y1, x2, y2], fill=(*GOLD, 200), width=3)

# spokes
for i in range(24):
    a = i * 2 * math.pi / 24 - math.pi / 2
    x1 = ecx + int(math.cos(a) * R * 0.30); y1 = ecy + int(math.sin(a) * R * 0.30)
    x2 = ecx + int(math.cos(a) * R * 0.95); y2 = ecy + int(math.sin(a) * R * 0.95)
    d.line([x1, y1, x2, y2], fill=(GOLD if i % 2 == 0 else (150, 130, 60)), width=2)

# core
core_r = int(R * 0.11)
img = Image.alpha_composite(img.convert("RGBA"), glow_layer(img.size,
        lambda dd: dd.ellipse([ecx-core_r, ecy-core_r, ecx+core_r, ecy+core_r], fill=(*GOLD, 200)), 60)).convert("RGB")
d = ImageDraw.Draw(img)
d.ellipse([ecx-core_r, ecy-core_r, ecx+core_r, ecy+core_r], fill=(255, 240, 190),
          outline=(255, 255, 255), width=3)

# top tick
d.polygon([(ecx, ecy - int(R*1.06) - 18), (ecx - 24, ecy - int(R*1.06) + 14), (ecx + 24, ecy - int(R*1.06) + 14)], fill=GOLD)

# minimal text bottom
center_text(d, "J A R V I S", F_BIG, int(H * 0.78), GOLD, glow=GOLD, glow_rad=10, )
center_text(d, "A I   A S S I S T A N T", F_MED, int(H * 0.84), GOLD_DEEP)
center_text(d, "jarvis-ai-3ba39.web.app", F_SM, int(H * 0.90), MUTED)

img = Image.alpha_composite(img.convert("RGBA"), starfield(img.size, 140, seed=11)).convert("RGB")
img = vignette(img, 0.42, color=(4, 8, 16))
img = film_grain(img, 10, 0.03)
img.save(f"{OUT}/jarvis_poster_2_arc_reactor.png", quality=95)
print(f"  saved poster 2  ({time.time()-t0:.0f}s)", flush=True)

# ============================================================
# POSTER 3 — "HUD / NEURAL INTERFACE" (techy HUD, neural net, Iron-Man suits-up)
# ============================================================
print("Poster 3: HUD / Neural Interface ...", flush=True)
img = radial_bg(W, H, (30, 44, 66), (6, 10, 18), power=1.3)
d = ImageDraw.Draw(img)

# scanlines
for y in range(0, H, 6):
    d.line([(0, y), (W, y)], fill=(*CYAN, 6))

# neural network web (seeded, sparse)
rng = random.Random(42)
nodes = [(rng.randint(int(W*0.08), int(W*0.92)), rng.randint(int(H*0.12), int(H*0.88))) for _ in range(90)]
for i, (x1, y1) in enumerate(nodes):
    for j in range(i + 1, len(nodes)):
        x2, y2 = nodes[j]
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < 300:
            a = int(60 * (1 - dist / 300))
            col = CYAN if (i + j) % 2 else GOLD
            d.line([x1, y1, x2, y2], fill=(*col, a), width=1)
for i, (x, y) in enumerate(nodes):
    s = 3 if i % 3 else 5
    col = GOLD if i % 2 else CYAN
    d.ellipse([x - s, y - s, x + s, y + s], fill=(*col, 180))

# reactor emblem upper-center
ecx, ecy = W // 2, int(H * 0.42)
R = int(H * 0.17)
img = Image.alpha_composite(img.convert("RGBA"), glow_layer(img.size,
        lambda dd: dd.ellipse([ecx-R-120, ecy-R-120, ecx+R+120, ecy+R+120], fill=(*GOLD, 24)), 160)).convert("RGB")
d = ImageDraw.Draw(img)
arc_reactor(d, ecx, ecy, R, [
    (1.0, GOLD, 5), (0.86, GOLD_DEEP, 4), (0.72, GOLD, 3),
    (0.58, NEON, 2), (0.44, CYAN, 2), (0.30, GOLD, 2), (0.16, NEON, 1),
], spokes=16, core_frac=0.16)

# HUD frame
hud_corners(d, m=0.045, size=0.075, width=6, color=GOLD, alpha=220)

# HUD labels
def hud_label(text, x, y, color, anchor_left=True):
    f = F_TINY
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    tx = x if anchor_left else x - tw
    d.text((tx, y), text, font=f, fill=color)
    return tx, y, tw

hud_label("SYS.ARM // ONLINE", int(W*0.062), int(H*0.115), CYAN)
hud_label("NEURAL LINK: ACTIVE", int(W*0.062), int(H*0.135), GOLD)
hud_label("LAT: 17.3850°N  LON: 78.4867°E", W - int(W*0.062), int(H*0.115), CYAN, anchor_left=False)
hud_label("QUOTA: 24 / DAY", W - int(W*0.062), int(H*0.135), NEON, anchor_left=False)
hud_label("PWR  ▮▮▮▮▮▮▮▮▯ 94%", int(W*0.062), H - int(H*0.10), GOLD)
hud_label("GROQ CORE v2.1", W - int(W*0.062), H - int(H*0.10), CYAN, anchor_left=False)

# title
center_text(d, "JARVIS", F_HERO, int(H * 0.70), GOLD, glow=GOLD, glow_rad=14)
center_text(d, "N E U R A L   I N T E R F A C E", F_MED, int(H * 0.77), CYAN, glow=CYAN, glow_rad=6)
center_text(d, "jarvis-ai-3ba39.web.app", F_SM, int(H * 0.85), NEON, glow=NEON, glow_rad=6)
center_text(d, "YOUR INTELLIGENCE. AMPLIFIED.", F_SM, int(H * 0.90), GOLD_DEEP)

img = Image.alpha_composite(img.convert("RGBA"), starfield(img.size, 300, seed=21)).convert("RGB")
img = vignette(img, 0.55)
img = film_grain(img, 14, 0.05)
img.save(f"{OUT}/jarvis_poster_3_hud_neural.png", quality=95)
print(f"  saved poster 3  ({time.time()-t0:.0f}s)", flush=True)

print(f"ALL DONE in {time.time()-t0:.0f}s -> {OUT}", flush=True)