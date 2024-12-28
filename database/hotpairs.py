from database.core import Core
from datetime import datetime


class Database(Core):
    def __init__(self, uri, database_name):
        super().__init__(uri, database_name, "hotpairs")

    async def create(self, ca):
        return await super().create(
            {
                "ca": ca,
                "created_at": datetime.now(),
            }
        )
