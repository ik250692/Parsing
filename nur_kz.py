import scrapy
from datetime import datetime, date, timedelta
import dateparser
import time
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Tv7Spider(CrawlSpider):
    name = 'nurkz'
    allowed_domains = ['nur.kz']
    a = date.today() - timedelta(days=1)
    month = str(a.month).lstrip('0')
    day = str(a.day).lstrip('0')
    b = f'{a.year}/{month}/{day}'
    start_urls = ['https://www.nur.kz/archive/'+b]
    handle_httpstatus_list = {401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500,
                              501, 502, 503, 504, 505}
    rules = (Rule(LinkExtractor(allow=('//'), deny=('/family', '/showbiz', '/project/brands')),
             callback="parse", follow=True),
             )
    def parse(self, response):
        if response.status == 200:
            time.sleep(20)
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//article[contains(@class, "article")]/h1/text()').get()
            date_str = str.strip(response.xpath('//div[contains(@class, "layout-content-type-page__wrapper-block")]/p/time/text()').get())
            date_str = date_str.replace('Вчера, ', '')
            date_str = date_str.split(',')[0]
            date_obj = dateparser.parse(date_str, languages=['ru'])
            if date_obj.date() == self.a:
                Item['date_news'] = date_obj.strftime('%d %B %Y')
                Item['description'] = response.xpath('//div[contains(@class, "formatted-body io-article-body")]/p/text()|//p[contains(@class, "align-left formatted-body__paragraph")]/strong/text()').getall()
                Item['link_img'] = 'nur.kz'
                yield Item
            else:
                pass
        elif response.status != 200:
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = 'Empty'
            Item['date_news'] = date.today() - timedelta(days=1)
            Item['description'] = 'Empty'
            Item['link_img'] = 'nur.kz'
            yield Item
        else:
            pass
