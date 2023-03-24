import os

from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto

PATH = os.path.dirname(__file__)
FONT_FACE = "Verdana.ttf"

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


def generate_font(font_face, size):
    return ImageFont.truetype(os.path.join(PATH, font_face), size)


def main():
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    font = generate_font(FONT_FACE, 40)

    message = "Welcome!"
    w, h = font.getsize(message)
    x = (inky_display.WIDTH / 2) - (w / 2)
    y = (inky_display.HEIGHT / 2) - (h / 2)

    draw.text((x, y), message, inky_display.BLACK, font)

    # Flip the image around
    inky_display.h_flip = True
    inky_display.v_flip = True

    inky_display.set_image(img)
    inky_display.show()


if __name__ == '__main__':
    main()
