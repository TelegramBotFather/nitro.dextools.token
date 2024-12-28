from database.core import Core
from datetime import datetime


class UserDatabase(Core):
    def __init__(self, uri, database_name):
        super().__init__(uri, database_name, "users")

    async def create(self, user_id):
        return await super().create(
            {
                "_id": user_id,
                "banned": False,
                "channels": {},  # {channel_id: {name: str, status}},
                "created_at": datetime.now(),
            }
        )
