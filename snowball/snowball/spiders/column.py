# -*- coding: utf-8 -*-
import json
import scrapy

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

class ColumnSpider(scrapy.Spider):
    name = 'column'
    allowed_domains = ['xueqiu.com']

    def __init__(self, userid = None):
        super().__init__()   # 或 scrapy.Spider.__init__(self)
        self.start_urls = ['http://xueqiu.com/%s/column' % userid]
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(10)
        self.column_item_file = "column_" + userid + ".json"
        self.column_items = [];

    def parse(self, response):
        try:
            self.driver.get(response.url)
        except Exception as e:
            # 第一次调用总会失败，报错：
            #   ConnectionAbortedError: [WinError 10053] 你的主机中的软件中止了一个已建立的连接 。
            # 原因未知，所以在捕获异常后再调用一次。
            try:
                self.driver.get(response.url)
            except Exception as e:
                self.log(e)
        
        wait = WebDriverWait(self.driver, 30)  # 最多等30秒
        wait.until(lambda driver: driver.find_element_by_class_name("pagination"))
        
        self.save_html(response)
        column_items = self.driver.find_elements_by_class_name("column__item")
        for item in column_items:
            a = item.find_element_by_tag_name("a")
            title = a.text
            link = a.get_attribute("href")
            self.column_items.append({'title': title, 'link': link})

    def save_html(self, response):
        page = response.url.split("//")[-1]
        filename = page.strip("/").replace("/", "_")
        if (not (filename.endswith(".html") or filename.endswith(".htm"))):
            filename = filename + ".html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def save_item_link(self):
        items = {'items': self.column_items}
        with open(self.column_item_file, 'w') as f:
            f.write(json.dumps(items, ensure_ascii=False, indent=2))

    def closed(self, reason):
        # Spider中没有 closed 方法，所以不需要如下语句
        # super().closed(reason);
        self.save_item_link()
        try:
            self.driver.close();
        except Exception as e:
            self.log(e)
        self.driver.quit()
        self.log("webdriver closed.")
