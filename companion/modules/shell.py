import asyncio
import os

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

    await event.edit(RESULT, parse_mode='html')


@CommandHandler(command='upload', args=['path'])
async def upload(event):
    """
    <b>param:</b> <code>path</code>
    <b>return:</b> <i>Uploaded File</i>
    """
    path = event.args.path
    if not path:
        await event.edit('Invalid or missing file path!')
    else:
        if os.path.isfile(path):
            if os.path.getsize(path) >= 1500000000:
                await event.edit('Selected file is too big. Max 1.5GB')
            else:
                f_name = os.path.basename(path)

                size = os.path.getsize(path)
                power = 2**10
                n = 0
                units = {
                0: '',
                1: 'kilobytes',
                2: 'megabytes',
                3: 'gigabytes',
                4: 'terabytes'}
                while size > power:
                    size /= power
                    n += 1
                await event.edit(f"**Uploading**:\n\n" \
                        f"  __File Name:__ `{f_name}`\n" \
                        f"  __Size__: `{round(size, 2)}` {units[n]}\n", parse_mode='md')
                await event.client.send_file(await event.get_chat(), path, file_name=f_name, force_document=True, progress_callback=None)
                await event.delete()

        else:
            await event.edit('Invalid or missing file path!')
