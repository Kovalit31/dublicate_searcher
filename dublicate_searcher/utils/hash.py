import hashlib

def get_sha_512(file_content):
    return hashlib.sha512(file_content).hexdigest()

def get_sha_256(file_content):
    return hashlib.sha256(file_content).hexdigest()

def get_sha_224(file_content):
    return hashlib.sha224(file_content).hexdigest()

def get_sha_1(file_content):
    return hashlib.sha1(file_content).hexdigest()

def get_sha_384(file_content):
    return hashlib.sha384(file_content).hexdigest()

def get_sha(file_content, hash_type=1):
    if 1 <= hash_type < 224:
        a = get_sha_1(file_content=file_content)
    elif 224 <= hash_type < 256:
        a = get_sha_224(file_content=file_content)
    elif 256 <= hash_type < 384:
        a = get_sha_256(file_content=file_content)
    elif 384 <= hash_type < 512:
        a = get_sha_512(file_content=file_content)
    else:
        a = get_sha_512(file_content=file_content)
    return a
    
if __name__ == "__main__":
    a = get_sha("no".encode("utf-8"), hash_type=512)
    print(a)