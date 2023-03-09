import scrapy

from datetime import datetime, date, timedelta
import dateparser
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Tv7Spider(CrawlSpider):
    name = 'kapital'
    allowed_domains = ['kapital.kz']
    a = date.today() - timedelta(days=1)
    b = a.strftime('%Y-%m-%d')
    start_urls = ['https://kapital.kz/news?page=1', 'https://kapital.kz/news?page=2', 'https://kapital.kz/news?page=3', 'https://kapital.kz/news?page=4']
    handle_httpstatus_list = {401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500,
                              501, 502, 503, 504, 505}
    rules = (
        Rule(LinkExtractor(allow='/', deny=('/lifestyle', '/dossiers', '/project/brands')),
             callback="parse", follow=True),
    )
    def parse(self, response):
        if response.status == 200:
            time.sleep(5)
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = response.xpath('//div[contains(@class, "main__page")]/article/header/h1/text()').get()
            date_str = response.xpath('//div[contains(@class, "article__info information-article")]/time/text()').get()
            date_news = datetime.strptime(date_str, '%d.%m.%Y · %H:%M')
            print(f'date_news = {date_news}')
            if date_news.date() == self.a:
                Item['date_news'] = date_news.date()
                Item['description'] = response.xpath('//div[contains(@class, "article__body")]/div/p/text()').getall()
                Item['link_img'] = 'kapital.kz'
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
            Item['link_img'] = 'kapital.kz'
            yield Item
        else:
            pass
