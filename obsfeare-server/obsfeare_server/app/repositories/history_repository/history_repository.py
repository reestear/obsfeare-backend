from pymongo.database import Database

# from typing import Any, Optional


class HistoryRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_history(self, user_request: str, response: str, user_id: str) -> bool:
        payload = {
            "userId": user_id,
            "request": user_request,
            "response": response,
        }

        try:
            self.database.chatdialogs.insert_one(payload)
        except Exception as e:
            print(e)
            return False

        return True

    def get_histories(self, user_id: str) -> list:
        print("Getting Histories of user: ", user_id)
        try:
            histories = self.database.chatdialogs.find({"userId": user_id})
        except Exception as e:
            print(e)
            return []
        return list(histories)
