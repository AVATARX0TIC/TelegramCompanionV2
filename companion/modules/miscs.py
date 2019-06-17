from companion.utils import CommandHandler
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import UserIdInvalidError
from html import escape


@CommandHandler(command="info", args=["user"], parse_mode="html")
async def user_info(event):
        """
            <b>param:</b> <code>(optional if reply) user id or username</code>
            <b>return:</b> <i>User's info</i>
        """

        if event.is_reply:
            message = await event.get_reply_message()
            user_id_or_name = message.from_id
        elif not event.args.user:
            message = event.message
            user_id_or_name = message.from_id
        else:
            message = event.message
            user_id_or_name = int(event.args.user) if event.args.user.isdigit() else event.args.user

        try:
            full_user = await event.client(GetFullUserRequest(user_id_or_name))
        except UserIdInvalidError:
            await event.edit("I don't seem to find this user by" + user_id_or_name + "!")
            return
        except TypeError:
            await event.edit("<code>{}</code> it's not a valid user!".format(str(user_id_or_name)))
            return

        is_self = full_user.user.is_self
        first_name = full_user.user.first_name
        last_name = full_user.user.last_name
        username = full_user.user.username
        user_id = str(full_user.user.id)
        profile_photo = full_user.profile_photo
        about = full_user.about
        common_chats = full_user.common_chats_count


        INFO = "<b>User Info:\n</b>"

        if first_name:
            INFO += "\nFirst Name: " + escape(first_name)
        if last_name:
            INFO += "\nLast Name: " + escape(last_name)
        if username:
            INFO += "\nUsername: " + escape(username)

        INFO += "\nUserID: " + user_id
        INFO += "\nPermanent user link: <a href=\"tg://user?id={}\">link</a>".format(user_id)

        if about:
            INFO += "\nAbout User: " + escape(about)

        if not is_self:
            INFO += "\nI have <code>{}</code> chats in common with this user.".format(common_chats)

        await event.client.send_message(event.input_chat, INFO, reply_to=message.id, file=profile_photo)
        await event.delete()


@CommandHandler(command="admins", parse_mode="html")
async def chat_admins(event):
    """
    <b>param:</b> <code>None</code>
    <b>return:</b> <i>Get all the admins from a chat!</i>
    """
    admins = "<b>Admins in this chat:</b>\n"
    async for admin in event.client.iter_participants(await event.get_input_chat(), filter=ChannelParticipantsAdmins):
        if not admin.deleted:
            admins += "\n<a href=\"tg://user?id={}\">{}</a> - {}".format(admin.id, admin.username or admin.first_name, "🤖" if admin.bot else "👤")

    await event.edit(admins)