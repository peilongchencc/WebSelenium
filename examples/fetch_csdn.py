"""
Description: 测试从csdn获取网页标题和网页文本。
"""
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