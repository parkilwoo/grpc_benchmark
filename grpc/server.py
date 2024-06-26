from concurrent import futures
import grpc
import test_pb2
import test_pb2_grpc
import base64

class TestServiceServicer(test_pb2_grpc.TestServiceServicer):
    def SendFile(self, request, context):
        file_content = request.file_content
        print(f"byte size: {len(file_content)}")
        encoded_data = base64.b64encode(file_content)
        return test_pb2.FileResponse(base64_data=encoded_data)

def serve(worker: int):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=worker),
                            options=[('grpc.max_receive_message_length', 150 * 1024 * 1024),
                                    ('grpc.max_send_message_length', 150 * 1024 * 1024)])
        test_pb2_grpc.add_TestServiceServicer_to_server(TestServiceServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("GRPC Server Start")
        server.wait_for_termination()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)

    args = parser.parse_args()
    serve(args.worker)
