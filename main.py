# coding:utf-8

import copy

import click
from diskcache import Cache

from cli import commands
from config import config as default_config
from server.account import Account
from server.main import server
from server.utils import md5

appName = 'PyOneDrive'


@click.group()
@click.version_option(version='0.0.1', prog_name='pyonedrive')
@click.option('--debug', default=False, help="debug mode", type=bool)
@click.pass_context
def cli(ctx, debug: bool):
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    cache = Cache(directory='./cache')
    ctx.obj['cache'] = cache
    Account.cache = cache


@cli.command('server')
@click.option("--port", default=23333, help="define the HTTP service port, default is 23333",
    type=int)
@click.option('--password', default='pyonedrive', prompt=True, confirmation_prompt=True,
    hide_input=True, help="set the admin password, default is pyonedrive", type=str)
@click.pass_obj
def create_server(obj, port: int, password: str):
    cache = obj['cache']
    config = cache.get('config', default=None)

    if obj['debug'] == 1:
        print('启用开发环境')
        config = None

    if config is None:
        config = copy.deepcopy(default_config)
        config['aes_key'] = md5(config['aes_key'])
    else:
        config = {**default_config, **config}

    obj['config'] = config

    server(obj, port, password)


cli.add_command(commands.cli)

# @cli.command(name='server')
# @click.option("--port", default=23333, help="define the HTTP service port, default is 23333")
# @click.option('--password', default='pyonedrive', prompt=True, confirmation_prompt=True,
#     hide_input=True, help="set the admin password, default is pyonedrive")
# @click.option('--debug', default=0, help="debug mode")
# @click.pass_context
# def server(ctx, port: int, password: str, debug: int):
#     config = ctx.cache.get('config', default=None)
#
#     # 开发环境，不使用缓存数据
#     if debug == 1:
#         print('开发环境', port, password)
#         config = None
#
#     if config is None:
#         config = copy.deepcopy(default_config)
#         config['aes_key'] = md5(config['aes_key'])
#     else:
#         config = {**default_config, **config}
#
#     config['password'] = sha256(password)
#     cache.set('config', config)
#     print('最终设置', cache.get('config'))
#     server.create(cache, port)
#     return
#
#     has_client_id = has_client_secret = False
#
#     if config is not None:
#         has_client_id = 'client_id' in config and len(config['client_id']) > 0
#         has_client_secret = 'client_Secret' in config and len(config['client_Secret']) > 0
#
#     if has_client_id:
#         print('client_id', config['client_id'])
#     if has_client_secret:
#         print('client_secret', config['client_secret'])
#
#     if not has_client_id:
#         hasKey = input('已经有OneDrive的应用ID和应用机密钥匙？[y/n]').lower() == 'y'
#         if hasKey:
#             config = inputInfo(inputIDFirst=True)
#             print('一定要检查这个应用设置：平台->重定向URL\n需要为 http://localhost:{port}\n如果不是请修改为这个值'.format(
#                 port=port))
#         else:
#             config = createOneDriveApp(appName=appName, port=port)
#
#     config['appName'] = appName
#     cache.set('config', config)
#     code = getCode(port=port, client_id=config['client_id'], cache=cache)


if __name__ == '__main__':
    cli(obj={})
