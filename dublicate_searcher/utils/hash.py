import hashlib

def _get_sha1(src):
    return hashlib.sha1(src).hexdigest()

def _get_sha224(src):
    return hashlib.sha224(src).hexdigest()

def _get_sha256(src):
    return hashlib.sha256(src).hexdigest()

def _get_sha512(src):
    return hashlib.sha512(src).hexdigest()

def _get_sha384(src):
    return hashlib.sha384(src).hexdigest()

def get_sha(src, sha_type=1, sha_len=1):
    if sha_type == 1:
        if 1 <= sha_len < 224:
            a = _get_sha1(src)
        elif 224 <= sha_len < 256:
            a = _get_sha224(src)
        elif 256 <= sha_len < 384:
            a = _get_sha256(src)
        elif 384 <= sha_len < 512:
            a = _get_sha384(src)
        elif 512 <= sha_len:
            a = _get_sha512(src)
        else:
            a = _get_sha512(src)
        return a
    elif sha_type == 3:
        pass
    else:
        raise IndentationError(f"No sha type 'v{str(sha_type)}'!")

def get_sha_v1_avialables() -> list:
    return [1, 224, 256, 384, 512]