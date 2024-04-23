"""
Description: 爬取github每日热门仓库。
Notes: 
github每日热门仓库没有写每日更新时间,推测一般都是午夜0点更新,为自己上班查看方便,需配合crontab每日9点爬取。
"""
from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class SeleniumScraper(WebSeleniumBase):
    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(0.5)
            title = self.driver.title
            # 爬取github每日热门仓库
            items = self.fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取github网页内容时发生错误：{str(e)}")
            return None, []
        return title, items

    def fetch_content(self):
        items = []
        try:
            # 尝试抓取内容
            items = self.driver.find_element(By.CSS_SELECTOR, ".td-content")
            items = [items.text]
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
            # 保证项目结构中这里的格式统一
            items = []
        return items