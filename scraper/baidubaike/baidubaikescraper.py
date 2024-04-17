from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class BaiduBaikeScraper(WebSeleniumBase):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'eager'

        super().__init__(options=options)  # 调用基类构造函数并传入自定义的 options
    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            title = self.driver.title
            # 爬取百度百科
            items = self._fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取baidubaike网页内容时发生错误：{str(e)}")
            return None, []
        finally:
            self.close_driver()

        return title, items

    def _fetch_content(self):
        try:
            # 定位百度百科的摘要部分
            summary = self.driver.find_element(By.CLASS_NAME, "lemmaSummary_pK63L.J-summary")
            # 定位百度百科的正文部分
            content = self.driver.find_element(By.CLASS_NAME, "J-lemma-content")
            text = summary.text + "\n" + content.text
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
            text = f"元素未找到: {str(e)}"
        return text