import scrapy

from datetime import datetime, date, timedelta
import dateparser
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class Tv7Spider(CrawlSpider):
    name = 'zakon'
    allowed_domains = ['zakon.kz']
    a = date.today() - timedelta(days=1)
    start_urls = ['https://www.zakon.kz/news/?p=1', 'https://www.zakon.kz/news/?p=2', 'https://www.zakon.kz/news/?p=3', 'https://www.zakon.kz/news/?p=4', 'https://www.zakon.kz/news/?p=5', 'https://www.zakon.kz/news/?p=6', 'https://www.zakon.kz/news/?p=7', 'https://www.zakon.kz/news/?p=8', 'https://www.zakon.kz/news/?p=9', 'https://www.zakon.kz/news/?p=10']
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('//'), deny=('/news/', '/category_open/', '/category/', 'online.zakon.kz', '/kaz.zakon.kz/', '/tags/', '/author/', '/document/', '/price.pdf/', '/01.pdf/', '/02.pdf/', '/privacy_policy/', '/sitemap/')),
             callback="parse", follow=True),
    )
    def parse(self, response):
        if response.status == 200:
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//h1/text()').get()
            date_news = dateparser.parse(response.xpath('//time[contains(@class, "date")]/text()').get())
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "content")]/p/text()|//div[contains(@class, "content")]/ul/li/p/text()|//div[contains(@class, "content")]/p/text()|//div[contains(@class, "content")]/blockquote/text()').getall()
                Item['link_img'] = 'zakon.kz'
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
            Item['link_img'] = 'zakon.kz'
            yield Item
        else:
            pass