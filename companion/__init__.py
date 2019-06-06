from distutils.util import strtobool as sb
from telethon import TelegramClient
from alchemysession import AlchemySessionContainer
from companion.version import __version__
import os
import logging
import dotenv
import socks


# Logger setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)


# Env variables setup
dotenv.load_dotenv("config.env")

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
CMD_PREFIX = os.environ.get("CMD_PREFIX", ".")
DB_URI = os.environ.get("DB_URI")
SESSION_NAME = os.environ.get("SESSION_NAME", "companion")

# Help variable as a dict where we append our function's docstring

CMD_HELP = {}

# Max len of a message allowed by telegram

MAX_TEXT_LEN = 4096

# Proxy setup

PROXY_TYPE = os.environ.get("PROXY_TYPE", None)
HOST = os.environ.get("HOST", None)
PORT = os.environ.get("PORT", None)
USERNAME = os.environ.get("USERNAME", None)
PASSWORD = os.environ.get("PASSWORD", None)

proxy = None
proxy_type = None
proxy_addr = HOST
proxy_port = PORT
proxy_username = USERNAME
proxy_password = PASSWORD

if PROXY_TYPE:
    if PROXY_TYPE == "HTTP":
        proxy_type = socks.HTTP
    elif PROXY_TYPE == "SOCKS4":
        proxy_type = socks.SOCKS4
    elif PROXY_TYPE == "SOCKS5":
        proxy_type = socks.SOCKS5
    else:
        proxy_type = None

    proxy = (
        proxy_type,
        proxy_addr,
        int(proxy_port),
        False,
        USERNAME,
        PASSWORD)



# Misc variables

STDOUT = "<b>Query:</b>\n<code>{}</code>\n\n<b>Result:</b>\n<code>{}</code>"
STDERR = "<b>Query:</b>\n<code>{}</code>\n\n<b>Error:</b>\n<code>{}</code>"
EXCEPTION = "<b>Query:</b>\n<code>{}</code>\n\n<b>Exception:</b>\n<code>{}</code>"
STATUS = "<b>Query:</b>\n<code>{}</code>\n\n<b>Status:</b>\n<code>{}</code>"

# Client setup

if DB_URI:
    container = AlchemySessionContainer(DB_URI)
    session = container.new_session(SESSION_NAME)
else:
    session = SESSION_NAME
client = TelegramClient(session, API_ID, API_HASH, device_model="tg_companion", app_version=__version__)
client.parse_mode = None
