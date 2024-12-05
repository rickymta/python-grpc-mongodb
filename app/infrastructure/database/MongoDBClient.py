from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri: str, database_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[database_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]
