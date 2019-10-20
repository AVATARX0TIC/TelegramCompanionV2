from telethon import events
from companion import client
from companion.modules.sql import private_locks_sql as sql
from companion.utils import CommandHandler, sql_only
from companion.utils.helpers.messages import get_message_type


@CommandHandler(command="lock", args=["type"], parse_mode="html")
@sql_only(reply=True)
async def lock(event):
    type = event.args.type
    lockables = sql.get_restrictions()
    if type in lockables:
        if lockables.get(type) is False:
            sql.update_restriction(type, True)
            await event.edit("Locked <code>{}</code>".format(type), parse_mode='html')
        else:
            await event.edit("<code>{}</code> messages are already locked".format(type), parse_mode='html')
    else:
        await event.edit("What are you trying to lock?")


@CommandHandler(command="unlock", args=["type"], parse_mode="html")
@sql_only(reply=True)
async def unlock(event):
    """
    <b>param:</b> <code>type</code>
    <b>return:</b> <i>Locks messages of certain types (available only in private)</i>
    """
    type = event.args.type
    lockables = sql.get_restrictions()
    if type in lockables:
        if lockables.get(type) is True:
            sql.update_restriction(type, False)
            await event.edit("Unlocked <code>{}</code>".format(type), parse_mode='html')
        else:
            await event.edit("<code>{}</code> messages are already unlocked".format(type), parse_mode='html')
    else:
        await event.edit("What are you trying to unlock?")

@client.on(
    events.NewMessage(
        incoming=True,
        func=lambda e: e.is_private and not e.out))
@sql_only(reply=False)
async def delete_lock(event):
    """
    <b>param:</b> <code>type</code>
    <b>return:</b> <i>Un-Locks messages of certain types (avaiable only in private)</i>
    """
    types = sql.get_restrictions()
    if bool(types.get(get_message_type(event.message))) is True:
        await event.delete()


@CommandHandler(command="locks", parse_mode="html")
async def locktypes(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Returns a list with all of the possible locktypes</i>
    """
    await event.edit("LockTypes:\n- " + " \n- ".join(sorted(list(sql.get_restrictions()))), parse_mode='html')
