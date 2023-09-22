import csv
import os

import requests
from bs4 import BeautifulSoup as bs


def get_fruugo_products(page_count, output_csv_file, file_encoding, headers, proxies):
    # 定义要获取的商品信息
    product_info = ["商品标题", "商品价格", "商品详情链接"]

    # 删除已存在的文件
    if os.path.exists(output_csv_file):
        os.remove(output_csv_file)

    # 创建Session对象
    session = requests.Session()

    # 逐页获取商品信息并写入CSV文件
    for page in range(1, page_count + 1):
        try:
            url = f"https://www.fruugo.co.uk/search?whcat=6205&wscat=WS48843298&page={page}"
            response = session.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()

            soup = bs(response.text, "html.parser")

            print(f"{response.status_code = }")
            print(f"{page = }")

            # 提取商品列表中的每个商品信息
            products = soup.find_all("div", attrs={"class": "col-6 col-lg-4 col-xl-3 product-item"})

            # 逐个提取商品信息并写入CSV文件
            with open(output_csv_file, mode="a", encoding=file_encoding, newline="") as file:
                writer = csv.writer(file)

                # 写入商品信息标题行
                writer.writerow(product_info)

                for product in products:
                    title = product["data-name"]
                    price = product["data-price"]
                    details_link = "https://www.fruugo.co.uk" + product.find("a")["href"]

                    # 写入商品信息行
                    writer.writerow([title, price, details_link])

        except requests.exceptions.RequestException as e:
            print(f"获取商品信息失败：{e}")
            continue

    print("商品信息获取完成！")


if __name__ == "__main__":
    # 定义请求头 Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31",
        "Referer": "https://www.fruugo.co.uk/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh-TW;q=0.6,zh;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    #! 设置代理，本机 V2Ray 代理为本机 localhost 地址，端口为 10809；具体视本机代理设置而定
    proxies = {
        "http": "http://127.0.0.1:10809",
        "https": "http://127.0.0.1:10809",
    }

    get_fruugo_products(page_count=10, output_csv_file="fruugo_products.csv", file_encoding="utf-8", headers=headers, proxies=proxies)
