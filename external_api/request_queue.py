#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itertools import cycle

from external_api.communication import fetch_internal


def fetch_api_ids():
    return [api["id"] for api in fetch_internal()["results"]]


class ApiQueue:
    list = fetch_api_ids()
    queue = cycle(list)

    def get_id(self):
        return next(self.queue)

    def remove_id(self, id_to_remove):
        self.list.remove(id_to_remove)
        self.queue = cycle(self.list)
