#!/usr/bin/env python3
"""Prepara imagens para a montagem de resultado de campo.

Uso:
  prepare_assets.py crop   ENTRADA SAIDA X0 Y0 X1 Y1     recorta uma região (pixels)
  prepare_assets.py logo   ENTRADA SAIDA [escala=4]       logo -> branco, fundo transparente, ampliado
  prepare_assets.py cutout-preto  ENTRADA SAIDA [limiar=16]   remove fundo preto de embalagem
  prepare_assets.py cutout-branco ENTRADA SAIDA [tol=12]      remove fundo branco ligado às bordas
Requer: pip install pillow numpy
"""
import sys
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter


def crop(src, out, x0, y0, x1, y1):
    Image.open(src).convert("RGB").crop((int(x0), int(y0), int(x1), int(y1))).save(out, quality=94)


def logo(src, out, k=4, gain=1.8):
    im = Image.open(src).convert("RGBA")
    rgb = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im).convert("RGB")
    # recorta a margem branca
    diff = ImageChops.difference(rgb, Image.new("RGB", im.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 25 else 0)
    rgb = rgb.crop(diff.getbbox())
    # alfa = "quanto não é branco"; amplia 4x e afia a borda (smoothstep)
    a = np.clip((255 - np.array(rgb).min(axis=2).astype(float)) / 255 * gain, 0, 1)
    A = Image.fromarray((a * 255).astype("uint8")).resize((rgb.width * int(k), rgb.height * int(k)), Image.LANCZOS)
    a = np.array(A).astype(float) / 255
    t = np.clip((a - 0.25) / 0.5, 0, 1)
    a = t * t * (3 - 2 * t)
    out_arr = np.zeros(a.shape + (4,), "uint8")
    out_arr[..., :3] = 255
    out_arr[..., 3] = (a * 255).astype("uint8")
    Image.fromarray(out_arr).save(out)


def _save_cut(img, mask, out, size=700):
    m = Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
    im = img.convert("RGBA")
    im.putalpha(m)
    im.thumbnail((size, size))
    im.save(out)


def cutout_preto(src, out, lim=16):
    img = Image.open(src).convert("RGB")
    _save_cut(img, np.array(img).max(axis=2) >= int(lim), out)


def cutout_branco(src, out, tol=12):
    img = Image.open(src).convert("RGB")
    mk = img.copy()
    for p in [(0, 0), (img.width - 1, 0), (0, img.height - 1), (img.width - 1, img.height - 1)]:
        ImageDraw.floodfill(mk, p, (255, 0, 255), thresh=int(tol))
    bg = (np.array(mk) == [255, 0, 255]).all(axis=2)
    _save_cut(img, ~bg, out)


if __name__ == "__main__":
    cmd, *a = sys.argv[1:] or ["-h"]
    {"crop": crop, "logo": logo, "cutout-preto": cutout_preto, "cutout-branco": cutout_branco}.get(cmd, lambda *_: print(__doc__))(*a)
