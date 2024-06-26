import grpc
import test_pb2
import test_pb2_grpc
import time
from concurrent.futures import ThreadPoolExecutor

CHUNK_SIZE = 1024 * 1024
def generate_chunks(file_path):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            yield test_pb2.FileRequest(file_content=chunk)

            

def do_request(file_path):
    channel = grpc.insecure_channel('localhost:50051')
    stub = test_pb2_grpc.TestServiceStub(channel)
    response_iter = stub.SendFile(generate_chunks(file_path))
    for _ in response_iter:
        pass

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

