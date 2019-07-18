import requests
from sanic.exceptions import ServerError

from .account import Account


def accountQuota(account: Account) -> dict:
    if account.token is None:
        raise ServerError('账号没有Token')
    res = requests.get('https://graph.microsoft.com/v1.0/me/drive',
        headers={'Authorization': 'Bearer ' + account.token['access_token']})
    return res.json()['quota']


def refreshToken(account: Account):
    data = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token'.format(
        client_id=account.client_id,
        client_secret=account.client_secret,
        refresh_token=account.token['refresh_token'],
        redirect_uri=account.url
    )
    res = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data)
