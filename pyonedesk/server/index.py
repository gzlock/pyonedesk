import os

from sanic import Blueprint, response
from sanic.exceptions import NotFound, ServerError

from .account import Account
from .admin import get_accounts_list

res_dir = os.path.join(os.path.dirname(__file__), 'res')

index = Blueprint('index', url_prefix='/')


@index.get('/')
async def index_page(request):
    return await response.file(os.path.join(res_dir, 'index.html'))


@index.get('/accounts')
async def accounts(request):
    return await get_accounts_list(request)


@index.get('/path/<user_id:string>')
async def accounts(request, user_id: str):
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号别名')
    path = request.raw_args.get('path')
    if path is None:
        path = '/'
    elif ':/content' in path:
        raise ServerError('不支持使用:/content读取文件内容')
    data = account.get_item(path=path)
    if isinstance(data, dict):
        return response.json(data)
    return response.raw(body=data)


@index.get('/path/<user_id:string>/rename')
async def accounts(request, user_id: str):
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号别名')
    path = request.raw_args.get('path')
    if path is None:
        path = '/'
    elif ':/content' in path:
        raise ServerError('不支持使用:/content读取文件内容')
    data = account.get_item(path=path)
    if isinstance(data, dict):
        return response.json(data)
    return response.raw(body=data)


@index.post('/path/<user_id:string>/save')
async def accounts(request, user_id: str):
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号别名')
    path = request.raw_args.get('path')
    if path is None:
        path = '/'
    elif ':/content' in path:
        raise ServerError('不支持使用:/content读取文件内容')
    data = account.get_item(path=path)
    if isinstance(data, dict):
        return response.json(data)
    return response.raw(body=data)
