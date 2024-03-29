import scrapy

from datetime import datetime, date, timedelta
import dateparser
import time
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SpiderTengri(CrawlSpider):
    name = 'tengri'
    allowed_domains = ['tengrinews.kz']
    a = date.today() - timedelta(days=1)
    start_urls = ['https://tengrinews.kz/kazakhstan_news/page/'+str(c) for c in range(0, 5)]
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('//'), deny=('/news/', 'kaz.tengrinews.kz', '/page/', '/mixnews/', '/tv/', '/pobediteli/', '/zakon/', 'school_online', '/heroes-among-us/', '/smart-generation/', '/tag/', '/find-out/', '/read/', 'take-look', '/weather/', '/press_releases', '/sitemap/')),
             callback="parse", follow=True),
    )
    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 600,
    }
    def parse(self, response):
        if response.status == 200:
            time.sleep(3)
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//h1[contains(@class, "tn-content-title")]/text()').get()
            date_news = dateparser.parse(response.xpath('//div[contains(@class, "tn-side-bar")]/time/text()').get())
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//article[contains(@class, "tn-news-text")]/p/text()').getall()
                Item['link_img'] = 'tengrinews.kz'
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
            Item['link_img'] = 'tengrinews.kz'
            yield Item
        else:
            pass


