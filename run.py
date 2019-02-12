import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from os import listdir
from selenium.webdriver.common.proxy import Proxy, ProxyType
from hidemynaCollector import HidemynaCollector
from dataBaseMaster import DataBaseMaster

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


if __name__ == '__main__':
    main()
