from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class TodoRepository:
    def __init__(self, client: AsyncIOMotorClient, database: AsyncIOMotorDatabase):
        self.client = client
        self.database = database

    async def get_todo_by_id(self, todo_id: str) -> dict:
        try:
            todo = await self.database.todos.find_one({"_id": todo_id})
        except Exception as e:
            print(e)
            return None
        return todo

    async def get_todos_by_query(self, query: dict) -> dict:
        try:
            todos_cursor = self.database.todos.find(query)
            todos = await todos_cursor.to_list(length=100)
        except Exception as e:
            print(e)
            return None
        return todos
