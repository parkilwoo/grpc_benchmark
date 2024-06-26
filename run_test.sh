#!/bin/bash

# Sample directory
SAMPLE_DIR="test_sample"

# 파일명 패턴
FILE_PATTERN="random_*MB.bin"

# 파일 갯수 확인
FILE_COUNT=$(ls $SAMPLE_DIR/$FILE_PATTERN 2>/dev/null | wc -l)

# 파일이 4개가 아니면 샘플 파일 생성
if [[ $FILE_COUNT -ne 4 ]]; then
    echo "샘플 파일 생성을 시작합니다."
    python3 random_file_creator.py
else
    echo "샘플 파일이 이미 존재합니다."
fi

# FastAPI 테스트 실행
echo "FastAPI 테스트를 시작합니다."
# 8090포트 사용중인 PID 찾아서 kill
PID_8090=$(lsof -ti:8090)
if [[ -n $PID_8090 ]]; then
    echo "FastAPI 서버를 시작하기 위해 $PID_8090 프로세스를 종료합니다."
    kill -9 $PID_8090
fi
cd fastapi
# 결과 파일이 존재하면 삭제
if [[ -f "fastapi_result.txt" ]]; then
    rm fastapi_result.txt
fi
python3 server.py &
sleep 3
python3 client.py > fastapi_result.txt 2>&1 && PID_8090=$(lsof -ti:8090) && kill -9 $PID_8090
echo "FastAPI 테스트가 완료되었습니다."

# grpc 테스트 실행
echo "gRPC 테스트(worker 1)를 시작합니다."
PID_50051=$(lsof -ti:50051)
if [[ -n $PID_50051 ]]; then
    echo "gRPC 서버를 시작하기 위해 $PID_50051 프로세스를 종료합니다."
    kill -9 $PID_50051
fi
cd ../grpc
# 결과 파일이 존재하면 삭제
if [[ -f "grpc_result_worker1.txt" ]]; then
    rm grpc_result_worker1.txt
fi
python3 server.py --worker 1 &
sleep 3
python3 client.py > grpc_result_worker1.txt 2>&1 && PID_50051=$(lsof -ti:50051) && kill -9 $PID_50051
echo "gRPC 테스트(worker 1)가 완료되었습니다."
echo "gRPC 테스트(worker 10)를 시작합니다."
# 결과 파일이 존재하면 삭제
if [[ -f "grpc_result_worker10.txt" ]]; then
    rm grpc_result_worker10.txt
fi
python3 server.py --worker 10 &
sleep 3
python3 client.py > grpc_result_worker10.txt 2>&1 && PID_50051=$(lsof -ti:50051) && kill -9 $PID_50051
echo "gRPC 테스트(worker 10)가 완료되었습니다."

# grpc chunk 테스트 실행
echo "gRPC Chunk 테스트(worker 1)를 시작합니다."
PID_50051=$(lsof -ti:50051)
if [[ -n $PID_50051 ]]; then
    echo "gRPC 서버를 시작하기 위해 $PID_50051 프로세스를 종료합니다."
    kill -9 $PID_50051
fi
cd ../grpc_chunk
# 결과 파일이 존재하면 삭제
if [[ -f "grpc_result_worker1_chunk.txt" ]]; then
    rm grpc_result_worker1_chunk.txt
fi
python3 server.py --worker 1 &
sleep 3
python3 client.py > grpc_result_worker1_chunk.txt 2>&1 && PID_50051=$(lsof -ti:50051) && kill -9 $PID_50051
echo "gRPC Chunk 테스트(worker 1)가 완료되었습니다."
echo "gRPC Chunk 테스트(worker 10)를 시작합니다."
# 결과 파일이 존재하면 삭제
if [[ -f "grpc_result_worker10_chunk.txt" ]]; then
    rm grpc_result_worker10_chunk.txt
fi
python3 server.py --worker 10 &
sleep 3
python3 client.py > grpc_result_worker10_chunk.txt 2>&1 && PID_50051=$(lsof -ti:50051) && kill -9 $PID_50051
echo "gRPC Chunk 테스트(worker 10)가 완료되었습니다."