from selenium.common.exceptions import NoSuchElementException

from abstractWebSiteCollector import AbstractWebSiteCollector, CollectorIsBroken
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from os import listdir
from selenium.webdriver.common.proxy import Proxy, ProxyType


class HidemynaCollector(AbstractWebSiteCollector):
    def __init__(self) -> None:
        super().__init__()

    def update(self, browser, page_limit=1):
        page_counter = 1
        self.proxy_list = []
        browser.get("https://hidemyna.me/en/proxy-list/")
        self._wait_for_proxy_list(browser)
        self._collect_proxy_from_current_page(browser)

        next_page = True
        while next_page and (page_counter < page_limit):
            page_counter += 1
            # try to find "next page marker"
            try:
                next_page = browser.find_element_by_class_name("arrow__right")
            except NoSuchElementException:
                next_page = None

            if next_page:
                print("Next page...")
                next_page = next_page.find_element_by_tag_name("a")
                next_page.click()
                self._wait_for_proxy_list(browser)
                self._collect_proxy_from_current_page(browser)

    def _wait_for_proxy_list(self, browser):
        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "proxy__in"))
            )
        except:
            raise CollectorIsBroken("Main page didn't load as expected")

    def _collect_proxy_from_current_page(self, browser):
        proxy_items = browser.find_element_by_class_name("proxy").find_element_by_class_name("proxy__t") \
            .find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")

        for item in proxy_items:
            proxy_details = item.find_elements_by_tag_name("td")

            proxy = {'ip': proxy_details[0].text,
                     'port': proxy_details[1].text,
                     'location': proxy_details[2].text,
                     'type': proxy_details[4].text}

            # print(f"Add {proxy}")
            self.proxy_list.append(proxy)
