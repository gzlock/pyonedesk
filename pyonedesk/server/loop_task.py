import time
from multiprocessing import Process

from diskcache import Cache

from .account import Account


def worker(cache: Cache):
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


def main(cache: Cache):
    try:
        Process(target=worker, args=(cache,)).start()
    except:
        pass
