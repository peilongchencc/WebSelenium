from ..web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class BaiduScraper(WebSeleniumBase):
    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            title = self.driver.title
            # 爬取百度热搜
            items = self._fetch_hot_search()
        except WebDriverException as e:
            logger.error(f"在使用Selenium时发生错误：{str(e)}")
            return None, []
        finally:
            self.close_driver()

        return title, items

    def _fetch_hot_search(self):
        items = []
        try:
            # 定位热搜
            elements = self.driver.find_elements(By.XPATH, '//ul[@id="hotsearch-content-wrapper"]/li/a')
            for element in elements:
                item_text = element.text
                # 获取热搜的网址,注意:百度热搜链接的网址是百度引擎搜索界面,不是具体的信息界面。
                item_href = element.get_attribute('href')
                items.append({'text': item_text, 'href': item_href})
            # 点击 "换一换" 获取下一批热搜
            refresh_button = self.driver.find_element(By.ID, "hotsearch-refresh-btn")
            refresh_button.click()

            elements = self.driver.find_elements(By.XPATH, '//ul[@id="hotsearch-content-wrapper"]/li/a')
            for element in elements:
                item_text = element.text
                item_href = element.get_attribute('href')
                items.append({'text': item_text, 'href': item_href})
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
        except WebDriverException as e:
            logger.error(f"在点击'换一换'后, 发生错误: {str(e)}")
        
        return items