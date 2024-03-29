import json
import os

import ow_pull

PATH = os.path.dirname(__file__)
DATA_FILE = os.path.join(PATH, 'ow.json')


def save_weather(weather):
    with open(DATA_FILE, 'w') as f:
        f.write(json.dumps(weather))


def load_weather():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.loads(f.readline())
    else:
        ow_pull.main()
        load_weather()
