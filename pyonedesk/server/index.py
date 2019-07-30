import json
import os

from diskcache import Cache
from sanic import Blueprint, response
from sanic.exceptions import NotFound, ServerError

from .account import Account
from .admin import get_accounts_list
from ..config import stylizes as default_stylizes

res_dir = os.path.join(os.path.dirname(__file__), 'res')

index = Blueprint('index', url_prefix='/')


@index.get('/')
async def index_page(request):
    cache: Cache = request.app.cache
    stylizes: dict = cache.get('stylizes', default=default_stylizes)
    with open(os.path.join(res_dir, 'index.html'), 'r', encoding='UTF-8') as file:
        html = file.read()

        default_icon_src = default_stylizes['icon']['src']
        html = html.replace(
            '<!--default_icon_src-->',
            '<script src="{}"></script>'.format(default_icon_src))

        custom_icon_src = stylizes['icon']['src']
        replace = ''
        if custom_icon_src != default_icon_src:
            replace = '<script src="{}"></script>'.format(custom_icon_src)

        custom_icons = stylizes['icon']['icons']

        replace += '<script>var Icons={}</script>'.format(json.dumps(custom_icons))
        html = html.replace('<!--icon_src-->', replace)
        html = html.replace('<!--styles-->', '<style>{}</style>'.format(stylizes['css']))
    return response.html(html)


@index.get('/stylizes')
async def get_stylizes(request):
    stylizes = request.app.cache.get('stylizes', default=default_stylizes)
    data = {
        'default_icon_src': default_stylizes['icon']['src'],
        'custom_icon_src': stylizes['icon']['src'],
        'icons': stylizes['icon']['icons']
    }
    return response.json(data)


@index.get('/scripts/default_icon_script')
async def default_icon_script(request):
    return response.redirect('https:' + default_stylizes['icon']['src'])


@index.get('/scripts/custom_icon_script')
async def custom_icon_script(request):
    stylizes = request.app.cache.get('stylizes', default=default_stylizes)
    try:
        src = stylizes['icon']['src']
        if len(src) > 0:
            return response.redirect(src)
    except:
        pass
    return response.text('', status=404)


@index.get('/scripts/icons_script')
async def icons_script(request):
    stylizes = request.app.cache.get('stylizes', default=default_stylizes)
    return response.text(
        'var Icons = ' + json.dumps(stylizes['icon']['icons']),
        content_type='application/javascript')


@index.get('/style')
async def style(request):
    stylizes = request.app.cache.get('stylizes', default=default_stylizes)
    return response.text(stylizes['css'], content_type='text/css')


@index.get('/accounts')
async def get_accounts(request):
    return await get_accounts_list(request)


@index.get('/path/<user_id:string>')
async def get_path_content(request, user_id: str):
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号')
    path = request.raw_args.get('path')
    # print('读取', request.raw_args)
    if path is None:
        path = '/'
    elif ':/content' in path:
        raise ServerError('不支持使用:/content读取文件内容')
    data = account.get_item(path=path)
    if 'error' in data:
        raise ServerError(data)
    if isinstance(data, dict):
        return response.json(data)
    return response.raw(body=data)


@index.get('/download/<user_id:string>')
async def download_file(request, user_id: str):
    account: Account = Account.get_by_id(user_id)
    if account is None:
        raise NotFound('不存在的账号')
    path: str = request.raw_args.get('path')
    if path is None or path.startswith(':/') is False:
        raise ServerError('path参数不正确')
    data = account.get_item(path=path)
    if '@microsoft.graph.downloadUrl' in data:
        return response.redirect(data['@microsoft.graph.downloadUrl'])
    return ServerError('不支持下载整个文件夹')
