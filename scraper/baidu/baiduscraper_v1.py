from web_selenium_base_class.web_selenium_base import WebSeleniumBase
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
            items = self.fetch_hot_search()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取baidu网页内容时发生错误：{str(e)}")
            return None, []
        return title, items

    def fetch_hot_search(self):
        items = []
        try:
            # 定位热搜
            elements = self.driver.find_elements(By.XPATH, '//ul[@id="hotsearch-content-wrapper"]/li/a')
            for element in elements:
                item_text = element.text
                # 获取热搜的网址,注意:百度热搜链接的网址是百度引擎搜索界面,不是具体的信息界面。
                item_href = element.get_attribute('href')
                if item_href:
                    items.append({'text': item_text, 'href': item_href})
            # 点击 "换一换" 获取下一批热搜
            refresh_button = self.driver.find_element(By.ID, "hotsearch-refresh-btn")
            refresh_button.click()

            elements = self.driver.find_elements(By.XPATH, '//ul[@id="hotsearch-content-wrapper"]/li/a')
            for element in elements:
                item_text = element.text
                item_href = element.get_attribute('href')
                if item_href:
                    
                    items.append({'text': item_text, 'href': item_href})
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
            # 报错只是追加为空,避免程序中断
            items.append({'text': '', 'href': ''})
        except WebDriverException as e:
            logger.error(f"在点击'换一换'后, 发生错误: {str(e)}")
            # 报错只是追加为空,避免程序中断
            items.append({'text': '', 'href': ''})
        return items

    def fetch_hot_search_exact_info(self, item_href):
        """获取热搜话题具体内容
        """
        # 单个热搜的具体内容
        hot_search_exact_info = []
        # 获取百度热搜对应的百度搜索引擎界面中所有的超链接
        hyperlinks = self.fetch_hot_search_hyperlinks(item_href)
        # 根据超链接爬取内容
        return hot_search_exact_info

    def fetch_hot_search_hyperlinks(self, item_href):
        """获取热搜话题对应的百度搜索界面第一页中的所有网址
        """
        hyperlinks = []
        try:
            self.driver.get(item_href)
            self.driver.implicitly_wait(5)
            hot_search_info = self.driver.find_elements(By.CSS_SELECTOR, '.tts-button_1V9FA')
            for each_hot_search_info in hot_search_info:
                hyperlink = each_hot_search_info.get_attribute('data-url')  # 获取tpl属性
                hyperlinks.append(hyperlink)
        except NoSuchElementException:
            hyperlinks = []
        return hyperlinks

    def crawl_text_content(self, hyperlink):
        """根据网址爬取文本内容
        """
        # "实际链接"为"direct_link"，而"重定向链接"为"redirected_link"。
        
        url_content = {}
        try:
            self.driver.get(hyperlink)
            self.driver.implicitly_wait(5)
            # 百度搜索引擎的部分网址为"重定向链接"("redirected_link"),不是"实际链接"("direct_link")。
            direct_link = self.driver.current_url
            
            # 根据域名选择合适的爬取策略。
            
        except NoSuchElementException:
            hyperlinks = []
        return hyperlinks