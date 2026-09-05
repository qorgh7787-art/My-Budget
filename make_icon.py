from PIL import Image, ImageDraw

SIZE = 1024
TOP = (63, 169, 224)      # --accent
BOTTOM = (31, 127, 179)   # --accent-deep
BOOK_BG = (255, 255, 255)
LINE_COLOR = (214, 232, 244)
COIN_FILL = (36, 180, 126)     # --income green
COIN_RIM = (20, 140, 96)


def make_base():
    img = Image.new("RGB", (SIZE, SIZE), TOP)
    px = img.load()
    for y in range(SIZE):
        t = y / (SIZE - 1)
        r = int(TOP[0] + (BOTTOM[0] - TOP[0]) * t)
        g = int(TOP[1] + (BOTTOM[1] - TOP[1]) * t)
        b = int(TOP[2] + (BOTTOM[2] - TOP[2]) * t)
        for x in range(SIZE):
            px[x, y] = (r, g, b)
    return img


def draw_passbook(img, scale=1.0):
    """scale < 1 shrinks the whole motif toward the center — used for the maskable
    variant so nothing important sits in the zone OS masks can crop away."""
    d = ImageDraw.Draw(img)
    cx, cy = SIZE / 2, SIZE / 2

    def s(x, y):
        return (cx + (x - cx) * scale, cy + (y - cy) * scale)

    margin_x = SIZE * 0.20
    top_y = SIZE * 0.28
    bottom_y = SIZE * 0.84
    bx0, by0 = s(margin_x, top_y)
    bx1, by1 = s(SIZE - margin_x, bottom_y)
    bw = bx1 - bx0
    bh = by1 - by0
    radius = bw * 0.09

    d.rounded_rectangle([bx0, by0, bx1, by1], radius=radius, fill=BOOK_BG)

    spine_w = bw * 0.16
    d.rounded_rectangle([bx0, by0, bx0 + spine_w, by1], radius=radius, fill=BOTTOM)
    # square off the spine's right edge so it reads as a straight binding, not a pill
    d.rectangle([bx0 + spine_w * 0.5, by0, bx0 + spine_w, by1], fill=BOTTOM)

    line_x0 = bx0 + spine_w + bw * 0.13
    line_x1 = bx1 - bw * 0.12
    for t in (0.30, 0.44, 0.58):
        ly = by0 + bh * t
        lh = bh * 0.045
        d.rounded_rectangle([line_x0, ly, line_x1, ly + lh], radius=lh / 2, fill=LINE_COLOR)

    # coin stack, overlapping the top-right corner of the passbook like savings tucked in
    coin_r = bw * 0.30
    coin_cx = bx1 - bw * 0.16
    coin_cy = by0 + bh * 0.02
    for dy in (coin_r * 0.55, 0):
        ccy = coin_cy + dy
        d.ellipse([coin_cx - coin_r, ccy - coin_r, coin_cx + coin_r, ccy + coin_r],
                  fill=COIN_FILL, outline=COIN_RIM, width=int(SIZE * 0.008))
    # embossed inner ring on the top coin (reads as a coin, not a symbol)
    inner_r = coin_r * 0.55
    d.ellipse([coin_cx - inner_r, coin_cy - inner_r, coin_cx + inner_r, coin_cy + inner_r],
              outline=COIN_RIM, width=int(SIZE * 0.008))


def rounded_mask(size, radius):
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return mask


def build_rounded(path, size):
    base = make_base()
    draw_passbook(base, scale=1.0)
    mask = rounded_mask(SIZE, int(SIZE * 0.22))
    rounded = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    rounded.paste(base, (0, 0), mask)
    rounded = rounded.resize((size, size), Image.LANCZOS)
    rounded.save(path)


def build_maskable(path, size):
    # full-bleed square, motif shrunk toward the center so an OS circle/squircle
    # mask never clips the passbook or coins
    base = make_base()
    draw_passbook(base, scale=0.72)
    base = base.resize((size, size), Image.LANCZOS)
    base.save(path)


if __name__ == "__main__":
    out = "C:/Users/dudtjs/Desktop/나만의 가계부"
    build_rounded(f"{out}/icon-192.png", 192)
    build_rounded(f"{out}/icon-512.png", 512)
    build_maskable(f"{out}/icon-maskable-192.png", 192)
    build_maskable(f"{out}/maskable-512.png", 512)
    print("done")
