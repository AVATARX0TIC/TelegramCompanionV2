import sqlalchemy as sa
from alchemysession import AlchemySessionContainer
from companion.env_vars import DB_URI, SESSION_NAME

if DB_URI:
    engine = sa.create_engine(DB_URI)
    connection = engine.connect()
    container = AlchemySessionContainer(DB_URI)
    container.core_mode = True
    SESSION = container.new_session(SESSION_NAME)
else:
    engine = None
    metadata = None
    connection = None
    SESSION = SESSION_NAME
