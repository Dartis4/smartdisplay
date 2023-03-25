#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import json

from displayconf.models import ApiData, API
from django.core.management import BaseCommand

from display import draw, data

class Command(BaseCommand):
    help = 'Fetch the internal data of a specified api'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='The id of the api to fetch from')
        parser.add_argument('--image-url', type=str, help='A url to retrieve the image if the data does not contain it. Use \{icon\} in place of the image value in the url.')
        parser.add_argument('--main-type', type=str, help='The data type of the main zone content.')
        parser.add_argument('--second-type', type=str, help='The data type of the second zone content.')

    def handle(self, *args, **options):
        api_data = ApiData.objects.get(api_id=options['id'])
        # print("image tags", api_data.tags)
        # print(api_data.data)
        json_data = json.loads(api_data.data)
        # print(json_data, type(json_data))
        tags = api_data.tags

        def parse_tag(value, temp_tags):
            val = temp_tags.pop(0)
            if val[0] == '#':
                val = int(val.replace('#', ''))
            return value[val], temp_tags

        def type_conv(value, vtype):
            # print("input type", vtype)
            if vtype:
                t = vtype
                if t == 'int':
                    # print("int convert")
                    # print(int(value))
                    return int(value)
                elif t == 'string' or 'str':
                    # print("string convert")
                    return str(value)
                elif t == 'float':
                    # print("float convert")
                    return float(value)
                return value
            return value

        main, tag = parse_tag(json_data, tags['main'].copy())
        # print(main)
        while len(tag):
            main, tag = parse_tag(main, tag)
            # print(main)

        main = type_conv(main, options['main_type'])

        second, tag = parse_tag(json_data, tags['second'].copy())
        # print(second)
        while len(tag):
            second, tag = parse_tag(second, tag)
            # print(second)

        second = type_conv(second, options['second_type'])

        image, tag = parse_tag(json_data, tags['image'].copy())
        # print(image)
        while len(tag):
            image, tag = parse_tag(image, tag)
            # print(image)

        if options['image_url']:
            image = options['image_url'].format(icon=image)
            # print(image)

        swap_zone = API.objects.get(pk=options['id']).switch_display_zones

        draw.update(data.get_data(main, second, image, swap_zone))
