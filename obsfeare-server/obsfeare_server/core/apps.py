from django.apps import AppConfig
from django.conf import settings
from motor import motor_asyncio
from openai import AsyncOpenAI


class CoreConfig(AppConfig):
    name = "obsfeare_server.core"

    def ready(self):
        try:
            if settings.MONGODB["MONGO_URI"] is not None:
                self.mongo_client = motor_asyncio.AsyncIOMotorClient(
                    settings.MONGODB["MONGO_URI"]
                )
            else:
                self.mongo_client = motor_asyncio.AsyncIOMotorClient(
                    settings.MONGODB["HOST"], settings.MONGODB["PORT"]
                )

            self.mongo_db = self.mongo_client[settings.MONGODB["NAME"]]
            print("MongoDB connection successful")

            openai = AsyncOpenAI(api_key=settings.OPENAI_KEY)
            self.openai = openai

        except Exception:
            print("Setup failed to lauch")
