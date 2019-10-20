import math
import re
import datetime

from PIL import Image


def resize_image(image, size, save_location):
    """ Copyright Rhyse Simpson:
        https://github.com/skittles9823/SkittBot/blob/master/tg_bot/modules/stickers.py
    """
    image = Image.open(image)
    if (image.width and image.height) < size[0]:
        w = image.width
        h = image.height
        if image.width > image.height:
            scale = size[0] / w
            w = size[0]
            h = h * scale
        else:
            scale = size[0] / h
            w = w * scale
            h = size[0]
        w = math.floor(w)
        h = math.floor(h)
        size = (w, h)
    else:
        image.thumbnail(size)
    image.save(save_location, "PNG")


def parse_time(str_time):
    pattern = r'\d*d|\d*h|\d*m|\d*s'
    findall = re.findall(str_time, pattern)
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    if not findall:
        return
    else:
        for match in findall:
            if match.endswith('d'):
                days = match[:-1]
            if match.endswith('h'):
                hours = match[:-1]
            if match.endswith('m'):
                minutes = match[:-1]
            if match.endswith('s'):
                seconds = match[:-1]

        now = datetime.datetime.now()
        after = now + \
            datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return after
