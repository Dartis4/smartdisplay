import glob
import os
import time
from sys import exit

from font_fredoka_one import FredokaOne
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

import json
import requests
import geocoder
from bs4 import BeautifulSoup

APIkey = "c6523aa9c6438436cbb0ff25d3518190"

CITY = "Rexburg"
COUNTRYCODE = "US"

# Convert a city name and country code to latitude and longitude
def get_coords(address):
    g = geocoder.arcgis(address)
    coords = g.latlng
    return coords

# Query Dark Sky (https://darksky.net/) to scrape current weather data
def get_weather(address):
    #coords = get_coords(address)
    weather = {}
    url = "https://api.openweathermap.org/data/2.5/weather?q={cityname}&units=imperial&appid={APIkey}".format(cityname=CITY,APIkey=APIkey)
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "html.parser")
        res = (json.loads(str(soup)))
        print(soup.prettify())
        weather["location"] = res["name"]
        weather["description"] = res["weather"][0]["description"]
        weather["temp"] = res["main"]["temp"]
        weather["feels"] = res["main"]["feels_like"]
        #print(soup.prettify())
        print(weather)

    else:
        print("Bad request")

# Get the weather data for the given location
location_string = "{city}, {countrycode}".format(city=CITY, countrycode=COUNTRYCODE)
weather = get_weather(location_string)
