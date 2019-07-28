# coding:utf-8

import copy
import os

import appdirs
import click
from diskcache import Cache
from hurry.filesize import size

from pyonedesk import __version__
from pyonedesk.cli.commands import cli
from pyonedesk.config import config as default_config
from pyonedesk.server.account import Account
from pyonedesk.server.main import server
from pyonedesk.utils import md5, get_tree_size


appName = 'PyOneDrive'

data_dir = os.path.join(appdirs.user_data_dir(appname=appName, appauthor='gzlock'), 'data')


@click.group()
@click.version_option(version=__version__, prog_name='pyonedesk')
@click.option('--debug', is_flag=True)
@click.pass_context
def main(ctx, debug: bool):
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug

    cache = Cache(directory=data_dir)

    ctx.obj['cache'] = cache
    Account.cache = cache


@main.command('server')
@click.option(
    "--port",
    default=23333,
    type=int,
    help="define the HTTP service port, default is 23333",
)
@click.option(
    '--password',
    default='pyonedesk',
    prompt=True,
    confirmation_prompt=True,
    hide_input=True,
    type=str,
    help="set the admin password, default is pyonedesk",
)
@click.pass_obj
def create_server(obj, port: int, password: str):
    cache = obj['cache']
    _config = cache.get('config', default=None)

    if obj['debug'] == 1:
        print('启用开发环境')
        _config = None

    if _config is None:
        config = copy.deepcopy(default_config)
    else:
        config = {**default_config, **_config}
    config.update({'aes_key': md5(default_config['aes_key'])})

    obj['config'] = config

    server(obj, port, password)


@main.command('info')
def show_info():
    info = '数据目录:\t' + data_dir
    info += '\n数据容量:\t' + size(get_tree_size(data_dir))
    info += '\n账号数量:\t' + str(len(Account.get_accounts().keys()))
    click.echo(info)


main.add_command(cli)

if __name__ == '__main__':
    main(obj={})
