import sqlalchemy as sa

from companion.env_vars import DB_URI

from . import connection, engine

metadata = sa.MetaData()

pm_tbl = sa.Table('pm', metadata,
                  sa.Column('chat_id', sa.String()))

pm_msg_tbl = sa.Table('pm_message', metadata,
                      sa.Column('message', sa.String()))

if DB_URI:
    metadata.create_all(
        bind=engine,
        tables=[
            pm_tbl,
            pm_msg_tbl],
        checkfirst=True)

ALLOWED_USERS = []
CUSTOM_MSG = None


def insert_in_pm(chat_id):
    global ALLOWED_USERS
    if str(chat_id) not in ALLOWED_USERS:
        query = sa.insert(pm_tbl).values(chat_id=str(chat_id))
        connection.execute(query)
        ALLOWED_USERS.append(str(chat_id))


def set_custom_msg(message):
    global CUSTOM_MSG
    if not CUSTOM_MSG:
        query = sa.insert(pm_msg_tbl).values(message=str(message))
        connection.execute(query)
    else:
        query = sa.update(pm_msg_tbl).values(message=str(message))
        connection.execute(query)
    CUSTOM_MSG = str(message)


def clear_custom_msg():
    global CUSTOM_MSG
    if CUSTOM_MSG:
        query = sa.delete(pm_msg_tbl)
        connection.execute(query)
        CUSTOM_MSG = None


def get_pm_msg():
    global CUSTOM_MSG
    PM_MESSAGE = "Hi! This user has enabled anti spam protection. Please wait for him to reply to you before " \
                 "sending him any messages or you will be blocked!"
    return CUSTOM_MSG or PM_MESSAGE


def _load_pm_users():
    global ALLOWED_USERS
    if DB_URI:
        query = sa.select([pm_tbl])
        privates = connection.execute(query).fetchall()
        for row in privates:
            ALLOWED_USERS.append(str(row[0]))


def _load_pm_msg():
    global CUSTOM_MSG
    if DB_URI:
        query = sa.select([pm_msg_tbl])
        privates = connection.execute(query).fetchall()
        for row in privates:
            CUSTOM_MSG = str(row[0])


_load_pm_msg()
_load_pm_users()
