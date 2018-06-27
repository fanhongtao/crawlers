# -*- coding: utf-8 -*-
import scrapy


class ColumnSpider(scrapy.Spider):
    name = 'column'
    allowed_domains = ['xueqiu.com']

    def start_requests(self):
        yield scrapy.Request('http://xueqiu.com/%s/column' % self.userid)

    def parse(self, response):
        pass
