from dataBaseMaster import DataBaseMaster
from proxyChecker import ProxyChecker
from hidemynaCollector import HidemynaCollector
db = DataBaseMaster()


def handle_new_proxy(proxy_list):
    print(f"Got {len(proxy_list)} proxy servers and {db.add_proxys(proxy_list)} of them is new")


def handle_collector_is_broken(msg):
    print(msg)


def main():
    test = HidemynaCollector()
    test.new_proxy_collected_cb = handle_new_proxy
    test.collector_is_broken_cb = handle_collector_is_broken
    test.start()

    proxy_check_manager = ProxyChecker(db)
    proxy_check_manager.start()


if __name__ == '__main__':
    main()
