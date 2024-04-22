"""
Description: 爬取github每日热门仓库。
Notes: 
1. github每日热门仓库没有写每日更新时间,推测一般都是午夜0点更新,为自己上班查看方便,需配合crontab每日9点爬取。
2. 爬取的速度好慢,暂时搞不懂因为什么。按理来说,我已经开启代理了啊。爬取的速度竟然在5s左右,离谱。
"""
import sys
import os
# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 将脚本路径转为项目根目录路径
project_root_directory = os.path.dirname(os.path.dirname(current_script_path))
# 将这个目录添加到 sys.path
sys.path.append(project_root_directory)

from selenium import webdriver
from scraper.github.githubscraper import GithubScraper
from url_utils.url_parse import ensure_https
from loguru import logger
import time
from loguru import logger
from dotenv import load_dotenv

# 加载环境变量
dotenv_path = '.env.local'
load_dotenv(dotenv_path=dotenv_path)

# 设置日志
logger.remove()
logger.add("selenium_data.log", rotation="1 GB", backtrace=True, diagnose=True, format="{time} {level} {message}")

# 设置代理环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

def open_driver():
    """开启浏览器"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无GUI界面启动浏览器
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.page_load_strategy = 'eager'    # 为提高爬取效率，默认采用低资源方式加载界面。

    try:
        driver = webdriver.Chrome(options=options)
        logger.info("chrome浏览器启动成功!!!!")
    except Exception as e:
        logger.error(f"基类中启动chrome时发生错误：{str(e)}")
    return driver

def close_driver(driver):
    """关闭浏览器"""
    driver.quit()
    logger.info("chrome浏览器成功关闭!!!!")

def test_github_scraper():
    url = "https://github.com/trending/python?since=daily"
    # 检查一个 URL 是否包含协议，并在没有协议的情况下添加 "https://"。
    checked_url = ensure_https(url)
    chrome_driver = open_driver()
    scraper = GithubScraper(chrome_driver)
    title, items = scraper.fetch_webpage_content(checked_url)
    close_driver(chrome_driver)
    logger.info(f"Title: {title}")
    logger.info(f"Content: {items}")
    logger.info(f"Content: {type(items)}")

if __name__ == "__main__":
    start_time = time.time() 
    test_github_scraper()
    end_time = time.time() 
    execution_time = end_time - start_time 
    logger.info(f"执行时间为：{execution_time} 秒")