import webbrowser
from sanic import Sanic
from sanic.response import html, text, redirect
from multiprocessing import Process
from diskcache import Cache
import time
from progress.spinner import Spinner
from requests import get
import socket


def hasBrowser() -> bool:
    try:
        webbrowser.get()
        return True
    except:
        return False


def getWanIP() -> str:
    res = get('http://ip.360.cn/IPShare/info')
    return res.json()['ip']


def getLanIP() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def __app_url(appName: str, ip: str, port: int) -> str:
    redirectUrl = 'http://{ip}:{port}'.format(ip=ip, port=port)
    return 'https://apps.dev.microsoft.com/?referrer=https%3a%2f%2fdeveloper.microsoft.com%2fzh-cn%2fgraph%2fquick-start#/quickstart/graphIO?publicClientSupport=false&appName={appName}&redirectUrl={redirectUrl}&allowImplicitFlow=false&ru=https:%2F%2Fdeveloper.microsoft.com%2Fzh-cn%2Fgraph%2Fquick-start%3FappID%3D_appId_%26appName%3D_appName_%26redirectUrl%3D{redirectUrl}%26platform%3Doption-Python'.format(
        appName=appName, redirectUrl=redirectUrl)


def __code_url(ip: str, client_id: str, port: int) -> str:
    redirectUrl = 'http://{ip}:{port}'.format(ip=ip, port=port)
    return 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirectUrl}&scope=offline_access%20Files.ReadWrite.All%20Files.ReadWrite'.format(
        redirectUrl=redirectUrl, client_id=client_id)


def createOneDriveApp(ip: str, appName: str = 'PyOneDisk', port: int = 23333) -> dict:
    url = __app_url(ip=ip, appName=appName, port=port)

    # print(url)

    if hasBrowser():
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


def getCode(ip: str, port: int, client_id: str, cache: Cache) -> str:
    redirectUrl = 'http://localhost:{port}'.format(port=port)
    code_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirectUrl}&scope=offline_access%20Files.ReadWrite.All%20Files.ReadWrite'.format(
        redirectUrl=redirectUrl, client_id=client_id)
    print(code_url)
    print('接下来会打开网页获取Code\n如无意外，整个过程是自动的')
    print(code_url)
    if hasBrowser():
        time.sleep(0.5)
        webbrowser.open(code_url)
    else:
        print('找不到浏览器，请自行使用浏览器打开链接：')
        print(code_url)
        print('打开网页并完成相应的后需要记下【应用ID】和【应用机密钥匙】\n后续的步骤需要填入')

    cache.pop('code')
    server = Process(target=__create_http_server__, args=(ip, port, cache, code_url))
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


def __create_http_server__(port: int, cache: Cache, app_url, code_url):
    app = Sanic()

    @app.route('/create_app')
    async def index(request):
        with open('./res/create_app.html') as file:
            content = str(file.read()).format(app_url)
        return html(content)

    @app.route('/open_code')
    async def openCodeUrl(request):
        return redirect(code_url)

    @app.route('/get_code')
    async def getCode(request):
        if 'code' not in request.raw_args:
            return html('不要自己随便打开这个网页啦')
        code = request.raw_args['code']
        cache.set('code', code)
        return html('<h2>程序已经自动记录Code：{code}<br>现在您可以关闭这个页面了</h2>'.format(code=code))

    @app.route('/check_ip')
    async def ip(request):
        return text('PyOneDisk')

    app.run(port=port)
