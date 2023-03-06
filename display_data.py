"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import time
from typing import Tuple

from PIL import Image

from display_text import Text, Font
from external_api_communication import fetch_info
from weather_data_management import save_weather, load_weather

FONT = Font("Verdana.tff", "Verdana", 18)
PATH = os.path.dirname(__file__)
ID = 123

def get_order():
    return True

def get_main(data) -> Text:
    text = u"{}°".format(data)
    return Text(text, FONT)

def get_secondary(data) -> Text:
    text = "{}".format(data)
    return Text(text, FONT)

def get_image(data) -> Image:
    if data is not None:
        fpath = os.path.join(PATH, "ow-resources/{icon}@2x.png".format(icon=data))
        return Image.open(fpath)

def get_datetime() -> Tuple[Text, Text]:
    now = time.strftime("%I:%M%p")
    date = time.strftime("%A, %m/%d")
    return Text(now, FONT), Text(date, FONT)

def get_data():
    save_weather(fetch_info(ID))
    data = load_weather()

    data_dict = {
        "second_on_top": get_order(),
        "main": get_main(data["main"]["temp"]),
        "secondary": get_secondary(data["name"]),
        "datetime": get_datetime(),
        "image": get_image(data["weather"][0]["icon"])
    }
    return data_dict
