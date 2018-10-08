# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.utils.markup import remove_tags
from news.items import NewsItem

class GloboSpider(scrapy.Spider):
    name = "globo"
    start_urls =[]
    custom_settings = {
        'ITEM_PIPELINES': {
            'news.pipelines.NewsPipeline': 300,
        }
    }

    # custom_settings = {
    #     # https://github.com/alecxe/scrapy-fake-useragent
    #     "RANDOM_UA_PER_PROXY": True,
    #     # Retry many times since proxies often fail
    #     "RETRY_TIMES": 10,
    #     # Retry on most error codes since proxies fail for different reasons
    #     "RETRY_HTTP_CODES": [500, 503, 504, 400, 403, 404, 408],

    #     "DOWNLOADER_MIDDLEWARES": {
    #         'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #         'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    #         'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    #         'scrapy_proxies.RandomProxy': 100,
    #         'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,

    #     # https://github.com/aivarsk/scrapy-proxies
    #     },
    #     "PROXY_LIST": '/home/joao/Documentos/notices/scrapy-noticias/list.txt',
    #     "PROXY_MODE": 0
    # }
    def __init__(self):
        super(GloboSpider, self).__init__()

        for i in range(1, 2000):
            self.start_urls.append('http://g1.globo.com/index/feed/pagina-' + str(i) + '.ghtml')

    def parse(self,response):
        for post in response.css('div.bastian-feed-item'):
            link_notice = post.css("a.feed-post-link::attr(href)").extract_first()
            yield response.follow(link_notice, self.parse_news)

        # next_page = response.css('div.load-more a::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)


    def parse_news(self,response):  
        article_body = []
        for column in response.css("div.mc-column.content-text"):
            text_with_tags = column.css("div.mc-column.content-text").extract_first()
            text_without_tags = remove_tags(text_with_tags)
            article_body.append(text_without_tags.strip())

        article_body = ''.join(article_body)
        dateTime = response.css("p.content-publication-data__updated time::text").extract_first()
        if dateTime:
            date = dateTime.split()[0]     
        else:
            date = None

        article = article_body
        # subtitle = response.css("h2.content-head__subtitle::text").extract_first()
        title = response.css("h1.content-head__title::text").extract_first()
        date = date,
        link = response.url,
        website = 'globo'
        yield NewsItem(title = title, article = article, date = date, link = link, website = website)


