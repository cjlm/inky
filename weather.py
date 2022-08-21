import copy
import json
import requests
import pytz
import time
from inky import InkyWHAT
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw

from dotenv import load_dotenv
load_dotenv()

import os

ICON_SIZE = 95

TILE_WIDTH = 100
TILE_HEIGHT = 150

FONT_SIZE = 22

SPACE = 2

USE_INKY = True

general_map = {
    200: "thunderstorm.PNG8",
    201: "thunderstorm.PNG8",
    202: "thunderstorm.PNG8",
    210: "lightning.PNG8",
    211: "lightning.PNG8",
    212: "lightning.PNG8",
    221: "lightning.PNG8",
    230: "thunderstorm.PNG8",
    231: "thunderstorm.PNG8",
    232: "thunderstorm.PNG8",
    300: "sprinkle.PNG8",
    301: "sprinkle.PNG8",
    302: "rain.PNG8",
    310: "rain-mix.PNG8",
    311: "rain.PNG8",
    312: "rain.PNG8",
    313: "showers.PNG8",
    314: "rain.PNG8",
    321: "sprinkle.PNG8",
    500: "sprinkle.PNG8",
    501: "rain.PNG8",
    502: "rain.PNG8",
    503: "rain.PNG8",
    504: "rain.PNG8",
    511: "rain-mix.PNG8",
    520: "showers.PNG8",
    521: "showers.PNG8",
    522: "showers.PNG8",
    531: "storm-showers.PNG8",
    600: "snow.PNG8",
    601: "snow.PNG8",
    602: "sleet.PNG8",
    611: "rain-mix.PNG8",
    612: "rain-mix.PNG8",
    615: "rain-mix.PNG8",
    616: "rain-mix.PNG8",
    620: "rain-mix.PNG8",
    621: "snow.PNG8",
    622: "snow.PNG8",
    701: "showers.PNG8",
    711: "smoke.PNG8",
    721: "day-haze.PNG8",
    731: "dust.PNG8",
    741: "fog.PNG8",
    761: "dust.PNG8",
    762: "dust.PNG8",
    771: "cloudy-gusts.PNG8",
    781: "tornado.PNG8",
    800: "day-sunny.PNG8",
    801: "cloudy-gusts.PNG8",
    802: "cloudy-gusts.PNG8",
    803: "cloudy-gusts.PNG8",
    804: "cloudy.PNG8",
    900: "tornado.PNG8",
    901: "storm-showers.PNG8",
    902: "hurricane.PNG8",
    903: "snowflake-cold.PNG8",
    904: "hot.PNG8",
    905: "windy.PNG8",
    906: "hail.PNG8",
    957: "strong-wind.PNG8"}

day_map = {
    200: "day-thunderstorm.PNG8",
    201: "day-thunderstorm.PNG8",
    202: "day-thunderstorm.PNG8",
    210: "day-lightning.PNG8",
    211: "day-lightning.PNG8",
    212: "day-lightning.PNG8",
    221: "day-lightning.PNG8",
    230: "day-thunderstorm.PNG8",
    231: "day-thunderstorm.PNG8",
    232: "day-thunderstorm.PNG8",
    300: "day-sprinkle.PNG8",
    301: "day-sprinkle.PNG8",
    302: "day-rain.PNG8",
    310: "day-rain.PNG8",
    311: "day-rain.PNG8",
    312: "day-rain.PNG8",
    313: "day-rain.PNG8",
    314: "day-rain.PNG8",
    321: "day-sprinkle.PNG8",
    500: "day-sprinkle.PNG8",
    501: "day-rain.PNG8",
    502: "day-rain.PNG8",
    503: "day-rain.PNG8",
    504: "day-rain.PNG8",
    511: "day-rain-mix.PNG8",
    520: "day-showers.PNG8",
    521: "day-showers.PNG8",
    522: "day-showers.PNG8",
    531: "day-storm-showers.PNG8",
    600: "day-snow.PNG8",
    601: "day-sleet.PNG8",
    602: "day-snow.PNG8",
    611: "day-rain-mix.PNG8",
    612: "day-rain-mix.PNG8",
    615: "day-rain-mix.PNG8",
    616: "day-rain-mix.PNG8",
    620: "day-rain-mix.PNG8",
    621: "day-snow.PNG8",
    622: "day-snow.PNG8",
    701: "day-showers.PNG8",
    711: "smoke.PNG8",
    721: "day-haze.PNG8",
    731: "dust.PNG8",
    741: "day-fog.PNG8",
    761: "dust.PNG8",
    762: "dust.PNG8",
    781: "tornado.PNG8",
    800: "day-sunny.PNG8",
    801: "day-cloudy-gusts.PNG8",
    802: "day-cloudy-gusts.PNG8",
    803: "day-cloudy-gusts.PNG8",
    804: "day-sunny-overcast.PNG8",
    900: "tornado.PNG8",
    902: "hurricane.PNG8",
    903: "snowflake-cold.PNG8",
    904: "hot.PNG8",
    906: "day-hail.PNG8",
    957: "strong-wind.PNG8"}

