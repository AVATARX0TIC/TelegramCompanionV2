
from functools import wraps

from companion.env_vars import DB_URI


def sql_only(reply=True):
    def _sql_only(f):
        @wraps(f)
        async def wrapper(event=None, *args, **kwargs):
            if not DB_URI:
                if reply is True:
                    await event.reply("Running on Non-SQL Mode!")
                return
            else:
                return await f(event, *args, **kwargs)
        return wrapper
    return _sql_only
