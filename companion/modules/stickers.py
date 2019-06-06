import emoji
import datetime
from PIL import Image
from io import BytesIO
from telethon.errors.rpcerrorlist import StickersetInvalidError, YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputPeerNotifySettings, InputStickerSetShortName, InputMediaUploadedDocument, DocumentAttributeFilename
from telethon import utils

from companion.utils import CommandHandler, has_image, resize_image


@CommandHandler(command="kang", args=["emoji"])
async def kang(event):
        """
        <b>param:</b> <code>emoji</code>
        <b>return:</b> <i>Sticker Pack link including the kanged sticker</i>
        """
        if not event.is_reply:
            await event.edit("There's no image given for me to kang!")
            return
        rep_msg = await event.get_reply_message()
        file = rep_msg.photo or rep_msg.document

        if has_image(file):
           st_emoji = event.args.emoji or "🤔"
           if st_emoji not in (list(emoji.EMOJI_UNICODE.values())):
               await event.edit("Not a valid emoji!")
               return

           user = await event.get_sender()
           packname = user.username or user.first_name + "'s sticker pack!"
           packshort = "tg_companion_" + str(user.id)
           await event.edit("Processing sticker! Please wait...")
           async with event.client.conversation('Stickers') as conv:
               until_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).timestamp()
               await event.client(UpdateNotifySettingsRequest(peer="Stickers", settings=InputPeerNotifySettings(show_previews=False, mute_until=until_time)))

               try:
                   await conv.send_message("/cancel")
               except YouBlockedUserError:
                    await event.reply("You blocked the sticker bot. Please unblock it and try again")
                    return

               file = await event.client.download_file(file)
               with BytesIO(file) as mem_file, BytesIO() as sticker:
                   resize_image(mem_file, (512, 512), sticker)
                   sticker.seek(0)
                   uploaded_sticker = await event.client.upload_file(sticker, file_name="sticker.png")

               try:
                   await event.client(GetStickerSetRequest(InputStickerSetShortName(packname)))
                   new_pack = False
               except StickersetInvalidError:
                   new_pack = True

               if new_pack is False:
                   await conv.send_message("/newpack")
                   response = await conv.get_response()
                   if not response.text.startswith("Yay!"):
                       await event.edit(response.text)
                       return

                   await conv.send_message(packname)
                   response = await conv.get_response()
                   if not response.text.startswith("Alright!"):
                        await event.edit(response.text)
                        return

                   await conv.send_file(InputMediaUploadedDocument(file=uploaded_sticker, mime_type='image/png', attributes=[DocumentAttributeFilename("sticker.png")]), force_document=True)
                   await conv.send_message(st_emoji)
                   await conv.send_message("/publish")
                   await conv.send_message("/skip")
                   await conv.send_message(packshort)
                   response = conv.get_response()
               else:
                   await conv.send_message("/addsticker")
                   await conv.send_message(packshort)
                   await conv.send_file(InputMediaUploadedDocument(file=uploaded_sticker, mime_type='image/png',
                                                                   attributes=[DocumentAttributeFilename(
                                                                       "sticker.png")]), force_document=True)
                   await conv.send_message(st_emoji)
                   await conv.send_message("/done")
           await event.edit("Sticker added! Your pack can be found [here](https://t.me/addstickers/{})".format(packshort))
        else:
            await event.edit("Not a valid media entity!")




