from concurrent import futures
import grpc
import test_pb2
import test_pb2_grpc
import base64

CHUNK_SIZE = 1024 * 1024
class TestServiceServicer(test_pb2_grpc.TestServiceServicer):
    def SendFile(self, request_iterator, context):
        total_data = bytearray()
        for request in request_iterator:
            total_data.extend(request.file_content)
        print(f"byte size: {len(total_data)}")
        encoded_data = base64.b64encode(total_data)
        for i in range(0, len(encoded_data), CHUNK_SIZE):
            yield test_pb2.FileResponse(base64_data=encoded_data[i:i+CHUNK_SIZE])
        # return test_pb2.FileResponse(base64_data=encoded_data)        

def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        test_pb2_grpc.add_TestServiceServicer_to_server(TestServiceServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("GRPC_Chunk Server Start")
        server.wait_for_termination()

if __name__ == '__main__':
    serve()
