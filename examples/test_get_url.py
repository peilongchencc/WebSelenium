from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def fetch_webpage_content(url):
    """测试selenium 4连接网络。
    Args:
        url: 网页链接
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
        print("网络连接成功")
        # 等待元素加载(隐式等待)
        driver.implicitly_wait(5)
        
        # 抓取标题(语法为selenium内置,无需修改)
        title = driver.title

        # 尝试抓取内容
        items = driver.find_element(By.CSS_SELECTOR, ".td-content")
        items = items.text
        print(f"网页标题为:{title}\n网页内容为:\n{items}")
        
    except:
        print(f"在使用Selenium时发生错误")

    finally:
        # 确保无论如何都关闭浏览器
        if driver:
            driver.quit()

    return

if __name__ == "__main__":
    url = "https://www.selenium.dev/documentation/"
    fetch_webpage_content(url)