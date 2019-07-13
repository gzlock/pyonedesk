from setuptools import setup, find_packages

setup(
    name='pyonedrive',  # 应用名
    version='0.0.1',  # 版本号
    author="gzlock",
    author_email="gzlock88@gmail.com",
    description="PyOneDrive",
    license="MIT",
    keywords="python onedrive multi account",
    url="https://github.com/gzlock/pyonedrive",

    # packages=find_packages(include=['./main.py', './config.py', 'cli', 'server'], exclude=['test']),
    packages=find_packages(),
    scripts=['main.py'],
    data_files=['config.py'],
    package_dir={
        '': './',
        'cli': 'cli',
        'server': 'server'
    },
    package_data={
        'server': ['res/*.html',
                   'res/resources/css/*',
                   'res/resources/fonts/*',
                   'res/resources/js/*']
    },
    exclude_package_data={'cli': ['__pycache__'], 'server': ['__pycache__']},
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
    ]
)
