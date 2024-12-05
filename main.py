from app.infrastructure.database.MongoDBClient import MongoDBClient
from app.infrastructure.repositories.TodoRepositoryImpl import MongoTodoRepository
from app.domain.services.TodoService import TodoService
from app.grpc.services.TodoGRPCService import TodoGRPCService
from app.grpc.generated import todo_pb2_grpc
from concurrent import futures
from dotenv import load_dotenv

import grpc
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

def main():
    db_client = MongoDBClient(MONGODB_URL, MONGODB_DB_NAME)
    repository = MongoTodoRepository(db_client)
    service = TodoService(repository)
    grpc_service = TodoGRPCService(service)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(grpc_service, server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()
