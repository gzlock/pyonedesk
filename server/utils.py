# coding:utf-8

import hashlib
from Crypto.Cipher import AES
import base64


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def md5(text: str) -> bytes:
    return hashlib.md5(text.encode()).digest()


def multiple16(text: str, fill: str = ' ') -> str:
    length = len(text)
    length = length - length % 16 + 16
    return text.ljust(length, fill)


def aesEncrypt(key: bytes, text: str, iv: str) -> str:
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b16encode(aes.encrypt(multiple16(text))).decode()


def aesDecrypt(key: bytes, text: str, iv: str) -> str:
    text = base64.b16decode(text)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(text).decode().strip()
