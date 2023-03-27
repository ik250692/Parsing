import scrapy
from datetime import datetime, date, timedelta
import dateparser
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SpiderInform(CrawlSpider):
    name = 'informburo'
    allowed_domains = ['informburo.kz']
    a = date.today() - timedelta(days=1)
    start_urls = ['https://informburo.kz/']
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/novosti/'), deny=('/cards/', '/mneniya/', '/special/', '/law.informburo.kz/', '/page/restrict/', '/kaz/', '/avtory/', '/top/')),
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
            Item['title'] = str.strip(response.xpath('//h1/text()').get())
            date_news = dateparser.parse(str.strip(response.xpath('//div[contains(@class, "uk-width-1-1 article-meta")]/small/text()')[1].get()))
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "article")]/p/text()|//div[contains(@class, "article")]/div/p/text()|//div[contains(@class, "article")]/div/article/p/text()').getall()
                Item['link_img'] = 'informburo.kz'
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
            Item['link_img'] = 'informburo.kz'
            yield Item
        else:
            pass
