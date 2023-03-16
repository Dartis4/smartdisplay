#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


import display.main as display
from external_api import communication


def main():
    """ Main entry point of the app """
    display.main()
    # communication.main()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
