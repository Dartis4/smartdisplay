"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

import os.path

import inky.auto as auto
from PIL import ImageFont

inky_display = auto(ask_user=True, verbose=True)


class Font:
    # class variables
    PATH = os.path.join(os.path.dirname(__file__), "../res/fonts")

    def __init__(self, font_face_filename: str, font_face_name: str, font_face_default_size: int):
        # instance variables
        self.face = font_face_name
        self.size = font_face_default_size
        self.path = os.path.join(self.PATH, font_face_filename)

    def __str__(self):
        return f"{self.face} {self.size}"

    # methods
    def generate(self, size=0):
        if size == 0:
            return ImageFont.truetype(self.path, self.size)
        else:
            return ImageFont.truetype(self.path, size)


class Text:
    # class variables
    def __init__(self, content: str, font: Font, color: str = 'black'):
        # instance variables
        self.font = font
        self.content = content
        self.color = color


def main():
    pass


if __name__ == '__main__':
    main()
