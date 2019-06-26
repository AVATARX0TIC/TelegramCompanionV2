import asyncio

from companion import MAX_TEXT_LEN, STATUS, STDERR, STDOUT
from companion.utils import CommandHandler


@CommandHandler(command="sh", args=['command'], parse_mode="html")
async def terminal(event):
    """
    <b>param:</b> <code>shell command</code>
    <b>return:</b> <i>Terminal compiled code</i>
    """

    cmd = event.args.command
    if not cmd:
        await event.edit(STATUS.format("None", "No command given!"))
        return

    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await event.edit("Connecting to PID: <code>{}</code>".format(process.pid))

    stdout, stderr = await process.communicate()

    if stderr.decode():
        RESULT = STDERR.format(cmd, stderr.decode())

    elif stdout.decode():
        RESULT = STDOUT.format(cmd, stdout.decode())

    else:
        RESULT = STATUS.format(cmd, "Success!")

    if len(RESULT) > MAX_TEXT_LEN:
        await event.edit(STATUS.format(cmd, "Output too long!"))
        return

    await event.edit(RESULT)
