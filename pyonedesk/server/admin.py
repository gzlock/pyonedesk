# coding:utf-8

import copy
import json
import os
import random

import requests
from diskcache import Cache
from requests import Response
from sanic import Blueprint, response
from sanic.exceptions import NotFound, ServerError
from shortuuid import ShortUUID

from pyonedesk.config import stylizes as default_stylizes
from pyonedesk.utils import upload
from .account import Account, make_header
from .utils import sha256, aes_decrypt, aes_encrypt, createAppUrl, getCodeUrl

admin = Blueprint('admin', url_prefix='/admin')
admin_api = Blueprint('admin_api', url_prefix='/admin/api')

prefix = '/admin'

res_dir = os.path.join(os.path.dirname(__file__), 'res')

__iv = 'This is an IV456'

uuid = ShortUUID()


def __checkToken(request) -> bool:
    """
    检查cookies['token']
    :param request:
    :return:
    """
    config = request.app.cache.get('config')
    token = request.cookies.get('token')
    if token is None:
        return False

    try:
        token = json.loads(aes_decrypt(config['aes_key'], token))
    except:
        return False
    return token['password'] == config['password']


@admin.get('/login')
async def admin_login_page(request):
    """
    登录页面
    :param request:
    :return:
    """
    if __checkToken(request):
        return response.redirect(admin.url_prefix)

    return await response.file(os.path.join(res_dir, 'admin_login.html'))


@admin.get('/')
async def admin_index_page(request):
    """后台首页"""
    if __checkToken(request):
        return await response.file(os.path.join(res_dir, 'admin.html'))
    return response.redirect(admin.url_prefix + '/login')


@admin.post('/login')
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
    password = request.json.get('password')
    if password is None:
        raise ServerError('缺少密码')
    password = sha256(password)
    print('登录', config['password'], password)
    print('登录', config['aes_key'])

    if config['password'] != password:
        return response.json({'code': 0})
    data = response.json({'code': 1})

    json_str = json.dumps({'password': password, 'r': random.random()})

    token = aes_encrypt(config['aes_key'], json_str)
    # print('token', type(token), token)
    data.cookies['token'] = token
    data.cookies['token']['httponly'] = True
    return data


@admin.middleware('request')
async def check_token(request):
    path: str = request.path
    # method: str = request.method.lower()
    if __checkToken(request) is False:
        res = None
        if path == '/admin':
            res = response.redirect(admin.url_prefix + '/login')
        elif path.startswith(admin_api.url_prefix):
            res = response.text('没有管理权限', status=403)
        if res is not None:
            del res.cookies['token']
            return res


@admin_api.get('/accounts')
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


@admin_api.get('/stylizes')
async def get_stylizes(request):
    """
    样式数据
    :param request:
    :return:
    """
    stylizes = copy.deepcopy(default_stylizes)
    stylizes.update(request.app.cache.get('stylizes', default={}))
    if stylizes['icon']['src'] == default_stylizes['icon']['src']:
        stylizes['icon']['src'] = ''
    res = {'default': default_stylizes, 'custom': stylizes, }
    return response.json(res)


@admin_api.post('/stylizes')
async def post_stylizes(request):
    """
    处理提交的样式数据
    :param request:
    :return:
    """
    data = request.json
    cache: Cache = request.app.cache
    cache.set('stylizes', data)
    return response.text('')


@admin_api.get('/account/<id:string>')
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
    if account.has_token:
        json['quota'] = account.get_quota()
    else:
        json['quota'] = {}
    json['default'] = default_id == id

    return response.json(json)


@admin_api.post('/account/<id:string>')
async def save_account(request, id: str):
    cache: Cache = request.app.cache
    account = Account.get_by_id(id)
    if account is None:
        raise NotFound()
    data = request.json
    default = data.get('default')
    name = data.get('name')
    code = data.get('code')
    if type(default) is bool:
        # print('默认账号')
        if default:
            cache.set('default_account_id', id)
        else:
            cache.delete('default_account_id')
    if name is not None and len(name) < 2:
        raise ServerError('账号别名的长度需要大于等于2个字符')

    accounts = Account.get_accounts().values()
    for _account in accounts:
        if _account.id != id and _account.name == name:
            raise ServerError('有其它相同别名的账号')

    if code is not None:
        state = account.request_token_by_code(code)
        if state is False:
            raise ServerError('Code无效')

    account.name = name
    account.save()
    return response.json({'code': 1})


@admin_api.get('/accounts/delete/<id:string>')
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


