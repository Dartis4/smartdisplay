#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import exit

import ow_pull

try:
    import json
except ImportError:
    exit("This script requires the json module\nInstall with: sudo pip install json")

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    exit("This script requires the bs4 module\nInstall with: sudo pip install beautifulsoup4==4.6.3")

def fetch_base_address(api_id):
    print(api_id)
    address = "https://api.openweathermap.org/data/2.5/weather"
    return address


def fetch_format(api_id):
    print(api_id)
    data_format = ""
    return data_format


def fetch_params(api_id):
    print(api_id)
    params = {"q": ["Rexburg", "ID", "US", ","], "units": ["imperial", ""]}
    return params


def fetch_key(api_id):
    print(api_id)
    token = ow_pull.pull_api_key()
    key = {'appid': [token, ""]}
    return key


def fetch_info(api_id):
    return get(fetch_base_address(api_id), fetch_format(api_id), fetch_params(api_id), fetch_key(api_id))


def get(base_address, request_format, parameters, token):
    parameters.update(token)

    def gen_query_params(k, d):
        delimiter = d[k].pop()
        return "{key}={values}".format(key=k, values=delimiter.join(d[k]))

    target = "{0}{1}?{parameters}".format(base_address, request_format, parameters='&'.join(
        [gen_query_params(key, parameters) for key in parameters.keys()]))

    print(target)

    response = requests.get(target)

    if response.status_code == 200:
        return json.loads(str(BeautifulSoup(response.content, "html.parser")))
    else:
        return "fail"


def main():
    print(fetch_info(123))


if __name__ == '__main__':
    main()
