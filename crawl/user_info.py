# -*- coding: utf-8 -*-
import scrapy


class UserInfoSpider(scrapy.Spider):
    name = 'user_info'
    allowed_domains = ['duwenzhang.com']

    def start_requests(self):
        urls = [
        'http://www.duwenzhang.com/member/index.php?uid=%D1%EE%C0%BC%E7%F9&action=infos',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # .extract()
        users_info = response.xpath("//div[@class='east']/dl[@class='border']/dd/table/td").extract()
        print(users_info)
        # for user_info in users_info:
        #     print(user_info)
        # print(response.text)