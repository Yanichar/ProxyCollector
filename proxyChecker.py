import threading
import time
import requests


class ProxyChecker(threading.Thread):
    """
    This module checks proxy for online and speed
    It uses request instead of selenium because of memory consumption
    """
    def __init__(self):
        super().__init__()
        self.get_next_proxy_cb = None
        self.check_proxy_result_cb = None

    def run(self):
        while True:
            if self.get_next_proxy_cb and self.check_proxy_result_cb:
                proxy = self.get_next_proxy_cb()

                if proxy is not None:
                    online, latency = self._check_online(proxy)
                    self.check_proxy_result_cb(proxy["id"], online, latency)
                else:
                    time.sleep(1)
            else:
                # just for case if no callback will be set before self.start() will be called
                time.sleep(10)

    def _check_online(self, proxy):
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
            s.get('https://2ip.ru/', proxies=proxies)
            latency = time.time() - start_time
            print("Online:", proxy)
            return "Online", latency
        except:
            print("Offline:", proxy)
            return "Offline", 0

