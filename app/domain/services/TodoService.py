from typing import List, Optional

from app.domain.entities import LogLevel
from app.domain.entities.InnerLog import InnerLog
from app.domain.entities.Todo import Todo
from app.domain.repositories.TodoRepository import TodoRepository

class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def create_todo(self, title: str, message: str, inner_log: Optional[InnerLog] = None) -> Todo:
        if inner_log:
            # Kiểm tra và chuyển đổi giá trị level nếu cần
            if isinstance(inner_log.level, str):
                inner_log.level = LogLevel[inner_log.level.upper()]  # Chuyển chuỗi thành LogLevel enum

        todo = Todo(
            title=title,
            message=message,
            inner_log=inner_log if inner_log else InnerLog(),
        )
        return self.repository.create(todo)

    def get_todo_by_id(self, todo_id: str) -> Todo:
        return self.repository.get_by_id(todo_id)

    def delete_todo_by_id(self, todo_id: str) -> bool:
        return self.repository.delete(todo_id)

    def list_all_todos(self):
        todos = self.repository.get_all_todos()  # Lấy tất cả todos từ repository
        return todos  # Trả về danh sách các đối tượng Todo đã được chuyển đổi trong repository

