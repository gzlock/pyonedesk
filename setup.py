from setuptools import setup

setup(
    name='pyonedrive',  # 应用名
    version='0.0.1',  # 版本号
    author="gzlock",
    author_email="gzlock88@gmail.com",
    description="PyOneDrive",
    license="MIT",
    keywords="python onedrive multi account",
    url="https://github.com/gzlock/pyonedrive",
    # zip_safe=False,
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
    entry_points={'console_scripts': ['pyonedrive = python.main:cli']},
)
