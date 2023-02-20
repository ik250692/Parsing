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
    name = 'vlast'
    allowed_domains = ['vlast.kz']
    a = date.today() - timedelta(days=1)
    start_urls = ['https://vlast.kz/novosti/'+str(x) for x in range(0, 4)]
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/'), deny=('/tags', '/samrukkazyna/', '/quiz/', '/vlas-qazaqsha/', '/gorod/', '/life/', '/explain/', '/gylymfaces/', '/project-syndicate/', '/politika/', '/zhizn/', '/filmy', '/regiony/', '/people/', '/avtory/', '/author/', '/obsshestvo/', '/persona/', '/beeline-business/')),
             callback="parse", follow=True),
    )
    def parse(self, response):
        if response.status == 200:
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = str.strip(response.xpath('//li[contains(@class, "has-title")]/h1/text()').get())
            date_news = dateparser.parse(str.strip(response.xpath('//ul[contains(@class, "meta item-expand-meta text-uppercase list-inline")]/li/time/text()').get()))
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "default-item-in js-editor js-img-caption js-mediator-article font-edit")]/p/text()').getall()
                Item['link_img'] = 'vlast.kz'
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
            Item['link_img'] = 'vlast.kz'
            yield Item
        else:
            pass