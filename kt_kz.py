import scrapy
from datetime import datetime, date, timedelta
import dateparser
import time
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Tv7Spider(CrawlSpider):
    name = 'kt'
    allowed_domains = ['kt.kz']
    a = date.today() - timedelta(days=1)
    start_urls = ['https://www.kt.kz/rus/all']
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('//'), deny=('/video/', '/gallery/', '/pisma_v_redakciu/')),
             callback="parse", follow=True),)
 def parse(self, response):
        if response.status == 200:
            time.sleep(3)
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//header[contains(@class, "page-heading")]/h1/text()').get()
            date_str = response.xpath('//div[contains(@class, "page-meta")]/span/text()').get()
            date_news = datetime.strptime(date_str, '%d.%m.%Y, %H:%M')
            print(f'date_news = {date_news}')
            self.a = date.today() - timedelta(days=1)
            print(f'self.a = {self.a}')
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "page-content")]/div/text()').getall()
                Item['link_img'] = 'kt.kz'
                yield Item
            else:
                pass
        elif response.status != 200:
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = 'Empty'
            Item['date_news'] = date.today()-timedelta(days=1)
            Item['description'] = 'Empty'
            Item['link_img'] = 'kt.kz'
            yield Item
        else:
            pass
