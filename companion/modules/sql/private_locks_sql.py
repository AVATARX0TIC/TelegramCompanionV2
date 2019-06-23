import sqlalchemy as sa

from companion.env_vars import DB_URI

from . import connection, engine

metadata = sa.MetaData()

pm_locks = sa.Table("pm_locks", metadata,
                    sa.Column("audio", sa.Boolean(), nullable=False),
                    sa.Column("voice", sa.Boolean(), nullable=False),
                    sa.Column("contact", sa.Boolean(), nullable=False),
                    sa.Column("video", sa.Boolean(), nullable=False),
                    sa.Column("video_note", sa.Boolean(), nullable=False),
                    sa.Column("document", sa.Boolean(), nullable=False),
                    sa.Column("photo", sa.Boolean(), nullable=False),
                    sa.Column("sticker", sa.Boolean(), nullable=False),
                    sa.Column("gif", sa.Boolean(), nullable=False),
                    sa.Column("url", sa.Boolean(), nullable=False),
                    sa.Column("forward", sa.Boolean(), nullable=False),
                    sa.Column("game", sa.Boolean(), nullable=False),
                    sa.Column("location", sa.Boolean(), nullable=False),
                    sa.Column("poll", sa.Boolean(), nullable=False),
                    sa.Column("poll", sa.Boolean(), nullable=False),
                    )

if DB_URI:
    metadata.create_all(
        bind=engine,
        tables=[pm_locks],
        checkfirst=True)

LOCKED = {}


def update_restriction(lock_type, is_locked):
    global LOCKED
    if is_locked is True:
        locked = sa.true()
    else:
        locked = sa.false()

    if lock_type == "audio":
        query = sa.update(pm_locks).values(audio=locked)
    elif lock_type == "voice":
        query = sa.update(pm_locks).values(voice=locked)
    elif lock_type == "contact":
        query = sa.update(pm_locks).values(contact=locked)
    elif lock_type == "video":
        query = sa.update(pm_locks).values(video=locked)
    elif lock_type == "video_note":
        query = sa.update(pm_locks).values(video_note=locked)
    elif lock_type == "document":
        query = sa.update(pm_locks).values(document=locked)
    elif lock_type == "photo":
        query = sa.update(pm_locks).values(photo=locked)
    elif lock_type == "gif":
        query = sa.update(pm_locks).values(gif=locked)
    elif lock_type == "sticker":
        query = sa.update(pm_locks).values(sticker=locked)
    elif lock_type == 'url':
        query = sa.update(pm_locks).values(url=locked)
    elif lock_type == 'forward':
        query = sa.update(pm_locks).values(forward=locked)
    elif lock_type == 'game':
        query = sa.update(pm_locks).values(game=locked)
    elif lock_type == 'location':
        query = sa.update(pm_locks).values(location=locked)
    elif lock_type == "poll":
        query = sa.update(pm_locks).values(poll=locked)
    connection.execute(query)
    LOCKED.update({lock_type: is_locked})


def get_restrictions():
    return LOCKED


def __init_table():
    query = sa.insert(pm_locks).values(
        audio=sa.false(),
        voice=sa.false(),
        contact=sa.false(),
        video=sa.false(),
        video_note=sa.false(),
        document=sa.false(),
        photo=sa.false(),
        sticker=sa.false(),
        gif=sa.false(),
        url=sa.false(),
        forward=sa.false(),
        game=sa.false(),
        location=sa.false(),
        poll=sa.false())
    connection.execute(query)


def __load_locks():
    global LOCKED
    if DB_URI:
        query = sa.select([pm_locks])
        locked = connection.execute(query).fetchall()
        for row in locked:
            for column, value in row.items():
                LOCKED.update({column: value})

        if bool(LOCKED) is False:
            __init_table()
            __load_locks()


__load_locks()
