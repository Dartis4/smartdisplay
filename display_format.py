"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

from dataclasses import dataclass
from typing import Tuple

from PIL import ImageDraw, Image

from display_text import Text


@dataclass
class Rectangle:
    width: float
    height: float


@dataclass
class Zone:
    x: float
    y: float
    dimension: Rectangle


class Window:
    OTHER_TEXT_HEIGHT_RATIO = 0.16

    def __init__(self, width, _height):
        self.width = width #- (width * 0.04)
        height = width * 0.488
        self.height = height #- (height * 0.02)

    def get_margin(self):
        return Rectangle(self.width * 0.04, self.height * 0.02)

    def get_main_box(self):
        return Rectangle(self.width * 0.6, self.height * 0.5)

    def get_secondary_box(self):
        width = self.width * 0.6
        return Rectangle(width, width * self.OTHER_TEXT_HEIGHT_RATIO)

    def get_image_box(self):
        width = height = self.width * 0.3
        return Rectangle(width, height)

    def get_datetime_box(self):
        width = self.width * 0.6
        return Rectangle(width, width * self.OTHER_TEXT_HEIGHT_RATIO)


class ZoneFormatter:

    def __init__(self, width, height, secondary_zone_on_top=True):
        self.second_zone_on_top = secondary_zone_on_top
        self.window = Window(width, height)
        self.canvas = ImageDraw.Draw(Image.new("P", (int(self.window.width), int(self.window.height))))
        margin = self.window.get_margin()
        self.start_x = margin.height
        self.start_y = margin.width

    def __text_zone(self, data: Text, zone: Zone):
        def text_is_smaller(box, zone_target):
            _, _, right, bottom = box
            t_right = zone_target.x + zone_target.dimension.width
            t_bottom = zone_target.y + zone_target.dimension.height
            if right < t_right and bottom < t_bottom:
                return True
            else:
                return False

        def find_largest_possible_font_size(canvas, text, target, start_size=5):
            while text_is_smaller(
                    canvas.textbbox((target.x, target.y), text.content, font=text.font.generate(start_size)), target):
                start_size += 1
            return start_size

        font_size = find_largest_possible_font_size(self.canvas, data, zone)
        return (zone.x, zone.y), data.content, data.color, data.font.generate(font_size)

    @staticmethod
    def __image_zone(data: str, zone: Zone) -> Image:
        img = Image.open(data)
        return img.resize((int(zone.dimension.width), int(zone.dimension.height))), (zone.x, zone.y)


    def _main_zone_layout(self) -> Zone:
        dimensions = self.window.get_main_box()
        if not self.second_zone_on_top:
            return Zone(self.start_x, self.start_y, dimensions)
        else:
            x = self.start_x
            y = self.start_y + self.window.get_secondary_box().height
            return Zone(x, y, dimensions)

    def _secondary_zone_layout(self) -> Zone:
        dimensions = self.window.get_secondary_box()
        if self.second_zone_on_top:
            return Zone(self.start_x, self.start_y, dimensions)
        else:
            x = self.start_x
            y = self.start_y + self.window.get_main_box().height
            return Zone(x, y, dimensions)

    def _image_zone_layout(self) -> Zone:
        dimensions = self.window.get_image_box()
        x = int(self.window.width - dimensions.width)
        y = int(self.start_y)
        return Zone(x, y, dimensions)

    def _datetime_zone_layout(self) -> Zone:
        dimensions = self.window.get_datetime_box()
        x = self.start_x
        y = self.window.height - dimensions.height
        return Zone(x, y, dimensions)

    def zone_main(self, data: Text) -> Image:
        # Main info - this will be the largest display zone and
        # should contain the most important info
        zone = self._main_zone_layout()
        return self.__text_zone(data, zone)

    def zone_secondary(self, data: Text) -> Image:
        # Secondary info - this will be a smaller descriptor of
        # the data that is in the main zone or additional info that
        # pairs with the main zone
        zone = self._secondary_zone_layout()
        return self.__text_zone(data, zone)

    def zone_image(self, data: Image) -> Image:
        # Icon - an appropriate image that pairs with the data
        # being displayed that adds additional context
        zone = self._image_zone_layout()
        return self.__image_zone(data, zone)

    def zone_datetime(self, data: Tuple[Text, Text]) -> Image:
        # This will be a static zone for displaying the date
        # and time. The user will not be able to modify this
        # data directly.
        date, time = data
        datetime = Text("\n".join((date.content, time.content)), date.font, date.color)
        zone = self._datetime_zone_layout()
        return self.__text_zone(datetime, zone)
