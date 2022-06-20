#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import key
import glob
import os
import time
from sys import exit

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

CITY = "Rexburg"
COUNTRYCODE = "US"
APIkey_file = './ow-key.txt'


# manage the api credentials
def pull_api_key():
    if key.check():
        return key.return_key()
    else:
        return key.update_key()


def get_weather(ow_key, address):
    weather = {}
    url = "https://api.openweathermap.org/data/2.5/weather?q={cityname}&units=imperial&appid={APIkey}".format(
        cityname=CITY, APIkey=ow_key)
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "html.parser")
        res = (json.loads(str(soup)))
        weather["location"] = res["name"]
        weather["description"] = res["weather"][0]["description"]
        weather["icon"] = res["weather"][0]["icon"]
        weather["temperature"] = int(res["main"]["temp"])
        weather["feels"] = int(res["main"]["feels_like"])
        return weather
    else:
        return weather


def main():
    ow_key = pull_api_key()
    # Get the weather data for the given location
    location_string = "{city}, {countrycode}".format(city=CITY, countrycode=COUNTRYCODE)
    # print(location_string)
    weather = get_weather(ow_key, location_string)

    # Placeholder variables
    description = "Unknown"
    temperature = 0
    weather_icon = None

    if weather:
        temperature = weather["temperature"]
        description = weather["description"]
        icon = weather["icon"]
    else:
        print("Warning, no weather information found!")

    with open("ow.json", "w") as f:
        f.write(json.dumps(weather))


if __name__ == '__main__':
    main()
