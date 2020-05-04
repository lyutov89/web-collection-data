# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import numpy as np

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy_spider
        self.treat = JobTreatPipeline()

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item = self.treat.item_treat(item, spider)
        collection.insert_one(item)
        return item


class JobTreatPipeline(object):
    def item_treat(self, item, spider):
        item['min_salary'] = np.nan
        item['max_salary'] = np.nan
        item['currency'] = np.nan
        if spider.name == 'hhru':
            item = self.hhru_item_treat(item)
        elif spider.name == 'sjru':
            item = self.sjru_item_treat(item)
        return item

    def hhru_item_treat(self, item):
        if len(item['salary']) != 0:
            for i in range(len(item['salary'])):
                if item['salary'] == 'от ':
                    item['min_salary'] = int(item['salary'][i+1].replace('\xa0', ''))
                elif (item['salary'] == ' до ') or (item['salary'] == 'до '):
                    item['max_salary'] = int(item['salary'][i+1].replace('\xa0', ''))
                elif (item['salary'][i] == 'руб.') or (item['salary'][i] == 'USD') or (item['salary'][i] == 'EUR'):
                    item['currency'] = item['salary'][i]
        return item

    def sjru_item_treat(self, item):
        if len(item['salary']) >= 2:
            if item['salary'][0] == "от":
                item['min_salary'] = int(item['salary'][2][:-4].replace('\xa0', ''))
                item['currency'] = item['salary'][2][-4:]
            elif item['salary'][0].replace('\xa0', '').isnumeric():
                item['min_salary'] = int(item['salary'][0].replace('\xa0', ''))
                item['max_salary'] = int(item['salary'][1].replace('\xa0', ''))
                item['currency'] = item['salary'][3]
        return (item)