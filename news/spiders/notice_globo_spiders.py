# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.utils.markup import remove_tags

class NoticeGloboSpider(scrapy.Spider):
    name = "notice_globo"
    def __init__(self, notice=None, *args, **kwargs):
        super(NoticeGloboSpider, self).__init__(*args, **kwargs)
        self.start_urls = [notice]

    def parse(self,response): 
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

        yield {
            'article': article_body,
            'subtitle': response.css("h2.content-head__subtitle::text").extract_first(),
            'title': response.css("h1.content-head__title::text").extract_first(),
            'date': date,
            'link': response.url,
            'website': 'globo'
            # 'image': response.xpath('//img/@src').extract_first() usar depois
        }

