# coding:utf-8

import json
import os
import random
import requests

from sanic import Blueprint, response

from .utils import sha256, aesDecrypt, aesEncrypt
from diskcache import Cache

admin = Blueprint('admin')
adminLogin = Blueprint('login')

prefix = '/admin'

res_dir = os.path.join(os.path.dirname(__file__), 'res', 'admin')

__iv = 'This is an IV456'


def __checkToken(request) -> bool:
    config = request.app.cache.get('config')
    token = request.cookies.get('token')
    if token is None:
        return False

    token = json.loads(aesDecrypt(config['aes_key'], token, __iv))
    return token['password'] == config['password']


@adminLogin.route(prefix + '/login', methods=['GET'])
async def loginPage(request):
    if __checkToken(request):
        return response.redirect(prefix)

    return await response.file(os.path.join(res_dir, 'login.html'))


@adminLogin.route(prefix + '/login', methods=['POST'])
async def loginAction(request):
    code = {'code': 0}
    if __checkToken(request):
        code['code'] = 1
        return response.json(code)

    config = request.app.cache.get('config')
    password = sha256(request.json['password'])
    print('登录', config['password'], password)
    print('登录', config['aes_key'])

    if config['password'] != password:
        return response.json({'code': 0})
    data = response.json({'code': 1})

    json_str = json.dumps({'password': password, 'r': random.random()})

    data.cookies['token'] = aesEncrypt(config['aes_key'], json_str, __iv)
    data.cookies['token']['httponly'] = True
    return data


# 检查所有/admin的网络请求是否有token
@admin.middleware('request')
async def checkToken(request):
    # print('admin 中间件')
    path = request.path
    method = request.method.lower()

    if path == prefix + '/login':
        pass
    else:
        if __checkToken(request) is False:
            res = response.redirect(prefix + '/login')
            del res.cookies['token']
            return res


@admin.route(prefix)
async def index(request):
    accounts: dict = request.app.cache.get('accounts', default=[])
    create_app_url = ''
    code_url = ''
    with open(os.path.join(res_dir, 'index.html'), 'r') as file:
        html = file.read() \
            .replace('{accounts}', json.dumps(accounts)) \
            .replace('{create_app_url}', create_app_url) \
            .replace('{code_url}', code_url)
        return response.html(html)


@admin.route(prefix + '/accounts')
async def getAccounts(request):
    accounts: dict = request.app.cache.get('accounts', default=[])
    return response.json(accounts)


@admin.route(prefix + '/accounts/add', methods=['POST'])
async def addAccount(request):
    cache: Cache = request.app.cache
    name = request.json['name']
    client_id = request.json['client_id']
    client_secret = request.json['client_secret']
    code = request.json['code']

    redirect_uri = '{scheme}://{host}/admin/get_code'.format(scheme=request.scheme, host=request.hot)
    data = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}&grant_type=authorization_code'.format(
        client_id=client_id, client_secret=client_secret, code=code, redirect_uri=redirect_uri)

    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    res = requests.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    print('验证code', res.json())
    accounts: list = cache.get('accounts', default=[])
    accounts.append({'name': name, 'client_id': client_id, 'client_secret': client_secret, 'token': res.json()})
    cache.set('accounts', accounts)
    return response.json({code: 1})


@admin.route(prefix + '/account/test', methods=['POST'])
async def testAccount(request):
    name = request.json['name']
    client_id = request.json['client_id']
    redirect_uri = '{scheme}://{host}/admin/get_code'.format(scheme=request.scheme, host=request.hot)
    scope = 'offline_access files.readwrite'
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&scope={scope}&response_type=code&redirect_uri={redirect_uri}'.format(
        client_id=client_id, scope=scope, redirect_uri=redirect_uri)
    return response.json({'url': url})
