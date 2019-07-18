# coding:utf-8

import base64
import hashlib

from Crypto.Cipher import AES

from .account import Account


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


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


def redirectUrl(request, id: str) -> str:
    return '{scheme}://{host}/admin/api/code/{id}'.format(scheme=request.scheme, host=request.host,
        id=id)


def createAppUrl(name: str, url: str) -> str:
    appName = 'PyOneDrive-' + name
    return 'https://apps.dev.microsoft.com/?referrer=https%3a%2f%2fdeveloper.microsoft.com%2fzh-cn%2fgraph%2fquick-start#/quickstart/graphIO?publicClientSupport=false&appName={appName}&redirectUrl={redirectUrl}&allowImplicitFlow=false&ru=https:%2F%2Fdeveloper.microsoft.com%2Fzh-cn%2Fgraph%2Fquick-start%3FappID%3D_appId_%26appName%3D_appName_%26redirectUrl%3D{redirectUrl}%26platform%3Doption-Python'.format(
        appName=appName, redirectUrl=url)


def getCodeUrl(account: Account) -> str:
    return 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirectUrl}&scope=offline_access%20Files.ReadWrite.All'.format(
        redirectUrl=account.url, client_id=account.client_id)
