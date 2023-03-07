"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

from PIL import Image, ImageDraw

try:
    import inky.auto as auto
except ImportError:
    exit("This script requires the inky module\nInstall with: sudo pip install inky")

import display_format

try:
    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_border(inky_display.WHITE)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


def update(data_dict: dict):
    # print(data_dict)
    if inky_display.resolution not in ((212, 104), (250, 122), (400, 300)):
        raise RuntimeError(f"{inky_display.WIDTH}x{inky_display.HEIGHT} is not a supported resolution")

    # noinspection DuplicatedCode
    def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
        mask_image = Image.new("1", source.size)
        w, h = source.size
        for x in range(w):
            for y in range(h):
                p = source.getpixel((x, y))
                if p in mask:
                    mask_image.putpixel((x, y), 255)
        return mask_image

    formatter = display_format.ZoneFormatter(inky_display.WIDTH, inky_display.HEIGHT,
                                             secondary_zone_on_top=data_dict["second_on_top"])

    # layers = [formatter.zone_main(data_dict["main"]),
    #           formatter.zone_secondary(data_dict["secondary"]),
    #           formatter.zone_datetime(data_dict["datetime"]),
    #           formatter.zone_image(data_dict["image"])]

    def draw_text(context, position, content, color, font):
        context.text(position, content, color, font=font)


    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    draw_text(draw, *formatter.zone_main(data_dict["main"]))
    draw_text(draw, *formatter.zone_secondary(data_dict["secondary"]))
    draw_text(draw, *formatter.zone_datetime(data_dict["datetime"]))
    img.paste(*formatter.zone_image(data_dict["image"]))

    inky_display.h_flip = True
    inky_display.v_flip = True

    inky_display.set_image(img)
    inky_display.show()
