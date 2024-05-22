import requests
from lxml import html

from pprint import pprint

response = None
items_list = []

def connect():
    global response

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
        "Accept": "*/*",
    }

    url = 'https://www.ebay.com/b/Fishing-Equipment-Supplies/1492/bn_1851047'

    params = {
        '_trkparms': 'parentrq%3A42692e5118f0a4f891b4eedaffffcb14|pageci%3A40340882-09e4-11ef-8cc4-92bcea3b02ee|c%3A4|iid%3A1|li%3A8874'
    }

    response = requests.get(url=url, params=params, headers=headers)


def parse_xpath_1():
    dom = html.fromstring(response.text)

    names = dom.xpath("//h3[@class='s-item__title']/text()")
    # links = dom.xpath("//h3[@class='s-item__title']/../@class")   # ::before
    links = dom.xpath("//a[@class='s-item__link']/@href")
    prices = dom.xpath("//span[@class='s-item__price']//text()")
    add_info = dom.xpath("//span[@class='NEGATIVE']")               # ::after

    print()


def parse_xpath_2():
    global items_list

    dom = html.fromstring(response.text)

    names = dom.xpath("//h3[@class='s-item__title']/text()")
    # links = dom.xpath("//h3[@class='s-item__title']/../@class")   # ::before
    links = dom.xpath("//a[@class='s-item__link']/@href")
    prices = dom.xpath("//span[@class='s-item__price']//text()")
    # add_info = dom.xpath("//span[@class='NEGATIVE']")             # ::after

    items = dom.xpath("//li[contains(@class, 's-item')]")
    for item in items:
        item_info = {}

        name = item.xpath(".//h3[@class='s-item__title']/text()")
        link = item.xpath(".//a[@class='s-item__link']/@href")
        prices = item.xpath(".//span[@class='s-item__price']//text()")
        add_info = item.xpath(".//span[@class='NEGATIVE']")

        item_info['name'] = name
        item_info['link'] = link
        item_info['prices'] = prices
        item_info['add_info'] = add_info

        items_list.append(item_info)

        # print()

    # print()


if __name__ == '__main__':
    connect()
    parse_xpath_2()

    print()
