# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, text_hh):
        self.start_urls = [
            f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={text_hh}&showClusters=false']

    def parse(self, response:HtmlResponse):
        next_page_hh = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

        yield response.follow(next_page_hh, callback=self.parse)

    def vacancy_parce(self, response:HtmlResponse):
        l = ItemLoader(item=JobparserItem(), response=response)
        l.add_value('url', response.url)
        l.add_css('name', "div.vacancy-title h1::text")
        l.add_xpath('salary', "//span[@class='bloko-header-2 bloko-header-2_lite']/text()")
        yield l.load_item()

        # name_hh = response.css("div.vacancy-title h1::text").extract_first() - через take first
        # salary_hh = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()



