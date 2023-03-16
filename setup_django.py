#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from os import path, environ
from sys import path as sys_path

from django import setup

PATH = path.dirname(__file__)

def main():
    """ Main entry point of the app """
    sys_path.append(path.join(PATH, "portal/portal/settings.py"))
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
    setup()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
