from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class BaijiahaoScraper(WebSeleniumBase):
    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            title = self.driver.title
            # 爬取百家号
            items = self._fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取baijiahao网页内容时发生错误：{str(e)}")
            return None, []
        finally:
            self.close_driver()

        return title, items

    def _fetch_content(self):
        try:
            # 定位百家号的正文
            content = self.driver.find_element(By.CLASS_NAME, "_18p7x")
            text = content.text
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
            text = f"元素未找到: {str(e)}"
        return text