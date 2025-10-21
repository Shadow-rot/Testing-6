import logging
import os
import sys
import time

from pyrogram import Client
from telethon import TelegramClient
from telegram.ext import Updater

StartTime = time.time()

# ---------- Logging ----------

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

for noisy in ["apscheduler", "telethon", "pymongo", "pyrogram", "pyrate_limiter"]:
    logging.getLogger(noisy).setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)

# ---------- Python version check ----------

if sys.version_info < (3, 6):
    LOGGER.error("You must run Python 3.6+ — bot quitting.")
    sys.exit(1)

# ---------- Environment / Config ----------

ENV = bool(os.environ.get("ENV", False))

if ENV:
    API_ID = int(os.environ["API_ID"])
    API_HASH = os.environ["API_HASH"]
    TOKEN = os.environ["TOKEN"]
    WORKERS = int(os.environ.get("WORKERS", 8))

    OWNER_ID = int(os.environ["OWNER_ID"])
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "DevilsHeavenMF")
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    DB_URI = os.environ.get("DATABASE_URL")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
    START_IMG = os.environ.get(
        "START_IMG", "https://telegra.ph/file/40eb1ed850cdea274693e.jpg"
    )
    
    # Additional optional configs
    INFOPIC = bool(os.environ.get("INFOPIC", False))
    BOT_API_URL = os.environ.get("BOT_API_URL", "https://api.telegram.org/bot")
    BOT_API_FILE_URL = os.environ.get(
        "BOT_API_FILE_URL", "https://api.telegram.org/file/bot"
    )
    DONATION_LINK = os.environ.get("DONATION_LINK")
    CERT_PATH = os.environ.get("CERT_PATH")
    PORT = int(os.environ.get("PORT", 5000))
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Webhook URL

    # Optional sets
    def parse_ids(var):
        return set(int(x) for x in os.environ.get(var, "").split() if x.strip())

    DRAGONS = parse_ids("DRAGONS")
    DEV_USERS = parse_ids("DEV_USERS")
    DEMONS = parse_ids("DEMONS")
    TIGERS = parse_ids("TIGERS")
    WOLVES = parse_ids("WOLVES")
    BL_CHATS = parse_ids("BL_CHATS")

else:
    from FallenRobot.config import Development as Config

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TOKEN = Config.TOKEN
    WORKERS = Config.WORKERS
    OWNER_ID = int(Config.OWNER_ID)
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    EVENT_LOGS = getattr(Config, "EVENT_LOGS", None)
    DB_URI = Config.DATABASE_URL
    MONGO_DB_URI = Config.MONGO_DB_URI
    START_IMG = Config.START_IMG
    
    INFOPIC = getattr(Config, "INFOPIC", False)
    BOT_API_URL = getattr(Config, "BOT_API_URL", "https://api.telegram.org/bot")
    BOT_API_FILE_URL = getattr(
        Config, "BOT_API_FILE_URL", "https://api.telegram.org/file/bot"
    )
    DONATION_LINK = getattr(Config, "DONATION_LINK", None)
    CERT_PATH = getattr(Config, "CERT_PATH", None)
    PORT = getattr(Config, "PORT", 5000)
    WEBHOOK = getattr(Config, "WEBHOOK", False)
    URL = getattr(Config, "URL", "")

    DRAGONS = set(Config.DRAGONS or [])
    DEV_USERS = set(Config.DEV_USERS or [])
    DEMONS = set(Config.DEMONS or [])
    TIGERS = set(Config.TIGERS or [])
    WOLVES = set(Config.WOLVES or [])
    BL_CHATS = set(Config.BL_CHATS or [])

# ---------- Custom constants ----------
ALLOW_EXCL = bool(os.environ.get("ALLOW_EXCL", True))
LOAD = os.environ.get("LOAD", "").split()
NO_LOAD = os.environ.get("NO_LOAD", "").split()
DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
WALL_API = os.environ.get("WALL_API", None)

# ---------- Core user sets ----------

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(5147822244)

# ---------- Bot clients ----------

updater = Updater(TOKEN, workers=WORKERS, use_context=True)
dispatcher = updater.dispatcher

telethn = TelegramClient("Fallen", API_ID, API_HASH)
pbot = Client("FallenRobot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

# ---------- Bot basic info ----------

print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

DRAGONS = list(DRAGONS | DEV_USERS)
DEV_USERS = list(DEV_USERS)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)
WOLVES = list(WOLVES)

# ---------- Load modules ----------

def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile

    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/modules/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(
                any(mod == module_name for module_name in all_modules)
                for mod in to_load
            ):
                LOGGER.error("Invalid loadorder names. Quitting.")
                quit(1)
        else:
            to_load = all_modules

        if NO_LOAD:
            LOGGER.info("Modules to load: %s", to_load)
            return [item for item in to_load if item not in NO_LOAD]

        return to_load

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
LOGGER.info("Modules to load: %s", ALL_MODULES)

# ---------- Custom handler patch ----------

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    RegexHandler,
)

from FallenRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# patch default handlers with custom ones
CommandHandler = CustomCommandHandler
MessageHandler = CustomMessageHandler
RegexHandler = CustomRegexHandler

print("[INFO]: Initialization complete.")