night_map = {
    200: "night-alt-thunderstorm.PNG8",
    201: "night-alt-thunderstorm.PNG8",
    202: "night-alt-thunderstorm.PNG8",
    210: "night-alt-lightning.PNG8",
    211: "night-alt-lightning.PNG8",
    212: "night-alt-lightning.PNG8",
    221: "night-alt-lightning.PNG8",
    230: "night-alt-thunderstorm.PNG8",
    231: "night-alt-thunderstorm.PNG8",
    232: "night-alt-thunderstorm.PNG8",
    300: "night-alt-sprinkle.PNG8",
    301: "night-alt-sprinkle.PNG8",
    302: "night-alt-rain.PNG8",
    310: "night-alt-rain.PNG8",
    311: "night-alt-rain.PNG8",
    312: "night-alt-rain.PNG8",
    313: "night-alt-rain.PNG8",
    314: "night-alt-rain.PNG8",
    321: "night-alt-sprinkle.PNG8",
    500: "night-alt-sprinkle.PNG8",
    501: "night-alt-rain.PNG8",
    502: "night-alt-rain.PNG8",
    503: "night-alt-rain.PNG8",
    504: "night-alt-rain.PNG8",
    511: "night-alt-rain-mix.PNG8",
    520: "night-alt-showers.PNG8",
    521: "night-alt-showers.PNG8",
    522: "night-alt-showers.PNG8",
    531: "night-alt-storm-showers.PNG8",
    600: "night-alt-snow.PNG8",
    601: "night-alt-sleet.PNG8",
    602: "night-alt-snow.PNG8",
    611: "night-alt-rain-mix.PNG8",
    612: "night-alt-rain-mix.PNG8",
    615: "night-alt-rain-mix.PNG8",
    616: "night-alt-rain-mix.PNG8",
    620: "night-alt-rain-mix.PNG8",
    621: "night-alt-snow.PNG8",
    622: "night-alt-snow.PNG8",
    701: "night-alt-showers.PNG8",
    711: "smoke.PNG8",
    721: "day-haze.PNG8",
    731: "dust.PNG8",
    741: "night-fog.PNG8",
    761: "dust.PNG8",
    762: "dust.PNG8",
    781: "tornado.PNG8",
    800: "night-clear.PNG8",
    801: "night-alt-cloudy-gusts.PNG8",
    802: "night-alt-cloudy-gusts.PNG8",
    803: "night-alt-cloudy-gusts.PNG8",
    804: "night-alt-cloudy.PNG8",
    900: "tornado.PNG8",
    902: "hurricane.PNG8",
    903: "snowflake-cold.PNG8",
    904: "hot.PNG8",
    906: "night-alt-hail.PNG8",
    957: "strong-wind.PNG8"}


class Day:
    def __init__(self, min, max, pop, id, sunrise, sunset):
        self.min = int(min + 0.5)
        self.max = int(max + 0.5)
        self.pop = pop
        self.id = id
        self.sunrise = sunrise
        self.sunset = sunset


def convert(img):  # 8 bit indexed color image (white, black, red)
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0))
    return img.convert("RGB").quantize(palette=pal_img)


def get_icon(name):
    return convert(Image.open(name))


def day_lists_not_identical(days, other_days):
    if (len(days) != len(other_days)):
        return True
    for i in range(len(days)):
        if (days[i].min != other_days[i].min):
            return True
        if (days[i].max != other_days[i].max):
            return True
        if (days[i].pop != other_days[i].pop):
            return True
        if (days[i].id != other_days[i].id):
            return True
    return False

def setWeather():
    api_key = os.environ.get('weather_token')
    if (api_key == None):
        print("You forgot to enter your API key")
        exit()
    lat = "48.415910"
    lon = "-123.373190"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=hourly&appid=%s&units=metric" % (
        lat, lon, api_key)

    tile_positions = []
    for i in range(2):
        for j in range(4):
            tile_positions.append((j * TILE_WIDTH, i * TILE_HEIGHT))

    inky_display = InkyWHAT("red")
    inky_display.set_border(inky_display.RED)

    font = ImageFont.truetype(
        "weather/fonts/BungeeColor-Regular_colr_Windows.ttf", FONT_SIZE)

    old_days = []

    try:
        response = requests.get(url)
        data = json.loads(response.text)
    except:
        None

    days = []
    daily = data["daily"]
    for day in daily:
        min = day["temp"]["min"]
        max = day["temp"]["max"]
        pop = day["pop"]
        id = day["weather"][0]["id"]
        sunrise = int(day["sunrise"])
        sunset = int(day["sunset"])
        days.append(Day(min, max, pop, id, sunrise, sunset))

    if (day_lists_not_identical(days, old_days)):
        old_days = copy.deepcopy(days)

        img = convert(Image.new("P", (400, 300), 255))
        draw = ImageDraw.Draw(img)

        for i in range(8):
            name = "weather/icons/wi-"
            t = int(time.time())
            if (t < days[i].sunset):
                name += day_map[days[i].id]
            else:
                name += night_map[days[i].id]
            icon = get_icon(name)
            x = tile_positions[i][0] + (TILE_WIDTH - ICON_SIZE) // 2
            y = tile_positions[i][1]
            img.paste(icon, (x, y))
            text = str(int(100 * days[i].pop)) + "%"
            w, h = font.getsize(text)
            x = tile_positions[i][0] + (TILE_WIDTH - w) // 2
            y = tile_positions[i][1] + ICON_SIZE + SPACE
            draw.text((x, y), text, inky_display.BLACK, font)
            text = str(days[i].min) + "|" + str(days[i].max) + "°"
            w, h = font.getsize(text)
            x = tile_positions[i][0] + (TILE_WIDTH - w) // 2
            y += FONT_SIZE
            draw.text((x, y), text, inky_display.RED, font)

        if (USE_INKY):
            inky_display.set_image(img)
            inky_display.show()
        else:
            img.show()

if __name__ == "__main__":
    setWeather()