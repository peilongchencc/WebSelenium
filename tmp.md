我使用的selenium4，我的项目目录如下:

```log
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data/WebSelenium# tree
.
├── examples
│   ├── fetch_baidu_hot_search_top10.py
│   ├── fetch_baijiahao.py
│   └── fetch_csdn.py
├── LICENSE
├── push_commit_to_git.sh
├── README.md
├── requirements.txt
├── scraper
│   ├── baidu
│   │   ├── baiduscraper.py
│   │   └── __pycache__
│   │       └── baiduscraper.cpython-310.pyc
│   ├── baijiahao
│   │   ├── baijiahaoscraper.py
│   │   └── __pycache__
│   │       └── baijiahaoscraper.cpython-310.pyc
│   └── csdn
│       ├── csdnscraper.py
│       └── __pycache__
│           ├── baijiahaoscraper.cpython-310.pyc
│           └── csdnscraper.cpython-310.pyc
├── scraper_strategies
│   └── scraping_strategies.py
├── selenium_data.log
├── tmp.md
├── url_utils
│   ├── __pycache__
│   │   └── url_parse.cpython-310.pyc
│   └── url_parse.py
└── web_selenium_base_class
    ├── __pycache__
    │   └── web_selenium_base.cpython-310.pyc
    └── web_selenium_base.py
```

```python
# web_selenium_base.py
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from loguru import logger

class WebSeleniumBase:
    def __init__(self, options=None):
        """配置浏览器,开启浏览器"""
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # 无GUI界面启动浏览器
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("chrome浏览器启动成功!!!!")
        except Exception as e:
            logger.error(f"基类中启动chrome时发生错误：{str(e)}")

    def fetch_webpage_content(self, url):
        """爬取网页正文,这个方法应由子类实现具体逻辑"""
        raise NotImplementedError("This method should be overridden by subclasses")

    def close_driver(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("chrome浏览器成功关闭!!!!")
```

```python
# csdnscraper.py
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
        options.add_argument('pageLoadStrategy=none')  # 添加 eager 加载策略

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
```

```python
# fetch_csdn.py
import sys
import os
# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 将脚本路径转为项目根目录路径
project_root_directory = os.path.dirname(os.path.dirname(current_script_path))
# 将这个目录添加到 sys.path
sys.path.append(project_root_directory)

from scraper.csdn.csdnscraper import CsdnScraper
from url_utils.url_parse import ensure_https
from loguru import logger
import time

# 设置日志
logger.remove()
logger.add("selenium_data.log", rotation="1 GB", backtrace=True, diagnose=True, format="{time} {level} {message}")

def test_csdn_scraper():
    url = "https://blog.csdn.net/weixin_43958105/article/details/114012590"
    # 检查一个 URL 是否包含协议，并在没有协议的情况下添加 "https://"。
    checked_url = ensure_https(url)
    scraper = CsdnScraper()
    title, items = scraper.fetch_webpage_content(checked_url)
    logger.info(f"Title: {title}")
    logger.info(f"Content: {items}")
    logger.info(f"Content: {type(items)}")

if __name__ == "__main__":
    start_time = time.time() 
    test_csdn_scraper()
    end_time = time.time() 
    execution_time = end_time - start_time 
    logger.info(f"执行时间为：{execution_time} 秒")
```

我是不是哪里写错了，我的代码不加入`options.add_argument('pageLoadStrategy=none')`抓取csdn的内容需要133s，加入后依旧耗时133s。我访问网页发现，网页可以迅速加载出正文内容，但开发者模式显示网页完全加载需要的时间确实是2分钟左右。我该怎样才能加快这个爬取呢？