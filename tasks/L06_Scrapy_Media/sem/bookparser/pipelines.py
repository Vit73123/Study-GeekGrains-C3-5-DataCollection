# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline


class BookparserPipeline:
    def process_item(self, item, spider):
        print()
        return item


# ImagesPipeline не заработал!

class BookPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print()
        if item['photos']:
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print()
        if results:
            item['photos'] =[itm[1] for itm in results if itm[0]]
        return item

# class BookPhotosPipeline(FilesPipeline):
#     def get_media_requests(self, item, info):
#         print()

#     def get_media_requests(self, item, info):
#         print("***************************************************************************")
#         return super().get_media_requests(item, info)
#
#     def process_item(self, item, spider):
#         print()
#         return super().process_item(item, spider)
#
#     def get_images(self, response, request, info, *, item=None):
#         print()



# class A:
#     def process_item(self, item, spider):
#         print()
#
#
# class B(ImagesPipeline):
#
#     def get_media_requests(self, item, info):
#         print("*********************************************************************************************")
#         return super().get_media_requests(item, info)
#
#     def file_path(self, request, response=None, info=None, *, item=None):
#         print()
#         return super().file_path(request, response, info, item=item)
#
#     def process_item(self, item, spider):
#         print()
#
#
# class C(FilesPipeline):
#
#     def get_media_requests(self, item, info):
#         print()
#         return super().get_media_requests(item, info)
#
#     def file_path(self, request, response=None, info=None, *, item=None):
#         print()
