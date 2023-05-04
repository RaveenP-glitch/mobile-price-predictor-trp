import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import csv

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

bucket_list = ['https://www.amazon.in/Garmin-010-02064-00-Instinct-Monitoring-Graphite/dp/B07HYX9P88/',
               'https://www.amazon.in/Rockerz-370-Headphone-Bluetooth-Lightweight/dp/B0856HRTJG/',
               'https://www.amazon.in/Logitech-MK215-Wireless-Keyboard-Mouse/dp/B012MQS060/',
               'https://www.amazon.in/Logitech-G512-Mechanical-Keyboard-Black/dp/B07BVCSRXL/',
               'https://www.amazon.in/BenQ-inch-Bezel-Monitor-Built/dp/B073NTCT4R/'
               ]


def get_amazon_price(dom):

    try:
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        price = price.replace(',', '').replace('₹', '').replace('.00', '')
        return int(price)
    except Exception as e:
        price = 'Not Available'
        return None


def get_product_name(dom):
    try:
        name = dom.xpath('//span[@id="productTitle"]/text()')
        [name.strip() for name in name]
        return name[0]
    except Exception as e:
        name = 'Not Available'
        return None

# write data into a csv file

with open('master_data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['product name', 'price', 'url'])

    for url in bucket_list:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')
        amazon_dom = et.HTML(str(soup))

        product_name = get_product_name(amazon_dom)
        product_price = get_amazon_price(amazon_dom)

        time.sleep(random.randint(2, 10))

        writer.writerow([product_name, product_price, url])
        print(product_name, product_price, url)