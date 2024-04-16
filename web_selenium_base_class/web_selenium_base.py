from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from loguru import logger

class WebSeleniumBase:
    def __init__(self):
        """配置浏览器,开启浏览器"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 无GUI界面启动浏览器
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("chrome浏览器启动成功!!!!")
        except WebDriverException as e:
            logger.error(f"基类中启动chrome时发生错误：{str(e)}")

    def fetch_webpage_content(self, url):
        """爬取网页正文,这个方法应由子类实现具体逻辑"""
        raise NotImplementedError("This method should be overridden by subclasses")

    def close_driver(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("chrome浏览器成功关闭!!!!")