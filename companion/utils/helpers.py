from telethon import utils
import math
from PIL import Image
from telethon.tl.types import Document, Photo, MessageEntityUrl, MessageEntityTextUrl

def has_image(entity):
    if isinstance(entity, Photo):
        return True

    if isinstance(entity, Document):
        if entity.mime_type.split("/")[0] == "image":
            return True
    return False


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


def get_message_type(message):
    if message.forward:
        return "forward"
    elif message.audio:
        return "audio"
    elif message.voice:
        return "voice"
    elif message.video:
        return "video"
    elif message.video_note:
        return "video_note"
    elif message.photo:
        return "photo"
    elif message.gif:
        return "gif"
    elif message.sicker:
        return "sticker"
    elif message.document:
        return "document"
    elif message.poll:
        return "poll"
    elif message.geo:
        return "geo"
    elif message.game:
        return "game"
    elif message.contact:
        return "contact"
    elif message.entities:
        for entity in message.entities:
            if isinstance(entity, (MessageEntityTextUrl, MessageEntityUrl)):
                return "url"
    else:
        return "text"