import scrapy
from datetime import datetime, date, timedelta
import dateparser
import time
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SpiderKazInform(CrawlSpider):
    name = 'kazinform'
    allowed_domains = ['inform.kz']
    a = date.today() - timedelta(days=1)
    start_urls = ['https://www.inform.kz']
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/ru/'), deny=('/kz/', '/qz/', '/en/', '/cn/', '/oz/', '/ar/', '/vybory-v-mazhilis_t12124/', '/c_c161/', '/ob-agentstve_c2/', '/marketing/', '/c_c141/', '/sitemap/')),
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
            Item['title'] = response.xpath('//div[contains(@class, "title_article_bl")]/h1/text()').get()
            date_news = dateparser.parse(response.xpath('//div[contains(@class, "time_article_bl")]/text()').get())
            print(f'date_news = {date_news}')
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "body_article_bl")]/p/text()').getall()
                Item['link_img'] = 'inform.kz'
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
            Item['link_img'] = 'inform.kz'
            yield Item
        else:
            pass
