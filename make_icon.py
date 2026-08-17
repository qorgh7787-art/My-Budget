import numpy as np
from PIL import Image, ImageDraw

def gradient_bg(size, c1, c2):
    ys, xs = np.mgrid[0:size, 0:size].astype(float)
    t = ((xs + ys) / (2 * (size - 1)))[..., None]
    c1 = np.array(c1, dtype=float)
    c2 = np.array(c2, dtype=float)
    arr = (c1 * (1 - t) + c2 * t).astype(np.uint8)
    return Image.fromarray(arr, mode='RGB')

def rotated_paste(base, layer_size, draw_fn, angle, pivot):
    layer = Image.new('RGBA', layer_size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_fn(d)
    rotated = layer.rotate(-angle, resample=Image.BICUBIC, expand=False, center=pivot)
    base.paste(rotated, (0, 0), rotated)

def make_icon(size):
    scale = size / 512
    bg = gradient_bg(size, (191, 233, 247), (234, 247, 255)).convert('RGBA')

    # note card group, rotated -7 deg around (256,256)*scale
    note_layer_size = (size, size)
    def draw_note(d):
        d.rounded_rectangle(
            [128*scale, 96*scale, 368*scale, 400*scale],
            radius=40*scale, fill=(255, 255, 255, 255),
            outline=(216, 236, 245, 255), width=max(1, int(6*scale)))
        d.rounded_rectangle([168*scale, 168*scale, 328*scale, 195*scale], radius=13.5*scale, fill=(63, 169, 214, 255))
        d.rounded_rectangle([168*scale, 232*scale, 296*scale, 259*scale], radius=13.5*scale, fill=(244, 162, 97, 255))
        d.rounded_rectangle([168*scale, 296*scale, 264*scale, 323*scale], radius=13.5*scale, fill=(155, 140, 242, 255))
    rotated_paste(bg, note_layer_size, draw_note, -7, (256*scale, 256*scale))

    # pen group, rotated 38 deg around (368,352)*scale
    def draw_pen(d):
        d.rounded_rectangle([336*scale, 192*scale, 384*scale, 400*scale], radius=19*scale, fill=(32, 100, 127, 255))
        d.polygon([(336*scale, 192*scale), (384*scale, 192*scale), (360*scale, 136*scale)], fill=(242, 193, 78, 255))
    rotated_paste(bg, note_layer_size, draw_pen, 38, (368*scale, 352*scale))

    return bg.convert('RGB')

for size, name in [(512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')]:
    icon = make_icon(size)
    icon.save(name, 'PNG')
    print('wrote', name)
