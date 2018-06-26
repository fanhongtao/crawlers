# -*- coding: utf-8 -*-
import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['fanhongtao.github.io']
    start_urls = ['http://fanhongtao.github.io/']

    def parse(self, response):
        pass
