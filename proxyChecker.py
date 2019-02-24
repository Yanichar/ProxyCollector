import random
import threading
import time
import requests
from multiprocessing.dummy import Pool as ThreadPool

SECONDS_PER_DAY = 60 * 60 * 24


class ProxyChecker(threading.Thread):
    """
    This module checks proxy for online and speed
    It uses request instead of selenium because of memory consumption
    """
    def __init__(self, db, min_online=10000, max_age=72000, max_threads=10):
        super().__init__()
        self.get_next_proxy_cb = None
        self.check_proxy_result_cb = None
        self.db = db
        self.min_online = min_online
        self.max_age = max_age
        self.max_threads = max_threads

    def run(self):
        while True:
            alive_proxy_count = self.db.get_alive_proxy_count(self.max_age)
            number_proxy_to_check = 0

            if alive_proxy_count < self.min_online:
                # we use +20% to reduce number of check cycles
                number_proxy_to_check = int((self.min_online - alive_proxy_count) * 1.2)

            print(f"Alive proxy count:{alive_proxy_count}, we need to check {number_proxy_to_check} proxy")

            if number_proxy_to_check > self.max_threads:
                number_proxy_to_check = self.max_threads

            # check all unchecked proxy
            proxy_list = self.db.get_unchecked_proxy(number_proxy_to_check)

            # we use random number of proxy to check
            proxy_list += self.db.get_alive_proxy(number_proxy_to_check, SECONDS_PER_DAY * 365)
            proxy_list += self.db.get_dead_proxy(number_proxy_to_check, SECONDS_PER_DAY * 365)

            # TODO: some optimize her: we dont't need to collect more then 'number_proxy_to_check'
            proxy_list = proxy_list[:number_proxy_to_check]

            pool = ThreadPool(self.max_threads)
            results = pool.map(self._check_online, proxy_list)
            pool.close()
            pool.join()
            # self._print_check_result(results)
            self.db.update_db_by_results_list(results)

            time.sleep(1)

    @staticmethod
    def _check_online(proxy):
        start_time = time.time()
        try:
            s = requests.Session()
            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
            })

            # cut type after "," and convert to lower: "HTTP, SOCKS4" => "http"
            proxy_type = proxy["type"][proxy["type"].find(",") + 1 : ].lower()

            proxies = {}
            if proxy_type == "socks4" or proxy_type == "socks5":
                proxies = {'http': f'{proxy_type}://{proxy["ip"]}:{proxy["port"]}',
                           'https': f'{proxy_type}://{proxy["ip"]}:{proxy["port"]}'}

            elif proxy_type == "http" or proxy_type == "https":
                proxies = {'http': f'{proxy["ip"]}:{proxy["port"]}',
                           'https': f'{proxy["ip"]}:{proxy["port"]}'}

            # TODO: It is better to use http://... address for http proxy
            s.get('https://2ip.ru/', proxies=proxies, timeout=30)
            latency = time.time() - start_time
            # print("Online:", proxy)

            result = {'id': proxy['id'], 'online': "Online", 'latency': latency}
            return result
        except:
            # print("Offline:", proxy)
            result = {'id': proxy['id'], 'online': "Offline", 'latency': 0}
            return result

