# -*- coding: utf-8 -*-

import json

import requests
from bs4 import BeautifulSoup


def request(target, rtype='get'):
    if rtype == 'get':
        response = requests.get(target)
    elif rtype == 'put':
        response = requests.put(target)
    elif rtype == 'delete':
        response = requests.delete(target)
    else:
        return "fail"

    if response.status_code == 200:
        return json.loads(str(BeautifulSoup(response.content, "html.parser")))
    else:
        return "fail"


def fetch_internal(api_id=None):
    if api_id is None:
        return request(f"http://127.0.0.1:8000/api/get/")
    else:
        return request(f"http://127.0.0.1:8000/api/get/{api_id}/")

def fetch_api_address(api_id):
    response = fetch_internal(api_id=api_id)
    if response != "fail":
        address = response["base_address"]
        form = response["format"]
        params = response["params"]
        key = response["token"]
        return address, form, params, key


def fetch_external(api_id):
    return get(*fetch_api_address(api_id=api_id))


def get(base_address: str, request_format: str, parameters: dict, token: dict):
    parameters.update(token)

    def gen_query_params(k, d):
        delimiter = d[k].pop()
        if delimiter == 'Blank':
            delimiter = ""
        return "{key}={values}".format(key=k, values=delimiter.join(d[k]))

    target = "{0}{1}?{parameters}".format(base_address, request_format, parameters='&'.join(
        [gen_query_params(key, parameters) for key in parameters.keys()]))

    print(target)
    return request(target)
