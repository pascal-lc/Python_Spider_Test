# fruugoSpider 说明文档

* -\*- encoding: utf-8 -\*-
* 2023/09/23 9:30:00
* Pascal LC

[TOC]

功能：爬取Fruugo网站上的商品信息，并将商品标题、价格和详情链接写入CSV文件中。

参数说明：

* page_count：要爬取的页数
* output_file：CSV文件的输出路径
* file_encoding：CSV文件的编码方式
* headers：请求头 Headers
* proxies：代理设置
* 返回值：无

代码说明：

## 导入所需模块

```py
import csv
import os
import requests
from bs4 import BeautifulSoup as bs
```

## 定义功能函数 `get_fruugo_products()`

程序整体采用模块化设计，将爬虫、分析、导出部分定义为函数 `get_fruugo_products()`，一定程度上提高可重用性。

定义要获取的商品信息，也就是 `CSV` 文件表头：

```py
product_info = ["商品标题", "商品价格", "商品详情链接"]
```

删除已存在的文件，确保每次重新运行程序时，文件读写函数使用 `a` 参数不会将新数据附在旧数据尾部，造成数据堆积：

```py
if os.path.exists(output_file):
    os.remove(output_file)
```

创建 Session 对象，使用 Session 对象可以自动管理 cookies，方便后续的请求操作。

```py
session = requests.Session()
```

逐页获取商品信息并写入 CSV 文件，其中使用 `try - except` 异常处理机制可以捕获网络请求的异常情况，避免程序出现崩溃。

```py
for page in range(1, page_count + 1):
    try:
        url = f"https://www.fruugo.co.uk/search?whcat=6205&wscat=WS48843298&page={page}"
        response = session.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        soup = bs(response.text, "html.parser")
        ...
    except requests.exceptions.RequestException as e:
        print(f"获取商品信息失败：{e}")
        continue

```

## 定义主程序

* 定义请求头 Headers，模拟浏览器访问

```py
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31",
    "Referer": "https://www.fruugo.co.uk/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh-TW;q=0.6,zh;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
```

* 设置代理

此处代理需要根据自身网络情况自行设定，以绕过**防火墙**屏蔽。

```py
proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809",
}
```

* 调用函数 `get_fruugo_products()`

```py
get_fruugo_products(page_count=10, output_file="fruugo_products.csv", file_encoding="utf-8", headers=headers, proxies=proxies)
```
