import grpc
import test_pb2
import test_pb2_grpc
import time
from concurrent.futures import ThreadPoolExecutor

def do_request(file_path):
    with open(file_path, "rb") as f:
        options = [('grpc.max_receive_message_length', 150 * 1024 * 1024),
                ('grpc.max_send_message_length', 150 * 1024 * 1024)]        
        with grpc.insecure_channel('localhost:50051', options=options) as channel:
            stub = test_pb2_grpc.TestServiceStub(channel)
            stub.SendFile(test_pb2.FileRequest(file_content=f.read()))

def test_file_request(file_path):
    # 단일 쓰레드 요청
    print(f"{file_path} 단일 쓰레드 요청 시작")
    single_thread_start = time.time()
    do_request(file_path)
    single_thread_end = time.time()
    print(f"{file_path} 단일 쓰레드 요청 소요 시간: {single_thread_end - single_thread_start:.2f}초")
    # 10개 쓰레드 동시 요청
    print(f"{file_path} 10개 쓰레드 동시 요청 시작")
    multi_thread_start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(do_request, file_path) for _ in range(10)]
        for future in futures:
            future.result()
    multi_thread_end = time.time()
    print(f"{file_path} 10개 쓰레드 동시 요청 소요 시간: {multi_thread_end - multi_thread_start:.2f}초\n")

if __name__ == '__main__':
    test_file_request("../test_sample/random_10MB.bin")
    test_file_request("../test_sample/random_30MB.bin")
    test_file_request("../test_sample/random_50MB.bin")
    test_file_request("../test_sample/random_100MB.bin")
