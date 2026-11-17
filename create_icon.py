import math

from pathlib import Path
from PIL import Image, ImageDraw


assets = Path(__file__).resolve().parent / "assets"

assets.mkdir(exist_ok=True)

size = 1024

image = Image.new(
    "RGBA",
    (size, size),
    (0, 0, 0, 0)
)

draw = ImageDraw.Draw(image)

draw.rounded_rectangle(
    (32, 32, 992, 992),
    radius=220,
    fill="#102331",
    outline="#456D8E",
    width=12
)

cx = size / 2
cy = size / 2


def rotate_point(x, y, angle):

    angle = math.radians(angle)

    return (
        cx + x * math.cos(angle) - y * math.sin(angle),
        cy + x * math.sin(angle) + y * math.cos(angle)
    )


def draw_line(start, end, angle):

    p1 = rotate_point(*start, angle)
    p2 = rotate_point(*end, angle)

    draw.line(
        [p1, p2],
        fill="#B9E3FF",
        width=38
    )

    for x, y in (p1, p2):

        draw.ellipse(
            (x - 19, y - 19, x + 19, y + 19),
            fill="#B9E3FF"
        )


for angle in range(0, 360, 60):

    draw_line((0, 0), (0, -350), angle)

    draw_line((0, -220), (-100, -305), angle)

    draw_line((0, -220), (100, -305), angle)

    draw_line((0, -120), (-75, -180), angle)

    draw_line((0, -120), (75, -180), angle)


draw.ellipse(
    (cx - 24, cy - 24, cx + 24, cy + 24),
    fill="white"
)

image = image.resize(
    (256, 256),
    Image.Resampling.LANCZOS
)

image.save(assets / "icon.png")

image.save(
    assets / "icon.ico",
    format="ICO",
    sizes=[
        (16, 16),
        (24, 24),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256)
    ]
)

print("Иконата е създадена успешно!")