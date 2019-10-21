import datetime
import json
import os
from io import BytesIO

import aiohttp
from telethon import events
from telethon.tl.types import InputPeerSelf
from tzlocal import get_localzone

from companion import client

CAS = os.environ.get('CAS_BANS', None)

@client.on(events.ChatAction())
async def combot(event):
    path = 'https://combot.org/api/cas/check?user_id='
    user = await event.get_user()
    if CAS:
        if event.user_added or event.user_joined:
            if not isinstance(user, InputPeerSelf):
                async with aiohttp.ClientSession() as session:
                    async with session.get(path + str(user.id)) as request:
                        if request.status == 200:
                            res = json.loads(await request.read())
                            user_banned = res.get('ok')
                            result = res.get('result')
                            offenses = None
                            date = None
                            messages = None
                            messages_file = ''
                            if user_banned:
                                if result:
                                    offenses = result.get('offenses')
                                    messages = result.get('messages')
                                    date = result.get('time_added')
                                    if date:
                                        tz = get_localzone()
                                        date = datetime.datetime.fromtimestamp(
                                            int(date))
                                        date = tz.localize(
                                            date).strftime('%c %Z')

                                if messages:
                                    for message in messages:
                                        messages_file += '{}\n\n'.format(
                                            message)
                                    with BytesIO(str.encode(messages_file)) as output:
                                        output.name = 'spam_messages.txt'

                                        await event.reply('**Potential spam thread!**'
                                                          f'\n**Banned**: `{date}`'
                                                          f'\n**Registered offenses**: {offenses}'
                                                          f'\n**Source**: [Combot CAS Bans](https://combot.org/cas/query?u={user.id})', file=output, parse_mode='md')
                                else:
                                    await event.reply('**Potential spam thread!**'
                                                      f'\n**Banned**: `{date}`'
                                                      f'\n**Registered offenses**: `{offenses}`'
                                                      f'\n**Source**: [Combot CAS Bans](https://combot.org/cas/query?u={user.id})', parse_mode='md')
