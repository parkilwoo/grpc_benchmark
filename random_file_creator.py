import os

def create_random_file(filename, size_in_mb):
    size_in_bytes = size_in_mb * 1024 * 1024  # MB to Bytes
    random_data = os.urandom(size_in_bytes)
    with open(filename, 'wb') as file:
        file.write(random_data)

# 파일 생성
create_random_file('random_10MB.bin', 10)
create_random_file('random_30MB.bin', 30)
create_random_file('random_50MB.bin', 50)
create_random_file('random_100MB.bin', 100)
