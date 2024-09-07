from pymongo.database import Database

# from typing import Any, Optional


class TreeRepository:
    def __init__(self, database: Database):
        self.database = database
