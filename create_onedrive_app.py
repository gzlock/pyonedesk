import webbrowser
from sanic import Sanic
from sanic.response import html, text
from multiprocessing import Process
from diskcache import Cache
import time
from progress.spinner import Spinner


def __has__browser() -> bool:
    try:
        webbrowser.get()
        return True
    except:
        return False


def createOneDriveApp(appName: str = 'PyOneDisk', port: int = 23333) -> dict:
    createAppUrl = 'https://apps.dev.microsoft.com/?referrer=https%3a%2f%2fdeveloper.microsoft.com%2fzh-cn%2fgraph%2fquick-start#/quickstart/graphIO?publicClientSupport=false&appName={appName}&redirectUrl={redirectUrl}&allowImplicitFlow=false&ru=https:%2F%2Fdeveloper.microsoft.com%2Fzh-cn%2Fgraph%2Fquick-start%3FappID%3D_appId_%26appName%3D_appName_%26redirectUrl%3D{redirectUrl}%26platform%3Doption-php'

    redirectUrl = 'http://localhost:{port}'.format(port=port)

    url = createAppUrl.format(appName=appName, redirectUrl=redirectUrl)

    # print(url)

    if __has__browser():
        print('第一步，打开网页并完成相应的后需要记下应用ID和应用机密钥匙\n后续的步骤需要填入')
        time.sleep(0.5)
        webbrowser.open(url)
    else:
        print('找不到浏览器，请自行使用浏览器打开链接：')
        print(url)
        print('打开网页并完成相应的操作后需要记下【应用ID】和【应用机密钥匙】\n后续的步骤需要填入')

    return inputInfo()


def inputInfo(inputIDFirst: bool = False) -> dict:
    if inputIDFirst:
        client_id = input('输入应用ID：')
        client_secret = input('输入应用机密钥匙：')
    else:
        client_secret = input('输入应用机密钥匙：')
        client_id = input('输入应用ID：')

    data = {'client_id': client_id, 'client_secret': client_secret}
    return data


def getCode(port: int, client_id: str, cache: Cache) -> str:
    redirectUrl = 'http://localhost:{port}'.format(port=port)
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirectUrl}&scope=offline_access%20Files.ReadWrite.All%20Files.ReadWrite'.format(
        redirectUrl=redirectUrl, client_id=client_id)
    print(url)
    print('接下来会打开网页获取Code\n如无意外，整个过程是自动的')
    print(url)
    if __has__browser():
        time.sleep(0.5)
        webbrowser.open(url)
    else:
        print('找不到浏览器，请自行使用浏览器打开链接：')
        print(url)
        print('打开网页并完成相应的后需要记下【应用ID】和【应用机密钥匙】\n后续的步骤需要填入')

    cache.pop('code')
    server = Process(target=__create_http_server__, args=(port, cache))
    server.start()
    spinner = Spinner('等待返回Code ')
    while True:
        spinner.next()
        code = cache.get('code', default=None)
        if code is not None:
            server.kill()
            cache.pop('code')
            return code
        time.sleep(0.2)


def __create_http_server__(port: int, cache: Cache):
    app = Sanic()

    @app.route('/create_app')
    async def index(request):
        return html('')

    @app.route('/open_code')
    async def openCodeUrl(request):
        return html('')

    @app.route('/get_code')
    async def getCode(request):
        if 'code' not in request.raw_args:
            return html('不要自己随便打开这个网页啦')
        code = request.raw_args['code']
        cache.set('code', code)
        return html('<h2>程序已经自动记录Code：{code}<br>现在您可以关闭这个页面了</h2>'.format(code=code))

    app.run(port=port)
