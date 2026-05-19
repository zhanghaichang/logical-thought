from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630

img = Image.new("RGB", (W, H), "#0a1628")
draw = ImageDraw.Draw(img)

# --- deep indigo palette ---
BG       = "#0a1628"
GOLD     = "#d4a843"
DEEP_GOLD= "#b8912a"
CYAN     = "#4fc3f7"
PALE_CYAN= "#81d4fa"
WHITE    = "#f0f4f8"
DIM_BLUE = "#1a3a5c"

# helper: draw a filled circle
def circle(draw, cx, cy, r, fill):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)

# helper: draw line with width
def thick_line(draw, xy, width, fill):
    draw.line(xy, fill=fill, width=width)

# ---- background texture: concentric very subtle rings ----
for i in range(6):
    r = 180 + i * 80
    circle(draw, W//2, H//2 - 20, r, None)
    draw.ellipse([W//2-r, H//2-20-r, W//2+r, H//2-20+r],
                 outline="#1a3a5c", width=1)

# ---- central hypothesis diagram ----
CX, CY = W//2, H//2 - 20

# branching paths: from center hypothesis outward to 6 nodes
paths = []
for k in range(6):
    angle = math.radians(60 * k - 90)
    ex = CX + int(210 * math.cos(angle))
    ey = CY + int(210 * math.sin(angle))
    paths.append((ex, ey))
    # draw path line
    thick_line(draw, [(CX, CY), (ex, ey)], 2, "#2a5a8c")

# small nodes along paths
for k, (ex, ey) in enumerate(paths):
    angle = math.radians(60 * k - 90)
    for t in [0.4, 0.7]:
        nx = CX + int(t * (ex - CX))
        ny = CY + int(t * (ey - CY))
        circle(draw, nx, ny, 3, "#1a4a7a")

# 6 outer nodes
for ex, ey in paths:
    circle(draw, ex, ey, 8, CYAN)

# outer ring of question marks — rendered as small circles + implied "?"
question_positions = []
for k in range(12):
    angle = math.radians(30 * k - 90)
    qx = CX + int(310 * math.cos(angle))
    qy = CY + int(310 * math.sin(angle))
    question_positions.append((qx, qy))
    circle(draw, qx, qy, 5, "#1a4a7a")

# gold question mark glyphs (drawn with arcs + line)
def draw_qmark(draw, cx, cy, size, fill):
    s = size
    # hook top arc
    draw.arc([cx-s, cy-s, cx+s, cy+s], start=200, end=300, fill=fill, width=3)
    # vertical stem
    draw.line([(cx, cy-int(s*0.3)), (cx, cy+int(s*0.7))], fill=fill, width=3)
    # dot below
    draw.ellipse([cx-2, cy+int(s*0.85), cx+2, cy+int(s*0.85)+4], fill=fill)

for qx, qy in question_positions:
    draw_qmark(draw, qx, qy, 9, PALE_CYAN)

# ---- center: hypothesis glow sphere ----
for r in range(38, 18, -4):
    alpha_val = int(255 * (1 - r/38) * 0.3)
    circle(draw, CX, CY, r, f"#{alpha_val:02x}{'d4a843'[:6]}")

circle(draw, CX, CY, 22, GOLD)
circle(draw, CX, CY, 12, "#f0d080")

# ---- radiating light rays from center ----
for k in range(12):
    angle = math.radians(30 * k)
    x1 = CX + int(30 * math.cos(angle))
    y1 = CY + int(30 * math.sin(angle))
    x2 = CX + int(80 * math.cos(angle))
    y2 = CY + int(80 * math.sin(angle))
    draw.line([(x1, y1), (x2, y2)], fill="#b8912a", width=2)

# ---- top right: logical branching icon ----
BX, BY = 900, 110
# fork from a root node upward
thick_line(draw, [(BX, BY+60), (BX, BY+30)], 2, CYAN)
thick_line(draw, [(BX, BY+30), (BX-35, BY)], 2, CYAN)
thick_line(draw, [(BX, BY+30), (BX+35, BY)], 2, CYAN)
for (lx, ly) in [(BX, BY+60), (BX, BY+30), (BX-35, BY), (BX+35, BY)]:
    circle(draw, lx, ly, 5, CYAN)
circle(draw, BX, BY+60, 6, CYAN)

# ---- bottom left: puzzle piece outline ----
PX, PY = 150, 480
pr = 40
# simple puzzle piece shape (square with tabs)
ps = 6
draw.rectangle([PX-pr, PY-pr, PX+pr, PY+pr], outline=GOLD, width=2)
draw.arc([PX-pr-ps, PY-pr-ps, PX-pr+ps*2, PY-pr+ps*2],
         start=180, end=270, fill=GOLD, width=2)
draw.arc([PX+pr-ps*2, PY-pr-ps, PX+pr+ps, PY-pr+ps*2],
         start=270, end=360, fill=GOLD, width=2)
draw.arc([PX-pr-ps, PY+pr-ps*2, PX-pr+ps*2, PY+pr+ps],
         start=90, end=180, fill=GOLD, width=2)
draw.arc([PX+pr-ps*2, PY+pr-ps*2, PX+pr+ps, PY+pr+ps],
         start=0, end=90, fill=GOLD, width=2)
# fill with very dim gold
tmp = Image.new("RGBA", (W, H), (0,0,0,0))
td = ImageDraw.Draw(tmp)
td.rectangle([PX-pr, PY-pr, PX+pr, PY+pr], fill=(212,168,67,30))
img.paste(tmp, (0,0), tmp)

# ---- decorative grid dots (top left quadrant) ----
for gx in range(40, 280, 22):
    for gy in range(40, 200, 22):
        circle(draw, gx, gy, 1, "#1a3a5c")

# ---- chapter number: "01" large and faint background ----
large_font_path = None
try:
    lf = ImageFont.truetype("C:/Windows/Fonts/Georgia.ttf", 200)
except:
    lf = ImageFont.load_default()

# draw huge "01" as watermark
tmp2 = Image.new("RGBA", (W, H), (0,0,0,0))
td2 = ImageDraw.Draw(tmp2)
td2.text((60, 180), "01", font=lf, fill=(26, 74, 122, 60))
img.paste(tmp2, (0,0), tmp2)

# ---- typography ----
try:
    title_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 72)
    subtitle_font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 28)
    label_font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 18)
    chn_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 36)
except:
    title_font = ImageFont.load_default()
    subtitle_font = label_font = chn_font = title_font

# Chinese title
title_text = "假设法"
draw.text((W//2 - 130, H - 120), title_text, font=title_font, fill=GOLD)

# English subtitle
sub_text = "Assumption Method"
draw.text((W//2 - 105, H - 55), sub_text, font=subtitle_font, fill=PALE_CYAN)

# Chapter label top-left
draw.text((40, 28), "CHAPTER 01", font=label_font, fill=CYAN)

# Thin decorative line under title
draw.line([(W//2 - 220, H - 130), (W//2 + 220, H - 130)], fill=GOLD, width=1)

# bottom-right small label
draw.text((W - 200, H - 40), "逻辑思维训练500题", font=label_font, fill="#4a6a8a")

img.save("D:/github/logical-thought/chapter1-cover.png")
print("Saved: chapter1-cover.png")