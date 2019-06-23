import math
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