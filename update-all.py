#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import time
from sys import exit
import json

from font_fredoka_one import FredokaOne
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

"""
To run this example on Python 2.x you should:
    sudo apt install python-lxml
    sudo pip install geocoder requests font-fredoka-one beautifulsoup4=4.6.3

On Python 3.x:
    sudo apt install python3-lxml
    sudo pip3 install geocoder requests font-fredoka-one beautifulsoup4
"""

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
    import geocoder
except ImportError:
    exit("This script requires the geocoder module\nInstall with: sudo pip install geocoder")

try:
    from bs4 import BeautifulSoup
except ImportError:
    exit("This script requires the bs4 module\nInstall with: sudo pip install beautifulsoup4==4.6.3")


print("""Inky pHAT: Weather

Displays weather information for a given location.

""")

# Get the current path
PATH = os.path.dirname(__file__)

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

if inky_display.resolution not in ((212, 104), (250, 122)):
    w, h = inky_display.resolution
    raise RuntimeError("This example does not support {}x{}".format(w, h))

inky_display.set_border(inky_display.WHITE)

# Details to customise your weather display

CITY = "Rexburg"
COUNTRYCODE = "US"

APIkey = "c6523aa9c6438436cbb0ff25d3518190"


def get_weather(address):
    # coords = get_coords(address)
    weather = {}
    url = "https://api.openweathermap.org/data/2.5/weather?q={cityname}&units=imperial&appid={APIkey}".format(cityname=CITY,APIkey=APIkey)
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "html.parser")
        res = (json.loads(str(soup)))
        weather["location"] = res["name"]
        weather["description"] = res["weather"][0]["description"]
        weather["icon"] = res["weather"][0]["icon"]
        weather["temperature"] = int(res["main"]["temp"])
        weather["feels"] = int(res["main"]["feels_like"])
        return weather
    else:
        return weather


def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image


# Get the weather data for the given location
location_string = "{city}, {countrycode}".format(city=CITY, countrycode=COUNTRYCODE)
# print(location_string)
weather = get_weather(location_string)

# Placeholder variables
description = "Unknown"
temperature = 0
weather_icon = None

if weather:
    temperature = weather["temperature"]
    description = weather["description"]
    icon = weather["icon"]

else:
    print("Warning, no weather information found!")

for a in weather:
    print(weather[a])

# Create a new canvas to draw on
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# Load the FredokaOne font
font50 = ImageFont.truetype(os.path.join(PATH, "Verdana.ttf"), 50)
font18 = ImageFont.truetype(os.path.join(PATH, "Verdana.ttf"), 18)

# Write text with weather values to the canvas
now = time.strftime("%I:%M%p")
date = time.strftime("%A, %m/%d")

# Draw the current weather icon over the backdrop
if weather["icon"] is not None:
    fpath = os.path.join(PATH, "ow-resources/{icon}@2x.png".format(icon=weather["icon"]))
    ico = Image.open(fpath)
    # print(ico)
    img.paste(ico, (140, -10), create_mask(ico))

else:
    draw.text((185, 25), "?", inky_display.BLACK, font=font50)

draw.text((10, 3), "{}".format(weather["location"]), inky_display.BLACK, font=font18)

draw.text((10, 19), u"{}°".format(temperature), inky_display.BLACK, font=font50)

draw.text((10, 77), now, inky_display.BLACK, font=font18)

draw.text((10, 100), date, inky_display.BLACK, font=font18)

draw.text((152, 68), "{}".format(description), inky_display.BLACK, font=font18)

#w, h = 185, 10
#shape = [(50, 50), (w, h)]
#draw.rectangle(shape, fill="#000000")

# Flip the image around
inky_display.h_flip = True
inky_display.v_flip = True

# Display the weather data on Inky pHAT
inky_display.set_image(img)
inky_display.show()
