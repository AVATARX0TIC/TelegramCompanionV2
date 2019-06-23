import importlib
import aiohttp
import time

from companion import CMD_HELP, MAX_TEXT_LEN, client, __version__
from companion.modules import get_modules
from companion.plugins import get_plugins
from companion.utils import CommandHandler

for module in get_modules():
    importlib.import_module("companion.modules." + module)

for plugin in get_plugins():
    importlib.import_module("companion.plugins." + plugin)


@CommandHandler("start", parse_mode="html")
async def start(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Replies to tell you that your userbot is running</i>
    """
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.google.com"):
            end_time = time.time()
            ping_time = float(end_time - start_time) * 1000

    companion_version = __version__
    python_version = __import__("platform").python_version()
    telethon_version = __import__("telethon").__version__

    await event.edit("Telegram Companion is up and running!\n"
					  "<i>Companion</i>(<b>{}</b>), <i>Python</i>(<b>{}</b>), <i>Telethon</i>(<b>{}</b>), <i>PingTime</i>(<b>{}ms</b>)".format(companion_version, python_version, telethon_version, round(ping_time, 2)))


@CommandHandler("help", args=["command"], parse_mode="html")
async def help(event):
    """
    <b>param:</b> <code>(optional) command</code>
    <b>return:</b> <i>The all available commands and their help or a specific command if an argument is given</i>
    """
    parts = 0
    saved_keys = []

    get_help_for = event.args.command

    if get_help_for:
        if get_help_for in CMD_HELP:
            cmd_help = CMD_HELP.get(get_help_for)
            if cmd_help:
                await client.reply("Here is the help for the `{}` command:\n".format(get_help_for) + cmd_help)
            else:
                await client.reply("There's no help available for `{}`".format(get_help_for))
        else:
            await client.reply("There's no `{}` command available".format(get_help_for))
        return

    if not event.is_private:
        await event.reply("Use this command in PM for help!")
        return

    OUTPUT = ""
    parts = 1

    for k, v in sorted(CMD_HELP.items()):
        OUTPUT += "{}: {}\n".format(k, v)
        saved_keys.append(k)
        if len(OUTPUT) >= MAX_TEXT_LEN - 500:
            parts += 1
            await event.reply("Here are all the commands you can use. Part {}: \n\n{}".format(parts, OUTPUT))
            OUTPUT = ""

    if OUTPUT:
        await event.reply("Here are all the commands you can use: \n\n{}".format(OUTPUT))



if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
