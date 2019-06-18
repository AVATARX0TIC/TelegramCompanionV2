import sqlalchemy as sa

from companion.env_vars import DB_URI

from . import connection, engine

metadata = sa.MetaData()

gnotes_tbl = sa.Table("gnotes", metadata,
                      sa.Column("notename", sa.String()),
                      sa.Column("content", sa.String()),
                      sa.Column("file_document", sa.Boolean()),
                      sa.Column("file_access_hash", sa.String()),
                      sa.Column("file_id", sa.String()),
                      sa.Column("file_reference", sa.String()))

if DB_URI:
    metadata.create_all(
        bind=engine,
        tables=[gnotes_tbl],
        checkfirst=True)


NOTES = {}


class CompanionNote:
    def __init__(
            self,
            name,
            content=None,
            file_document=False,
            access_hash=None,
            file_id=None,
            file_reference=None):
        self.name = name
        self.content = content
        self.file_document = file_document
        self.access_hash = access_hash
        self.file_id = file_id
        self.file_reference = file_reference


def insert_note(
        name,
        content=None,
        file_document=False,
        access_hash=None,
        file_id=None,
        file_reference=None):
    global NOTES
    if name not in NOTES:
        query = sa.insert(gnotes_tbl).values(
            notename=name,
            content=content,
            file_document=file_document,
            file_access_hash=access_hash,
            file_id=file_id,
            file_reference=file_reference)

    else:
        query = sa.update(gnotes_tbl).where(
            gnotes_tbl.c.notename == name).values(
            name,
            content,
            file_document=False,
            access_hash=None,
            file_id=None,
            file_reference=file_reference)
    cls = CompanionNote(
        name,
        content,
        file_document,
        access_hash,
        file_id,
        file_reference)
    connection.execute(query)
    NOTES.update({name: cls})


def rem_note(name):
    global NOTES
    if name in NOTES:
        query = gnotes_tbl.delete().where(gnotes_tbl.c.notename == name)
        connection.execute(query)
        del NOTES[name]
        return True
    return


def get_note(name):
    return NOTES.get(name)

def get_all_notes():
    return [note[0] for note in NOTES.items()]

def __load_notes():
    global Notes
    if DB_URI:
        query = sa.select([gnotes_tbl])
        notes = connection.execute(query).fetchall()
        for row in notes:
            cls = CompanionNote(
                row.notename,
                row.content,
                row.file_document,
                row.file_access_hash,
                row.file_id,
                row.file_reference)
            NOTES.update({row.notename: cls})


__load_notes()
