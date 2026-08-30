#!/usr/bin/env python3
"""
JARVIS AI — Cinematic 8K Poster Generator
Pipeline: DESIGN.md → analysis.md → structured-content.md → prompts/infographic.md → this script
Output: jarvis_poster_HERO.png (3840x2160 4K base, instruction for 8K upscale included)
"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
import math, random, os, time, struct

# ══════════════════════════════════════════════════════════════
# DESIGN SYSTEM TOKENS (from DESIGN.md — single source of truth)
# ══════════════════════════════════════════════════════════════
MIDNIGHT   = (11, 20, 33)     # #0B1421  primary/bg
CHARCOAL   = (26, 29, 36)     # #1A1D24  secondary/surface
SURFACE2   = (22, 27, 38)     # #161B26  elevated
GOLD       = (232, 197, 74)   # #E8C54A  tertiary/accent
GOLD_DEEP  = (212, 175, 55)   # #D4AF37  gold-deep
GOLD_WARM  = (200, 170, 60)   # gold-warm (ring variant)
NEON       = (255, 0, 51)     # #FF0033  neon/alert
CYAN       = (30, 200, 230)   # #1EC8E6  cyan/data
CYAN_DEEP  = (10, 58, 74)     # #0A3A4A  cyan-deep
TEXT       = (234, 246, 248)   # #EAF6F8  primary text
MUTED      = (138, 160, 176)   # #8AA0B0  secondary text

# ══════════════════════════════════════════════════════════════
# OUTPUT PATHS
# ══════════════════════════════════════════════════════════════
OUT = "/data/data/com.termux/files/home/jarvis-reconstruct/posters"
os.makedirs(OUT, exist_ok=True)

# ══════════════════════════════════════════════════════════════
# GENERATION CONFIG
# ══════════════════════════════════════════════════════════════
SCALE = 2  # render at W/SCALE x H/SCALE, final upscaled
RAW_W, RAW_H = 7680, 4320  # 8K target
W, H = RAW_W // SCALE, RAW_H // SCALE  # actual render: 3840x2160

print(f"Render resolution: {W}×{H} (base for {RAW_W}×{RAW_H} 8K upscale)")

# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

F_HERO  = load_font("/system/fonts/DroidSans-Bold.ttf", int(H * 0.092))
F_BIG   = load_font("/system/fonts/DroidSans-Bold.ttf", int(H * 0.051))
F_MED   = load_font("/system/fonts/DroidSans-Bold.ttf", int(H * 0.030))
F_SM    = load_font("/system/fonts/DroidSans.ttf", int(H * 0.022))
F_TINY  = load_font("/system/fonts/DroidSans.ttf", int(H * 0.016))
F_MICRO = load_font("/system/fonts/DroidSans.ttf", int(H * 0.011))

def radial_bg(w, h, c_center, c_edge, power=1.6, steps=80):
    """Upscale-friendly radial gradient via small canvas."""
    sw, sh = max(12, w // 32), max(12, h // 32)
    small = Image.new("RGB", (sw, sh), c_edge)
    sd = ImageDraw.Draw(small)
    cx, cy = sw / 2, sh / 2
    maxd = math.hypot(cx, cy)
    for i in range(steps, 0, -1):
        t = i / steps
        r = maxd * t
        k = t ** power
        col = tuple(int(c_center[j] * (1 - k) + c_edge[j] * k) for j in range(3))
        sd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    return small.resize((w, h), Image.LANCZOS)

def vignette_mask(w, h, strength=0.55, inner=0.35, scale=4):
    """Vignette: transparent center -> opaque edges. Returns L mask."""
    sw, sh = max(8, w // scale), max(8, h // scale)
    mask = Image.new("L", (sw, sh), 0)
    md = ImageDraw.Draw(mask)
    cx, cy = sw / 2, sh / 2
    maxd = math.hypot(cx, cy)
    steps = 80
    for i in range(steps, 0, -1):
        t = i / steps
        r = maxd * t
        # inner radius = no darkening, outer = full
        if t > inner:
            alpha = int(255 * strength * ((t - inner) / (1.0 - inner)) ** 2)
        else:
            alpha = 0
        md.ellipse([cx - r, cy - r, cx + r, cy + r], outline=alpha, width=2)
    return mask.resize((w, h), Image.LANCZOS)

def film_grain(sigma=14):
    """C-level noise, no per-pixel loops."""
    return Image.effect_noise((W, H), sigma)

def draw_text_centered(draw, text, font, cy, color, glow=None, glow_r=0):
    """Draw horizontally centered at vertical cy, with glow."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = cy - (bbox[3] + bbox[1]) // 2
    if glow and glow_r:
        gl = glow if isinstance(glow, tuple) else color
        for o in range(glow_r, 0, -1):
            a = int(100 * (o / glow_r) ** 2)
            for dx, dy in ((o, 0), (-o, 0), (0, o), (0, -o)):
                draw.text((tx + dx, ty + dy), text, font=font, fill=(*gl, a))
    return draw.text((tx, ty), text, font=font, fill=color)

