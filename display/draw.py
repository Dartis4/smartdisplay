"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

import functools
import time

from PIL import Image, ImageDraw

from display.format import ZoneFormatter

try:
    # noinspection PyUnresolvedReferences
    import inky.auto as auto
except ImportError:
    exit("This script requires the inky module\nInstall with: sudo pip install inky")

try:
    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_border(inky_display.WHITE)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


def update(data_dict: dict):
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

    draw_text_here = functools.partial(draw_text, draw)

    draw_text_here(*formatter.zone_main(data_dict["main"]))
    draw_text_here(*formatter.zone_secondary(data_dict["secondary"]))
    draw_text_here(*formatter.zone_time(data_dict["time"]))
    draw_text_here(*formatter.zone_date(data_dict["date"]))
    img.paste(*formatter.zone_image(data_dict["image"]))

    inky_display.h_flip = True
    inky_display.v_flip = True

    inky_display.set_image(img)
    inky_display.show()
