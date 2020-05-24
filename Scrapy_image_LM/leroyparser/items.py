# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose

def cleaner_price_to_int(values):
    return int(values.replace(' ', ''))

class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(cleaner_price_to_int), output_processor=TakeFirst())
    photos_url = scrapy.Field()
    photos_paths = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    tech_char = scrapy.Field()
    params_for_tech = scrapy.Field()
    pass
