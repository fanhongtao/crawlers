# -*- coding: utf-8 -*-
import json
import os
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
        self.column_path = "column/" + userid
        if (not os.path.exists(self.column_path)):
            os.makedirs(self.column_path)

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
        
        while True:
            wait = WebDriverWait(self.driver, 30)  # 最多等30秒
            wait.until(lambda driver: driver.find_element_by_class_name("pagination"))
            
            self.save_html(response)
            column_items = self.driver.find_elements_by_class_name("column__item")
            for item in column_items:
                a = item.find_element_by_tag_name("a")
                title = a.text
                link = a.get_attribute("href")
                self.column_items.append({'title': title, 'link': link})
                yield scrapy.Request(link, callback=self.parse_column_item)
            
            next_page = self.driver.find_element_by_class_name("pagination__next")
            next_page_style = next_page.get_attribute("style")
            if (next_page_style.count("none") != 0):  # 找到 style="display: none;" ，说明已经是最后一页了
                break
            else:
                self.log("Click for next page ...")
                next_page.click()   # 通过在浏览器上点击“下一页”，获取新数据

    def parse_column_item(self, response):
        self.save_html(response)   # 专栏在具体文章，直接保存

    def save_html(self, response):
        page = response.url.split("//")[-1]
        filename = self.column_path + "/" + page.strip("/").replace("/", "_")
        if (not (filename.endswith(".html") or filename.endswith(".htm"))):
            filename = filename + ".html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def save_item_link(self):
        items = {'items': self.column_items}
        filename = self.column_path + "/" + self.column_item_file
        with open(filename, 'w') as f:
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
