from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class CsdnScraper(WebSeleniumBase):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('pageLoadStrategy=eager')  # 添加 eager 加载策略

        super().__init__(options=options)  # 调用基类构造函数并传入自定义的 options
        # self.driver.implicitly_wait(10)  # 设置隐式等待10秒

    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            title = self.driver.title
            # 爬取csdn
            items = self._fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取csdn网页内容时发生错误：{str(e)}")
            return None, []
        finally:
            self.close_driver()

        return title, items

    def _fetch_content(self):
        try:
            # 定位csdn的正文
            content = self.driver.find_element(By.ID, "content_views")
            text = content.text
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
        return text