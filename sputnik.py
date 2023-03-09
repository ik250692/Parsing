import scrapy

from datetime import datetime, date, timedelta
import dateparser
import time
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Tv7Spider(CrawlSpider):
    name = 'sputnik'
    allowed_domains = ['ru.sputnik.kz']
    a = date.today() - timedelta(days=1)
    b = a.strftime('%Y%m%d')
    start_urls = ['https://ru.sputnik.kz/'+b+'/']
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/'), deny=('docs/', 'cms/', 'app/')),
             callback="parse", follow=True),
    )
 def parse(self, response):
        if response.status == 200:
            time.sleep(3)
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//div[contains(@class, "article__header")]/h1/text()').get()
            date_str = response.xpath('//div[contains(@class, "article__info-date")]/a/text()').get()
            date_news = datetime.strptime(date_str, '%H:%M %d.%m.%Y')
            print(f'date_news = {date_news}')
            print(self.a)
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "article__text")]/text()').getall()
                Item['link_img'] = 'sputnik.kz'
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
            Item['link_img'] = 'sputnik.kz'
            yield Item
        else:
            pass
