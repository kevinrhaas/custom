#!/usr/bin/env python3
"""Create lightweight isometric PNG previews without external CAD software."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from generate_models import Mesh, bishop, cross, king, knight, normalize, pawn, queen, rook, sub


ROOT = Path(__file__).resolve().parent
PREVIEW = ROOT / "preview"
PREVIEW.mkdir(exist_ok=True)
SCALE = 4


def font(size: int, bold: bool = False, scaled: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        "/System/Library/Fonts/Supplemental/Futura.ttc",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for path in names:
        try:
            return ImageFont.truetype(path, size=size * (SCALE if scaled else 1), index=1 if bold else 0)
        except OSError:
            pass
    return ImageFont.load_default()


def projected(v: tuple[float, float, float], yaw: float = -58.0) -> tuple[float, float, float]:
    """Orthographic three-quarter view, looking toward the alligator's face (-Y)."""
    x, y, z = v
    a = math.radians(yaw)
    x1 = math.cos(a) * x - math.sin(a) * y
    y1 = math.sin(a) * x + math.cos(a) * y
    return x1, z + 0.28 * y1, y1


def render_piece(model: Mesh, width: int, height: int, title: str, subtitle: str,
                 background: tuple[int, int, int] = (232, 230, 225)) -> Image.Image:
    canvas = Image.new("RGB", (width * SCALE, height * SCALE), background)
    draw = ImageDraw.Draw(canvas)
    pverts = [projected(v) for v in model.vertices]
    min_x, max_x = min(v[0] for v in pverts), max(v[0] for v in pverts)
    min_z, max_z = min(v[1] for v in pverts), max(v[1] for v in pverts)
    usable_w = width - 44
    usable_h = height - 78
    factor = min(usable_w / (max_x - min_x), usable_h / (max_z - min_z)) * SCALE
    cx = width * SCALE / 2
    floor_y = (height - 43) * SCALE

    def xy(v: tuple[float, float, float]) -> tuple[float, float]:
        return (cx + (v[0] - (min_x + max_x) / 2) * factor,
                floor_y - (v[1] - min_z) * factor)

    footprint = (max_x - min_x) * factor
    draw.ellipse((cx - footprint * 0.53, floor_y - 4 * SCALE,
                  cx + footprint * 0.53, floor_y + 5 * SCALE), fill=(198, 197, 190))
    light = normalize((-0.8, -1.0, 1.5))
    faces: list[tuple[float, tuple[tuple[float, float], ...], tuple[int, int, int]]] = []
    base = (111, 122, 101)
    for ia, ib, ic in model.faces:
        a, b, c = model.vertices[ia], model.vertices[ib], model.vertices[ic]
        n = normalize(cross(sub(b, a), sub(c, a)))
        # Two-sided lighting is intentional because disconnected solids can reveal internal ordering.
        diffuse = max(0.0, n[0] * light[0] + n[1] * light[1] + n[2] * light[2])
        shade = 0.62 + 0.38 * diffuse
        color = tuple(max(0, min(255, round(ch * shade))) for ch in base)
        pa, pb, pc = pverts[ia], pverts[ib], pverts[ic]
        depth = (pa[2] + pb[2] + pc[2]) / 3
        faces.append((depth, (xy(pa), xy(pb), xy(pc)), color))
    # Positive rotated Y is farther from the camera; draw it first.
    for _, polygon, color in sorted(faces, reverse=True):
        draw.polygon(polygon, fill=color)

    draw.text((width * SCALE / 2, 10 * SCALE), title.upper(), font=font(15, True),
              fill=(54, 62, 52), anchor="ma")
    draw.text((width * SCALE / 2, (height - 27) * SCALE), subtitle, font=font(8),
              fill=(88, 86, 79), anchor="ma")
    return canvas.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    models = [
        (pawn(), "Pawn", "Compact hatchling bust"),
        (rook(), "Rook", "Cranial battlements"),
        (knight(), "Knight", "Core alligator form"),
        (bishop(), "Bishop", "Split mitre planes"),
        (queen(), "Queen", "Five-plate crown"),
        (king(), "King", "Diamond cross crest"),
    ]
    cards: list[Image.Image] = []
    for model, name, subtitle in models:
        card = render_piece(model, 300, 390, name, subtitle)
        cards.append(card)
        card.save(PREVIEW / f"{model.name}.png", optimize=True)

    sheet = Image.new("RGB", (900, 860), (221, 220, 215))
    for i, card in enumerate(cards):
        x = (i % 3) * 300
        y = (i // 3) * 390 + 58
        sheet.paste(card, (x, y))
    d = ImageDraw.Draw(sheet)
    d.text((450, 18), "TOMORROWLAND ALLIGATORS", font=font(20, True, scaled=False),
           fill=(54, 62, 52), anchor="ma")
    d.text((450, 825), "Six support-free, reference-driven low-poly alligator busts · dimensions in millimetres",
           font=font(9, scaled=False), fill=(88, 86, 79), anchor="ma")
    sheet.save(PREVIEW / "alligator_chess_family.png", optimize=True)
    print(PREVIEW / "alligator_chess_family.png")


if __name__ == "__main__":
    main()
