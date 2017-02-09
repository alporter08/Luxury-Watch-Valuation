# -*- coding: utf-8 -*-
import scrapy
from collections import defaultdict

class WatchbotSpider(scrapy.Spider):
    name = "watchbot"
    allowed_domains = ["chrono24.com"]
    start_urls = ['http://www.chrono24.com/{}/index.htm'.format(x) for x in ['Rolex', 'Omega', 'IWC', \
    'Breitling', 'PatekPhilippe', 'AudemarsPiguet', 'Panerai', 'JaegerLeCoultre', 'TagHeuer', 'Hublot']]


    def parse(self, response):

        # follow links to individual watch pages
        for i in response.xpath('//div[contains(@id, "watch-")]'):
            link = i.xpath('.//a/@href').extract()
            text = i.xpath('.//strong[@class="col-xs-14"]//text()').extract()
            text = [x.strip() for x in text]
            title = i.xpath('.//span[contains(@onclick,"watch-headline-click")]//text()').extract()[-1].strip()
            # print(dict(title=title, text=text, link=link))

            # follow links to individual watch pages
            yield scrapy.Request(response.urljoin(link[0]),
                                 callback=self.parse_ind_watch)


        # follow pagination links
        pages = response.xpath('//ul[@class="pagination inline pull-xs-none pull-sm-right"]')[-1]
        last_page_str = pages.xpath('.//li//text()').extract()[-2].strip()
        max_pages = 300
        if last_page_str != '':
            last_page_int = int(last_page_str)
            if last_page_int > max_pages:
                last_page_int = max_pages

            for i in range(201, last_page_int + 1):
                i = str(i)
                url_stub = 'index-{}.htm'.format(i)
                next_page = response.urljoin(url_stub)

                yield scrapy.Request(next_page, callback=self.parse)

    def parse_ind_watch(self, response):
         watch_dict = defaultdict(str)
         watch_info = response.xpath('//div[@class="col-md-12"]')[0]

         for i in watch_info.xpath('.//tr'):
             key = i.xpath('.//td//text()').extract()
             if len(key) < 3:
                 watch_dict[key[0].strip()] = key[-1].strip()

         watch_dict['url'] = response.url

         yield watch_dict
