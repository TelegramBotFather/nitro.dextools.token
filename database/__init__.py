from .users import UserDatabase
from bot.config import Config
from .config import ConfigDB
from .hotpairs import Database as HotPairsDatabase

class Database:
    def __init__(self):
        self.users = UserDatabase(Config.DATABASE_URL, Config.DATABASE_NAME)
        self.config = ConfigDB(Config.DATABASE_URL, Config.DATABASE_NAME)
        self.hotpairs = HotPairsDatabase(Config.DATABASE_URL, Config.DATABASE_NAME)

db = Database()
