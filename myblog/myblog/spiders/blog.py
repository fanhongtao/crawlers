# -*- coding: utf-8 -*-
import scrapy
import os

class BlogSpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['fanhongtao.github.io']
    start_urls = ['https://fanhongtao.github.io/']

    def __init__(self):
        super().__init__();
        self.url_file = "visited_url.txt"
        self.html_path = "saved"
        if (not os.path.exists(self.html_path)):
            os.mkdir(self.html_path)
        if (os.path.exists(self.url_file)):
            os.remove(self.url_file)

    def parse(self, response):
        self.log_url(response)
        self.save_html(response)
        for href in response.css('a::attr(href)'):
            url = href.extract()
            if (url.endswith(".html") or url.endswith(".htm") or url.endswith("/")):
                yield response.follow(href, callback=self.parse)

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
