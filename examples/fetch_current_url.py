"""
Description: 对于网址的重定向,测试重定向后的url输出,决定后续的爬取策略。
Notes: 
Example of terminal output:
Title: 视频暂时不能查看
Current_url: https://haokan.baidu.com/v?pd=wisenatural&vid=17084920392880833985
"""
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def fetch_current_url(url):
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
        current_url = driver.current_url

    except WebDriverException as e:
        title, current_url = None, None
        print(f"在使用Selenium时发生错误：{str(e)}")

    finally:
        # 确保无论如何都关闭浏览器
        if driver:
            driver.quit()

    return title, current_url

if __name__ == "__main__":
    url = 'https://www.baidu.com/link?url=YejGZyVpLc0lYpYntmstxbSDjTqDZ0pKxdNo_cURXWuFNNAwJch3Tn38dQGCFBdNhlaFRK-Z-bGYs8F-OfeeyaWkFGMniWTiK_gMR7Eq6EK&amp;wd=&amp;eqid=dbf20f6e01930f8300000002662078cc'
    title, current_url = fetch_current_url(url)
    print("Title:", title)
    print("Current_url:", current_url)