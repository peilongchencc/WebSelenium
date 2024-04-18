"""
File path:fetch_webpage_content.py
Author: peilongchencc@163.com
Description: 通过selenium 4获取网页的标题和内容。
Requirements: 
1. pip install selenium 
2. 查看自己的chrome版本
3. 安装与自己的chrome版本对应的chrome driver
Reference Link: 
Notes: 
1. selenium更新频繁且会改动函数名,如果代码无法执行,大概率是selenium版本不对,需要调整代码或selenium版本。
2. 笔者使用的selenium版本为 `selenium 4.18.1`。
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def fetch_webpage_content(url):
    """通过selenium 4获取网页的标题和内容。
    Args:
        url: 网页链接
    Returns:
        title, text: 网页标题,网页内容。
    Notes:
        1. 运行前需要先分析并修改函数中的xpath,确保xpath对应的是自己需要抓取的内容。
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 让浏览器在无头模式下运行（不显示界面）
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'eager'
        
        # 实例化 WebDriver
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # 等待元素加载(隐式等待)
        driver.implicitly_wait(5)
        
        # 抓取标题(语法为selenium内置,无需修改)
        title = driver.title
        text = "爬取百度热搜网址列表"
        # 尝试抓取内容
        try:
            results = driver.find_elements(By.CSS_SELECTOR, '.tts-button_1V9FA')
            for result in results:
                url_list = result.get_attribute('data-url')  # 获取tpl属性
                print(url_list)

        except NoSuchElementException:
            text = "内容元素未找到"
            
    except WebDriverException as e:
        title, text = None, None
        print(f"在使用Selenium时发生错误：{str(e)}")

    finally:
        # 确保无论如何都关闭浏览器
        if driver:
            driver.quit()

    return title, text

if __name__ == "__main__":
    url = 'https://www.baidu.com/s?wd=%E6%BE%B3%E4%BA%BF%E4%B8%87%E5%AF%8C%E8%B1%AA%E4%B9%8B%E5%A5%B3%E5%9C%A8%E6%82%89%E5%B0%BC%E8%A2%AD%E5%87%BB%E6%A1%88%E4%B8%AD%E9%81%87%E5%AE%B3&sa=fyb_n_homepage&rsv_dl=fyb_n_homepage&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1'
    title, text = fetch_webpage_content(url)
    print("Title:", title)
    print("Content:", text)