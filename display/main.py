#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from display.data import get_data
from display.draw import update


def main():
    """ Main entry point of the app """
    update(get_data())


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
