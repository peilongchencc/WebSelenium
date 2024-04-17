"""
Description: 测试从百度百科获取网页标题和网页文本。
"""
import sys
import os
# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 将脚本路径转为项目根目录路径
project_root_directory = os.path.dirname(os.path.dirname(current_script_path))
# 将这个目录添加到 sys.path
sys.path.append(project_root_directory)

from scraper.baidubaike.baidubaikescraper import BaiduBaikeScraper
from url_utils.url_parse import ensure_https
from loguru import logger
import time

# 设置日志
logger.remove()
logger.add("selenium_data.log", rotation="1 GB", backtrace=True, diagnose=True, format="{time} {level} {message}")

def test_baidubaike_scraper():
    # url = "https://baike.baidu.com/item/4%C2%B713%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A%E6%82%89%E5%B0%BC%E8%B4%AD%E7%89%A9%E4%B8%AD%E5%BF%83%E6%8C%81%E5%88%80%E8%A1%8C%E5%87%B6%E4%BA%8B%E4%BB%B6/64284796?fr=api_baidu_opex_festival"
    url = "https://baike.baidu.com/item/%E8%8A%B1%E5%8D%89/229536"
    # 检查一个 URL 是否包含协议，并在没有协议的情况下添加 "https://"。
    checked_url = ensure_https(url)
    scraper = BaiduBaikeScraper()
    title, items = scraper.fetch_webpage_content(checked_url)
    logger.info(f"Title: {title}")
    logger.info(f"Content: {items}")
    logger.info(f"Content: {type(items)}")

if __name__ == "__main__":
    start_time = time.time() 
    test_baidubaike_scraper()
    end_time = time.time() 
    execution_time = end_time - start_time 
    logger.info(f"执行时间为：{execution_time} 秒")