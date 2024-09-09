from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# from typing import Any, Optional


class HistoryRepository:
    def __init__(self, client: AsyncIOMotorClient, database: AsyncIOMotorDatabase):
        self.client = client
        self.database = database

    async def create_history(
        self, user_request: str, response: str, user_id: str
    ) -> str | None:
        payload = {
            "userId": user_id,
            "request": user_request,
            "response": response,
        }

        try:
            result = await self.database.chatdialogs.insert_one(payload)
        except Exception as e:
            print(e)
            return None

        return str(result.inserted_id)

    async def get_histories(self, user_id: str) -> list | None:
        try:
            # most recent history first
            histories_cursor = self.database.chatdialogs.find({"userId": user_id}).sort(
                "createdAt", -1
            )

            histories = await histories_cursor.to_list(length=100)

            histories.reverse()
        except Exception as e:
            print(e, flush=True)
            return None
        return list(histories)

    async def get_history_by_id(self, history_id: str) -> dict | None:
        try:
            history = await self.database.chatdialogs.find_one({"_id": history_id})
        except Exception as e:
            print(e)
            return None
        return history
