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
        parser.add_argument('id', type=int, help='the id of the api to fetch from')

    def handle(self, *args, **options):
        api_data = ApiData.objects.get(api_id=options['id'])
        print(api_data.data)
        json_data = json.loads(api_data.data)
        tags = api_data.tags

        def parse_tag(value, tags):
            val = tags.pop(0)
            if val[0] == '#':
                val = int(val.replace('#', ''))
            return value[val], tags

        main, tag = parse_tag(json_data, tags['main'].copy())
        while len(tag):
            main, tag = parse_tag(main, tag)

        second, tag = parse_tag(json_data, tags['second'].copy())
        while len(tag):
            second, tag = parse_tag(second, tag)

        image, tag = parse_tag(json_data, tags['image'].copy())
        while len(tag):
            image, tag = parse_tag(image, tag)

        swap_zone = API.objects.get(pk=options['id']).switch_display_zones

        draw.update(data.get_data(main, second, image, swap_zone))