@admin_api.get('/account/create_id')
async def creat_account_id(request):
    accounts = Account.get_accounts()
    id: str
    while True:
        id = uuid.random(length=5)
        if id not in accounts:
            break
    return response.json({'id': id})


@admin_api.post('/accounts/add')
async def add_account(request):
    """
    添加OneDrive账号
    :param request:
    :return:
    """
    id = request.json.get('id')
    name = request.json.get('name')
    client_id = request.json.get('client_id')
    client_secret = request.json.get('client_secret')
    if len(id) != 5:
        raise ServerError('ID格式不符合规则')
    if name is None:
        raise ServerError('缺少昵称')
    elif len(name) < 2:
        raise ServerError('昵称最少需要两个字符')
    if client_id is None:
        raise ServerError('缺少client_id')
    if client_secret is None:
        raise ServerError('缺少client_secret')

    accounts = Account.get_accounts()

    if id in accounts:
        raise ServerError('已经有相同ID的账号')

    for account in accounts.values():
        if account.name == name:
            raise ServerError('已经相同别名的账号')

    account = Account(id=id, name=name, client_id=client_id, client_secret=client_secret)
    account.save()
    return response.json(account.to_json())


@admin_api.get('/code/<id:string>')
async def get_code(request, id: str):
    """
    从微软的跳转接收Code
    :param request:
    :param id:
    :return:
    """
    account = Account.get_by_id(id)
    code = request.raw_args.get('code')

    if account is None or code is None:
        return response.html('<h1>小伙子不要自己打开这个页面哟</h1>')

    state = int(account.request_token_by_code(code))
    print('接收Code', account.name, code, state)
    with open(os.path.join(res_dir, 'admin_get_code.html'), 'r', encoding='UTF-8') as file:
        html = file.read().replace("'{data}'", json.dumps(
            {'account': account.to_json(), 'state': state, 'code': code}))
        return response.html(html)


@admin_api.get('/go_create_app/<id:string>/<name:string>')
async def redirect_to_create_app_url(request, id: str, name: str):
    """
    跳转到创建微软开发应用的网址，只需要用到 别名
    :param request:
    :param id:
    :param name:
    :return:
    """
    go_url = createAppUrl(name=name)
    #  print(url, go_url)
    return response.redirect(go_url)


@admin_api.get('/go_get_code/<id:string>')
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


@admin_api.post('/upload/<user_id:string>')
async def upload_file(request, user_id: str):
    """
    从微软接口返回上传文件的url，由网页前端上传文件到微软
    :param request:
    :param user_id:
    :return:
    """
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号别名')
    path = request.raw_args.get('path')
    if path is None:
        ServerError('参数path是必须的')
    if path == '/':
        ServerError('path参数不能是/')

    content_type = request.raw_args.get('type')
    if content_type is None or content_type not in ['text', 'file']:
        ServerError('参数type是必须的，有text和file两种值')

    if content_type == 'file':
        content = request.files.get('file')
        if content is None:
            return response.text('缺少文件字段名file', status=500)
        content = content.body
    else:
        content = request.body

    if not path.startswith('/'):
        path = '/' + path

    upload_url = account.get_upload_url(path=path, behavior='replace')
    # print('上传url', upload_url)
    try:
        res = upload(upload_url, content)
        res = account.get_item(path='/items/{}?expand=thumbnails'.format(res['id']))
        return response.json(res)
    except Exception as e:
        ServerError(e)


@admin_api.delete('/<user_id:string>')
async def delete_file(request, user_id: str):
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号别名')
    path = request.raw_args.get('path')
    if path is None:
        raise ServerError('参数path是必须的')
    if path == '/':
        raise ServerError('path参数不能是/')

    info = account.get_item(':{}'.format(path))
    # print(info)
    if 'error' in info:
        raise NotFound('路径不存在')
    elif 'id' in info:
        url = 'https://graph.microsoft.com/v1.0/me/drive/items/' + info['id']
        headers = make_header(account.token['access_token'])
        # print('删除', url, headers)
        res: Response = requests.delete(url, headers=headers)
        if res.status_code == 204:
            return response.text('ok')
        else:
            raise ServerError('删除失败：{}\n原因：{}'.format(path, res.json()['error']['message']))


@admin_api.get('/create_folder/<user_id:string>')
async def create_folder(request, user_id: str):
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号别名')
    path = request.raw_args.get('path')
    name = request.raw_args.get('name')
    if path is None:
        raise ServerError('参数path是必须的')
    if name is None:
        raise ServerError('参数name是必须的')

    data = account.create_folder(path=path, name=name)
    if 'id' not in data:
        raise ServerError('创建文件夹失败')
    return response.json(data)
