from django.apps import apps

from .history_repository.history_repository import HistoryRepository

# from .tree_repository.tree_repository import TreeRepository

mongo_db = apps.get_app_config("core").mongo_db

history_repository = HistoryRepository(mongo_db)
