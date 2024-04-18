"""
Author: peilongchencc@163.com
Description: 利用百度搜索引擎,连网获取相关内容。
Notes: 
"""
"""
Description: 测试从百度百科获取网页标题和网页文本。
"""
from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from domain_map.domain_map_strategy import crawler_map
from url_utils.url_parse import ensure_https, extract_domain_from_url
from loguru import logger
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# 设置日志
logger.remove()
logger.add("baidu_search_result.log", rotation="1 GB", backtrace=True, diagnose=True, format="{time} {level} {message}")

class BaiduSearchScraper(WebSeleniumBase):
    def __init__(self):
        """重写基类的init,启动浏览器
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'eager'  # 默认是normal模式
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("chrome浏览器启动成功!!!!")
        except Exception as e:
            logger.error(f"启动chrome时发生错误：{str(e)}")

    def fetch_webpage_content(self, user_input):
        try:            
            self.driver.get("https://www.baidu.com/")
            # 在搜索框中输入搜索词
            search_box = self.driver.find_element(By.ID, "kw")
            search_box.send_keys(user_input)
            # 提交搜索
            search_box.send_keys(Keys.RETURN)
            # 等待页面加载完成
            self.driver.implicitly_wait(5)
            
            # 获取百度搜索结果
            items = self.fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取baidu网页内容时发生错误：{str(e)}")
            return None, []
        finally:
            self.close_driver()

        return items

    def fetch_content(self):
        fetched_content = []
        try:
            search_result = self.driver.find_elements(By.CSS_SELECTOR, '.tts-button_1V9FA')
            # 必须先收集到所有的url信息，避免定位错误导致DOM失效
            hyperlinks = [result.get_attribute('data-url') for result in search_result]

            for hyperlink in hyperlinks:
                crawl_content = self.crawl_text_content(hyperlink)
                fetched_content.append(crawl_content)
        except Exception as e:
            logger.error(f"元素未找到: {str(e)}")
        return fetched_content

    def crawl_text_content(self, hyperlink):
        """根据网址爬取文本内容
        """
        crawl_content = {}
        try:
            self.driver.get(hyperlink)
            self.driver.implicitly_wait(5)
            # 百度搜索引擎的部分网址为"重定向链接"("redirected_link"),不是"实际链接"("direct_link")。
            direct_link = self.driver.current_url
            # 域名识别
            domain = extract_domain_from_url(direct_link)
            # 根据域名选择对应的爬取类
            crawler_class = crawler_map.get(domain)
            
            logger.info(f"{direct_link} 分发到的爬虫类为:\n{crawler_class}\n")
            
            # 如果有制定爬虫策略再爬取
            if crawler_class:
                # 实例化
                crawler_instance = crawler_class(self.driver)
                # 调用类的公共方法
                title, content = crawler_instance.fetch_webpage_content(direct_link)
                crawl_content["title"] = title
                crawl_content["content"] = content
                crawl_content["source_url"] = direct_link
            else:
                crawl_content["title"] = ""
                crawl_content["content"] = ""
                crawl_content["source_url"] = ""
        except Exception as e:
            logger.error(f"执行爬取时报错: {str(e)}")
            crawl_content["title"] = ""
            crawl_content["content"] = ""
            crawl_content["source_url"] = ""
        return crawl_content

    def close_driver(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("chrome浏览器成功关闭!!!!")

if __name__ == "__main__":
    start_time = time.time()
    baidu_search = BaiduSearchScraper()
    rtn = baidu_search.fetch_webpage_content("澳亿万富豪之女在悉尼袭击案中遇害")
    logger.info(f"百度搜索的结果为:{rtn}")
    end_time = time.time() 
    execution_time = end_time - start_time 
    logger.info(f"执行时间为：{execution_time} 秒")