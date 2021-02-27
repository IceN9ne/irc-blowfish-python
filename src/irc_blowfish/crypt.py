import os
from base64 import b64decode, b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import Blowfish
from cryptography.hazmat.primitives.ciphers.modes import CBC, ECB

from .base64 import base64_decode, base64_encode


def encrypt_ecb(plaintext: bytes, key: bytes) -> bytes:
    encryptor = Cipher(algorithm=Blowfish(key), mode=ECB(), backend=default_backend()).encryptor()

    return base64_encode(encryptor.update(pad(plaintext, Blowfish.block_size // 8)) + encryptor.finalize())


def decrypt_ecb(ciphertext: bytes, key: bytes) -> bytes:
    decryptor = Cipher(algorithm=Blowfish(key), mode=ECB(), backend=default_backend()).decryptor()

    return unpad(decryptor.update(base64_decode(ciphertext)) + decryptor.finalize())


def encrypt_cbc(plaintext: bytes, key: bytes) -> bytes:
    iv = os.urandom(8)
    encryptor = Cipher(algorithm=Blowfish(key), mode=CBC(iv), backend=default_backend()).encryptor()

    return b64encode(iv + encryptor.update(pad(plaintext, Blowfish.block_size // 8)) + encryptor.finalize())


def decrypt_cbc(ciphertext: bytes, key: bytes) -> bytes:
    ciphertext = b64decode(ciphertext)
    decryptor = Cipher(algorithm=Blowfish(key), mode=CBC(ciphertext[:8]), backend=default_backend()).decryptor()

    return unpad(decryptor.update(ciphertext[8:]) + decryptor.finalize())


def pad(data: bytes, block_size: int) -> bytes:
    if offset := len(data) % block_size:
        return data + b"\0" * (block_size - offset)
    else:
        return data


def unpad(data: bytes) -> bytes:
    return data.rstrip(b"\0")
