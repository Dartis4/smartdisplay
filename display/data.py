#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import time

from _deprecated.weather_data_management import load_weather, save_weather
from display.text import Font, Text
from external_api.communication import fetch_info

FONT = Font("Verdana.ttf", "Verdana", 18)
PATH = os.path.dirname(__file__)
ID = 123


def get_order():
    return True


def get_main(data):
    text = u"{}°".format(data)
    return Text(text, FONT)


def get_secondary(data):
    text = "{}".format(data)
    return Text(text, FONT)


def get_image(data):
    if data is not None:
        return os.path.join(PATH, "../res/ow-resources/{icon}@2x.png".format(icon=data))


def get_datetime(time_t, date_t):
    return Text(time_t, FONT), Text(date_t, FONT)


def get_data():
    save_weather(fetch_info(ID))
    data = load_weather()
    print(data)
    print(int(data["main"]["temp"]))

    print(data["name"])
    print(data["weather"][0]["icon"])

    t = time.strftime("%I:%M%p")
    d = time.strftime("%A, %m/%d")

    data_dict = {
        "second_on_top": get_order(),
        "main": get_main(int(data["main"]["temp"])),
        "secondary": get_secondary(data["name"]),
        "datetime": get_datetime(t, d),
        "image": get_image(data["weather"][0]["icon"])
    }
    return data_dict
