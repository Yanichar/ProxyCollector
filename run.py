from dataBaseMaster import DataBaseMaster
from proxyChecker import ProxyChecker
from hidemynaCollector import HidemynaCollector
import argparse

db = DataBaseMaster()


def handle_new_proxy(proxy_list):
    print(f"Got {len(proxy_list)} proxy servers and {db.add_proxys(proxy_list)} of them is new")


def handle_collector_is_broken(msg):
    print(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_online', nargs='?', type=int, default=10000, help='How many alive proxy do you need')
    parser.add_argument('--max_age', nargs='?', type=int, default=72000, help='Max time after check to consider'
                                                                              ' proxy as alive in Seconds')
    parser.add_argument('--max_threads', nargs='?', type=int, default=10, help='Max threads to check proxy')
    parser.add_argument('--update_interval', nargs='?', type=int, default=3600, help='Interval to update proxy lists '
                                                                                     'from web sites in Seconds')

    args = parser.parse_args()

    test = HidemynaCollector(args.update_interval)
    test.new_proxy_collected_cb = handle_new_proxy
    test.collector_is_broken_cb = handle_collector_is_broken
    test.start()

    proxy_check_manager = ProxyChecker(db, min_online=args.min_online,
                                       max_age=args.max_age,
                                       max_threads=args.max_threads)
    proxy_check_manager.start()


if __name__ == '__main__':
    main()
