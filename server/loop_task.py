import time
from multiprocessing import Process

from diskcache import Cache

from server.account import Account


def worker(cache: Cache):
    Account.cache = cache
    while True:
        work = 0
        accounts: dict = cache.get('accounts', default={})
        for account in accounts.values():
            if account.has_token:
                continue
            account.refresh_token()
            work += 1
        print('worker 工作汇报：', work, '个账号刷新Token')
        time.sleep(30)


def main(cache: Cache):
    Process(target=worker, args=(cache,)).start()
