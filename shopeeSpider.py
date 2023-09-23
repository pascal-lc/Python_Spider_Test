import csv
import time

import requests
from bs4 import BeautifulSoup as bs


def get_shopee_products(shop_url, output_file):
    # 定义要获取的商品信息
    product_info = ["商品ID", "商品名字", "价格", "月销量", "总销量"]

    # 删除已存在的文件
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(product_info)

    # 创建Session对象
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    })

    # 获取店铺的商品列表
    page = 0
    while True:
        try:
            url = f"{shop_url}?page={page}&sortBy=pop"
            response = session.get(url, timeout=10)
            response.raise_for_status()

            soup = bs(response.text, "html.parser")

            # Debug
            with open('shopee_shop.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())

            # 提取商品列表中的每个商品信息
            products = soup.find_all("div", attrs={"class": "col-xs-2-4 shopee-search-item-result__item"})

            # 逐个提取商品信息并写入CSV文件
            with open(output_file, mode="a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)

                for product in products:
                    itemid = product["data-itemid"]
                    itemname = product.find("div", attrs={"class": "yQmmFK _1POlWt _36CEnF"}).text.strip()
                    itemprice = product.find("span", attrs={"class": "_29R_un"}).text.strip()

                    # 获取月销量和总销量
                    item_url = f"https://shopee.ph/product-i.{itemid}"
                    item_response = session.get(item_url, timeout=10)
                    item_response.raise_for_status()
                    item_soup = bs(item_response.text, "html.parser")

                    item_sold = item_soup.find("div", attrs={"class": "flex items-center _2Fy0tZ"}).text.strip()
                    item_sold = item_sold.replace("sold", "").replace(",", "").strip()
                    item_sold_monthly = item_soup.find("div", attrs={"class": "_22sp0A"}).text.strip()
                    item_sold_monthly = item_sold_monthly.replace("sold", "").replace(",", "").strip()

                    # 写入商品信息行
                    writer.writerow([itemid, itemname, itemprice, item_sold_monthly, item_sold])

            # 判断是否还有下一页
            if soup.find("button", attrs={"class": "shopee-button-outline shopee-button-outline--disabled"}):
                break
            else:
                page += 1
                time.sleep(5)  # 防止访问过于频繁

        except requests.exceptions.RequestException as e:
            print(f"获取商品信息失败：{e}")
            continue

    print("商品信息获取完成！")


if __name__ == "__main__":
    url = "https://shopee.ph/shop/160357616/search"
    output_csv_file = "shopee_products.csv"

    get_shopee_products(shop_url=url, output_file=output_csv_file)
