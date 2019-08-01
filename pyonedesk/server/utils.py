# coding:utf-8

import hashlib

from pyonedesk.server import get_code_url
from .account import Account


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


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
