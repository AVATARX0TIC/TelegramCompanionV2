from telethon import events
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.types import InputPeerSelf, InputUserSelf

from companion import client
from companion.env_vars import ANTI_SPAM
from companion.modules.sql import private_messages_sql as sql
from companion.utils import CommandHandler, sql_only

WARNS = {}


@client.on(events.NewMessage(outgoing=True, incoming=False))
@sql_only()
async def approve_pm(event):
    if event.is_private and ANTI_SPAM:
        input_chat = await event.get_input_chat()
        if not isinstance(input_chat, InputPeerSelf):
            if str(input_chat.user_id) not in sql.ALLOWED_USERS:
                sql.insert_in_pm(input_chat.user_id)
                await event.reply("Allowed private messages from this user")


@CommandHandler(incoming=True, parse_mode="md")
@sql_only(reply=False)
async def await_approve(event):
    global WARNS
    if event.is_private and ANTI_SPAM:
        chat = await event.get_chat()
        if str(chat.id) not in sql.ALLOWED_USERS:
            if not isinstance(chat, InputUserSelf):
                if not chat.is_self or not chat.bot or not chat.verified:
                    if chat.id not in WARNS:
                        WARNS.update({chat.id: 1})
                    if WARNS[event.chat.id] == 3:
                        await event.reply(
                            "You are spamming this user's inbox! You are now restricted from sending any messages to him!")
                        await event.client(BlockRequest(chat.id))
                        WARNS[chat.id] = 1
                    else:
                        if not event.message.text.startswith("⚠️⚠️⚠️⚠️:\n"):
                            await event.reply("⚠️⚠️⚠️⚠️:\n" + sql.get_pm_msg())
                        WARNS[chat.id] += 1
                else:
                    await sql.insert_in_pm(chat.id)


@CommandHandler(command="setpm", args=["message"])
@sql_only
async def set_custom_msg(event):
    """
    <b>param:</b> <code>message</code>
    <b>return:</b> <i>Sets a custom message for the pm antispam module.</i>
    """
    if event.args.message:
        sql.set_custom_msg(str(event.args.message))
        await event.reply("New Custom PM message has been added!")
    else:
        await event.reply("You need to give me a message to send to users!")


@CommandHandler(command="clearpm")
@sql_only
async def set_custom_msg(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Clears the custom message for the pm antispam module.</i>
    """
    sql.clear_custom_msg()
    await event.reply("Cleared all custom messages!!")
