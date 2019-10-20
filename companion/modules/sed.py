import re

from companion.utils import CommandHandler

FLAGS = {
    "i": re.I,
    "l": re.L,
    "m": re.M,
    "s": re.S,
    "a": re.A,
    "x": re.X
}


@CommandHandler(
    command="sed/",
    prefix=None,
    args=[
        "to_replace",
        "replace_with",
        "flag"],
    args_delimiter="/",
    parse_mode="md")
async def sed(event):
    """
    <b>param:</b> <code>to_replace/replace_with/optional_flag or times to replace in string</code>
    <b>return:</b> <i>Sed like text replacement</i>
    """

    if not event.is_reply:
        await event.edit("Reply to a text to use sed!")
        return

    regex_cmd = r"\/((?:\\\/|[^\/])+)\/((?:\\\/|[^\/])*)(?:\/(.*))?"
    regex_group = re.search(regex_cmd, event.text)
    group_len = 0
    args = event.args
    to_replace = args.to_replace
    replace_with = args.replace_with
    flag = args.flag

    if not to_replace or not replace_with:
        await event.edit("Invalid sed format!")
        return

    for group in regex_group.groups():
        if group:
            group_len += 1

    if group_len < 2:
        await event.edit("Invalid sed format!")
        return

    rep_msg = await event.get_reply_message()
    text = re.sub("^「sed」\n", "", rep_msg.text)

    replacement = replace_with.replace('\\/', '/')
    flags = 0
    count = 1

    if args.flag:
        for flag in args.flag:
            if flag == "g":
                count = 0
            elif flag.lower() in "ilmsax":
                flags |= FLAGS[flag.lower()]
            else:
                await event.edit("Unknown flag: <code>{}</code>".format(regex_group.group(3)), parse_mode='html')
                return

    final_text = re.sub(
        to_replace,
        replacement,
        text,
        count=count,
        flags=flags)
    await event.edit("「sed」\n" + final_text)
