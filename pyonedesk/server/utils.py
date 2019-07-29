# coding:utf-8

import hashlib
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util import Padding

from pyonedesk.server import get_code_url
from .account import Account


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def aes_encrypt(key: bytes, text: str) -> str:
    iv = key[8:AES.block_size + 8]
    aes = AES.new(key, AES.MODE_CBC, iv)
    text = Padding.pad(text.encode('utf-8'), AES.block_size)
    return b64encode(aes.encrypt(text)).decode('utf-8')


def aes_decrypt(key: bytes, text: str) -> str:
    text = b64decode(text.encode('utf-8'))
    iv = key[8:AES.block_size + 8]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return Padding.unpad(aes.decrypt(text), AES.block_size).decode('utf-8')


def redirectUrl(request, id: str) -> str:
    return '{scheme}://{host}/admin/api/code/{id}'.format(scheme=request.scheme, host=request.host,
        id=id)


def createAppUrl(name: str) -> str:
    appName = 'PyOneDrive-' + name
    return 'https://apps.dev.microsoft.com/?referrer=https%3a%2f%2fdeveloper.microsoft.com%2fzh-cn%2fgraph%2fquick-start#/quickstart/graphIO?publicClientSupport=false&appName={appName}&redirectUrl={redirectUrl}&allowImplicitFlow=false&ru=https:%2F%2Fdeveloper.microsoft.com%2Fzh-cn%2Fgraph%2Fquick-start%3FappID%3D_appId_%26appName%3D_appName_%26redirectUrl%3D{redirectUrl}%26platform%3Doption-Python'.format(
        appName=appName, redirectUrl=get_code_url)


def getCodeUrl(account: Account) -> str:
    return 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirectUrl}&scope=offline_access%20Files.ReadWrite.All'.format(
        redirectUrl=get_code_url, client_id=account.client_id)
