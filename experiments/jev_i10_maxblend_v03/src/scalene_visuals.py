"""Geometry and deliberately plain images for a non-proof Jev Vision benchmark."""
from __future__ import annotations

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

A = (140.0, 440.0)
B = (640.0, 440.0)
SHAPES = {"left": (275.0, 105.0), "right": (505.0, 105.0)}
METHODS = ("angle", "segment", "orthogonal", "decoy_a", "decoy_b")
MODES = ("free", "angle", "segment", "orthogonal")


def length(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def fractions(shape):
    apex = SHAPES[shape]
    la, lb = length(A, apex), length(apex, B)
    result = {
        "angle": la / (la + lb),
        "segment": 0.5,
        "orthogonal": (apex[0] - A[0]) / (B[0] - A[0]),
        "decoy_a": 0.08,
        "decoy_b": 0.94,
    }
    assert len({round(v, 6) for v in result.values()}) == len(result)
    assert all(0.0 < x < 1.0 for x in result.values())
    return result


def label_order(shape, mode):
    options = list(METHODS)
    seed = sum((i + 1) * ord(ch) for i, ch in enumerate(shape + "::" + mode))
    random.Random(seed).shuffle(options)
    return {"K" + str(i + 1): item for i, item in enumerate(options)}, seed


def render(path, shape, method=None):
    apex = SHAPES[shape]
    im = Image.new("RGB", (780, 550), "white")
    d = ImageDraw.Draw(im)
    foreground = "#384047"
    for p, q in ((A, B), (A, apex), (apex, B)):
        d.line([p, q], fill=foreground, width=4)
    coords = {"A": A, "B": B, "C": apex}
    if method:
        t = fractions(shape)[method]
        foot = (A[0] + (B[0] - A[0]) * t, A[1])
        coords["D"] = foot
        d.line([apex, foot], fill=foreground, width=4)
    path.parent.mkdir(parents=True, exist_ok=True)
    font_file = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    font = ImageFont.truetype(str(font_file), 20) if font_file.exists() else ImageFont.load_default()
    offsets = {"A": (-22, 8), "B": (9, 8), "C": (-5, -30), "D": (-5, 11)}
    for name, (x, y) in coords.items():
        d.ellipse((x-4, y-4, x+4, y+4), fill=foreground)
        dx, dy = offsets[name]
        d.text((x+dx, y+dy), name, font=font, fill=foreground)
    im.save(path)
    return path
