# -*- coding: utf-8 -*-
import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['fanhongtao.github.io']
    start_urls = ['http://fanhongtao.github.io/']

    def parse(self, response):
        self.save_html(response)

    def save_html(self, response):
        page = response.url.split("//")[-1]
        filename = page.strip("/").replace("/", "_")
        if (not (filename.endswith(".html") or filename.endswith(".htm"))):
            filename = filename + ".html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
