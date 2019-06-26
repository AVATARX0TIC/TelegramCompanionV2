import logging
import socks
from telethon import TelegramClient

from companion.version import __version__
from companion.modules.sql import SESSION
from companion.env_vars import HOST, PORT, USERNAME, PASSWORD, PROXY_TYPE, API_ID, API_HASH

# Logger setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# Help variable as a dict where we append our function's docstring

CMD_HELP = {}

# Max len of a message allowed by telegram

MAX_TEXT_LEN = 4096

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

client = TelegramClient(
    SESSION,
    API_ID,
    API_HASH,
    device_model="tg_companion",
    app_version=__version__)
client.parse_mode = None
