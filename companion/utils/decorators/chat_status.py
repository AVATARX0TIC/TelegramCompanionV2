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
    return wrapper