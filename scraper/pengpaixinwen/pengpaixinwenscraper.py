from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class PengpaixinwenScraper(WebSeleniumBase):
    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            title = self.driver.title
            # 爬取澎湃新闻
            items = self.fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取澎湃新闻网页内容时发生错误：{str(e)}")
            return None, []
        return title, items

    def fetch_content(self):
        try:
            # 定位澎湃新闻的正文部分
            content = self.driver.find_element(By.CLASS_NAME, "index_cententWrap__Jv8jK")
            text = content.text
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
            text = f"元素未找到: {str(e)}"
        return text