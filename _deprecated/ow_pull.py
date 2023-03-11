#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sys import exit

from _deprecated import key, location
from display import data

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

# Get the current path
PATH = os.path.dirname(__file__)
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'


# manage the api credentials
def pull_api_key():
    if key.check():
        return key.return_key()
    else:
        return key.update_key()


def pull_location():
    if location.check():
        return location.return_loc()
    else:
        return location.update_loc()


def get_weather(ow_key, address):
    weather = {}
    res = requests.get(f'{BASE_URL}?q={address}&units=imperial&appid={ow_key}')
    if res.status_code == 200:
        res = (json.loads(str(BeautifulSoup(res.content, "html.parser"))))
        weather["location"] = res["name"]
        weather["description"] = res["weather"][0]["description"]
        weather["icon"] = res["weather"][0]["icon"]
        weather["temperature"] = int(res["main"]["temp"])
        weather["feels"] = int(res["main"]["feels_like"])
        return weather
    else:
        return weather


def main():
    # Placeholder variables
    temperature = 0
    description = "Unknown"
    icon = None

    # Get the weather data for the given location
    location_string = pull_location()
    weather = get_weather(pull_api_key(), location_string)

    if weather:
        temperature = weather["temperature"]
        description = weather["description"]
        icon = weather["icon"]
        print(location_string)
        print(temperature)
        print(description)
        print(icon)
    else:
        print("Warning, no weather information found!")

    data.save_weather(weather)


if __name__ == '__main__':
    main()
