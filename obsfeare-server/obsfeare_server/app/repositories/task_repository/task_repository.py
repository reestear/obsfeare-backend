from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class TaskRepository:
    def __init__(
        self, client: AsyncIOMotorClient, database: AsyncIOMotorDatabase
    ) -> None:
        self.client = client
        self.database = database

    # def create_task(self, task_title: str, user_id: str, **kwargs) -> str:
    #     payload = {
    #         "taskTitle": task_title,
    #         "userId": user_id,
    #         "done": False,
    #         **kwargs,
    #     }
    #     try:
    #         result = self.database.tasks.insert_one(payload)
    #     except Exception as e:
    #         print(e)
    #         return None
    #     return str(result.inserted_id)

    async def get_task_by_id(self, task_id: str) -> dict:
        try:
            task = await self.database.tasks.find_one({"_id": task_id})
        except Exception as e:
            print(e)
            return None
        return task

    async def update_task_by_id(self, task_id: str, properties: dict) -> bool:
        try:
            await self.database.tasks.update_one({"_id": task_id}, {"$set": properties})
        except Exception as e:
            print(e)
            return False
        return True
