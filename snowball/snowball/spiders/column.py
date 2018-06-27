# -*- coding: utf-8 -*-
import scrapy


class ColumnSpider(scrapy.Spider):
    name = 'column'
    allowed_domains = ['xueqiu.com']

    def start_requests(self):
        yield scrapy.Request('http://xueqiu.com/%s/column' % self.userid)

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
