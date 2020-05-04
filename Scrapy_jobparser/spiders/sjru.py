# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['https://russia.superjob.ru/']

    def __init__(self, text_sj):
        self.start_urls = [f"https://russia.superjob.ru/vacancy/search/?keywords={text_sj}"]

    def parse(self, response: HtmlResponse):
        sj_link = 'https://russia.superjob.ru'

        vacancy_links = response.xpath("//div[@class = 'acdxh GPKTZ _1tH7S']/div/a/@href").extract()
        for link in vacancy_links:
            next_link = sj_link + link
            yield response.follow(next_link, callback = self.vacancy_parse)

        next_page_sj = sj_link + response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        yield response.follow(next_page_sj, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        l = ItemLoader(item=JobparserItem(), response=response)
        l.add_value('url', response.url)
        l.add_xpath('name', "//h1[@class = '_3mfro rFbjy s1nFK _2JVkc']/text()")
        l.add_xpath('salary', "//span[@class = '_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()")
        yield l.load_item()



        # name_sj = response.xpath("//h1[@class = '_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first() - аналог take first
        # url = response.url
        # salary_sj = response.xpath("//span[@class = '_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        # yield JobparserItem(name=name_sj, salary=salary_sj)