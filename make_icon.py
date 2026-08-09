import numpy as np
from PIL import Image, ImageDraw

NAVY = (19, 42, 69)
NAVY2 = (14, 32, 54)
WHITE = (255, 255, 255)
MINT = (62, 207, 142)
MINT_DARK = (31, 157, 104)

def gradient_bg(size, c1, c2):
    ys, xs = np.mgrid[0:size, 0:size].astype(float)
    t = ((xs + ys) / (2 * (size - 1)))[..., None]
    c1 = np.array(c1, dtype=float)
    c2 = np.array(c2, dtype=float)
    arr = (c1 * (1 - t) + c2 * t).astype(np.uint8)
    return Image.fromarray(arr, mode='RGB')

def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)

def make_icon(size):
    s = size / 512
    bg = gradient_bg(size, NAVY, NAVY2).convert('RGBA')
    d = ImageDraw.Draw(bg)

    # open book (two pages) - white
    book_top = 190 * s
    spine_x = 256 * s
    page_w = 130 * s
    page_h = 150 * s

    d.polygon([
        (spine_x, book_top),
        (spine_x - page_w, book_top + 20 * s),
        (spine_x - page_w, book_top + page_h + 20 * s),
        (spine_x, book_top + page_h),
    ], fill=WHITE)
    d.polygon([
        (spine_x, book_top),
        (spine_x + page_w, book_top + 20 * s),
        (spine_x + page_w, book_top + page_h + 20 * s),
        (spine_x, book_top + page_h),
    ], fill=(235, 240, 246))

    # page lines (left page)
    for i, ly in enumerate([book_top + 55*s, book_top + 80*s, book_top + 105*s]):
        d.line([(spine_x - page_w + 20*s, ly), (spine_x - 15*s, ly + 6*s)], fill=(180, 195, 210), width=max(1, int(4*s)))
    for i, ly in enumerate([book_top + 55*s, book_top + 80*s, book_top + 105*s]):
        d.line([(spine_x + 15*s, ly + 6*s), (spine_x + page_w - 20*s, ly)], fill=(200, 210, 220), width=max(1, int(4*s)))

    # mint timer/clock circle bottom-right, overlapping the book
    cx, cy, r = 340*s, 350*s, 95*s
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=MINT)
    d.ellipse([cx-r+10*s, cy-r+10*s, cx+r-10*s, cy+r-10*s], outline=WHITE, width=max(2, int(7*s)))
    # clock hands
    d.line([(cx, cy), (cx, cy - r*0.55)], fill=WHITE, width=max(2, int(8*s)))
    d.line([(cx, cy), (cx + r*0.4, cy + r*0.15)], fill=WHITE, width=max(2, int(8*s)))
    d.ellipse([cx-6*s, cy-6*s, cx+6*s, cy+6*s], fill=WHITE)
    # small knob on top of clock
    d.rounded_rectangle([cx-14*s, cy-r-14*s, cx+14*s, cy-r+4*s], radius=6*s, fill=MINT_DARK)

    return bg.convert('RGB')

for size, name in [(512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')]:
    icon = make_icon(size)
    icon.save(name, 'PNG')
    print('wrote', name)
