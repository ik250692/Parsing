import scrapy

from datetime import datetime, date, timedelta
import dateparser
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Spiderforbes(CrawlSpider):
    name = 'forbes'
    allowed_domains = ['forbes.kz']
    start_urls = ['https://forbes.kz/']
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/finances/', '/made_in_kz/', '/process/', '/massmedia/', '/travels/', '/auto/'), deny=('/news', '/news/', '/blogs/', '/ranking/', '/authors/', '/archive/', '/lang/', '/photostory/', '/leader/', '/life/', '/woman/', '/video/')),
             callback="parse", follow=True),
    )
    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 600,
    }
    def parse(self, response):
        if response.status == 200:
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//div[contains(@class, "inner-content")]/article/h1/text()').get()
            date_news = dateparser.parse(str.strip(response.xpath('//div[contains(@class, "article__date is-tcell")]/span/text()').get()))
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "inner-news")]/p/text()|//article[contains(@class, "inner-news")]/p/text()').getall()
                Item['link_img'] = 'forbes.kz'
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
            Item['link_img'] = 'forbes.kz'
            yield Item
        else:
            pass
