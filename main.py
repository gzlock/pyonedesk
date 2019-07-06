from diskcache import Cache

from create_onedrive_app import createOneDriveApp, inputInfo, getCode

port = 23333

if __name__ == '__main__':
    cache = Cache(directory='./cache')
    config = cache.get('config', default=None)

    has_client_id = has_client_secret = False

    if config is not None:
        has_client_id = 'client_id' in config and len(config['client_id']) > 0
        has_client_secret = 'client_Secret' in config and len(config['client_Secret']) > 0

    if has_client_id:
        print('client_id', config['client_id'])
    if has_client_secret:
        print('client_secret', config['client_secret'])

    if not has_client_id:
        hasKey: bool = input('已经有OneDrive的应用ID和应用机密钥匙？[y/n]').lower() == 'y'
        if hasKey:
            config = inputInfo(inputIDFirst=True)
            print('一定要检查这个应用设置：平台->重定向URL\n需要为 http://localhost:{port}\n如果不是请修改为这个值'.format(port=port))
        else:
            config = createOneDriveApp(port=port)

    cache.set('config', config)
    code = getCode(port=port, client_id=config['client_id'], cache=cache)
