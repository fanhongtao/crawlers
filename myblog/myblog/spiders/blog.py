# -*- coding: utf-8 -*-
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class BlogSpider(CrawlSpider):
    name = 'blog'
    allowed_domains = ['fanhongtao.github.io']
    start_urls = ['https://fanhongtao.github.io/']
    rules = (
        Rule(LinkExtractor(allow=".*html"), callback="parse_html", follow=True),
    )

    def __init__(self):
        super().__init__();
        self.url_file = "visited_url.txt"
        self.html_path = "saved"
        if (not os.path.exists(self.html_path)):
            os.mkdir(self.html_path)
        if (os.path.exists(self.url_file)):
            os.remove(self.url_file)

    def parse_html(self, response):
        self.log_url(response)
        self.save_html(response)

    def log_url(self, response):
        with open(self.url_file, 'a') as f:
            f.write(response.url)
            f.write("\n")

    def save_html(self, response):
        page = response.url.split("//")[-1]
        filename = self.html_path + "/" + page.strip("/").replace("/", "_")
        if (not (filename.endswith(".html") or filename.endswith(".htm"))):
            filename = filename + ".html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
