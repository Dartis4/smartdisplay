#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Dane Artis"
__version__ = "0.1.0"
__license__ = "MIT"

import requests
from bs4 import BeautifulSoup
from displayconf.models import API, ApiData
from django.core.management import BaseCommand


def request(target):
    response = requests.get(target)

    if response.status_code == 200:
        return str(BeautifulSoup(response.content, "html.parser"))
    else:
        return "fail"


def build_target(base_address: str, request_format: str, parameters: dict, token: dict):
    def gen_query_params(k, d):
        delimiter = d[k].pop()
        if delimiter == 'Blank':
            delimiter = ""
        return "{key}={values}".format(key=k, values=delimiter.join(d[k]))
    parameters.update(token)


    target = "{0}{1}?{parameters}".format(base_address, request_format, parameters='&'.join(
        [gen_query_params(key, parameters) for key in parameters.keys()]))
    return target


class Command(BaseCommand):
    help = 'Fetch the external data of a specified api'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, nargs='?', help='the id of the api to fetch data for')
        parser.add_argument('--main', type=str, nargs='+',
                            help='the json tag for the data to be displayed in the main zone')
        parser.add_argument('--secondary', type=str, nargs='+',
                            help='the json tag for the data to be displayed in the main zone')
        parser.add_argument('--image', type=str, nargs='+',
                            help='the json tag for the data to be displayed in the main zone')

    def handle(self, *args, **options):
        api = API.objects.get(pk=options['id'])
        self.stdout.write(f"Fetching data for {api.name}...")
        target = build_target(api.base_address, api.format, api.params, api.token)
        # print(target)
        res = request(target)
        # print(res)
        if res != 'fail':
            self.stdout.write(res)
            # print(api.apidata_set.get(pk=1).data)
            if api.apidata_set.count() == 0:
                api.apidata_set.create(data=res)
            else:
                api_data = ApiData.objects.get(api_id=options['id'])
                api_data.data = res
                api_data.tags = {'main': options['main'], 'second': options['secondary'], 'image': options['image']}
                print(api_data.tags)
                api_data.save()
