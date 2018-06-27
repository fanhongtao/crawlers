# -*- coding: utf-8 -*-
import scrapy


class ColumnSpider(scrapy.Spider):
    name = 'column'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']

    def parse(self, response):
        pass
