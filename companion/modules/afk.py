import datetime

from telethon.events import StopPropagation
from telethon.tl.functions.account import GetPrivacyRequest
from telethon.tl.types import (InputPrivacyKeyStatusTimestamp,
                               PrivacyValueAllowAll)

from companion.utils import CommandHandler

IS_AFK, AFK_REASON = None, None
AFK_TIME = None

intervals = (
    ('weeks', 604800),
    ('days', 86400),
    ('hours', 3600),
    ('minutes', 60),
    ('seconds', 1),
)


@CommandHandler(
    command="afk",
    args=["reason"],
    parse_mode="html",
    func=lambda x: not AFK_REASON)
async def set_afk(event):
    global IS_AFK
    global AFK_TIME
    global AFK_REASON

    last_seen_status = await event.client(GetPrivacyRequest(InputPrivacyKeyStatusTimestamp()))
    for rule in last_seen_status.rules:
        if isinstance(rule, PrivacyValueAllowAll):
            AFK_TIME = datetime.datetime.now()
        IS_AFK = True
    if event.args.reason:
        AFK_REASON = event.args.reason

    await event.edit("<b>I will be afk for a while!</b>" + "\n<i>Reason:</i> {}".format(AFK_REASON) if AFK_REASON else "<b>I will be afk for a while!</b>", parse_mode='html')
    raise StopPropagation


@CommandHandler(command=None, func=lambda x: IS_AFK, parse_mode='html')
async def unset_afk(event):
    global IS_AFK
    global AFK_REASON
    IS_AFK, AFK_REASON = None, None

    await event.client.send_message(event.input_chat, "<b>I'm no longer afk!</b>", parse_mode='html')


def __afk_lock(event):
    if IS_AFK is True:
        if event.mentioned or event.is_private:
            return True
    return


@CommandHandler(command=None, incoming=True, func=__afk_lock, parse_mode='md')
async def afk(event):
    if AFK_TIME:
        now = datetime.datetime.now()

        dt = now - AFK_TIME
        time = float(dt.seconds)
        days = time // (24 * 3600)
        time = time % (24 * 3600)
        hours = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time

        if days == 1:
            afk_since = "**Yesterday**"
        elif days > 1:
            if days > 6:
                date = now + \
                    datetime.timedelta(days=-days, hours=-hours, minutes=-minutes)
                afk_since = date.strftime('%A, %Y %B %m, %H:%I')
            else:
                wday = now + datetime.timedelta(days=-days)
                afk_since = wday.strftime('%A')
        elif hours > 1:
            afk_since = "`{}h{}m` **ago**".format(int(hours), int(minutes))
        elif minutes > 0:
            afk_since = "`{}m{}s` **ago**".format(int(minutes), int(seconds))
        else:
            afk_since = "`{}s` **ago**".format(int(seconds))
    else:
        afk_since = "`a while ago!`"

    if not AFK_REASON:
        afk_msg = "I'm afk since {} and I will be back soon!".format(afk_since)
    else:
        afk_msg = "I'm afk since {} \n**Reason:** {}".format(
            afk_since, AFK_REASON)

    if not event.text.startswith("I'm afk since"):
        await event.reply(afk_msg, parse_mode='md')
