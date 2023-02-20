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
    name = 'forbes1'
    allowed_domains = ['forbes.kz']
    a = date.today() - timedelta(days=1)
    start_urls = ['https://forbes.kz/']
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/news'), deny=('/news/2022/06/', '/news/2022/05/', '/news/2022/04/', '/news/2022/03/', '/news/2022/02/', '/news/2022/01/', '/news/2021/', '/auto/', '/travels/', '/massmedia/', '/process/', '/made_in_kz/', '/finances/', '/blogs/', '/ranking/', '/authors/', '/archive/', '/lang/', '/photostory/', '/leader/', '/life/', '/woman/', '/video/', '/pages/')),
             callback="parse", follow=True),
    )
    def parse(self, response):
        if response.status == 200:
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//div[contains(@class, "inner-content")]/article/h1/text()').get()
            date_news = dateparser.parse(response.xpath('//div[contains(@class, "article__date is-tcell")]/span/text()').get())
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