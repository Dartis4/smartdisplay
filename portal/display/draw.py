"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

# import inky.auto as auto
from inky.mock import InkyMockWHAT
from PIL import Image, ImageDraw

from .format import ZoneFormatter

# inky_display = auto(ask_user=True, verbose=True)
inky_display = InkyMockWHAT("black")
inky_display.set_border(inky_display.WHITE)


def update(data_dict: dict):
    print()
    # print(data_dict)
    if inky_display.resolution not in ((212, 104), (250, 122), (400, 300)):
        raise RuntimeError(f"{inky_display.WIDTH}x{inky_display.HEIGHT} is not a supported resolution")

    formatter = ZoneFormatter(inky_display.WIDTH, inky_display.HEIGHT,
                              main_zone_on_top=data_dict["main_on_top"])

    def draw_text(context, position, content, color, font):
        if color == 'red':
            inky_color = inky_display.RED
        elif color == 'yellow':
            inky_color = inky_display.YELLOW
        elif color == 'white':
            inky_color = inky_display.WHITE
        else:
            inky_color = inky_display.BLACK
        context.text(position, content, inky_color, font=font)

    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    def conv_color(color):
        if color == 'red':
            return inky_display.RED
        elif color == 'yellow':
            return inky_display.YELLOW
        elif color == 'white':
            return inky_display.WHITE
        else:
            return inky_display.BLACK

    zones = formatter.zones(data_dict)
    [draw.text(pos, cont, conv_color(color), font=font) for pos, cont, color, font in zones["text"]]
    img.paste(*zones["image"])

    inky_display.h_flip = True
    inky_display.v_flip = True

    inky_display.set_image(img)
    inky_display.show()


def main():
    pass


if __name__ == '__main__':
    main()
