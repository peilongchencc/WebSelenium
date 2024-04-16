# WebSelenium

基于selenium 4实现网页数据抓取，本项目仅用于个人测试和学习。<br>
- [WebSelenium](#webselenium)
  - [网址覆盖范围:](#网址覆盖范围)
  - [使用教程:](#使用教程)
  - [网址爬取测试:](#网址爬取测试)
  - [关于项目:](#关于项目)


## 网址覆盖范围:

域名   |网址示例                                                                        |支持
------|-------------------------------------------------------------------------------|---
百度   | "https://www.baidu.com"                                                       | ✅
百家号 | "https://baijiahao.baidu.com/s?id=1796368810044659826&wfr=spider&for=pc"      | ✅
CSDN  | "https://blog.csdn.net/weixin_43958105/article/details/114012590"             | ✅


## 使用教程:

1. 安装selenium。

2. 安装Chrome driver。

   安装Chrome driver教程可参考[这里](https://github.com/peilongchencc/selenium_data/tree/main/browser_driver)。<br>

3. 运行examples下的文件，或参考examples下的文件编写适合自己场景的代码。


## 网址爬取测试:

所有的测试文件均写在 `examples` 文件夹下，大家可以根据需要自行选择需要执行的文件。<br>


## 关于项目:

由于爬虫的特殊性，需要根据网页的变化而更改代码，大家在使用的过程中发现某个网址爬取失败，欢迎提交issue。<br>

另外，大家如果有想要爬取的网页，也欢迎在issue中提出，笔者优先撰写相关代码。<br>