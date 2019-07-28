import threading
import time

from pyonedesk.server.account import Account


class LoopTask(threading.Thread):

    def __init__(self, cache):
        threading.Thread.__init__(self)
        self.start()

    def run(self) -> None:
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
