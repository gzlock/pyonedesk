import sys
import threading
import time
from multiprocessing import Process

from diskcache import Cache

from .account import Account


def worker(cache):
    # print('干活啦')
    Account.cache = cache
    while True:
        work = 0
        accounts: [] = Account.get_accounts().values()
        for account in accounts:
            if account.has_refresh_token is False or account.has_token is True:
                continue
            account.refresh_token()
            work += 1
        print('worker 工作汇报：', work, '个账号刷新Token')
        time.sleep(30)


def run(cache: Cache):
    if 'win' in sys.platform:
        threading.Thread(target=worker, args=(cache,)).start()
    else:
        Process(target=worker, args=(cache,)).start()
