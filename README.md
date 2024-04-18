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
澎湃新闻    | "https://www.thepaper.cn/newsDetail_forward_27031399"                         | ✅


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

3. 为提高爬取效率，默认采用低资源(`eager`)方式加载界面。用户如果想使用完全加载模式，可以参考以下写法重写 `__init__` 方法。

```python
class BaiduSearchScraper(WebSeleniumBase):
    def __init__(self):
        """重写基类的init,启动浏览器
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'eager'  # 默认是normal模式
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("chrome浏览器启动成功!!!!")
        except Exception as e:
            logger.error(f"启动chrome时发生错误：{str(e)}")

    def fetch_webpage_content(self, url):
        # 省略
        pass
```

4. selenium对于浏览器的关闭和开启很敏感，使用时一定要注意，避免出错。


## FAQ:

1. 爬取的耗时如何？

项目使用的selenium，selenium为同步操作，单个网页爬取的耗时一般在2s内，如果网页内容特别多，耗时会增加(例如百科类网址)。<br>

2. 采用你的代码后，爬取对应网址的耗时严重，竟然需要133s。要如何解决？

selenium的网页加载策略默认是等待网页内容全部加载结束，对于需要加载内容非常多的网址，需要更改网页加载策略。具体代码可参考 `scraper/csdn/csdnscraper.py`。<br>

3. 不能抓取目标网站的图片、视频吗？

项目爬取目标为网站文本，常规状态下不抓取图片、视频。大家可以根据自己的业务场景，添加合适的代码。<br>

4. 我想要的内容没有爬取到。

如果你想要的内容没有爬取到，请检查代码中的CSS选择器或XPATH。笔者的爬取逻辑是覆盖常用内容，部分内容不在这个范围内，大家可以根据自己的业务场景修改代码。<br>

5. 为什么我的代码结构正确，但是依旧提示 `ERROR 元素未找到: Message: stale element reference: stale element not found`？具体结构如下:

```python
class BaiduSearchScraper(WebSeleniumBase):
    def __init__(self):
        pass
        # 省略
    def fetch_content(self):
        fetched_content = []
        try:
            # 定位搜索结果
            search_result = self.driver.find_elements(By.CSS_SELECTOR, '.tts-button_1V9FA')
            for each_search_result in search_result:
                hyperlink = each_search_result.get_attribute('data-url')  # 
                
                logger.info(f"\n当前待爬取链接为:{hyperlink}\n")
                
                # fetched_content.append(hyperlink)
                
                crawl_content = self.crawl_text_content(hyperlink)
                fetched_content.append(crawl_content)
        except Exception as e:
            logger.error(f"元素未找到: {str(e)}")
        return fetched_content

    def crawl_text_content(self, hyperlink):
        """根据网址爬取文本内容
        """
        crawl_content = {}
        self.driver.get(hyperlink)
        self.driver.implicitly_wait(5)
        # 百度搜索引擎的部分网址为"重定向链接"("redirected_link"),不是"实际链接"("direct_link")。
        direct_link = self.driver.current_url
        logger.info(f"实际链接为:{direct_link}")
        return crawl_content
```

这是因为，你尝试获取某个网页元素的属性，然后使用这个属性（如一个链接）来访问另一个页面。在这个过程中，原来的网页环境发生了变化（例如，由于页面跳转到了新的URL），那么原始的网页元素会变得不再有效，导致这种错误。<br>

即在 `crawl_text_content` 方法中，使用 `self.driver.get(hyperlink)` 访问了新的URL，这导致原来的 `search_result` 中的元素失效。当尝试在循环中处理下一个元素时，原来的元素已经不在DOM中了，因此报出了“stale element reference”的错误。<br>

在处理动态页面和导航时，selenium的表现与普通的用户操作非常相似。当你使用 `self.driver.get()` 方法导航到一个新的页面时，WebDriver 的上下文会转移到新页面，原页面的 DOM 结构会被卸载。这就是为什么原来通过 `find_elements` 获取的元素集合会变得不再有效的原因。<br>

🔥🔥🔥解决方案为修改 `fetch_content` 方法，使其先收集所有链接，然后再逐一处理：:<br>

```python
def fetch_content(self):
    fetched_content = []
    try:
        search_result = self.driver.find_elements(By.CSS_SELECTOR, '.tts-button_1V9FA')
        hyperlinks = [result.get_attribute('data-url') for result in search_result]

        for hyperlink in hyperlinks:
            crawl_content = self.crawl_text_content(hyperlink)
            fetched_content.append(crawl_content)
    except Exception as e:
        logger.error(f"元素未找到: {str(e)}")
    return fetched_content
```


## 关于项目:

由于爬虫的特殊性，需要根据网页的变化而更改代码，大家在使用的过程中发现某个网址爬取失败，欢迎提交issue。<br>

另外，大家如果有想要爬取的网页，也欢迎在issue中提出，笔者优先撰写相关代码。<br>