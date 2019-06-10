import os
import dotenv

# Env variables setup
dotenv.load_dotenv("config.env")

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
CMD_PREFIX = os.environ.get("CMD_PREFIX", ".")
SESSION_NAME = os.environ.get("SESSION_NAME", "companion")

ANTI_SPAM = os.environ.get("ANTI_SPAM", None)


# Proxy setup

PROXY_TYPE = os.environ.get("PROXY_TYPE", None)
HOST = os.environ.get("HOST", None)
PORT = os.environ.get("PORT", None)
USERNAME = os.environ.get("USERNAME", None)
PASSWORD = os.environ.get("PASSWORD", None)


# SESSION AND DB SETUP
SESSION_NAME = os.environ.get("SESSION_NAME", "companion")
DB_URI = os.environ.get("DB_URI")