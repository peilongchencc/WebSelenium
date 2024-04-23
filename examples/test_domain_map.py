"""
Description: 测试爬虫类的分发。
"""
import sys
import os
# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 将脚本路径转为项目根目录路径
project_root_directory = os.path.dirname(os.path.dirname(current_script_path))
# 将这个目录添加到 sys.path
sys.path.append(project_root_directory)

from url_utils.url_parse import extract_domain_from_url
from domain_map.domain_map_strategy import crawler_map

print(f"爬虫分发映射为:\n{crawler_map}\n")

url = "https://www.selenium.dev/documentation/"
domain = extract_domain_from_url(url)
print(f"{url} 的域名为:\n{domain}\n")

# 根据域名选择对应的爬取类
crawler_class = crawler_map.get(domain)
print(f"{url} 分发到的爬虫类为:\n{crawler_class}\n")