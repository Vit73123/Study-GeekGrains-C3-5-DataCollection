# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose
from twisted.web.html import output

def process_name(value):
    value[0] = value[0].strip()
    # value = value[0].strip()  # Отдельное значение в Compose() всё равно преобразуется в список из одного элемента
    return value

def process_price(value):
    value = value[0].strip().replace('\xa0', ' ').split()
    if value[0].isdigit():
        value[0] = int(value[0])
    return value

def process_photo(value: str):
    if value.startswith('//'):
        value = 'https:' + value.split()[0]
    else:
        value = value.split()[1]
    return value


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    # name = scrapy.Field(input_processor=Compose(process_name))    # Compose() не позволит вернуть только значение:
                                        # в любом случае возвращает список - из одного элемента,
                                        # поэтому потребуется применять TakeFirst() в пост-обработчике посл Compose()
    price = scrapy.Field(input_processor=Compose(process_price))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photo))
    _id = scrapy.Field()
