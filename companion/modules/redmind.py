from companion.utils import CommandHandler
import datetime
import re


@CommandHandler(command='remind', args=['date', 'message'])
async def remind(event):
    str_time = event.args.date
    if not str_time:
        await event.reply('Invalid time!')
    else:
        pattern = '\d*d|\d*h|\d*m|\d*s'
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
            after = now + datetime.timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))

            message = event.args.message
            if not event.is_reply:
                if message:
                    to_sched = event.message
                else:
                    await event.reply('Missing message to schedule!')
                    return
            else:
                to_sched = await event.get_reply_message()

            await to_sched.forward_to(await event.get_chat(), schedule=datetime.datetime.timestamp(after))
            await event.reply('Scheduled message for {}!'.format(after.strftime('%d, %b, %H:%M, %Y')))

@CommandHandler(command='remindme', args=['date', 'message'])
async def remindme(event):
    str_time = event.args.date
    if not str_time:
        await event.reply('Invalid time!')
    else:
        pattern = '\d*d|\d*h|\d*m|\d*s'
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
            after = now + datetime.timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))

            message = event.args.message
            if not event.is_reply:
                if message:
                    to_sched = event.message.split(None, 1)[1]
                else:
                    await event.reply('Missing message to schedule!')
                    return
            else:
                to_sched = await event.get_reply_message()

            await to_sched.forward_to('me', schedule=datetime.datetime.timestamp(after))
            await event.reply('Scheduled message for {}!'.format(after.strftime('%d, %b, %H:%M, %Y')))