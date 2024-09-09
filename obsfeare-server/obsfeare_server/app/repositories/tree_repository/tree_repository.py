from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# from typing import Any, Optional


class TreeRepository:
    def __init__(self, client: AsyncIOMotorClient, database: AsyncIOMotorDatabase):
        self.client = client
        self.database = database

    async def create_tree(
        self, user_id: str, node_id: str, done: bool, **kwargs
    ) -> str:
        payload = {
            "nodeId": node_id,
            "userId": user_id,
            "done": done,
            "createdAt": datetime.now(),
            **kwargs,
        }
        try:
            result = await self.database.trees.insert_one(payload)
        except Exception as e:
            print(e)
            return None
        return str(result.inserted_id)

    async def get_trees_by_user_id(self, user_id: str) -> list:
        try:
            trees_cursor = self.database.trees.find({"userId": user_id})
            trees = await trees_cursor.to_list(length=100)

        except Exception as e:
            print(e)
            return None
        return trees

    async def get_tree_by_id(self, tree_id: str) -> dict:
        try:
            tree = await self.database.trees.find_one({"_id": tree_id})
        except Exception as e:
            print(e)
            return None
        return tree

    async def update_tree_by_id(self, tree_id: str, properties: dict) -> bool:
        try:
            await self.database.trees.update_one({"_id": tree_id}, {"$set": properties})
        except Exception as e:
            print(e)
            return False
        return True
