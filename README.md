Python proto loader - Compile ProtoBuf proto files on the fly

```
pip install protol
```

```python
import protol

# https://grpc.io/docs/quickstart/python.html

helloworld_pb2, helloworld_pb2_grpc = protol.load('/abs/path/to/helloworld.proto')

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)

```

```
MIT License
```
