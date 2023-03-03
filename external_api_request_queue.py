#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itertools import cycle

def fetch_api_ids():
    return [123]

class ApiQueue:
    api_ids = fetch_api_ids()
    queue = cycle(api_ids)

    def get_next_id(self):
        return next(self.queue)

    def remove_id(self, id_to_remove):
        # TODO switch this to remove from the database and request the new list
        self.api_ids.remove(id_to_remove)
        self.queue = cycle(self.api_ids)


def main():
    pass

if __name__ == '__main__':
    main()
