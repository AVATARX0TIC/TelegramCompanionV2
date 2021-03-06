import datetime
from tzlocal import get_localzone
import re
from io import BytesIO
from companion.utils import CommandHandler
from telethon.tl.functions.messages import GetScheduledHistoryRequest


@CommandHandler(command='remind', args=['date', 'message'])
async def remind(event):
    """
    <b>param:</b> <code>the date to which the message will be scheduled in format [x]d[x]h[x]m[x]s</code>
    <b>param:</b> <code>the message will be scheduled. Ignore if it's reply</code>
    <b>return:</b> <i>Scheduled message at a specific time to chat</i>
    """
    str_time = event.args.date
    tz = get_localzone()
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

            message = event.args.message
            if not event.is_reply:
                if message:
                    to_sched = message
                else:
                    await event.reply('Missing message to schedule!')
                    return
            else:
                to_sched = await event.get_reply_message()
            if isinstance(to_sched, str):
                await event.client.send_message(await event.get_chat(), to_sched, schedule=datetime.datetime.timestamp(after))
            else:
                await to_sched.forward_to(await event.get_chat(), schedule=datetime.datetime.timestamp(after))
            await event.reply('Scheduled message to this chat for {}!'.format(tz.localize(after).strftime('%c %Z')))


@CommandHandler(command='remindme', args=['date', 'message'])
async def remindme(event):
    """
    <b>param:</b> <code>the date to which the message will be scheduled in format [x]d[x]h[x]m[x]s</code>
    <b>param:</b> <code>the message will be scheduled. Ignore if it's reply</code>
    <b>return:</b> <i>Scheduled message at a specific time to yourself</i>
    """
    str_time = event.args.date
    tz = get_localzone()
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

            message = event.args.message
            if not event.is_reply:
                if message:
                    to_sched = message
                else:
                    await event.reply('Missing message to schedule!')
                    return
            else:
                to_sched = await event.get_reply_message()

            if isinstance(to_sched, str):
                await event.client.send_message('me', to_sched, schedule=datetime.datetime.timestamp(after))
            else:
                await to_sched.forward_to('me', schedule=datetime.datetime.timestamp(after))
            await event.reply('Scheduled message to myself for {}!'.format(tz.localize(after).strftime('%c %Z')))



@CommandHandler(command='reminders')
async def get_reminders(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>get all reminders from a chat in UTC timezone.</i>
    """
    scheduled = await event.client(GetScheduledHistoryRequest(peer=await event.get_chat(), hash=0))
    sched_file = ''
    tz = get_localzone()
    if not scheduled.messages:
        await event.edit('There are no reminders in this chat!')
    else:
        for message in scheduled.messages:
            date = message.date.astimezone(tz)
            sched_file += '\n{}\n-------\n\n{}\n\n-------\n\n'.format(date.strftime('%c %Z'), message.message or 'MessageWIthNoText')
        with BytesIO(str.encode(sched_file)) as output:
            output.name = 'scheduled.txt'
            await event.reply(file=output)
