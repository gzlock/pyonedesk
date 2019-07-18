# coding:utf-8


import os
import shutil

from setuptools import setup


# 读取文件内容
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        long_description = f.read()
    return long_description


clear_dir = ['./build', './dist']

for dir in clear_dir:
    if os.path.exists(dir):
        shutil.rmtree(dir)

setup(
    name='pyonedesk',  # 应用名
    version='0.0.10',  # 版本号
    author="gzlock",
    author_email="gzlock88@gmail.com",
    description="PyOneDesk",
    license="MIT",
    keywords="OneDrive Web Desk",
    url="https://github.com/gzlock/pyonedesk",
    long_description=read_file('./README.md'),
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.7',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    zip_safe=True,
    packages=['pyonedesk', 'pyonedesk.server', 'pyonedesk.cli'],
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
    entry_points={'console_scripts': ['pyonedesk = pyonedesk.main:main']},
)
