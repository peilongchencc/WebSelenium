import sys
import os
# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 将脚本路径转为项目根目录路径
project_root_directory = os.path.dirname(os.path.dirname(current_script_path))
# 将这个目录添加到 sys.path
sys.path.append(project_root_directory)

from url_utils.url_parse import extract_domain_from_url

url = "https://www.thepaper.cn/newsDetail_forward_27031399"
domain = extract_domain_from_url(url)
print(f"{url} 的域名为:\n{domain}")