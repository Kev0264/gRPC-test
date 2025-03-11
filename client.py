import grpc
import task_manager_pb2
import task_manager_pb2_grpc

def run():
    # Connect to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_manager_pb2_grpc.TaskManagerStub(channel)
        
        # Add a task
        print('Adding task...')
        add_response = stub.AddTask(task_manager_pb2.AddTaskRequest(
            title='Buy groceries',
            description='Milk, cheese, bread'
        ))
        print(f'Added task: {add_response.task.title} (ID: {add_response.task.id})')
        
        # List tasks
        print('\nListing tasks...')
        list_response = stub.ListTasks(task_manager_pb2.ListTasksRequest())
        for task in list_response.tasks:
            print(f'{task.title} (Completed: {task.completed})')
        
        # Complete a task
        print('\nCompleting task...')
        complete_response = stub.CompleteTask(task_manager_pb2.CompleteTaskRequest(
            id=add_response.task.id
        ))
        print(f'Completed task: {complete_response.task.title} (ID: {complete_response.task.id})')

        # List tasks again
        print('\nListing tasks...')
        list_response = stub.ListTasks(task_manager_pb2.ListTasksRequest())
        for task in list_response.tasks:
            print(f'{task.title} (Completed: {task.completed})')

if __name__ == '__main__':
    run()