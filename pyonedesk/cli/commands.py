import os

import click
import requests
from click import Context
from diskcache import Cache
from hurry.filesize import size
from requests import Response

from ..server.account import Account
from ..utils import upload


@click.group()
@click.option('--select', '-s', 'select_account_name', default='', help='要进行后续操作的账号别名')
@click.pass_context
def cli(ctx: Context, select_account_name: str):
    obj: dict = ctx.obj
    cache: Cache = obj['cache']
    # 没有输入--select 参数，使用默认账号

    obj['default_account'] = Account.get_by_id(cache.get('default_account_id'))
    obj['select_account'] = None

    if select_account_name == '':
        obj['select_account'] = None
    else:
        account: Account = Account.get_by_name(select_account_name)
        if account is None:
            click.secho('没有别名为 {} 的账号'.format(select_account_name), fg='red')
            exit(1)
        obj['select_account'] = account


@cli.command('accounts')
@click.pass_obj
def account_list(obj: dict):
    accounts = Account.get_accounts().values()
    if len(accounts) == 0:
        click.echo('账号列表为空')
    else:
        default_id = obj['default_account'].id if obj['default_account'] else None
        names = ['*' + account.name if account.id == default_id else account.name
                 for account in accounts]
        click.echo('账号别名列表：[ {} ]\n有*的是默认账号'.format(', '.join(names)))


@cli.command('default')
@click.pass_obj
def set_default_account(obj: dict):
    cache: Cache = obj['cache']
    account = obj['select_account']
    if account is None:
        click.secho('请使用--select 选择要操作的账号', fg='red')
        exit(1)
    cache.set('default_account_id', account.id)
    click.secho('成功将账号 {} 设置为默认账号'.format(account.name), fg='green')


@cli.command('delete')
@click.pass_obj
def delete_account(obj: dict):
    account = obj['select_account']
    if account is None:
        click.secho('请使用--select 选择要操作的账号', fg='red')
        exit(1)
    if click.confirm('确认删除账号 {} ？'.format(account.name)):
        Account.delete_by_id(account.id)


def __get_account_or_exit(obj: dict) -> Account:
    if obj['default_account'] is None and obj['select_account'] is None:
        click.secho('没有默认账号也没有选择账号，不能进行后续操作', fg='red')
        exit(1)
    account = obj['select_account'] if obj['select_account'] is not None else obj['default_account']

    account.auto_get_token()
    return account


def __cd_path(obj: dict, account: Account, path: str) -> str:
    if path.startswith('/'):
        return path
    key = 'account-{}-cd'.format(account.id)
    cache: Cache = obj['cache']
    return cache.get(key, default='') + '/' + path


@cli.command('cd')
@click.argument('path', type=str, default='')
@click.pass_obj
def cd(obj: dict, path: str):
    account: Account = __get_account_or_exit(obj=obj)
    if path == '':
        click.echo('当前目录：{}'.format(__cd_path(obj, account, path)))
        exit(0)

    path = __cd_path(obj, account, path)

    print('cd', path)

    cache: Cache = obj['cache']
    key = 'account-{}-cd'.format(account.id)
    # 保存当前目录
    cache.set(key, path)


def __file_name(file: dict) -> str:
    name = file['name']
    if 'folder' in file:
        name += '/'
    return name


@cli.command('ls')
@click.pass_obj
def ls(obj: dict):
    account: Account = __get_account_or_exit(obj=obj)
    path = __cd_path(obj=obj, account=account, path='')
    path += '/children'
    data = account.get_item(path=path)
    files: list = data['value']
    # print(json.dumps(files, sort_keys=True, indent=4, separators=(',', ':')))
    files = [*map(__file_name, files)]
    click.echo(' '.join(files))


def make_header(token: str) -> dict:
    return {'Authorization': 'bearer ' + token}


@cli.command('upload')
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('target_path', type=str, default='')
@click.option('--force', '-f', 'force', is_flag=True)
@click.pass_obj
def upload_file(obj: dict, file_path: str, target_path: str, force: bool):
    print({'obj': obj, 'target_path': target_path, 'force': force})
    if os.path.exists(file_path) is False:
        click.secho('{} 不存在', fg='red')
        exit(1)
    if os.path.isdir(file_path):
        click.secho('{} 是文件夹，不能上传', fg='red')
        exit(1)
    account = __get_account_or_exit(obj=obj)
    path = __cd_path(obj=obj, account=account, path=target_path)
    print('上传目录', path)
    file_name = os.path.basename(file_path)

    token = account.token
    headers = make_header(token=token['access_token'], )
    headers['Content-Type'] = 'application/json'
    behavior = 'replace' if force else 'fail'
    if not path.endswith('/'):
        path += '/'
    path += file_name
    account.get_upload_url(path=path, behavior=behavior)
    url = 'https://graph.microsoft.com/v1.0/me/drive/root:{}:/createUploadSession'.format(path)
    print('url', url)

    upload_url = account.get_upload_url(path=path, behavior=behavior)
    try:
        upload(upload_url, file_path)
        click.secho('上传成功：' + path, fg='green')
    except Exception as e:
        click.secho('上传失败：{}\n原因：{}'.format(path, e), fg='red')


@cli.command('rm')
@click.argument('path', type=str)
@click.pass_obj
def delete_path(obj: dict, path: str):
    if path is None:
        click.secho('缺少要删除的路径参数', fg='red')
        exit(1)
    if path == '/':
        click.secho('不能删除根目录', fg='red')
        exit(1)

    account: Account = __get_account_or_exit(obj)

    path = __cd_path(obj, account, path)

    info = account.get_item(':{}'.format(path))
    # print(info)
    if 'error' in info:
        click.secho('路径不存在', fg='red')
    elif 'id' in info:
        url = 'https://graph.microsoft.com/v1.0/me/drive/items/' + info['id']
        headers = make_header(account.token['access_token'])
        # print('删除', url, headers)
        res: Response = requests.delete(url, headers=headers)
        if res.status_code == 204:
            click.secho('成功删除：' + path, fg='green')
        else:
            click.secho('删除失败：{}\n原因：{}'.format(path, res.json()['error']['message']), fg='red')


@cli.command('get')
@click.argument('path', type=str)
@click.pass_obj
def get_item(obj: dict, path: str):
    if path is None:
        click.secho('缺少要删除的路径参数', fg='red')
        exit(1)

    account: Account = __get_account_or_exit(obj)

    if path.startswith('/') is False:
        path = __cd_path(obj, account, path)

    info = account.get_item(':{}'.format(path))
    if 'error' in info:
        click.secho('路径不存在：{}\n{}'.format(path, info['error']['message']), fg='red')
    elif 'id' in info:
        # print(info)
        is_folder = 'folder' in info
        data = '名称：\t{}\n路径：\t{}\n文件类型：{}'.format(info['name'], path, '文件夹' if is_folder else '文件')
        data += '\n大小：\t' + size(info['size'])
        if is_folder is False:
            data += '\nhash：\t' + info['file']['hashes']['sha1Hash']
            data += '\n下载链接：' + info['@microsoft.graph.downloadUrl']
        click.secho(data)
