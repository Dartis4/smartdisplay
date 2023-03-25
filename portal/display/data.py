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

import requests

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
    # print("image data", data)
    response = requests.get(data)
    # print("image response", response)
    return response


def get_time():
    return Text(time.strftime("%I:%M%p"), FONT)


def get_date():
    return Text(time.strftime("%A, %m/%d"), FONT)


def get_data(main, second, image, order):

    data_dict = {
        "main_on_top": order,
        "main": get_main(main),
        "secondary": get_secondary(second),
        "time": get_time(),
        "date": get_date(),
        "image": get_image(image)
    }
    return data_dict
