class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    API_ID = 29871943
    API_HASH = "31009b6d7f489680ba7d66e3323a249e"

    CASH_API_KEY = ""  # Get this value for currency converter from https://www.alphavantage.co/support/#api-key

    DATABASE_URL = "postgres://uf0rq148kethbk:pe7bfc383f862d959dd60453cb69dad02e3d4539dd5eafe518911575f763c4ce5@cfrvfq74n7n5dp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d134luiuq6ltbe"  # A sql database url from elephantsql.com

    EVENT_LOGS = (-1002191083108)  # Event logs channel to note down important bot level events

    MONGO_DB_URI = "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority"  # Get ths value from cloud.mongodb.com

    # Telegraph link of the image which will be shown at start command.
    START_IMG = "https://te.legra.ph/file/40eb1ed850cdea274693e.jpg"

    SUPPORT_CHAT = "loooooooohkooe"  # Your Telegram support group chat username where your users will go and bother you

    TOKEN = "7891572866:AAEKgMqTNK0vQ_mAw63YFKdL6bD2oEiss14"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = ""  # Get this value from https://timezonedb.com/api

    OWNER_ID = 5147822244  # User id of your telegram account (Must be integer)

    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
