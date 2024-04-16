# scraping_strategies.py

from selenium.webdriver.common.by import By

# 定义不同网站正文的抓取策略
strategies = {
    'baijiahao.baidu.com': (By.CLASS_NAME, '_18p7x'),
    'news.sina.com.cn': (By.ID, 'article'),
    'www.zhihu.com': (By.XPATH, '//div[@class="RichText ztext"]'),
    # 添加更多网站和对应的策略
}
