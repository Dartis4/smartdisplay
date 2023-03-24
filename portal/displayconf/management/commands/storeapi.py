#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

from django.core.management.base import BaseCommand

from displayconf.models import API


class Command(BaseCommand):
    help = 'Creates a new api in the database'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='an arbitrary human-readable name for this api')
        parser.add_argument('base-address', type=str,
                            help='the main address portion for the target of all requests made for this api')
        parser.add_argument('--format', nargs='?', type=str, help='the format portion of api request target')
        parser.add_argument('--query-param', nargs=3, metavar=('PARAM', 'ARGS,...', 'DELIMITER'), action='append',
                            type=str,
                            help='PARAM is the query parameter, ARGS is a comma separated list of arguments to be passed to PARAM, DELIMITER indicates how the ARGS should be delimited when the query target of the request is formed (use "Blank" to indicate no delimiter)')
        parser.add_argument('--api-token', nargs=2, metavar=('QUERY_PARAM', 'TOKEN'), type=str,
                            help='QUERY_PARAM is the label the api uses to indicate the api token/key, TOKEN is the api token/key value')
        parser.add_argument('--zone-swap', action='store_true',
                            help='indicates if the main zone should be swapped so that it is at the top of the display')

    def handle(self, *args, **options):
        api = API(name=options['name'], base_address=options['base-address'])
        if options['format']:
            api.format = options['format']
        if options['query_param']:
            params = dict()
            for param in options['query_param']:
                values = param.copy()
                label = values.pop(0)
                delim = values.pop()
                arg = values.pop().split(",")
                params.update({label: arg + [delim]})
            api.params = params
        if options['api_token']:
            val = options['api_token']
            api.token = {val[0]: [val[1], ""]}
        if options['zone_swap']:
            api.switch_display_zones = options['zone_swap']
        api.save()
        self.stdout.write("{name}(id:{aid}) saved.".format(name=api.name, aid=api.id))
