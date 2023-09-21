import requests
from bs4 import BeautifulSoup
import csv

# 定义要获取的商品页数和商品信息
page_count = 1
product_info = ["商品标题", "商品价格", "商品详情链接"]

# 定义输出文件名和文件编码
output_file = "fruugo_products.csv"
file_encoding = "utf-8"

# 定义请求头 Headers
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
cookies = "consents=essential%2Canalytics%2Cadvertising; ak_bmsc=6219B8AFAC0EE674C3C67303AB06350D~000000000000000000000000000000~YAAQPn8auIM875GKAQAAbMhAthWKZo87Is4u43Uh0TbZEutXqIkpaXJaGa83fed1dCWKffeh7OKhDWhXbCrohPHgwUQ6wdC7EAVWi8Xf44Eo+ltyUPax0GKQ6V6/NXPUhMWU9oTexTcQXyOcTQUGad0pgH7TpX3w/KwUiU8dauvjsQ46Dz7NLqeQ4io6hwd5yFYLpXa7r9Y+YfCv/jaQ35f5XVNS/Ivmc/xOQVYsVqWxcEaninBn2U63gtg53VKUHVAtXElZCE2irRVOBPM2fzXmDoO1nfro1X3mtLsz7zI3vnWCEn5iH7a354e33HqR2jCNSq/CJKeP/7DOr3s91VM9sbJV3PjOjeEs2auGd4lNlg1B0XPoAavJl0wZ4j6qW+Amloio0mMtsXjo; bm_mi=78CE36EA130D7D647EA4B8D5360959D0~YAAQPX8auNEED7KKAQAAbDFPthUVLk3m7S5Hf5gqKcyDwthoHtQ1mM9c9VsnwhUGvWbYGitaTv2g+2yCu4C/PCingnVH23Q4uyy5zIIvVE60MHtjmTQseMXcjL1cRoBX0M5uNpt7WfoDv22u9phdI58e1hmwL43ZbudylDbdRp+CLcDIvzebAJ1QNEcmFuHPhTKimzGh4XtDAzc3ayfyO7NSV/KumUZqnilztZwD7i9y/r1EK1kcDeyRe6bifo4YfpIZOPvoC0J7gLKpSYc9IhaleCLGHum6NaXSGgmvwPQpAU/Zs5+3/iVZ5cNhxIHlMtJTuhc0~1; bm_sv=3D14EBA6A01B03663D0C5F1EB718AA2B~YAAQPX8auBkFD7KKAQAA6zVPthXzOccr5l3iCpY56c1M1njaLhwod9dWxkcdJqwVIb5fsg2FWTCoizFpXZ4ApU+xcPgJC6dgEHPXmD7CfT0ZGXBdlNAcXbA7LknvuF42B3tYtdHFzcnHhXzNjO8CCJ72f7MltTfCGN1dd0r1ysNQ6Pf0WfaqSrU/YXW7dK3mSOeG21ur/31Cahpq80d+Z1ou97KQDx0DEFluOOrmufz2qtdM2YxCvmFIiRLD1MdsvJA=~1"
headers = {
    "User-Agent": user_agent,
    "Cookie": cookies,
    "Refer": "https://www.fruugo.co.uk/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh-TW;q=0.6,zh;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
# 设置 `requests` 库代理
proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809",
}
# 逐页获取商品信息并写入CSV文件
for page in range(1, page_count + 1):
    url = f"https://www.fruugo.co.uk/search?whcat=6205&wscat=WS48843298&page={page}"
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # 提取商品列表中的每个商品信息
    # products = soup.find("div", attrs={"class": "products-list row"})
    product_list = soup.find_all("div", attrs={"class": "col-6 col-lg-4 col-xl-3 product-item"})

# Debug
    with open("fruugo_products.html", mode="w", encoding=file_encoding) as f:
        f.write(response.text)
    
    # with open("products.txt", mode='w', encoding=file_encoding) as f:
    #     f.write(str(products))
    with open("product_list.txt", mode='w', encoding=file_encoding) as f:
        f.write(str(product_list))

    # print(f"{products = }")
    # print(f"{product_list = }")

    # 逐个提取商品信息并写入CSV文件
    with open(output_file, mode="a", encoding=file_encoding, newline="") as file:
        writer = csv.writer(file)
        writer.writerow(product_info)  # 写入商品信息标题行
        for product in product_list:
            print(f"{product = }")
            title = product["data-name"]
            price = product["data-price"]
            details_link = product.find("a")["href"]
            writer.writerow([title, price, details_link])  # 写入商品信息行
