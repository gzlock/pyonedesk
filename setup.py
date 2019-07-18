# coding:utf-8


import os

from setuptools import setup


# 读取文件内容
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        long_description = f.read()
    return long_description


setup(
    name='pyonedesk',  # 应用名
    version='0.0.1',  # 版本号
    author="gzlock",
    author_email="gzlock88@gmail.com",
    description="PyOneDesk",
    license="MIT",
    keywords="python onedrive web desk",
    url="https://github.com/gzlock/pyonedesk",
    long_description=read_file('./README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['python', 'python/server', 'python/cli'],
    include_package_data=True,
    install_requires=[  # 依赖列表
        'hurry.filesize',
        'click',
        'requests',
        'sanic',
        'diskcache',
        'progress',
        'pycrypto',
        'shortuuid',
        'colorama',
        'appdirs',
    ],
    entry_points={'console_scripts': ['pyonedesk = python.main:cli']},
)
