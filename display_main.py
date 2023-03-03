#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from display_data import get_data
from display_draw import update


def main():
    """ Main entry point of the app """
    data = get_data()
    update(data)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
