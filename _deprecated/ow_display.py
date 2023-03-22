#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto

from display import data

# Get the current path
PATH = os.path.dirname(__file__)
FONT_FACE = "Verdana.ttf"

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


def generate_font(font_face, size):
    return ImageFont.truetype(os.path.join(PATH, "../res", "fonts", font_face), size)


def get_offset(source):
    w, h = source.size
    return w // 2, h // 2


def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)
    return mask_image


def main():
    # Check for display compatibility
    if inky_display.resolution not in ((212, 104), (250, 122), (400, 300)):
        w, h = inky_display.resolution
        raise RuntimeError(f"{inky_display.WIDTH}x{inky_display.HEIGHT} is not a supported resolution")

    # Initialize weather info to placeholder values
    temperature = 0
    description = "Unknown"
    location = "Nowhere"
    icon = None

    # Load the fonts
    font18 = generate_font(FONT_FACE, 18)
    font50 = generate_font(FONT_FACE, 50)

    # Frame the display
    inky_display.set_border(inky_display.WHITE)

    # Create a new canvas to draw on
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    # Load the data from file
    weather = data.load_weather()

    if weather:
        temperature = weather["temperature"]
        description = weather["description"]
        location = weather["location"]
        icon = weather["icon"]
    else:
        print("Warning: no weather information found!")

    now = time.strftime("%I:%M%p")
    date = time.strftime("%A, %m/%d")

    # Draw the current weather icon over the backdrop
    if icon is not None:
        fpath = os.path.join(PATH, "../res/ow-resources", "{icon}@2x.png".format(icon=icon))
        ico = Image.open(fpath)
        x, y = get_offset(ico)
        img.paste(ico, (197 - x, 56 - y), create_mask(ico))
    else:
        draw.text((185, 25), "?", inky_display.BLACK, font=font50)

    draw.text((10, 3), "{}".format(location), inky_display.BLACK, font=font18)

    draw.text((10, 19), u"{}°".format(temperature), inky_display.BLACK, font=font50)

    draw.text((10, 77), now, inky_display.BLACK, font=font18)

    draw.text((10, 100), date, inky_display.BLACK, font=font18)

    # conditions = textwrap.wrap(f'{description}', width=9, subsequent_indent="  ")
    # for i in range(len(conditions)):
    #     draw.text((152, 63 + (19 * i)), conditions[i], inky_display.BLACK, font=font18)

    # Flip the image around
    inky_display.h_flip = True
    inky_display.v_flip = True

    # Display the weather data on Inky pHAT
    inky_display.set_image(img)
    inky_display.show()


if __name__ == '__main__':
    main()
