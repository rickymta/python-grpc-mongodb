from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from app.domain.entities.Todo import Todo

class TodoRepository:
    def __init__(self, db_client):
        self.db = db_client.get_database()  # Giả sử bạn đã định nghĩa get_database trong MongoDBClient
        self.collection = self.db["volcanion-logging"]  # Tên collection trong MongoDB

    def create(self, todo: Todo) -> Todo:
        todo_data = {
            "title": todo.title,
            "message": todo.message,
            "inner_log": todo.inner_log.__dict__,  # Lưu inner_log dưới dạng dictionary
            "created_at": todo.created_at,
        }
        result = self.collection.insert_one(todo_data)
        todo.id = str(result.inserted_id)
        return todo

    def get_by_id(self, todo_id: str) -> Optional[Todo]:
        data = self.collection.find_one({"_id": ObjectId(todo_id)})
        if data:
            return Todo(
                id=str(data["_id"]),  # Chuyển _id thành id để khớp với Todo
                title=data["title"],
                message=data["message"],
                inner_log=data["inner_log"],
                created_at=data.get("created_at", datetime.utcnow()),  # Sử dụng giá trị mặc định nếu không có
            )
        return None

    def delete(self, todo_id: str) -> bool:
        # Xóa Todo dựa trên ID
        result = self.collection.delete_one({"_id": ObjectId(todo_id)})
        return result.deleted_count > 0  # Nếu xóa thành công, trả về True

    def list_all(self) -> List[Todo]:
        todos = self.collection.find()
        return [
            Todo(
                id=str(todo["_id"]),  # Chuyển _id thành id
                title=todo.get("title", ""),
                message=todo.get("message", ""),
                inner_log=todo.get("inner_log", False),
                created_at=todo.get("created_at", datetime.utcnow()),  # Sử dụng giá trị mặc định nếu không có
            )
            for todo in todos
        ]

    def get_all_todos(self):
        todos = self.collection.find()  # Truy vấn tất cả các Todo từ MongoDB
        return [
            Todo(
                id=str(todo["_id"]),  # Chuyển _id thành id
                title=todo.get("title", ""),
                message=todo.get("message", ""),
                inner_log=todo.get("inner_log", False),
                created_at=todo.get("created_at", datetime.utcnow()),  # Đảm bảo rằng các trường khác được gán đúng
            )
            for todo in todos
        ]
