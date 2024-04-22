# Github 每日热点项目爬取

由于页面中部分项目没有 `<p>` 标签，因此下列写法会报错。<br>

```python
        items = []
        # 尝试抓取内容
        # 查找所有包含类名为 Box-row 的 article 元素
        box_rows = driver.find_elements(By.CSS_SELECTOR, "article.Box-row")

        for box in box_rows:
            p_text = None  # 默认情况下，p_text 设置为 None
            # find_element 获取单个元素,使用 find_elements 获取多个元素
            href = box.find_element(By.CSS_SELECTOR, "h2 a").get_attribute('href')  # 获取 href 属性

            # 尝试抓取 p 标签的文本
            p_tag = box.find_element(By.CSS_SELECTOR, "p")
            if p_tag:
                p_text = p_tag.text

            items.append({'description': p_text, 'href': href})
```

报错信息:<br>

```log
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data/WebSelenium# python fetch_webpage_content.py 
在使用Selenium时发生错误：Message: no such element: Unable to locate element: {"method":"css selector","selector":"p"}
  (Session info: chrome-headless-shell=123.0.6312.105); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
```

主要问题出现在寻找页面元素时。错误信息 "no such element" 表明 Selenium 在尝试定位具有指定 CSS 选择器的元素时失败了。这通常意味着页面上确实没有该元素，或者当 Selenium 尝试访问这个元素时，它还没有被加载出来。<br>

🚨🚨🚨在上述代码中，`p_tag = box.find_element(By.CSS_SELECTOR, "p")` 这一行出现了问题，因为可能有些 `article.Box-row` 元素中不存在 `<p>` 标签。<br>

**这种情况下，`find_element` 方法会抛出 `NoSuchElementException`，因为它期望找到至少一个符合条件的元素。** <br>

为了解决这个问题，你可以改用 `find_elements` 方法，**它在找不到元素时会返回一个空列表而不是抛出异常** ‼️。接着你可以检查列表是否为空来决定如何处理这种情况。<br>

这里是你可以考虑修改的代码段：<br>

```python
        # 尝试抓取 p 标签的文本
        p_tags = box.find_elements(By.CSS_SELECTOR, "p")
        if p_tags:  # 如果找到 p 标签
            p_text = p_tags[0].text  # 取第一个 p 标签的文本
        else:
            p_text = "无相关描述"  # 如果没有找到 p 标签，可以设定一个默认文本
```

这样修改后，如果某些 `article.Box-row` 中不存在 `<p>` 标签，代码将不会抛出异常，而是继续处理其他数据。此外，使用 `find_elements` 和检查列表是否为空是处理可能缺失的 HTML 元素的一种安全做法。<br>