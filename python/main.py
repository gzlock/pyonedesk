# coding:utf-8

import copy

import click
from diskcache import Cache

from python.cli import commands
from python.config import config as default_config
from python.server.account import Account
from python.server.main import server
from python.server.utils import md5

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

if __name__ == '__main__':
    cli(obj={})
