"""
Description: 实现一个基于映射(mapping)的分发系统,将每个域名与对应的爬取类关联起来,从而避免使用多个if-else语句或复杂的条件判断。
Notes: 
"""
from scraper.baidu.baiduscraper import BaiduScraper
from scraper.baidubaike.baidubaikescraper import BaiduBaikeScraper
from scraper.baijiahao.baijiahaoscraper import BaijiahaoScraper
from scraper.csdn.csdnscraper import CsdnScraper
from scraper.pengpaixinwen.pengpaixinwenscraper import PengpaixinwenScraper

# 映射字典，将域名关联到相应的爬取类
crawler_map = {
    'baike.baidu.com': BaiduBaikeScraper,
    'baijiahao.baidu.com': BaijiahaoScraper,
    'blog.csdn.net': CsdnScraper,
    'www.thepaper.cn': PengpaixinwenScraper,
}