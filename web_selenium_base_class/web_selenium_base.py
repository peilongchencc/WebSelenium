from selenium.common.exceptions import WebDriverException
from loguru import logger

class WebSeleniumBase:
    def __init__(self, driver):
        """传入浏览器驱动
        """
        self.driver = driver

    def fetch_webpage_content(self, url):
        """爬取网页正文,这个方法应由子类实现具体逻辑"""
        raise NotImplementedError("This method should be overridden by subclasses")