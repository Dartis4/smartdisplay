#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

from .draw import update
from .data import get_data


__name__ = "display"
__all__ = ["data", "draw", "format", "text"]

def main():
    """ Main entry point of the app """
    update(get_data())


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
