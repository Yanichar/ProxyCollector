from dataBaseMaster import DataBaseMaster
from proxyChecker import ProxyChecker

db = DataBaseMaster()


def handle_new_proxy(proxy_list):
    print(f"Got {len(proxy_list)} proxy servers and {db.add_proxys(proxy_list)} of them is new")


def handle_collector_is_broken(msg):
    print(msg)


def main():
    db.get_proxy_to_check()

    for i in range(10):
        test = ProxyChecker()
        test.get_next_proxy_cb = db.get_proxy_to_check
        test.check_proxy_result_cb = db.update_online_status
        test.start()

    """
    test = HidemynaCollector()
    test.new_proxy_collected_cb = handle_new_proxy
    test.collector_is_broken_cb = handle_collector_is_broken
    test.start()
    """


if __name__ == '__main__':
    main()
