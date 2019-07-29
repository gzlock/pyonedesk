from __future__ import annotations

import json
import time
import urllib.parse
from typing import Optional, Dict

import requests
from diskcache import Cache

from pyonedesk.server import get_code_url

ms_token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'


class Account:
    cache: Cache

    def __init__(self, id: str, name: str, client_id: str, client_secret: str):
        self.__id = id
        self.__name = name
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__refresh_token = None

    def to_json(self) -> dict:
        return {
            'id': self.__id,
            'name': self.__name,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'has_token': self.has_token and self.has_refresh_token,
            'refresh_token': self.__refresh_token}

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self.save()

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str):
        self.__client_id = value
        self.save()

    @property
    def client_secret(self) -> str:
        return self.__client_secret

    @client_secret.setter
    def client_secret(self, value: str):
        self.__client_secret = value
        self.save()

    def refresh_token(self) -> bool:
        """
        发送请求给微软，刷新Token
        :return:
        """
        data = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token'.format(
            client_id=self.__client_id,
            client_secret=self.__client_secret,
            refresh_token=self.__refresh_token,
            redirect_uri=get_code_url
        )
        res = requests.post(ms_token_url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=data)
        if res.status_code == 200:
            token = res.json()
            print('成功刷新Token', token)
            self.__refresh_token = token['refresh_token']
            self.save()
            self.__save_token(token)
            return True
        print('刷新Token错误', res.content)
        return False

    @staticmethod
    def create_redirect_url(scheme: str, host: str, id: str) -> str:
        """
        创建微软回调链接
        :param scheme:
        :param host:
        :return:
        """
        return '{scheme}://{host}/admin/api/code/{id}'.format(scheme=scheme, host=host, id=id)

    def request_token_by_code(self, code: str) -> bool:
        """
        发送请求给微软，获取Token
        :param code:
        :return:
        """
        data = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}&grant_type=authorization_code'.format(
            client_id=self.client_id, client_secret=self.client_secret,
            redirect_uri=get_code_url, code=code)
        res = requests.post(ms_token_url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=data)
        if res.status_code == 200:
            token = res.json()
            self.__refresh_token = token['refresh_token']
            self.save()
            self.__save_token(token)
            return True
        print('拿token失败', res.text)
        return False

    def __save_token(self, token: dict):
        token['time'] = int(time.time())
        self.cache.set(self.token_key, token, 3500)

    @staticmethod
    def get_accounts() -> Dict[str, Account]:
        return Account.cache.get('accounts', default={})

    @staticmethod
    def get_by_id(account_id: str) -> Optional[Account]:
        if account_id is None or account_id == '':
            return None
        if 'accounts' not in Account.cache:
            return None
        if account_id not in Account.cache['accounts']:
            return None
        return Account.cache['accounts'][account_id]

    @staticmethod
    def get_by_name(name: str) -> Optional[Account]:
        if name is None or name == '':
            return None
        accounts = Account.get_accounts()
        for account in accounts.values():
            if account.name == name:
                return account
        return None

    @staticmethod
    def delete_by_id(account_id: str) -> bool:
        accounts = Account.get_accounts()
        if account_id in accounts:
            token = accounts[account_id].token_key
            if token in Account.cache:
                del Account.cache[accounts[account_id].token_key]
            del accounts[account_id]
            Account.cache['accounts'] = accounts
            if account_id == Account.cache.get('default_account_id'):
                Account.cache.delete('default_account_id')
            return True
        return False

    @property
    def token_key(self) -> str:
        """在cache存放access_token的key"""
        return 'token-' + self.id

    @property
    def has_token(self) -> bool:
        return self.token_key in Account.cache

    @property
    def has_refresh_token(self):
        return self.__refresh_token is not None

    @property
    def token(self) -> dict:
        if self.has_token is False:
            self.refresh_token()
        return Account.cache.get(self.token_key)

    def auto_get_token(self):
        if self.has_token is False:
            self.refresh_token()

    def save(self) -> Account:
        """
        保存账号数据
        :return:
        """
        accounts = self.get_accounts()
        accounts[self.id] = self
        Account.cache['accounts'] = accounts
        return self

    def get_upload_url(self, path: str, behavior: str = 'replace'):
        path = ':{}:/createUploadSession'.format(path)
        data = json.dumps({'item': {'@microsoft.graph.conflictBehavior': behavior}})
        return self.get_item(path=path, method='post', data=data).get('uploadUrl')

    def get_item(self, path: str = None, method: str = 'get', data: str = '',
                 headers: dict = {},
                 url: str = 'https://graph.microsoft.com/v1.0/me/drive') -> Optional[dict, bytes]:
        """
        获取OneDrive文件信息
        :return:
        """
        if path is None:
            url += '/root'
        elif path == '/':
            url += 'root'
        elif path.startswith('/items/'):
            url += path
        else:
            url += '/root' + path

        headers.update(make_header(self.token.get('access_token')))
        if method.lower() == 'post':
            headers.update({'Content-Type': 'application/json'})
        print('get_item', url)
        # res = requests.get(url, headers=make_header(self.token.get('access_token')))
        res = requests.request(
            method=method, url=url, data=data,
            headers=headers)
        try:
            return res.json()
        except:
            return res.content

    def get_quota(self, url: str = 'https://graph.microsoft.com/v1.0/me/drive'):
        res = requests.get(url, headers=make_header(self.token.get('access_token')))
        # print('quota', res.json())
        return res.json()['quota']

    def create_folder(self, path: str, name: str,
                      url: str = 'https://graph.microsoft.com/v1.0/me/drive'):
        headers = make_header(self.token.get('access_token'))
        headers.update({'Content-Type': 'application/json'})
        if not path.endswith('/'):
            path += '/'
        path = urllib.parse.urljoin(path, 'children')
        url = url + path

        print('创建文件夹', path, url)
        data = {'name': name,
                'folder': {},
                '@microsoft.graph.conflictBehavior': 'replace'}
        return requests.post(url, headers=headers, data=json.dumps(data)).json()


def make_header(token: str) -> dict:
    return {'Authorization': 'bearer ' + token}
