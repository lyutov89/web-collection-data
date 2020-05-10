# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LmerlinSpider(scrapy.Spider):
    name = 'LMerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, text):
        self.start_urls = [
            f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response:HtmlResponse):
        lm_links = response.xpath("//div[@class='product-name']/a/@href").extract()
        next_page_lm = response.xpath("//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()

        for link in lm_links:
            yield response.follow(link, callback=self.light_parce)

        yield response.follow(next_page_lm, callback=self.parse)

    def light_parce(self, response:HtmlResponse):
        l=ItemLoader(item = LeroyparserItem(), response=response)
        l.add_xpath('name', "//uc-pdp-card-ga-enriched[@class='card-data']/h1/text()")
        l.add_xpath('price', "//uc-pdp-price-view[@class='primary-price']/span[@slot='price']/text()")
        l.add_xpath('photos_url', "//img/@data-origin")
        l.add_xpath('tech_char',"//dt[@class = 'def-list__term']/text()")
        l.add_xpath('params_for_tech', "//dd[@class = 'def-list__definition']/text()")
        l.add_value('link', response.url)
        yield l.load_item()

