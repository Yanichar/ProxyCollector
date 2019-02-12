"""
This module describing interface of web site collector
"""


class CollectorIsBroken(Exception):
    def __init__(self, text):
        CollectorIsBroken.txt = text


class AbstractWebSiteCollector(object):
    def __init__(self) -> None:
        super().__init__()
        self.url = None
        self.proxy_list = []

    def update(self, browser):
        raise NotImplementedError

