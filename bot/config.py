import os
from dotenv import load_dotenv

if os.path.exists("config.env"):
    load_dotenv("config.env")
else:
    load_dotenv()


def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


class Config(object):
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "tg_bot")
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    OWNER_ID = int(os.environ.get("OWNER_ID"))

    DEXTOOLS_API_KEY = os.environ.get("DEXTOOLS_API_KEY")

    # Optional
    WEB_SERVER = is_enabled(os.environ.get("WEB_SERVER", "False"), False)

    DEBUG = is_enabled(os.environ.get("DEBUG", "False"), False)

    MAIN_CHAT = {
        "chat_id": int(os.environ.get("MAIN_CHAT_ID")),
        "topic_id": int(os.environ.get("MAIN_CHAT_TOPIC_ID")),
        "new_token_topic_id": int(os.environ.get("NEW_TOKEN_TOPIC_ID")),
    }


class Script(object):
    START_MESSAGE = """**👋 Hi {mention}!**

Welcome to the Solana Nitro Pairs Bot! 🔥

I track and notify you about trending token pairs on Solana through DexTools. Stay informed about:

• Top performing Solana pairs
• New hot token listings (marked with 🔥)
• Real-time price and pair explorer links

Get instant notifications when new trending pairs are detected!

https://www.dextools.io/app/en/solana/token-race
"""
