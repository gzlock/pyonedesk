import os

import click
import pytest
from click.testing import CliRunner
from diskcache import Cache

from ..cli import commands
from ..server.account import Account


@click.group()
@click.version_option(version='0.0.1', prog_name='pyonedesk')
@click.option('--debug', default=False, help="debug mode", type=bool)
@click.pass_context
def main(ctx, debug: bool):
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    cache = Cache(directory='./cache')
    ctx.obj['cache'] = cache
    Account.cache = cache


main.add_command(commands.cli)


@pytest.fixture(scope='function')
def runner(request):
    print('\n')
    return CliRunner()


def test_show_account_list(runner):
    print('显示账号列表 测试')
    result = runner.invoke(main, ['cli', 'accounts'])
    print('结果', result.output)


def test_set_default_account(runner):
    print('设置默认账号 测试')

    # 不输入别名
    result = runner.invoke(main, ['cli', 'default'])
    print('不输入别名 结果', result.output)

    # 设置不存在的别名 abc 为默认账号
    result = runner.invoke(main, ['cli', '--select=abc' 'default'])
    print('结果', result.output)

    # 设置已存在的别名 123 为默认账号
    result = runner.invoke(main, ['cli', '-s=123', 'default'])
    print('结果', result.output)


def test_cd_ls(runner):
    # cd 选择文件夹 和 ls 列出文件夹内项目 测试
    result = runner.invoke(main, ['cli', 'cd'])
    print('cd无路径参数', result.output)

    result = runner.invoke(main, ['cli', 'cd', '/'])
    result = runner.invoke(main, ['cli', 'ls'])
    print('结果', result.output)


def atest_upload_file(runner):
    # ⚠️测试用的上传文件不包含在github项目里
    file1 = os.path.abspath('./upload_test.zip')  # 文件大小超过 10M
    file2 = os.path.abspath('./upload_test_1.zip')  # 文件的大小少于 10M

    result = runner.invoke(main, ['cli', 'cd', '/测试a'])
    print('切换目录', result.output)
    result = runner.invoke(main, ['cli', 'upload', file1, '/', '-f'])
    print('第1个文件', result.output)
    #
    # result = runner.invoke(main, ['cli', 'cd', '/测试', 'upload', file2, '--force', ])
    # print('第2个文件', result.output)


# 函数名前加个a，已经测试过并且不需要再测试了
def atest_delete_path(runner):
    print('删除文件 测试')

    # 不存在的文件夹
    result = runner.invoke(main, ['cli', 'rm', '/测试a'])
    assert 'error' in result.output

    # 真实存在的文件夹
    result = runner.invoke(main, ['cli', 'rm', '/测试'])
    print(result.output)


def test_get(runner):
    print('获取路径信息 测试')

    # 不存在的文件夹
    result = runner.invoke(main, ['cli', 'get', '/测试a'])
    print(result.output)

    # 真实存在的文件夹
    result = runner.invoke(main, ['cli', 'cd', '/测试'])
    result = runner.invoke(main, ['cli', 'get', 'upload_test.zip'])
    print(result.output)
