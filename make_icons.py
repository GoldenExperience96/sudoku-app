from PIL import Image, ImageDraw, ImageFont

ACCENT = (51, 84, 158)      # #33549e
ACCENT_DK = (38, 62, 122)   # darker for gradient
WHITE = (255, 255, 255)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Ein paar vorgegebene Zahlen fürs Icon-Motiv (r, c, ziffer)
GIVENS = [(0,1,'5'), (1,2,'3'), (2,0,'8'), (0,2,'1'),
          (1,0,'9'), (2,2,'4'), (1,1,'6'), (2,1,'2'), (0,0,'7')]

def make_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)

    # vertikaler Farbverlauf als Hintergrund
    for y in range(size):
        t = y / size
        r = int(ACCENT[0]*(1-t) + ACCENT_DK[0]*t)
        g = int(ACCENT[1]*(1-t) + ACCENT_DK[1]*t)
        b = int(ACCENT[2]*(1-t) + ACCENT_DK[2]*t)
        d.line([(0,y),(size,y)], fill=(r,g,b,255))

    # Safe-Zone: maskable braucht Rand (Content in inneren ~76%)
    pad = int(size * 0.20) if maskable else int(size * 0.13)
    grid = size - 2*pad
    cell = grid / 3.0

    # Zahlen einzeichnen
    fnt = ImageFont.truetype(FONT, int(cell * 0.62))
    for (rr, cc, ch) in GIVENS:
        cx = pad + cc*cell + cell/2
        cy = pad + rr*cell + cell/2
        bb = d.textbbox((0,0), ch, font=fnt)
        w, h = bb[2]-bb[0], bb[3]-bb[1]
        d.text((cx - w/2 - bb[0], cy - h/2 - bb[1]), ch, font=fnt, fill=WHITE)

    # dünne Gitterlinien (halbtransparentes Weiß)
    lw = max(2, size//160)
    for k in range(4):
        x = pad + k*cell
        d.line([(x,pad),(x,pad+grid)], fill=(255,255,255,110), width=lw)
        d.line([(pad,x),(pad+grid,x)], fill=(255,255,255,110), width=lw)
    # kräftiger Außenrahmen
    d.rectangle([pad,pad,pad+grid,pad+grid], outline=(255,255,255,220), width=lw*2)

    if not maskable:
        # abgerundete Ecken für App-Icon-Optik
        radius = int(size * 0.22)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0,0,size,size], radius=radius, fill=255)
        img.putalpha(mask)
    return img

# Standard (abgerundet) + maskable (voll)
make_icon(192).save("icons/icon-192.png")
make_icon(512).save("icons/icon-512.png")
make_icon(192, maskable=True).save("icons/icon-192-maskable.png")
make_icon(512, maskable=True).save("icons/icon-512-maskable.png")
make_icon(180).save("icons/apple-touch-icon.png")
make_icon(32).save("icons/favicon-32.png")
print("Icons erstellt.")
