# coding:utf-8

import json
import os
import random

from diskcache import Cache
from sanic import Blueprint, response
from sanic.exceptions import Forbidden, NotFound, ServerError
from shortuuid import ShortUUID

from .account import Account
from .utils import sha256, aesDecrypt, aesEncrypt, createAppUrl, getCodeUrl

admin = Blueprint('admin', url_prefix='/admin')
admin_api = Blueprint('admin_api', url_prefix='/admin/api')

prefix = '/admin'

res_dir = os.path.join(os.path.dirname(__file__), 'res')

__iv = 'This is an IV456'

uuid = ShortUUID()


def __checkToken(request) -> bool:
    config = request.app.cache.get('config')
    token = request.cookies.get('token')
    if token is None:
        return False

    token = json.loads(aesDecrypt(config['aes_key'], token, __iv))
    return token['password'] == config['password']


@admin.route('/login')
async def admin_login_page(request):
    """
    登录页面
    :param request:
    :return:
    """
    if __checkToken(request):
        return response.redirect(admin.url_prefix)

    return await response.file(os.path.join(res_dir, 'admin_login.html'))


@admin.route('/')
async def admin_index_page(request):
    """后台首页"""
    if __checkToken(request):
        return await response.file(os.path.join(res_dir, 'admin.html'))
    return response.redirect(admin.url_prefix + '/login')


@admin.route('/login', methods=['POST'])
async def login_action(request):
    """
    ajax 登录
    :param request:
    :return:
    """
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


@admin.middleware('request')
async def check_token(request):
    path: str = request.path
    method: str = request.method.lower()
    if path == admin.url_prefix + '/login':
        pass
    elif path == '/admin' or path.startswith(admin_api.url_prefix):
        if __checkToken(request) is False:
            raise Forbidden('请登录')


@admin_api.route('/accounts')
async def get_accounts_list(request):
    """
    获取账号列表
    :param request:
    :return:
    """
    res = {}
    accounts = Account.get_accounts()
    default_id = request.app.cache.get('default_account_id')
    for account in accounts.values():
        res[account.id] = account.to_json()
        if account.id == default_id:
            res[account.id]['default'] = True
    return response.json(res)


@admin_api.route('/account/<id:string>')
async def get_account(request, id: str):
    """
    获取指定账号的信息
    :param request:
    :param id:
    :return:
    """
    account = Account.get_by_id(id)
    if account is None:
        raise NotFound('找不到对应的账号')

    default_id = request.app.cache.get('default_account_id')

    json = account.to_json()
    json['quota'] = account.get_quota()
    json['default'] = default_id == id

    return response.json(json)


@admin_api.route('/account/<id:string>', methods=['POST'])
async def save_account(request, id: str):
    cache: Cache = request.app.cache
    account = Account.get_by_id(id)
    if account is None:
        raise NotFound()
    if 'default' in request.json:
        print('默认账号', request.json['default'])
        if request.json['default']:
            cache.set('default_account_id', id)
        else:
            cache.delete('default_account_id')
    account.save()
    return response.json({'code': 1})


@admin_api.route('/accounts/delete/<id:string>')
async def delete_account(request, id: str):
    """
    删除账号
    :param request:
    :param id
    :return:
    """
    if Account.delete_by_id(id):
        return response.json({'code': 1})
    raise NotFound()


@admin_api.route('/account/create_id')
async def creat_account_id(request):
    accounts = Account.get_accounts()
    id: str
    while True:
        id = uuid.random(length=5)
        if id not in accounts:
            break
    return response.json({'id': id})


@admin_api.route('/accounts/add', methods=['POST'])
async def add_account(request):
    """
    添加OneDrive账号
    :param request:
    :return:
    """
    id = request.json['id']

    if len(id) != 5:
        raise ServerError('ID格式不符合规则')

    accounts = Account.get_accounts()

    if id in accounts:
        raise ServerError('已经相同ID的账号了')

    name = request.json['name']

    for account in accounts.values():
        if account.name == name:
            raise ServerError('已经相同别名的账号了')

    client_id = request.json['client_id']
    client_secret = request.json['client_secret']
    url = Account.create_redirect_url(scheme=request.scheme, host=request.host, id=id)

    account = Account(id=id, name=name, client_id=client_id,
        client_secret=client_secret, url=url)
    account.save()
    return response.json(account.to_json())


@admin_api.route('/code/<id:string>')
async def get_code(request, id: str):
    """
    从微软的跳转接收Code
    :param request:
    :param id:
    :return:
    """
    account = Account.get_by_id(id)

    if account is None or 'code' not in request.raw_args:
        return response.html('<h1>小伙子不要自己打开这个页面哟</h1>')

    code = request.raw_args['code']
    print('接收Code', account.name, code)
    state = int(account.request_token_by_code(code))
    with open(os.path.join(res_dir, 'admin_get_code.html'), 'r') as file:
        html = file.read().replace('{data}', json.dumps(
            {'account': account.to_json(), 'state': state, 'code': code}))
        return response.html(html)


@admin_api.route('/go_create_app/<id:string>/<name:string>')
async def redirect_to_create_app_url(request, id: str, name: str):
    """
    跳转到创建微软开发应用的网址，只需要用到 别名
    :param request:
    :param id:
    :param name:
    :return:
    """
    url = Account.create_redirect_url(scheme=request.scheme, host=request.host,
        id=id)
    go_url = createAppUrl(name=name, url=url)
    #  print(url, go_url)
    return response.redirect(go_url)


@admin_api.route('/go_get_code/<id:string>')
async def redirect_to_get_code_url(request, id: str):
    """
    跳转到微软获取Code的网址
    :param request:
    :param id:
    :return:
    """
    account = Account.get_by_id(id)
    if account is None:
        return response.html('<h1>找不到对应的账号</h1>')
    return response.redirect(getCodeUrl(account=account))
