"""
Description: 爬取github每日热门仓库。
Notes: 
github每日热门仓库没有写每日更新时间,推测一般都是午夜0点更新,为自己上班查看方便,需配合crontab每日9点爬取。
"""
from web_selenium_base_class.web_selenium_base import WebSeleniumBase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from loguru import logger

class GithubScraper(WebSeleniumBase):
    def fetch_webpage_content(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(0.5)
            title = "Github每日热门仓库"    # 占位,保证项目的返回值统一
            # 爬取github每日热门仓库
            items = self.fetch_content()
        except WebDriverException as e:
            logger.error(f"在使用Selenium获取github网页内容时发生错误：{str(e)}")
            return None, []
        return title, items

    def fetch_content(self):
        try:
            items = []
            # 尝试抓取内容
            # 查找所有包含类名为 Box-row 的 article 元素
            box_rows = self.driver.find_elements(By.CSS_SELECTOR, ".Box-row")

            for box in box_rows:
                p_text = None  # 默认情况下，p_text 设置为 None
                # find_element 获取单个元素,使用 find_elements 获取多个元素
                href = box.find_element(By.CSS_SELECTOR, "h2 > a").get_attribute('href')  # 获取 href 属性

                # 尝试抓取 p 标签的文本
                p_tags = box.find_elements(By.CSS_SELECTOR, "p")
                if p_tags:  # 如果找到 p 标签
                    p_text = p_tags[0].text  # 取第一个 p 标签的文本
                else:
                    p_text = "无相关描述"  # 如果没有找到 p 标签，可以设定一个默认文本

                items.append({'description': p_text, 'href': href})
                
        except NoSuchElementException as e:
            logger.error(f"元素未找到: {str(e)}")
            # 保证项目结构中这里的格式统一
            items = []
        return items