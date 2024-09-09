from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# from typing import Any, Optional


class NodeRepository:
    def __init__(self, client: AsyncIOMotorClient, database: AsyncIOMotorDatabase):
        self.client = client
        self.database = database

    async def create_node(
        self,
        node_title: str,
        user_id: str,
        tree_id: str,
        children: list,
        done: bool,
        is_root: bool,
        is_leaf: bool,
        focus: bool = False,
    ) -> str:
        payload = {
            "nodeTitle": node_title,
            "userId": user_id,
            "treeId": tree_id,
            "taskId": None,
            "children": children,
            "done": done,
            "isRoot": is_root,
            "isLeaf": is_leaf,
            "focus": focus,
            "createdAt": datetime.now(),
        }
        try:
            result = await self.database.nodes.insert_one(payload)
        except Exception as e:
            print(e)
            return None
        return str(result.inserted_id)

    async def get_nodes_by_query(self, query: dict) -> dict:
        try:
            nodes_cursor = self.database.nodes.find(query)
            nodes = await nodes_cursor.to_list(length=100)
        except Exception as e:
            print(e)
            return None
        return nodes

    async def get_node_by_id(self, node_id: str) -> dict:
        try:
            node = await self.database.nodes.find_one({"_id": node_id})
        except Exception as e:
            print(e)
            return None
        return node

    async def update_node_by_id(self, node_id: str, properties: dict) -> bool:
        try:
            await self.database.nodes.update_one({"_id": node_id}, {"$set": properties})
        except Exception as e:
            print(e)
            return False
        return True
