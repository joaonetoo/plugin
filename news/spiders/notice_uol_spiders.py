# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.utils.markup import remove_tags,remove_tags_with_content
from datetime import date,datetime

class NoticeUolSpider(scrapy.Spider):
    name = "notice_uol"
    def __init__(self, notice=None, *args, **kwargs):
        super(NoticeUolSpider, self).__init__(*args, **kwargs)
        self.start_urls = [notice]

    def parse(self,response):

        have_image = response.css("div.imagem-representativa").extract_first()
        
        if have_image :
            text = remove_tags_with_content(response.css("div#texto").extract_first(),which_ones=("div","script",))
            body_article = remove_tags(text)
        else:
            try:
                text = remove_tags_with_content(response.css("div#texto").extract_first(),which_ones=("script",))
            except:
                text = remove_tags_with_content(response.css("div.texto").extract_first(),which_ones=("script",))

            body_article = remove_tags(text)

        dateTime = response.css("span.color1::text").extract_first()
        
        if dateTime:
            date = dateTime.split('-')[0].strip()
        else:
            date = None

        yield {
            'title': response.css("div.header > h1::text").extract_first(),
            'article': body_article,
            'date': date,
            'link': response.url,
            'website': 'uol'

        }
