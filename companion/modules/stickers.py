import datetime
from io import BytesIO

import emoji
from telethon.errors.rpcerrorlist import (StickersetInvalidError,
                                          YouBlockedUserError)
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (DocumentAttributeFilename,
                               DocumentAttributeSticker,
                               InputMediaUploadedDocument,
                               InputPeerNotifySettings, InputStickerSetID,
                               InputStickerSetShortName)

from companion.utils import CommandHandler
from companion.utils.helpers.messages import has_image, sticker_animated
from companion.utils.helpers.tools import resize_image


async def kang_image(event, file):
    st_emoji = event.args.emoji or "🤔"
    if st_emoji not in (list(emoji.EMOJI_UNICODE.values())):
        await event.edit("Not a valid emoji!")
        return
    user = await event.get_sender()
    packname = user.username or user.first_name + "'s sticker pack!"
    packshort = "tg_companion_" + str(user.id)
    await event.edit("Processing sticker! Please wait...")
    async with event.client.conversation('Stickers') as conv:
        until_time = (
            datetime.datetime.now() +
            datetime.timedelta(
                minutes=1)).timestamp()
        await event.client(UpdateNotifySettingsRequest(peer="Stickers",
                                                       settings=InputPeerNotifySettings(show_previews=False,
                                                                                        mute_until=until_time)))

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

            await conv.send_file(InputMediaUploadedDocument(file=uploaded_sticker, mime_type='image/png',
                                                            attributes=[DocumentAttributeFilename("sticker.png")]),
                                 force_document=True)
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
    await event.edit("Sticker added! Your pack can be found [here](https://t.me/addstickers/{})".format(packshort),
                     parse_mode='md')


async def kang_animated(event, file):
    st_emoji = event.args.emoji or "🤔"
    if st_emoji not in (list(emoji.EMOJI_UNICODE.values())):
        await event.edit("Not a valid emoji!")
        return
    user = await event.get_sender()
    packname = "{}'s animated sticker pack!".format(
        user.username or user.first_name)
    packshort = "tg_companion_anim_" + str(user.id)
    await event.edit("Processing sticker! Please wait...")

    async with event.client.conversation('Stickers') as conv:
        until_time = (
            datetime.datetime.now() +
            datetime.timedelta(
                minutes=1)).timestamp()
        await event.client(UpdateNotifySettingsRequest(peer="Stickers",
                                                       settings=InputPeerNotifySettings(show_previews=False,
                                                                                        mute_until=until_time)))

        try:
            await conv.send_message("/cancel")
        except YouBlockedUserError:
            await event.reply("You blocked the sticker bot. Please unblock it and try again")
            return
        try:
            await event.client(GetStickerSetRequest(InputStickerSetShortName(packshort)))
            new_pack = False
        except StickersetInvalidError:
            new_pack = True

        if new_pack is True:
            await conv.send_message("/newanimated")
            response = await conv.get_response()
            if not response.text.startswith("Yay!"):
                await event.edit(response.text)
                return

            await conv.send_message(packname)
            response = await conv.get_response()
            if not response.text.startswith("Alright!"):
                await event.edit(response.text)
                return
            file = await event.client.download_file(file)
            uploaded_sticker = await event.client.upload_file(file, file_name="sticker.tgs")
            await conv.send_file(file=uploaded_sticker)
            response = await conv.get_response()
            if not response.text.startswith('Thanks!'):
                await event.edit(response.text)
                return
            await conv.send_message(st_emoji)
            await conv.send_message("/publish")
            await conv.send_message("<" + packname + ">")
            await conv.send_message("/skip")
            await conv.send_message(packshort)
            response = conv.get_response()
        else:
            await conv.send_message("/addsticker")
            await conv.send_message(packshort)
            file = await event.client.download_file(file)
            uploaded_sticker = await event.client.upload_file(file, file_name="sticker.tgs")
            await conv.send_file(file=uploaded_sticker)
            response = await conv.get_response()
            if not response.text.startswith('Thanks!'):
                await event.edit(response.text)
                return
            await conv.send_message(st_emoji)
            await conv.send_message("/done")
        await event.edit("Sticker added! Your pack can be found [here](https://t.me/addstickers/{})".format(packshort),
                         parse_mode='md')


@CommandHandler(command="kang", args=["emoji"], parse_mode='md')
async def kang_base(event):
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
        await kang_image(event, file)
    elif sticker_animated(file):
        await kang_animated(event, file)
    else:
        await event.edit("Not a valid media entity!")


@CommandHandler(command='packinfo')
async def get_pack_info(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Sticker's pack info!</i>
    """
    if not event.is_reply:
        await event.edit('Reply to a sticker to get the pack details')
    else:
        rep_msg = await event.get_reply_message()
        if not rep_msg.document:
            await event.edit('Reply to a sticker to get the pack details')
        else:
            stickerset_attr = rep_msg.document.attributes[1] if len(
                rep_msg.document.attributes) > 1 else rep_msg.document.attributes[0]
            if not isinstance(stickerset_attr, DocumentAttributeSticker):
                await event.edit(
                    'The message you replied to doesn\'t have any sticker object or the respective sticker doesn\'t belong in a sticker-pack!')
            else:
                get_stickerset = await event.client(
                    GetStickerSetRequest(InputStickerSetID(id=stickerset_attr.stickerset.id,
                                                           access_hash=stickerset_attr.stickerset.access_hash)))
                pack_emojis = []
                for document_sticker in get_stickerset.packs:
                    if document_sticker.emoticon not in pack_emojis:
                        pack_emojis.append(document_sticker.emoticon)
                await event.edit(
                    f"**Sticker Title:** `{get_stickerset.set.title}\n`"
                    f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
                    f"**Official:** `{get_stickerset.set.official}`\n"
                    f"**Archived:** `{get_stickerset.set.archived}`\n"
                    f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n"
                    f"**Emojis In Pack:** {' '.join(pack_emojis)}",
                    parse_mode='md')
