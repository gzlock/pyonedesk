# coding:utf-8
from diskcache import Cache
from sanic import Sanic
from .admin import admin, adminLogin


def create(cache: Cache, port: int):
    app = Sanic()

    @app.listener('before_server_start')
    async def setup_db(app, loop):
        app.cache = cache

    app.blueprint(admin)
    app.blueprint(adminLogin)

    app.run(host='0.0.0.0', port=port)
