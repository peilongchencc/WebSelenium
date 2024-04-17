# WebSelenium

基于selenium 4实现网页数据抓取，本项目仅用于个人测试和学习。<br>
- [WebSelenium](#webselenium)
  - [网址覆盖范围:](#网址覆盖范围)
  - [使用教程:](#使用教程)
  - [网址爬取测试:](#网址爬取测试)
  - [注意事项:](#注意事项)
  - [FAQ:](#faq)
  - [关于项目:](#关于项目)


## 网址覆盖范围:

域名       |网址示例                                                                        |支持
----------|-------------------------------------------------------------------------------|---
百度       | "https://www.baidu.com"                                                       | ✅
百度百科    | "https://baike.baidu.com/item/花卉/229536"                                    | ✅
百家号     | "https://baijiahao.baidu.com/s?id=1796368810044659826&wfr=spider&for=pc"      | ✅
CSDN      | "https://blog.csdn.net/weixin_43958105/article/details/114012590"             | ✅


## 使用教程:

1. 安装selenium。

2. 安装Chrome driver。

   安装Chrome driver教程可参考[这里](https://github.com/peilongchencc/selenium_data/tree/main/browser_driver)。<br>

3. 运行examples下的文件，或参考examples下的文件编写适合自己场景的代码。


## 网址爬取测试:

所有的测试文件均写在 `examples` 文件夹下，大家可以根据需要自行选择需要执行的文件。<br>


## 注意事项:

1. 网址尽量传入完整的网址(带有协议部分)，如果传入的网址不含有协议，将自动在网址前添加 "https://"。

2. URL格式编码的网址可以直接传入，不需要解码。

例如 "https://baike.baidu.com/item/%E8%8A%B1%E5%8D%89/229536" 可以直接传入执行爬取操作，不需要解码为 "https://baike.baidu.com/item/花卉/229536"。<br>


## FAQ:

1. 爬取的耗时如何？

项目使用的selenium，selenium为同步操作，单个网页爬取的耗时一般在2s内，如果网页内容特别多，耗时会增加(例如百科类网址)。<br>

2. 采用你的代码后，爬取对应网址的耗时严重，竟然需要133s。要如何解决？

selenium的网页加载策略默认是等待网页内容全部加载结束，对于需要加载内容非常多的网址，需要更改网页加载策略。具体代码可参考 `scraper/csdn/csdnscraper.py`。<br>


## 关于项目:

由于爬虫的特殊性，需要根据网页的变化而更改代码，大家在使用的过程中发现某个网址爬取失败，欢迎提交issue。<br>

另外，大家如果有想要爬取的网页，也欢迎在issue中提出，笔者优先撰写相关代码。<br>