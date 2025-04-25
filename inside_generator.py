
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def render_inside_image(message, output_path="/Users/dmcg/ComfyUI/output/card_inside.png"):
    WIDTH, HEIGHT = 768, 1024
    MARGIN = 60
    FONT_PATH = "/System/Library/Fonts/Supplemental/Georgia.ttf"
    FONT_SIZE = 36

    img = Image.new("RGB", (WIDTH, HEIGHT), color="#fffaf4")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()

    # Wrap the message
    wrapped = textwrap.fill(message, width=40)
    text_size = draw.textbbox((0, 0), wrapped, font=font)
    text_height = text_size[3] - text_size[1]
    y = (HEIGHT - text_height) // 2

    draw.text((MARGIN, y), wrapped, fill="#3e2f2f", font=font)

    img.save(output_path)
    return output_path
