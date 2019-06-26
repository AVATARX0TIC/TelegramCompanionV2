from telethon.tl.types import Document, Photo, MessageEntityUrl, MessageEntityTextUrl, MessageEntityBotCommand
from companion.utils.decorators.commandhandler import MessageEntityUserBotCommand

def has_image(entity):
    if isinstance(entity, Photo):
        return True

    if isinstance(entity, Document):
        if entity.mime_type.split("/")[0] == "image":
            return True
    return False

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
    elif message.sticker:
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
            if isinstance(entity, (MessageEntityBotCommand, MessageEntityUserBotCommand)):
                return "command"
    else:
        return "text"