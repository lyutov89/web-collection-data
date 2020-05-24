# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from urllib.parse import urlparse
import os

class LeroyparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_image_parse

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LeroyPhotoPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        fold_way = 'images/' + item['link'].split('/')[-2].replace('-','_')
        os.mkdir(fold_way)
        if item['photos_url']:
            for img in item['photos_url']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        file_name = os.path.basename(urlparse(request.url).path)   #90134168_01.jpg
        path = os.getcwd() + '\images'
        file_path_list = [i[0] for i in os.walk(path)]
        for list_path in file_path_list:
            if list_path[-8:] == file_name[:8]:
                product_name = list_path.split('\\')[-1]
                return f'{product_name}/{file_name}'
        #return 'images/' + os.path.basename(urlparse(request.url).path) #C:\Users\Anatoly\PycharmProjects\LMparser\leroyparser\

    def item_completed(self, results, item, info):
        photos_paths = [x['path'] for ok, x in results if ok]
        if not photos_paths:
            raise DropItem("Item contains no images")
        item['photos_paths'] = photos_paths
        return item


