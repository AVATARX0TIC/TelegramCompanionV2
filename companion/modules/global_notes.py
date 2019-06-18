from telethon.tl.types import (InputDocument, InputPhoto,
                               MessageMediaPhoto, MessageMediaWebPage)

from companion.modules.sql import global_notes_sql as sql
from companion.utils import CommandHandler


@CommandHandler(
    command="save",
    args=[
        "notename",
        "content"],
    parse_mode="md")
async def save(event):
    """
    <b>param:</b> <code>notename, content</code> - <i>The content argument is required only if you don't reply to a message.</i>
    <b>return:</b> <i>Globally save a note.</i>
    """
    if event.args.notename:
        if event.is_reply:
            msg = await event.get_reply_message()
            content = msg.text
        else:
            if not event.args.content:
                await event.edit("There's nothing to save!")
            else:
                msg = event.message
                content = event.args.content
        if msg.document:
            file_id = msg.document.id
            access_hash = msg.document.access_hash
            file_reference = msg.document.file_reference
            is_document = True
        elif msg.media:
            if isinstance(msg.media, MessageMediaPhoto):
                file_id = msg.media.photo.id
                access_hash = msg.media.photo.access_hash
                file_reference = msg.media.photo.file_reference
                is_document = False
            elif isinstance(msg.media, MessageMediaWebPage):
                file_id = None
                access_hash = None
                file_reference = None
                is_document = None
            else:
                await event.edit("Can't save this message! Invalid media type!")
        else:
            file_id = None
            access_hash = None
            file_reference = None
            is_document = None
        sql.insert_note(
            event.args.notename,
            content,
            is_document,
            access_hash,
            file_id,
            file_reference)
        await event.reply("Note <code>{}</code> saved! get it with `get {}`".format(event.args.notename, event.args.notename))
    else:
        await event.edit("There's no note name given!")


@CommandHandler(command="get", args=["notename"], parse_mode="md")
async def get(event):
    """
    <b>param:</b> <code>notename</code>
    <b>return:</b> <i>Gets a note by name and returns note's content!</i>
    """
    if event.args.notename:
        note = sql.get_note(event.args.notename)
        if note:
            if note.file_id:
                if note.file_document:
                    file = InputDocument(
                        id=note.file_id,
                        access_hash=note.access_hash,
                        file_reference=note.file_reference)
                else:
                    file = InputPhoto(
                        id=note.file_id,
                        access_hash=note.access_hash,
                        file_reference=note.file_reference)
            else:
                file = None
            await event.client.send_message(await event.get_input_chat(),
                                            message=note.content, file=file, reply_to=event.message)
        else:
            await event.edit("There's no note named `{}`".format(event.args.notename))
    else:
        await event.edit("I can't find any notes with that!")


@CommandHandler(command="rmnote", args=["notename"], parse_mode="html")
async def rmnote(event):
    """
    <b>param:</b> <code>notename</code>
    <b>return:</b> <i>Removes a note from a database!</i>
    """
    if event.args.notename:
        to_remove = sql.rem_note(event.args.notename)
        if to_remove is True:
            await event.edit("Successfully removed <cde>{}</code>".format(event.args.notename))
        else:
            await event.edit("There's no note with that name!")
    else:
        await event.edit("You have to give me a note name to remove!")


@CommandHandler(command="getnotes", parse_mode="html")
async def getnotes(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Returns all the notes saved in the database!</i>
    """
    notes = "<b>Globally saved notes:</b>\n\n"
    for note in sql.get_all_notes():
        notes += "\n- <code>{}</code>".format(note)
    await event.reply(notes)