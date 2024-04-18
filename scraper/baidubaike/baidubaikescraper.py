"""
Description: 
Notes: 
经测试百度百科网页的结构是变化的,但会有共性部分,含有 "J-summary",故不能使用 `By.CLASS_NAME`,需要使用 `By.CSS_SELECTOR`。
    错误示例:
    `summary = self.driver.find_element(By.CLASS_NAME, "lemmaSummary_pK63L.J-summary")`

"""
from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class BaiduBaikeScraper(WebSeleniumBase):
    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            title = self.driver.title
            # 爬取百度百科
            items = self.fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取baidubaike网页内容时发生错误：{str(e)}")
            return None, []
        return title, items

    def fetch_content(self):
        try:
            # 定位百度百科的摘要部分
            summary = self.driver.find_element(By.CSS_SELECTOR, ".J-summary")
            # 定位百度百科的正文部分
            content = self.driver.find_element(By.CSS_SELECTOR, ".J-lemma-content")
            text = summary.text + "\n" + content.text
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
            text = f"元素未找到: {str(e)}"
        return text