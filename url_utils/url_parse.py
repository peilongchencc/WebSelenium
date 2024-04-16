"""
File path: url_parse.py
Author: peilongchencc@163.com
Description: URL解码器, 目的是将URL编码的网址转换回原始的URL格式, 达到可以直接访问的形式。
Requirements: 
Reference Link: 
Notes: 
网页开发者模式经常能够看到网址为 "https%3A/%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%25..." 格式, 这种是URL编码的结果,无法直接访问, 
需要使用URL解码器将它转换回原始的URL格式,然后你就可以在浏览器中使用它了。

必要性: URL编码的主要目的是确保URL中的特殊字符和非ASCII字符能够被正确传输和解析,同时也能够避免一些潜在的安全问题。
"""
import urllib.parse
from urllib.parse import urlparse

def extract_domain_from_url(url):
    """解析URL以获取域名。
    Args:
        url(str)
    Return:
        domain(str):网址域名。
    Example:
        "https://baijiahao.baidu.com/s?id=1793832549445442560" --> "baijiahao.baidu.com"
        "https://www.zhihu.com/question/36809525/answer/1928922951" --> "www.zhihu.com"
    """
    # 解析URL以获取域名
    domain = urlparse(url).netloc
    return domain

def decoded_url(encoded_url):
    """URL解码器, 目的是将URL编码的网址转换回原始的URL格式, 达到可以直接访问的形式。
    Args:
        encoded_url(str): 待解析的URL编码的网址。
    Return:
        decoded_url(str): 解码后的URL, 用户可以通过粘贴该结果直接访问对应网址。
    """
    # 解码URL
    decoded_url = urllib.parse.unquote(encoded_url)
    return decoded_url

if __name__ == '__main__':
    # 要解码的 URL 字符串
    encoded_url = "https%3A/%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%25BE%25B3%25E4%25BA%25BF%25E4%25B8%2587%25E5%25AF%258C%25E8%25B1%25AA%25E4%25B9%258B%25E5%25A5%25B3%25E5%259C%25A8%25E6%2582%2589%25E5%25B0%25BC%25E8%25A2%25AD%25E5%2587%25BB%25E6%25A1%2588%25E4%25B8%25AD%25E9%2581%2587%25E5%25AE%25B3%26sa%3Dfyb_n_homepage%26rsv_dl%3Dfyb_n_homepage%26from%3Dsuper%26cl%3D3%26tn%3Dbaidutop10%26fr%3Dtop1000%26rsv_idx%3D2%26hisfilter%3D1"
    # 调用URL解码器解码
    rtn = decoded_url(encoded_url)
    print("解码后的 URL:\n", rtn)