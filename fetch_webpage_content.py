"""
Description: 通过selenium 4获取网页的标题和内容。
Notes: 
# 尝试抓取 p 标签的文本
p_tags = box.find_elements(By.CSS_SELECTOR, "p")
if p_tags:  # 如果找到 p 标签
    p_text = p_tags[0].text  # 取第一个 p 标签的文本
else:
    p_text = "无相关描述"  # 如果没有找到 p 标签，可以设定一个默认文本
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def fetch_webpage_content(url):
    """通过selenium 4获取网页的标题和内容。
    Args:
        url: 网页链接
    Returns:
        title, text: 网页标题,网页内容。
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
        items = []
        # 尝试抓取内容
        # 查找所有包含类名为 Box-row 的 article 元素
        box_rows = driver.find_elements(By.CSS_SELECTOR, "article.Box-row")

        for box in box_rows:
            p_text = None  # 默认情况下，p_text 设置为 None
            # find_element 获取单个元素,使用 find_elements 获取多个元素
            href = box.find_element(By.CSS_SELECTOR, "h2 a").get_attribute('href')  # 获取 href 属性

            # 尝试抓取 p 标签的文本
            p_tags = box.find_elements(By.CSS_SELECTOR, "p")
            if p_tags:  # 如果找到 p 标签
                p_text = p_tags[0].text  # 取第一个 p 标签的文本
            else:
                p_text = "无相关描述"  # 如果没有找到 p 标签，可以设定一个默认文本

            items.append({'description': p_text, 'href': href})
            
    except WebDriverException as e:
        title, items = None, None
        print(f"在使用Selenium时发生错误：{str(e)}")

    finally:
        # 确保无论如何都关闭浏览器
        if driver:
            driver.quit()

    return title, items

if __name__ == "__main__":
    url = "https://github.com/trending/python?since=daily"
    title, items = fetch_webpage_content(url)
    print("Title:", title)
    print("Content:", items)