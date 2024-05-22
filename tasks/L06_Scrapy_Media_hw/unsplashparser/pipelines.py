# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import re
from pprint import pprint


class UnsplashparserPipeline:
    def process_item(self, item, spider):
        # print()
        return item


class UnsplashPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # print()
        if item['photos']:
            for url, q in item['photos'].items():
                try:
                    yield scrapy.Request(url)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        # print()
        name = re.sub('\\W', '_', item['name'])
        return f"full/{name}/{item['photos'][request.url]}.jpg"

    def item_completed(self, results, item, info):
        # print()
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
