import scrapy

from datetime import datetime, date, timedelta
import dateparser
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# from fake_useragent import UserAgent
# ua = UserAgent()
# ua.update()

class Tv7Spider(CrawlSpider):
    name = 'inbus'
    allowed_domains = ['inbusiness.kz']
    a = date.today() - timedelta(days=1)
    c = date.today()
    b = a.strftime('%Y-%m-%d')
    start_urls = ['https://inbusiness.kz/ru/lastnews?date='+b]
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/last/', '/news/'), deny=('/tv_programs/', '/hr/', '/ratings/', '/specprojects/', '/amp/')),
             callback="parse", follow=True),
    )

    def parse(self, response):
        if response.status == 200:
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//div[contains(@class, "newscont")]/h1/text()').get()
            date_news = dateparser.parse(response.xpath('//div[contains(@class, "extra")]/time/text()').get())
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "text")]/p/text()').getall()
                Item['link_img'] = 'inbusiness.kz'
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
            Item['link_img'] = 'inbusiness.kz'
            yield Item
        else:
            pass
