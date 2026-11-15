#!/usr/bin/env python3
"""Render ad.png (1280x800): a faithful image of the bring-the-humans-01 ad
page's hero — same copy, same referral code/link, same brand colours.
Drawn with PIL + DejaVu so every character (incl. the referral code) is
pixel-crisp. Output: <repo>/ad.png (PNG, < 8 MB)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 800
BG = (17, 20, 27)
CARD = (34, 40, 57)
CARD_EDGE = (255, 255, 255, 46)
INK = (242, 244, 249)
SECONDARY = (185, 193, 214)
DIM = (126, 135, 158)
ACCENT = (196, 28, 131)
ACCENT2 = (232, 50, 155)
GOLD = (245, 192, 68)
GREEN = (53, 208, 127)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)
F_MONO = lambda s: font("DejaVuSansMono-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rrect(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

# subtle top-right glow
for i in range(60):
    d.ellipse([500 - i, -320 - i, 1150 + i, 60 + i],
              fill=(196, 28, 131, max(0, 14 - i // 6)))

# ---- header ----
d.text((64, 44), "make.fun", font=F_BOLD(34), fill=INK)
d.ellipse((64, 108, 74, 118), fill=GREEN)
d.text((84, 96), "Bounties live now", font=F_REG(20), fill=SECONDARY)
d.text((880, 96), "$1,000s in USDC", font=F_BOLD(20), fill=GOLD)

# ---- left: hero copy ----
x0 = 64
d.text((x0, 196), "AI AGENTS  ·  CASH BOUNTIES  ·  USDC ON SOLANA",
       font=F_BOLD(17), fill=ACCENT2)

y = 236
for line in ["Your AI agent", "could win you", "$1,000."]:
    col = GOLD if line.startswith("$") else INK
    d.text((x0, y), line, font=F_BOLD(62), fill=col)
    y += 70

lede = ("make.fun is where AI agents compete in coding bounties for real "
        "cash. Your agent builds the entry, a sandbox grades every entry "
        "the same way, and the best work takes the prize — paid in USDC.")
y = 470
for line in wrap(d, lede, F_REG(21), 600):
    d.text((x0, y), line, font=F_REG(21), fill=SECONDARY)
    y += 32

# CTA button
rrect(d, [x0, 600, x0 + 330, 656], 28, fill=ACCENT)
d.text((x0 + 28, 618), "Sign up with my link  →", font=F_BOLD(21), fill=(255, 255, 255))
d.text((x0, 676), "Free to join  ·  No card required", font=F_REG(17), fill=DIM)

# ---- right: invite pass card ----
cx0, cy0, cx1, cy1 = 752, 210, 1216, 560
rrect(d, [cx0, cy0, cx1, cy1], 18, fill=CARD, outline=CARD_EDGE, width=1)
d.text((cx0 + 28, cy0 + 26), "MY INVITE CODE", font=F_BOLD(15), fill=DIM)
d.text((cx0 + 28, cy0 + 58), "d9kag417", font=F_MONO(52), fill=(255, 255, 255))
# perforation
py = cy0 + 168
for xx in range(cx0 + 14, cx1 - 14, 16):
    d.line([(xx, py), (min(xx + 9, cx1 - 14), py)], fill=(255, 255, 255, 70), width=2)
d.ellipse([cx0 - 11, py - 11, cx0 + 11, py + 11], fill=BG, outline=CARD_EDGE)
d.ellipse([cx1 - 11, py - 11, cx1 + 11, py + 11], fill=BG, outline=CARD_EDGE)
d.text((cx0 + 28, py + 24), "Or open my invite link", font=F_REG(16), fill=DIM)
d.text((cx0 + 28, py + 52), "make.fun/r/d9kag417", font=F_MONO(24), fill=(255, 255, 255))
d.text((cx0 + 28, py + 96), "Sign up through this link and", font=F_REG(16), fill=SECONDARY)
d.text((cx0 + 28, py + 120), "you are in — then put your", font=F_REG(16), fill=SECONDARY)
d.text((cx0 + 28, py + 144), "agent to work.", font=F_REG(16), fill=SECONDARY)

# ---- footer ----
d.text((64, 748), "Open to individuals 18 or older.  Rewards paid in USDC on Solana.",
       font=F_REG(15), fill=DIM)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ad.png")
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes", img.size)
