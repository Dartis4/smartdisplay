#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import time
from sys import exit
import json

from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont


# Get the current path
PATH = os.path.dirname(__file__)

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


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
    if inky_display.resolution not in ((212, 104), (250, 122)):
        w, h = inky_display.resolution
        raise RuntimeError("{}x{} is not a supported resolution".format(w, h))

    inky_display.set_border(inky_display.WHITE)

    # Create a new canvas to draw on
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    # Load the FredokaOne font
    font50 = ImageFont.truetype(os.path.join(PATH, "Verdana.ttf"), 50)
    font18 = ImageFont.truetype(os.path.join(PATH, "Verdana.ttf"), 18)

    with open('ow.json', 'r') as f:
        weather = json.loads(f.readline())

    temperature = 0
    description = "Unknown"
    icon = None

    if weather:
        temperature = weather["temperature"]
        description = weather["description"]
        icon = weather["icon"]
    else:
        print("Warning: no weather information found!")

    now = time.strftime("%I:%M%p")
    date = time.strftime("%A, %m/%d")

    # Draw the current weather icon over the backdrop
    if weather["icon"] is not None:
        fpath = os.path.join(PATH, "ow-resources/{icon}@2x.png".format(icon=weather["icon"]))
        ico = Image.open(fpath)
        img.paste(ico, (140, -10), create_mask(ico))
    else:
        draw.text((185, 25), "?", inky_display.BLACK, font=font50)

    draw.text((10, 3), "{}".format(weather["location"]), inky_display.BLACK, font=font18)

    draw.text((10, 19), u"{}°".format(temperature), inky_display.BLACK, font=font50)

    draw.text((10, 77), now, inky_display.BLACK, font=font18)

    draw.text((10, 100), date, inky_display.BLACK, font=font18)

    draw.text((152, 68), "{}".format(description), inky_display.BLACK, font=font18)

    # Flip the image around
    inky_display.h_flip = True
    inky_display.v_flip = True

    # Display the weather data on Inky pHAT
    inky_display.set_image(img)
    inky_display.show()


if __name__ == '__main__':
    main()