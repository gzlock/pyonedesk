import os

from sanic import Blueprint, response

from server.admin import get_accounts_list

res_dir = os.path.join(os.path.dirname(__file__), 'res')

index = Blueprint('index', url_prefix='/')


@index.route('/')
async def index_page(request):
    return await response.file(os.path.join(res_dir, 'index.html'))


@index.route('/accounts')
async def accounts(request):
    return await get_accounts_list(request)
