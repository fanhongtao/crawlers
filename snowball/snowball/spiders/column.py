# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver

class ColumnSpider(scrapy.Spider):
    name = 'column'
    allowed_domains = ['xueqiu.com']

    def __init__(self, userid = None):
        super().__init__()   # 或 scrapy.Spider.__init__(self)
        self.start_urls = ['http://xueqiu.com/%s/column' % userid]
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(10)

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

    def closed(self, reason):
        # Spider中没有 closed 方法，所以不需要如下语句
        # super().closed(reason);
        try:
            self.driver.close();
        except Exception as e:
            self.log(e)
        self.driver.quit()
        self.log("webdriver closed.")
