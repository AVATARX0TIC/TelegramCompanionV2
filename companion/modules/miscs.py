from html import escape
import re
import aiohttp
import json
from telethon.errors import UserIdInvalidError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.types import User, InputPeerNotifySettings
import datetime
from companion.utils import CommandHandler


@CommandHandler(command="info", args=["user"], parse_mode="html")
async def user_info(event):
    """
        <b>param:</b> <code>(optional if reply) user id or username</code>
        <b>return:</b> <i>User's info</i>
    """

    if event.is_reply:
        message = await event.get_reply_message()
        user_id_or_name = message.from_id
    elif not event.args.user:
        message = event.message
        user_id_or_name = message.from_id
    else:
        message = event.message
        user_id_or_name = int(
            event.args.user) if event.args.user.isdigit() else event.args.user

    try:
        full_user = await event.client(GetFullUserRequest(user_id_or_name))
    except (UserIdInvalidError, ValueError):
        await event.edit("I don't seem to find this user by: " + str(user_id_or_name) + "!")
        return
    except TypeError:
        await event.edit("<code>{}</code> it's not a valid user!".format(str(user_id_or_name)))
        return

    is_self = full_user.user.is_self
    first_name = full_user.user.first_name
    last_name = full_user.user.last_name
    username = full_user.user.username
    user_id = str(full_user.user.id)
    profile_photo = full_user.profile_photo
    about = full_user.about
    common_chats = full_user.common_chats_count
    cas_banned = None
    async with aiohttp.ClientSession() as session:
        async with session.get('https://combot.org/api/cas/check?user_id=' + str(user_id)) as request:
            if request.status == 200:
                res = json.loads(await request.read())
                user_banned = res.get('ok')
                result = res.get('result')
                if user_banned is True:
                    cas_banned = '<a href=\"https://combot.org/cas/query?u={}\">Yes!</a>'.format(user_id)
                elif user_banned is False:
                    cas_banned = '<a href=\"https://combot.org/cas/query?u={}\">No!</a>'.format(user_id)
                else:
                    cas_banned = 'Not available!'
            else:
                cas_banned = 'Not available!'


    INFO = "<b>User Info:\n</b>"

    if first_name:
        INFO += "\nFirst Name: " + escape(first_name)
    if last_name:
        INFO += "\nLast Name: " + escape(last_name)
    if username:
        INFO += "\nUsername: " + escape(username)

    INFO += "\nUserID: " + user_id
    INFO += "\nPermanent user link: <a href=\"tg://user?id={}\">link</a>".format(
        user_id)
    INFO += "\nCAS Banned: " + cas_banned

    if about:
        INFO += "\nAbout User: " + escape(about)

    if not is_self:
        INFO += "\nI have <code>{}</code> chats in common with this user.".format(
            common_chats)

    await event.client.send_message(event.input_chat, INFO, reply_to=message.id, file=profile_photo, parse_mode='html')
    await event.delete()


@CommandHandler(command="admins", parse_mode="html")
async def chat_admins(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Get all the admins from a chat!</i>
    """
    admins = "<b>Admins in this chat:</b>\n"
    async for admin in event.client.iter_participants(await event.get_input_chat(), filter=ChannelParticipantsAdmins):
        if not admin.deleted:
            admins += "\n{}<a href=\"tg://user?id={}\">{}</a>".format(
                "🤖" if admin.bot else "👤", admin.id, escape(
                    admin.username or admin.first_name))

    await event.edit(admins, parse_mode='html')


@CommandHandler(command='readall')
async def readall(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Marks all the unread messages as read!</i>
    """
    await event.edit("Marking all the unread messages as read.. Please wait...")
    async for dialog in event.client.iter_dialogs(limit=None):
        await event.client.send_read_acknowledge(dialog, clear_mentions=True)
    await event.edit("Yay. All the messages are marked as read")


@CommandHandler(command='disconnect')
async def disconnect(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Disconnects the companion from Telegram.</i>
    """
    await event.edit("Thanks for using Telegram Companion. Goodbye!")
    await event.client.disconnect()

@CommandHandler(command='logout')
async def logout(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Logs out the companion from Telegram and deletes the session.</i>
    """
    await event.edit("Thanks for using Telegram Companion. Logging out.. Goodbye!")
    await event.client.log_out()



@CommandHandler(command='mute', args=['date'])
async def mute_chat(event):
    """
    <b>param:</b> <code>the date untill the chat will be muted in format [x]d[x]h[x]m[x]s</code>
    <b>return:</b> <i>Mutes a chat for a given time!</i>
    """
    str_time = event.args.date
    if not str_time:
        await event.reply('Invalid time!')
    else:
        pattern = r'\d*d|\d*h|\d*m|\d*s'
        findall = re.findall(pattern, str_time)
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        if not findall:
            await event.reply('Invalid time!')
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
            after = now + datetime.timedelta(days=int(days),
                                             hours=int(hours),
                                             minutes=int(minutes),
                                             seconds=int(seconds))
            mute_for = await event.client(UpdateNotifySettingsRequest(peer=event.chat_id,
                                                                      settings=InputPeerNotifySettings(
                                                                              show_previews=False,
                                                                              mute_until=datetime.datetime.timestamp(after))))
            if mute_for:
                await event.edit(f"Chat muted until: {after.strftime('%c %z')}")
            else:
                await event.edit("Failed to mute this chat!")