def arc_reactor(draw, cx, cy, R, rings, spokes=16, core_frac=0.11):
    """Arc reactor: rings + spokes + core. Token-exact."""
    for rm, color, width in rings:
        r = int(R * rm)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    for i in range(spokes):
        a = i * 2 * math.pi / spokes - math.pi / 2
        x1 = cx + int(math.cos(a) * R * 0.35)
        y1 = cy + int(math.sin(a) * R * 0.35)
        x2 = cx + int(math.cos(a) * R * 0.95)
        y2 = cy + int(math.sin(a) * R * 0.95)
        draw.line([x1, y1, x2, y2], fill=GOLD, width=2)
    cr = int(R * core_frac)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=GOLD)
    # tiny bright core
    cr2 = int(R * 0.04)
    draw.ellipse([cx - cr2, cy - cr2, cx + cr2, cy + cr2], fill=(255, 250, 220))

def glow_circle(w, h, cx, cy, radius, color, alpha=40, blur=60):
    """Single glow circle on transparent layer."""
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for r in range(radius, 0, -max(1, radius // 40)):
        a = int(alpha * (r / radius) ** 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    return lay.filter(ImageFilter.GaussianBlur(blur))

def hud_bracket(draw, cx, cy, size, color, alpha=220, width=5):
    """L-bracket at viewport corner."""
    # Main L
    draw.line([cx, cy, cx + size, cy], fill=(*color, alpha), width=width)
    draw.line([cx, cy, cx, cy + size], fill=(*color, alpha), width=width)
    # Tips
    draw.line([cx + size, cy, cx + size, cy + int(size * 0.18)],
              fill=(*color, alpha), width=width)
    draw.line([cx, cy + size, cx + int(size * 0.18), cy + size],
              fill=(*color, alpha), width=width)

def coord_label(draw, text, x, y, font, color=CYAN, alpha=140):
    """SEC-XX coordinate label at module boundary."""
    draw.text((x, y), text, font=font, fill=(*color, alpha))

def micro_annotation(draw, text, x, y, font, color=MUTED, alpha=100):
    """Micro-technical annotation."""
    draw.text((x, y), text, font=font, fill=(*color, alpha))

# ══════════════════════════════════════════════════════════════
# RINGS SPEC (from DESIGN.md: 7 concentric, token-exact)
# ══════════════════════════════════════════════════════════════
REACTOR_RINGS = [
    (1.00, GOLD, 5),       # outermost
    (0.86, GOLD_DEEP, 4),
    (0.72, GOLD, 3),
    (0.58, NEON, 2),
    (0.44, CYAN, 2),
    (0.30, GOLD, 2),
    (0.16, NEON, 1),       # innermost ring
]

t0 = time.time()

# ══════════════════════════════════════════════════════════════
# BASE BACKGROUND (Midnight radial → deeper edges)
# ══════════════════════════════════════════════════════════════
print("[1/8] Rendering midnight radial background...")
img = radial_bg(W, H, (20, 34, 52), MIDNIGHT, power=1.3)
img = img.convert("RGBA")

# ══════════════════════════════════════════════════════════════
# REACTOR GLOW LAYERS (center bloom)
# ══════════════════════════════════════════════════════════════
print("[2/8] Rendering reactor glow layers...")
ecx, ecy = W // 2, int(H * 0.42)
R = int(H * 0.21)  # reactor radius
min_dim = min(W, H)

# Layer 1: wide gold bloom
img = Image.alpha_composite(img, glow_circle(W, H, ecx, ecy, int(R * 1.8), GOLD, alpha=22, blur=80))
# Layer 2: medium gold bloom
img = Image.alpha_composite(img, glow_circle(W, H, ecx, ecy, int(R * 1.2), GOLD, alpha=35, blur=50))
# Layer 3: tight core bloom
img = Image.alpha_composite(img, glow_circle(W, H, ecx, ecy, int(R * 0.5), GOLD, alpha=50, blur=30))
# Layer 4: cyan accent (upper-right neural)
img = Image.alpha_composite(img, glow_circle(W, H, int(W * 0.82), int(H * 0.15), int(min_dim * 0.18), CYAN, alpha=28, blur=100))
# Layer 5: neon accent (lower-left alert)
img = Image.alpha_composite(img, glow_circle(W, H, int(W * 0.18), int(H * 0.82), int(min_dim * 0.14), NEON, alpha=22, blur=100))
# Layer 6: secondary cyan (below reactor)
img = Image.alpha_composite(img, glow_circle(W, H, ecx, int(H * 0.72), int(min_dim * 0.10), CYAN, alpha=16, blur=60))

# ══════════════════════════════════════════════════════════════
# NEURAL WEB (SEC-03) — background texture
# ══════════════════════════════════════════════════════════════
print("[3/8] Rendering neural web texture...")
rng = random.Random(42)
nodes = []
for _ in range(90):
    x = rng.randint(int(W * 0.08), int(W * 0.92))
    y = rng.randint(int(H * 0.10), int(H * 0.90))
    # avoid reactor zone
    dist = math.hypot(x - ecx, y - ecy)
    if dist > R * 1.4:
        nodes.append((x, y))

neural = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(neural)
for i, (x1, y1) in enumerate(nodes):
    for j in range(i + 1, len(nodes)):
        x2, y2 = nodes[j]
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < min_dim * 0.10:
            a = int(45 * (1 - dist / (min_dim * 0.10)))
            col = CYAN if (i + j) % 2 else GOLD
            nd.line([x1, y1, x2, y2], fill=(*col, a), width=1)
for i, (x, y) in enumerate(nodes):
    s = 2 if i % 3 else 4
    col = GOLD if i % 2 else CYAN
    nd.ellipse([x - s, y - s, x + s, y + s], fill=(*col, 140))
# scanlines
for y in range(0, H, int(H * 0.0028)):
    a = int(8 + 4 * math.sin(y * 0.003))
    nd.line([(0, y), (W, y)], fill=(*CYAN, a), width=1)
neural = neural.filter(ImageFilter.GaussianBlur(0.8))
img = Image.alpha_composite(img, neural)

# ══════════════════════════════════════════════════════════════
# ARC REACTOR (SEC-01) — hero emblem
# ══════════════════════════════════════════════════════════════
print("[4/8] Rendering arc reactor emblem...")
reactor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(reactor)
arc_reactor(rd, ecx, ecy, R, REACTOR_RINGS, spokes=16, core_frac=0.11)
# Triangular orientation tick
tri_s = int(R * 0.06)
rd.polygon([
    (ecx, ecy - int(R * 1.06) - tri_s),
    (ecx - tri_s, ecy - int(R * 1.06) + tri_s),
    (ecx + tri_s, ecy - int(R * 1.06) + tri_s),
], fill=GOLD)
# Crosshair at core center
ch_size = int(R * 0.02)
ch_len = int(R * 0.05)
rd.line([ecx - ch_len, ecy, ecx + ch_len, ecy], fill=(*GOLD, 160), width=1)
rd.line([ecx, ecy - ch_len, ecx, ecy + ch_len], fill=(*GOLD, 160), width=1)
# micro annotation near reactor
micro_annotation(rd, "CORE 0.11R | PULSE 0.8s", ecx + int(R * 0.35), ecy - int(R * 0.40), F_MICRO, MUTED, 80)
micro_annotation(rd, "16 SPOKES @ 22.5\u00B0", ecx + int(R * 0.35), ecy - int(R * 0.34), F_MICRO, MUTED, 80)
# Ring ratio labels (pop-lab precision)
micro_annotation(rd, "R1.00  R0.86  R0.72  R0.58  R0.44  R0.30  R0.16",
                 ecx - int(R * 1.10), ecy + int(R * 1.15), F_MICRO, CYAN, 70)
img = Image.alpha_composite(img, reactor)

# ══════════════════════════════════════════════════════════════
# HUD FRAME (SEC-02) — corner brackets + labels
# ══════════════════════════════════════════════════════════════
print("[5/8] Rendering HUD corner brackets...")
hud = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hud)
bracket_size = int(min_dim * 0.075)
bracket_margin = int(min_dim * 0.045)
bw = max(2, int(min_dim * 0.0012))

# 4 corners
corners = [
    (bracket_margin, bracket_margin),                         # TL
    (W - bracket_margin, bracket_margin),                     # TR
    (bracket_margin, H - bracket_margin),                     # BL
    (W - bracket_margin, H - bracket_margin),                 # BR
]
for i, (cx, cy) in enumerate(corners):
    direction = 1  # outward from center
    # Determine L direction
    if cx > W // 2:  # right side
        dx = -1
    else:
        dx = 1
    if cy > H // 2:  # bottom
        dy = -1
    else:
        dy = 1
    # L-shape
    hd.line([cx, cy, cx + dx * bracket_size, cy], fill=(*GOLD, 220), width=bw)
    hd.line([cx, cy, cx, cy + dy * bracket_size], fill=(*GOLD, 220), width=bw)
    # Tips (perpendicular bars)
    tip_len = int(bracket_size * 0.18)
    hd.line([cx + dx * bracket_size, cy, cx + dx * bracket_size, cy + dy * tip_len],
            fill=(*GOLD, 180), width=bw)
    hd.line([cx, cy + dy * bracket_size, cx + dx * tip_len, cy + dy * bracket_size],
            fill=(*GOLD, 180), width=bw)
    # Subtle glow around bracket
    hd.ellipse([cx - int(bracket_size * 0.3), cy - int(bracket_size * 0.3),
                cx + int(bracket_size * 0.3), cy + int(bracket_size * 0.3)],
               fill=None, outline=(*GOLD, 20), width=1)

# HUD labels (per structured-content.md)
hud_margin = int(min_dim * 0.055)
label_offset = int(min_dim * 0.018)

# TL: SYS.ARM // ONLINE
hd.text((hud_margin, hud_margin + label_offset), "SYS.ARM // ONLINE", font=F_TINY, fill=(*CYAN, 200))
# TR: NEURAL LINK: ACTIVE
bbox_tr = hd.textbbox((0, 0), "NEURAL LINK: ACTIVE", font=F_TINY)
hd.text((W - hud_margin - (bbox_tr[2] - bbox_tr[0]), hud_margin + label_offset),
        "NEURAL LINK: ACTIVE", font=F_TINY, fill=(*GOLD, 200))
# BL: LAT/LON
hd.text((hud_margin, H - hud_margin - label_offset - int(min_dim * 0.02)),
        "LAT: 17.3850\u00B0N  LON: 78.4867\u00B0E", font=F_TINY, fill=(*CYAN, 180))
# BR: QUOTA
bbox_br = hd.textbbox((0, 0), "QUOTA: 24 / DAY", font=F_TINY)
hd.text((W - hud_margin - (bbox_br[2] - bbox_br[0]), H - hud_margin - label_offset - int(min_dim * 0.02)),
        "QUOTA: 24 / DAY", font=F_TINY, fill=(*NEON, 200))

# SEC-XX coordinate labels (pop-lab precision)
coord_label(hd, "SEC-01", ecx - int(R * 1.2), ecy - int(R * 1.2), F_MICRO, CYAN, 80)
coord_label(hd, "SEC-02", bracket_margin + int(min_dim * 0.005), bracket_margin + int(min_dim * 0.005), F_MICRO, GOLD, 80)
coord_label(hd, "SEC-03", int(W * 0.78), int(H * 0.15), F_MICRO, CYAN, 60)
coord_label(hd, "SEC-04", int(W * 0.92), int(H * 0.92), F_MICRO, MUTED, 50)
coord_label(hd, "SEC-05", int(W * 0.05), int(H * 0.88), F_MICRO, MUTED, 40)
coord_label(hd, "SEC-06", ecx + int(R * 1.15), ecy + int(R * 0.8), F_MICRO, GOLD, 70)
coord_label(hd, "SEC-07", int(W * 0.42), H - int(H * 0.06), F_MICRO, CYAN, 60)

img = Image.alpha_composite(img, hud)

# ══════════════════════════════════════════════════════════════
# TYPOGRAPHY HIERARCHY (SEC-06)
# ══════════════════════════════════════════════════════════════
print("[6/8] Rendering typography hierarchy...")
typo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(typo)

# "JARVIS" — hero, centered at ~55% height (below reactor)
hero_y = int(H * 0.58)
draw_text_centered(td, "JARVIS", F_HERO, hero_y, GOLD, glow=GOLD, glow_r=20)

# "A I   A S S I S T A N T" — muted, below hero
sub_y = int(H * 0.65)
draw_text_centered(td, "A I   A S S I S T A N T", F_MED, sub_y, MUTED, glow=GOLD, glow_r=4)

# "YOUR INTELLIGENCE. AMPLIFIED." — cyan tagline
tag_y = int(H * 0.74)
draw_text_centered(td, "YOUR INTELLIGENCE. AMPLIFIED.", F_SM, tag_y, CYAN, glow=CYAN, glow_r=6)

# "jarvis-ai-3ba39.web.app" — neon URL
url_y = int(H * 0.80)
draw_text_centered(td, "jarvis-ai-3ba39.web.app", F_SM, url_y, NEON, glow=NEON, glow_r=4)

img = Image.alpha_composite(img, typo)

# ══════════════════════════════════════════════════════════════
# DEPLOYMENT BADGES (SEC-07)
# ══════════════════════════════════════════════════════════════
print("[7/8] Rendering deployment badges...")
badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(badge)

pills = [
    ("LIVE \u2022 FIREBASE + CF WORKERS", GOLD),
    ("GROQ \u2022 LLAMA-3.3-70B \u2022 MIXTRAL", CYAN),
    ("AUTH \u2022 24/DAY QUOTA", NEON),
]
pill_font = F_MICRO
pill_h = int(H * 0.014)
pill_spacing = int(W * 0.012)
total_width = 0
pill_widths = []
for text, _ in pills:
    bbox = bd.textbbox((0, 0), text, font=pill_font)
    w = bbox[2] - bbox[0] + int(H * 0.020)
    pill_widths.append(w)
    total_width += w
total_width += pill_spacing * (len(pills) - 1)
start_x = (W - total_width) // 2
pill_y = H - int(H * 0.055)

for i, ((text, color), pw) in enumerate(zip(pills, pill_widths)):
    # Glass pill background
    x0 = start_x
    y0 = pill_y
    x1 = x0 + pw
    y1 = pill_y + pill_h
    # Draw rounded rect pill
    bd.rounded_rectangle([x0, y0, x1, y1], radius=int(pill_h * 0.3),
                         fill=(*SURFACE2, 160), outline=(*GOLD, 40), width=1)
    # Pill text
    t_bbox = bd.textbbox((0, 0), text, font=pill_font)
    t_w = t_bbox[2] - t_bbox[0]
    t_h = t_bbox[3] - t_bbox[1]
    bd.text((x0 + (pw - t_w) // 2, y0 + (pill_h - t_h) // 2), text,
            font=pill_font, fill=(*color, 200))
    # Dot indicator
    dot_r = int(pill_h * 0.15)
    bd.ellipse([x0 + int(H * 0.008), y0 + (pill_h - dot_r) // 2,
                x0 + int(H * 0.008) + dot_r * 2, y0 + (pill_h - dot_r) // 2 + dot_r * 2],
               fill=(*color, 220))
    start_x += pw + pill_spacing

img = Image.alpha_composite(img, badge)

# ══════════════════════════════════════════════════════════════
# POST-PROCESS: Vignette + Film Texture (SEC-04 + SEC-05)
# ══════════════════════════════════════════════════════════════
print("[8/8] Applying vignette + film texture...")

# Vignette: SEC-04 — elliptical radial gradient 35% clear → 92% midnight
vig = vignette_mask(W, H, strength=0.60, inner=0.35, scale=3)
dark = Image.new("RGB", (W, H), (4, 4, 6))
img_rgb = img.convert("RGB")
img_rgb = Image.composite(dark, img_rgb, vig)
img = img_rgb.convert("RGBA")

# Film grain: SEC-05 — σ=12, blend 4% multiply
grain = film_grain(sigma=12).convert("RGB")
# Normalize grain to center at 128
from PIL import ImageOps
grain_norm = ImageOps.autocontrast(grain)
grain_blend = Image.blend(img_rgb, ImageChops.multiply(img_rgb, grain_norm.convert("RGBA").convert("RGB")), 0.04)

# Final convert
img_final = grain_blend

# ══════════════════════════════════════════════════════════════
# SAVE (4K base + metadata)
# ══════════════════════════════════════════════════════════════
hero_path = f"{OUT}/jarvis_poster_HERO.png"
img_final.save(hero_path, quality=100)
file_size = os.path.getsize(hero_path)
elapsed = time.time() - t0

print(f"\n{'='*60}")
print(f"  JARVIS AI POSTER — GENERATION COMPLETE")
print(f"{'='*60}")
print(f"  Output:       {hero_path}")
print(f"  Resolution:   {W}×{H} (4K base)")
print(f"  File size:    {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
print(f"  Time:         {elapsed:.1f}s")
print(f"{'='*60}")
print(f"\n  Pipeline artifacts:")
print(f"    DESIGN.md              — design system tokens")
print(f"    analysis.md            — infographic analysis")
print(f"    structured-content.md  — 7-module structured content")
print(f"    prompts/infographic.md — assembled generation prompt")
print(f"    jarvis_poster_HERO.png — final output")
print(f"\n  To upscale to 8K (7680×4320):")
print(f"    ffmpeg -i hero.png -vf scale=7680:4320 -lanczos jarvis_poster_8K.png")
print(f"\n  Slop self-audit: run claude-design Step 7 after visual inspection")
