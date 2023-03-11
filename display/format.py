"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

from dataclasses import dataclass
from typing import Tuple

from PIL import ImageDraw, Image

from display.text import Text


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
        self.width = width - (width * 0.04)
        height = width * 0.488
        self.height = height - (height * 0.02)

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

    def get_time_box(self):
        width = self.width * 0.6
        return Rectangle(width, width * self.OTHER_TEXT_HEIGHT_RATIO)

    def get_date_box(self):
        width = self.width * 0.6
        return Rectangle(width, width * self.OTHER_TEXT_HEIGHT_RATIO)


class ZoneFormatter:

    def __init__(self, width, height, secondary_zone_on_top=True):
        self.second_zone_on_top = secondary_zone_on_top
        self.window = Window(width, height)
        self.canvas = ImageDraw.Draw(Image.new("P", (int(width), int(height))))
        margin = self.window.get_margin()
        self.start_x = margin.width
        self.start_y = margin.height

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
    def __image_zone(data: str, zone: Zone):
        img = Image.open(data)
        new_img = img.resize((int(zone.dimension.width), int(zone.dimension.height)))
        return new_img, (zone.x, zone.y)

    def _main_zone_layout(self):
        dimensions = self.window.get_main_box()
        print("Main dimensions:", dimensions)
        if not self.second_zone_on_top:
            return Zone(self.start_x, self.start_y, dimensions)
        else:
            x = self.start_x
            y = self.start_y + self.window.get_secondary_box().height
            return Zone(x, y, dimensions)

    def _secondary_zone_layout(self):
        dimensions = self.window.get_date_box()
        print("Secondary dimensions:", dimensions)
        if self.second_zone_on_top:
            return Zone(self.start_x, self.start_y, dimensions)
        else:
            x = self.start_x
            y = self.start_y + self.window.get_main_box().height
            return Zone(x, y, dimensions)

    def _image_zone_layout(self):
        dimensions = self.window.get_image_box()
        print("Image dimensions:", dimensions)
        x = int((self.window.width * 0.79) - dimensions.width // 2)
        y = int((self.window.height * 0.46) - dimensions.height // 2)
        return Zone(x, y, dimensions)

    def _time_zone_layout(self):
        dimensions = self.window.get_time_box()
        print("Time dimensions:", dimensions)
        x = int(self.window.width * 0.04)
        y = int(self.window.height * 0.63)
        if y + dimensions.height > self.window.height - self.start_y:
            print("Height error time")
        return Zone(x, y, dimensions)

    def _date_zone_layout(self):
        dimensions = self.window.get_date_box()
        print("Date dimensions:", dimensions)
        x = int(self.window.width * 0.04)
        y = int(self.window.height * 0.82)
        if y + dimensions.height > self.window.height:
            print("Height error date")
        return Zone(x, y, dimensions)

    def zone_main(self, data: Text):
        # Main info - this will be the largest display zone and
        # should contain the most important info
        zone = self._main_zone_layout()
        return self.__text_zone(data, zone)

    def zone_secondary(self, data: Text):
        # Secondary info - this will be a smaller descriptor of
        # the data that is in the main zone or additional info that
        # pairs with the main zone
        zone = self._secondary_zone_layout()
        return self.__text_zone(data, zone)

    def zone_image(self, data: Image):
        # Icon - an appropriate image that pairs with the data
        # being displayed that adds additional context
        zone = self._image_zone_layout()
        return self.__image_zone(data, zone)

    def zone_time(self, data: Text):
        zone = self._time_zone_layout()
        return self.__text_zone(data, zone)

    def zone_date(self, data: Text):
        zone = self._date_zone_layout()
        return self.__text_zone(data, zone)

    def zone_datetime(self, data: Tuple[Text, Text]) -> Image:
        # This will be a static zone for displaying the date
        # and time. The user will not be able to modify this
        # data directly.
        time, date = data
        return self.__text_zone(time, self._time_zone_layout()), self.__text_zone(date, self._date_zone_layout())
