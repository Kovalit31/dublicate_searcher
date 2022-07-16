import hashlib

class SHA:
    def get_sha_512(self, src):
        return hashlib.sha512(src).hexdigest()

    def get_sha_256(self, src):
        return hashlib.sha256(src).hexdigest()

    def get_sha_224(self, src):
        return hashlib.sha224(src).hexdigest()

    def get_sha_1(self, src):
        return hashlib.sha1(src).hexdigest()

    def get_sha_384(self, src):
        return hashlib.sha384(src).hexdigest()

class SHA3:
    pass

class MD5:
    pass

class BLAKE:
    pass

class SHAKE:
    pass

def get_sha(src, hash_type=1):
    available = hashlib.algorithms_available
    sha = SHA()
    if 1 <= hash_type < 224 and "sha1" in available:
        return sha.get_sha_1(src=src)
    elif 224 <= hash_type < 256 and "sha224" in available:
        return sha.get_sha_224(src=src)
    elif 256 <= hash_type < 384 and "sha256" in available:
        return sha.get_sha_256(src=src)
    elif 384 <= hash_type < 512 and "sha512" in available:
        return sha.get_sha_512(src=src)
    else:
        if "sha512" in available:
            return sha.get_sha_512(src=src)
        else:
            return None

def get_hashsum(src, type="sha", number=1, blake_char="s"):
    if type == "sha":
        return get_sha(src, number)
    elif type == "md5":
        return None
    elif type == "sha3":
        return None
    elif type == "blake":
        return None
    elif type == "shake":
        return None
    else:
        return None
    
if __name__ == "__main__":
    a = get_hashsum("no".encode("utf-8"), number=468)
    print(a)