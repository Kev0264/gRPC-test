import grpc
from concurrent import futures
import task_manager_pb2
import task_manager_pb2_grpc

# In-memory storage for tasks
tasks = []

class TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer):
    def AddTask(self, request, context):
        # Create a new task
        task = task_manager_pb2.Task(
            id=str(len(tasks) + 1),
            title=request.title,
            description=request.description,
            completed=False
        )
        tasks.append(task)
        return task_manager_pb2.AddTaskResponse(task=task)
    
    def ListTasks(self, request, context):
        # Return all tasks
        return task_manager_pb2.ListTasksResponse(tasks=tasks)
    
    def CompleteTask(self, request, context):
        # Mark a task as completed
        for task in tasks:
            if task.id == request.id:
                task.completed = True
                return task_manager_pb2.CompleteTaskResponse(task=task)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Task not found')
        return task_manager_pb2.CompleteTaskResponse()
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_manager_pb2_grpc.add_TaskManagerServicer_to_server(TaskManagerServicer(), server)
    server.add_insecure_port('[::]:50051')
    print('Starting server. Listening on port 50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    