from django.apps import apps
from motor.motor_asyncio import AsyncIOMotorDatabase

from .history_repository.history_repository import HistoryRepository
from .node_repository.node_repository import NodeRepository
from .task_repository.task_repository import TaskRepository
from .todo_repository.todo_repository import TodoRepository
from .tree_repository.tree_repository import TreeRepository

mongo_db: AsyncIOMotorDatabase = apps.get_app_config("core").mongo_db
mongo_client = apps.get_app_config("core").mongo_client

history_repository = HistoryRepository(mongo_client, mongo_db)
node_repository = NodeRepository(mongo_client, mongo_db)
tree_repository = TreeRepository(mongo_client, mongo_db)
task_repository = TaskRepository(mongo_client, mongo_db)
todo_repository = TodoRepository(mongo_client, mongo_db)
