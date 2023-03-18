#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import time

from _deprecated.weather_data_management import load_weather, save_weather
from external_api.communication import fetch_info
from .text import Font, Text

FONT = Font("Verdana.ttf", "Verdana", 18)
PATH = os.path.dirname(__file__)
ID = 123


def get_order():
    return False


def get_main(data):
    text = u"{}°".format(data)
    return Text(text, FONT)


def get_secondary(data):
    text = "{}".format(data)
    return Text(text, FONT)


def get_image(data):
    if data is not None:
        return os.path.join(PATH, "../res/ow-resources/{icon}@2x.png".format(icon=data))


def get_time():
    return Text(time.strftime("%I:%M%p"), FONT)


def get_date():
    return Text(time.strftime("%A, %m/%d"), FONT)


def get_data():
    save_weather(fetch_info(ID))
    data = load_weather()
    print(data)
    print(int(data["main"]["temp"]))
    print(data["name"])
    print(data["weather"][0]["icon"])

    data_dict = {
        "main_on_top": get_order(),
        "main": get_main(int(data["main"]["temp"])),
        "secondary": get_secondary(data["name"]),
        "time": get_time(),
        "date": get_date(),
        "image": get_image(data["weather"][0]["icon"])
    }
    return data_dict


def main():
    pass


if __name__ == '__main__':
    main()
