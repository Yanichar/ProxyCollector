import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from os import listdir
from selenium.webdriver.common.proxy import Proxy, ProxyType
from hidemynaCollector import HidemynaCollector
from dataBaseMaster import DataBaseMaster

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    # get chromedriver from
    # https://sites.google.com/a/chromium.org/chromedriver/downloads

    with webdriver.Chrome(options=options) as browser:
        test = HidemynaCollector()

        while True:
            test.update(browser, page_limit=1)
            db = DataBaseMaster()
            print(f"Collected {len(test.proxy_list)} and {db.add_proxys(test.proxy_list)} were new")
            time.sleep(10)


if __name__ == '__main__':
    main()
