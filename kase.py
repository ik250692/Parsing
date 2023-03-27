import scrapy

from datetime import datetime, date, timedelta
import time
import dateparser
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SpiderKase(CrawlSpider):
    name = 'kase'
    allowed_domains = ['kase.kz']
    a = date.today() - timedelta(days=1)
    b = a.strftime('%d.%m.%Y')
    start_urls = ['https://kase.kz/ru/news/' + b + '/' + b]
    handle_httpstatus_list = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505]
    rules = (
        Rule(LinkExtractor(allow=('/ru'), deny=(
        '/future-listing-about/', '/private-kase/', '/foreign/', '/subscribers/', '/shares/', '/bonds/', '/mifs/',
        '/gsecs/', '/currency/', '/repo/', '/futures/', '/stock_market/', '/money_market/', '/mutual_indices/',
        '/pmi-indicator/', '/tickers/', '/account/', '/reglament/', '/clearing/', '/documents/', '/issuers/', '/esg/',
        '/disclosure/', '/issuers_diplomas/', '/membership/', '/marketmakers/', '/clearing/', '/dma/',
        '/members_diplomas/', '/services/', '/daily-market-review/', '/newsletter/', '/kase_connection/',
        '/tech_support/', '/kase_moex_connection/', '/moex_spectra/', '/kase_rules/', '/legislation/', '/rules_other/',
        '/events/', '/brochures/', '/publications/', '/presentations/', '/press_releases/', '/history/', '/mission/',
        '/kase_management/', '/authorities/', '/kase_membership/', '/corporate_documents/', '/museum/',
        '/shareholders/', '/shareholders_reports/', '/news_for_shareholders/', '/corporate_style/', '/requisites/',
        '/vacancies/', '/contacts/')),
             callback="parse", follow=True),
    )
    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 600,
    }

    def parse(self, response):
        if response.status == 200:
            time.sleep(10)
            Item = TutorialItem()
            Item['date_parse'] = datetime.now()
            Item['link'] = response.url
            Item['status'] = response.status
            Item['title'] = str.strip(response.xpath('//h1/text()').get())
            date_str = response.xpath('//div[contains(@style, "padding:5px;")]/div/text()').get()
            date_news = datetime.strptime(date_str, '%d.%m.%y %H:%M')
            if date_news.date() == self.a:
                Item['date_news'] = date_news
                Item['description'] = response.xpath('//div[contains(@class, "news-block")]/text()|//div[contains(@class, "news-block")]/a/@href').getall()
                Item['link_img'] = 'kase.kz'
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
            Item['link_img'] = 'kase.kz'
            yield Item
        else:
            pass
