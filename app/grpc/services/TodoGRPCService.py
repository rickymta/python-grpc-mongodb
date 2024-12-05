from app.domain.entities.InnerLog import InnerLog
from app.domain.entities.LogLevel import LogLevel
from app.domain.services import TodoService
from app.grpc.generated import todo_pb2, todo_pb2_grpc
import grpc

class TodoGRPCService(todo_pb2_grpc.TodoServiceServicer):
    def __init__(self, service: TodoService):
        self.service = service

    def CreateTodo(self, request, context):
        title = request.title
        message = request.message
        inner_log = None

        if request.HasField('inner_log'):
            level_value = request.inner_log.level
            print(f"Level value: {level_value}")
            print(LogLevel.is_valid(level_value))

            # Kiểm tra xem giá trị level có hợp lệ không
            if not LogLevel.is_valid(level_value):
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(f"Invalid LogLevel: {level_value}")
                return todo_pb2.TodoResponse()

            inner_log = InnerLog(
                message=request.inner_log.message,
                exception=request.inner_log.exception,
                stacktrace=request.inner_log.stacktrace,
                level=LogLevel(level_value)  # Chuyển thành LogLevel enum
            )

        todo = self.service.create_todo(title, message, inner_log)

        return todo_pb2.TodoResponse(
            id=todo.id,
            title=todo.title,
            message=todo.message,
            inner_log=todo_pb2.InnerLog(
                message=todo.inner_log.message,
                exception=todo.inner_log.exception,
                stacktrace=todo.inner_log.stacktrace,
                level=todo.inner_log.level.name  # Trả về tên của enum LogLevel
            ) if todo.inner_log else None,
        )

    def GetTodo(self, request, context):
        todo = self.service.get_todo_by_id(request.id)
        if todo:
            return todo_pb2.TodoResponse(
                id=todo.id, title=todo.title, message=todo.message, inner_log=todo.inner_log
            )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Todo not found")
        return todo_pb2.TodoResponse()

    def DeleteTodoById(self, request, context):
        try:
            success = self.service.delete_todo_by_id(request.id)
            return todo_pb2.DeleteTodoResponse(success=success)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return todo_pb2.DeleteTodoResponse(success=False)

    def ListTodos(self, request, context):
        todos = self.service.list_all_todos()  # Gọi service để lấy tất cả todos
        return todo_pb2.TodosResponse(
            todos=[todo_pb2.TodoResponse(
                id=todo.id,
                title=todo.title,
                message=todo.message,
                inner_log=todo.inner_log
            ) for todo in todos]
        )
