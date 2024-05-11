# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient, errors
from urllib.parse import parse_qs, urlparse


class JobparserPipeline:
    def __init__(self):
        client = MongoClient(host='localhost', port=27017)
        self.mongo_base = client.vacancies231023

    def process_item(self, item, spider):
        print()

        # item['salary'] = item.get('salary')
        # item['salary']['min_salary' = item.get('salary')[1]
        # item['max_salary' = item.get('salary')[3]

        try:
            item['_id'] = urlparse(item['url']).path.split('/')[-1]
        except:
            print()

        if item['salary']:
            new_salary = []
            for i in range(len(item['salary']) - 2):
                try:
                    num = int(item['salary'][i].replace('\xa0', ''))
                    new_salary.append(num)
                except:
                    if '₽' in item['salary'][i]:
                        new_salary.append("руб")
                    else:
                        pass
            new_salary.append(item['salary'][-1])
            item['salary'] = new_salary

        collection = self.mongo_base[spider.name]

        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            pass

        return item
