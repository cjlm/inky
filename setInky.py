import random

from setMeme import setMeme
from setAiMeme import setAiMeme
from setHighlight import setHighlight
from weather import setWeather

random.choice([setMeme, setAiMeme, setWeather, setHighlight])()