from functools import wraps

def admins_only(f):
    @wraps(f)
    async def wrapper(event):
        if not event.is_private:
            chat = await event.get_chat()
            if chat.creator or chat.admin_rights:
                chat_creator = chat.creator
                chat_admin_rights = chat.admin_rights
                return await f(event, chat, chat_creator, chat_admin_rights)
            else:
                await event.reply("This command was made for chat admins only!")
        else:
            chat = await event.get_chat()
            chat_creator = True
            chat_admin_rights = PrivateAdminRights()
            return await f(event, chat, chat_creator, chat_admin_rights)
    return wrapper

class PrivateAdminRights:
    def __init__(self):
        self.change_info = True
        self.post_messages = True
        self.edit_messages = True
        self.delete_messages = True
        self.ban_users = True
        self.invite_users = True
        self.pin_messages = True
        self.add_admins = True