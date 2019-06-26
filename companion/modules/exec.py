import html
import io
import sys

from telethon.tl import types

from companion.utils import CommandHandler


async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)


@CommandHandler(command="exec", args=['code'], parse_mode="html")
async def execute(event):
    """
    <b>param:</b> <code>code</code>
    <b>return:</b> <i>Python compiled code</i>
    """

    if event.is_reply:
        rep_msg = await event.get_reply_message()
        code_entities = rep_msg.get_entities_text(types.MessageEntityCode)
        if code_entities:
            ent, code = code_entities[0]
        else:
            code = event.args.code
    else:
        code = event.args.code
    if not code:
        await event.edit(STATUS.format("None", "No code given!"))
        return

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(code, event)
    except Exception:
        import traceback
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        RESULT = EXCEPTION.format(html.escape(code), html.escape(exc))

    elif stderr:
        RESULT = STDERR.format(html.escape(code), html.escape(stderr))

    elif stdout:
        RESULT = STDOUT.format(html.escape(code), html.escape(stdout))
    else:
        RESULT = STATUS.format(html.escape(code), "Success")

    if len(RESULT) > MAX_TEXT_LEN:

        await event.edit(STATUS.format(code, "Output too long!"))
        return

    await event.edit(RESULT)
