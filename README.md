# gRPC-test

## Create Virtual Environment

```
python -m venv myvenv
```

# Generated Python Code

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. task_manager.proto
```
