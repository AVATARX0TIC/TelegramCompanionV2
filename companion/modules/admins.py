from companion.utils import CommandHandler, admins_only

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (ChannelParticipantBanned, ChatBannedRights, ChannelParticipantSelf, ChannelParticipantAdmin, ChannelParticipantCreator, User)
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
import datetime


@CommandHandler(command="ban", args=["user"], private_lock=True, parse_mode='html')
@admins_only
async def ban(event, chat, chat_creator, chat_admin):
    """
    <b>param:</b> <code>(required if not reply) user</code>
    <b>return:</b> <i>Bans an user in the chat!</i>
    """
    if chat_creator or chat_admin.can_ban:
        if event.is_reply:
            rep_msg = await event.get_reply_message()
            to_ban = rep_msg.from_id
        elif event.args.user:
            to_ban = event.args.user
        else:
            await event.reply("There's no user to ban!")
            return
        try:
            ent = await event.client.get_entity(to_ban)
        except Exception:
            await event.reply("I don't seem to find this user")
            return
        if isinstance(ent, User):
            try:
                chat_participant = await event.client(GetParticipantRequest(chat, ent.id))
            except UserNotParticipantError:
                await event.reply("This user is not a participant of this chat!")
                return
            if isinstance(chat_participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                await event.reply("I can't ban chat admins!")
            elif isinstance(chat_participant.participant, ChannelParticipantBanned):
                await event.reply("This user has already been restricted in this chat!")
            elif isinstance(chat_participant.participant, ChannelParticipantSelf):
                await event.reply("You can't ban yourself!")
            else:
                await event.client(EditBannedRequest(chat, ent.id, ChatBannedRights(until_date=None,
                                                                      view_messages=True)))
                await event.reply("Banned <code>{}</code>".format(ent.username or ent.first_name))
    else:
        await event.reply("You don't have the rights to restrict users here!")


@CommandHandler(command="unban", args=["user"], private_lock=True, parse_mode='html')
@admins_only
async def unban(event, chat, chat_creator, chat_admin):
    """
    <b>param:</b> <code>(required if not reply) user</code>
    <b>return:</b> <i>Un-Bans an user in the chat!</i>
    """
    if chat_creator or chat_admin.can_ban:
        if event.is_reply:
            rep_msg = await event.get_reply_message()
            to_ban = rep_msg.from_id
        elif event.args.user:
            to_ban = event.args.user
        else:
            await event.reply("There's no user to unban!")
            return
        try:
            ent = await event.client.get_entity(to_ban)
        except Exception:
            await event.reply("I don't seem to find this user")
            return
        if isinstance(ent, User):
            try:
                chat_participant = await event.client(GetParticipantRequest(chat, ent.id))
            except UserNotParticipantError:
                await event.reply("This user is not a participant of this chat!")
                return
            if isinstance(chat_participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                await event.reply("I can't unban chat admins because they can't be banned!")
            elif not isinstance(chat_participant.participant, ChannelParticipantBanned):
                await event.reply("This user isn't banned in this chat!")
            elif isinstance(chat_participant.participant, ChannelParticipantSelf):
                await event.reply("You can't unban yourself!")
            else:
                print(chat_participant.participant)
                await event.client(EditBannedRequest(chat, ent.id, ChatBannedRights(until_date=None,
                                                                      view_messages=None)))
                await event.reply("Un-Banned <code>{}</code>".format(ent.username or ent.first_name))
    else:
        await event.reply("You don't have the rights to restrict users here!")

@CommandHandler(command="kick", args=["user"], private_lock=True, parse_mode='html')
@admins_only
async def kick(event, chat, chat_creator, chat_admin):
    """
    <b>param:</b> <code>(required if not reply) user</code>
    <b>return:</b> <i>Kicks an user in the chat!</i>
    """
    if chat_creator or chat_admin.can_ban:
        if event.is_reply:
            rep_msg = await event.get_reply_message()
            to_ban = rep_msg.from_id
        elif event.args.user:
            to_ban = event.args.user
        else:
            await event.reply("There's no user to kick!")
            return
        try:
            ent = await event.client.get_entity(to_ban)
        except Exception:
            await event.reply("I don't seem to find this user")
            return
        if isinstance(ent, User):
            try:
                chat_participant = await event.client(GetParticipantRequest(chat, ent.id))
            except UserNotParticipantError:
                await event.reply("This user is not a participant of this chat!")
                return
            if isinstance(chat_participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                await event.reply("I can't kick chat admins!")
            elif isinstance(chat_participant.participant, ChannelParticipantBanned):
                await event.reply("This user has already been restricted in this chat!")
            elif isinstance(chat_participant.participant, ChannelParticipantSelf):
                await event.reply("You can't kick yourself!")
            else:
                print(chat_participant.participant)
                await event.client(EditBannedRequest(chat, ent.id, ChatBannedRights(until_date=datetime.timedelta(seconds=1),
                                                                      view_messages=None)))
                await event.reply("Kicked <code>{}</code>".format(ent.username or ent.first_name))
    else:
        await event.reply("You don't have the rights to restrict users here!")

@CommandHandler(command="pin", args=["loud"], private_lock=True, parse_mode='html')
@admins_only
async def pin(event, chat, chat_creator, chat_admin):
    """
    <b>param:</b> <code>loud</code> - <i>Set to anything to notify all members</i>
    <b>return:</b> <i>Pins a message in the chat!</i>
    """
    if event.is_reply:
        if chat_creator or chat_admin.can_pin:
            await (await event.get_reply_message()).pin()
        else:
            await event.reply("You don't have the rights to pin messages here!")
    else:
        await event.reply("Please reply to a message to pin it!")