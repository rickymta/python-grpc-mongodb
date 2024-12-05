from app.domain.repositories.TodoRepository import TodoRepository
from app.domain.entities.Todo import Todo
from app.infrastructure.database.MongoDBClient import MongoDBClient
from bson.objectid import ObjectId
from typing import List, Optional

class MongoTodoRepository(TodoRepository):
    def __init__(self, db_client: MongoDBClient):
        self.collection = db_client.get_collection("volcanion-logging")

    def create(self, todo: Todo) -> Todo:
        print(todo.__dict__)
        result = self.collection.insert_one(todo.__dict__)
        todo.id = str(result.inserted_id)
        return todo

    def get_by_id(self, todo_id: str) -> Optional[Todo]:
        data = self.collection.find_one({"_id": ObjectId(todo_id)})
        if data:
            return Todo(**data, id=str(data["_id"]))
        return None

    def delete(self, todo_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(todo_id)})
        return result.deleted_count > 0

    def list_all(self) -> List[Todo]:
        return [Todo(**doc, id=str(doc["_id"])) for doc in self.collection.find()]
