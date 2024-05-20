# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose, MapCompose
from pprint import pprint


def process_photo(value):
    # print()
    links = {}
    for link in value[0].split(", "):
        url, q = link.split()
        links[url] = q
    # print()
    return links


class UnsplashparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # print()
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    # photos = scrapy.Field()
    photos = scrapy.Field(input_processor=Compose(process_photo), output_processor=TakeFirst())
    _id = scrapy.Field()
