"""
Description: 爬取csdn主页内容。
Reference Link: https://github.com/SeleniumHQ/seleniumhq.github.io/blob/trunk//examples/python/tests/drivers/test_options.py#L7-L9
Notes: 
1. 由于csdn网页页面资源极多,selenium默认会完整加载网页资源,然后再执行爬取,故耗时严重。测试爬取需要133s左右,难以接受。
2. 由于耗时严重,所以重写了爬虫基类的`__init__`方法,设置了网页加载策略。
3. 网页加载策略( `page_load_strategy` )的设置方式和常规参数不同。
4. `options.add_argument('pageLoadStrategy=none')` 这种参数设置方式无效,但不报错,需要万分注意!
"""
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
        options.page_load_strategy = 'eager'

        super().__init__(options=options)  # 调用基类构造函数并传入自定义的 options

    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(0.5)
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