# 爬取百度热搜top10

## 网页HTML分析:

热搜内容全部处于页面的 "content_left" 字段。<br>

```html
<div id="content_left" tabindex="0" style="margin-left: -150px; padding-left: 150px;">
```

### 特殊内容示例:

"content_left"下一共有3个 "result-op c-container xpath-log new-pmd" class属性。分别为:<br>

```html
<!-- 百度百科(页面上部) -->
<div class="result-op c-container xpath-log new-pmd" srcid="5893" id="3" tpl="rel-baike" mu="http://nourl.ubs.baidu.com/5893">

<!-- 资讯、实时新闻(百度百科下方) -->
<div class="result-op c-container xpath-log new-pmd" srcid="19" id="4" tpl="news-realtime" mu="https://www.baidu.com/s?tn=news&amp;rtt=1&amp;bsst=1&amp;wd=%E6%BE%B3%E4%BA%BF%E4%B8%87%E5%AF%8C%E8%B1%AA%E4%B9%8B%E5%A5%B3%E5%9C%A8%E6%82%89%E5%B0%BC%E8%A2%AD%E5%87%BB%E6%A1%88%E4%B8%AD%E9%81%87%E5%AE%B3&amp;cl=2" >

<!-- 短视频合集(页面中部)(不做爬取) -->
<div class="result-op c-container xpath-log new-pmd" srcid="4295" id="7" tpl="short_video" mu="http://3108.lightapp.baidu.com/%B0%C4%D2%DA%CD%F2%B8%BB%BA%C0%D6%AE%C5%AE%D4%DA%CF%A4%C4%E1%CF%AE%BB%F7%B0%B8%D6%D0%D3%F6%BA%A6" ><div>

<!-- "大家还在搜" 模块(页面中下部)(不做爬取) -->
<div class="result-op c-container new-pmd" srcid="28608" id="8" tpl="recommend_list" mu="http://28608.recommend_list.baidu.com" data-op="{'y':'F75FF627'}" data-click="{&quot;p1&quot;:8,&quot;rsv_bdr&quot;:&quot;&quot;,&quot;fm&quot;:&quot;alop&quot;,&quot;rsv_stl&quot;:0,&quot;p5&quot;:4}" data-cost="{&quot;renderCost&quot;:1,&quot;dataCost&quot;:1}" m-name="aladdin-san/app/recommend_list/result_6b5afc7" m-path="https://pss.bdstatic.com/r/www/cache/static/aladdin-san/app/recommend_list/result_6b5afc7" nr="1">
```

你遗漏了一点，`tpl="short_video"` 和 `tpl="recommend_list"` 对应的内容不爬取。

### 常规内容示例:

```html
<!-- 常规默认内容(外部网站示例) -->
<div class="result c-container xpath-log new-pmd" srcid="1599" id="9" tpl="se_com_default" mu="http://news.cqnews.net/1/detail/1229359012710080512/app/content_1229359012710080512.html">

<!-- 常规默认内容(百度创作平台百家号示例) -->
<div class="result c-container xpath-log new-pmd" srcid="1599" id="6" tpl="se_com_default" mu="https://baijiahao.baidu.com/s?id=1796372270263933487&amp;wfr=spider&amp;for=pc">
```

### 差异:

特殊内容和常规内容的class的值相同，区别点在于 `tpl` 不同。<br>


## FAQ:

1. 为什么爬取的网站列表和自己登录界面查看到的网页不同？

笔者采用的网页加载策略是低资源型(`eager`)，网页加载慢的资源没有显示在第一页很正常。如果你想要爬取的结果和网页结构一致，将 `eager` 模式注释即可，selenium默认是网页完全加载后再执行操作。<br>




我使用的selenium 4，我爬取了百度热搜top10，但发现热搜的链接是百度搜索的结果页面，内部有大量网页标签，全部都集中在下列标签中:

```html
<div id="content_left" tabindex="0" style="margin-left: -150px; padding-left: 150px;">
```











我如果想获取其中每个网页的URL应该怎么做呢？遍历这个标签？


我使用的selenium 4，我需要的内容的结构如下，我是否能直接定位到tpl呢？因为tpl的可选值很多，我只需要以下种类。


我的css选择器为 "div#content_left"，下列内容都是"div#content_left"下级的内容，我该如何定位呢，请给出示例：

```html
<!-- 资讯、实时新闻(百度百科下方) -->
<div class="result-op c-container xpath-log new-pmd" srcid="19" id="4" tpl="news-realtime" mu="https://www.baidu.com/s?tn=news&amp;rtt=1&amp;bsst=1&amp;wd=%E6%BE%B3%E4%BA%BF%E4%B8%87%E5%AF%8C%E8%B1%AA%E4%B9%8B%E5%A5%B3%E5%9C%A8%E6%82%89%E5%B0%BC%E8%A2%AD%E5%87%BB%E6%A1%88%E4%B8%AD%E9%81%87%E5%AE%B3&amp;cl=2" >

<!-- 常规默认内容(外部网站示例) -->
<div class="result c-container xpath-log new-pmd" srcid="1599" id="9" tpl="se_com_default" mu="http://news.cqnews.net/1/detail/1229359012710080512/app/content_1229359012710080512.html">

<!-- 常规默认内容(百度创作平台百家号示例) -->
<div class="result c-container xpath-log new-pmd" srcid="1599" id="6" tpl="se_com_default" mu="https://baijiahao.baidu.com/s?id=1796372270263933487&amp;wfr=spider&amp;for=pc">
```

我需要加上class属性，只有给你的那2种class是需要的。


div#content_left > div.result-op
