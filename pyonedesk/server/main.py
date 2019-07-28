# coding:utf-8
import os
import sys
import threading

from sanic import Sanic
from sanic.exceptions import NotFound, ServerError, Forbidden
from sanic.response import text
from shortuuid import ShortUUID

from pyonedesk.server import win_thread
from . import loop_task
from .account import Account
from .admin import admin, admin_api
from .index import index
from ..server.utils import sha256


def server(obj, port: int, password: str):
    config = obj['config']
    cache = obj['cache']

    config['password'] = sha256(password)
    cache.set('config', config)
    print('服务器 最终设置', cache.get('config'))

    app = Sanic()

    Account.cache = cache
    Account.uuid = ShortUUID()

    @app.listener('before_server_start')
    async def setup_db(app, loop):
        app.cache = cache

    @app.exception(Forbidden)
    async def _403(request, exception):
        return text(exception, status=403)

    @app.exception(NotFound)
    async def _404(request, exception):
        return text(exception, status=404)

    @app.exception(ServerError)
    async def _500(request, exception):
        return text(exception, status=500)

    app.blueprint(index)
    app.blueprint(admin)
    app.blueprint(admin_api)

    # 静态文件资源
    res_path = os.path.join(os.path.dirname(__file__), 'res', 'resources')
    app.static('/resources/', res_path)

    favicon = os.path.join(os.path.dirname(__file__), 'res', 'favicon.ico')
    app.static('/favicon.ico', favicon)

    loop_task.run(cache=cache)
    
    if 'win' in sys.platform:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=port, workers=4)
