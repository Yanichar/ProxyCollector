"""
This module describing interface of web site collector
"""
import threading
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from os import listdir
from selenium.webdriver.common.proxy import Proxy, ProxyType
from dataBaseMaster import DataBaseMaster

class CollectorIsBroken(Exception):
    def __init__(self, text):
        CollectorIsBroken.txt = text


class AbstractWebSiteCollector(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.url = None
        self.proxy_list = []
        self.interval = 3600
        self.error_counter = 0
        self.new_proxy_collected_cb = None
        self.collector_is_broken_cb = None

    def update(self, browser, page_limit=1):
        raise NotImplementedError

    def run(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        # get chromedriver from
        # https://sites.google.com/a/chromium.org/chromedriver/downloads

        while True:
            # print("Collector is alive")
            try:
                with webdriver.Chrome(options=options) as browser:
                    self.update(browser, page_limit=1)
                    self.error_counter = 0
                    # browser.close()
            except:
                self.error_counter += 1
                if self.error_counter > 3:
                    self.error_counter = 0
                    if self.collector_is_broken_cb is not None:
                        self.collector_is_broken_cb("Collector didn't get data 3 time in a row")

            if self.new_proxy_collected_cb is not None:
                self.new_proxy_collected_cb(self.proxy_list)

            time.sleep(self.interval)




