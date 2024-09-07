from django.apps import AppConfig
from django.conf import settings
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class CoreConfig(AppConfig):
    name = "obsfeare_server.core"

    def ready(self):
        try:

            if settings.MONGODB["MONGO_URI"] is not None:
                mongo_client = MongoClient(settings.MONGODB["MONGO_URI"])
            else:
                mongo_client = MongoClient(
                    settings.MONGODB["HOST"], settings.MONGODB["PORT"]
                )

            self.mongo_db = mongo_client[settings.MONGODB["NAME"]]
            print("MongoDB connection successful")
        except ConnectionFailure:
            print("MongoDB connection failed")
