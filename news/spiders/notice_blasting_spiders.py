# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.utils.markup import remove_tags,remove_tags_with_content,replace_escape_chars

class NoticeBlastingSpider(scrapy.Spider):
    name = "notice_blasting"

    def __init__(self, notice=None, *args, **kwargs):
        super(NoticeBlastingSpider, self).__init__(*args, **kwargs)
        self.start_urls = [notice]

    def parse(self,response):
        date = response.css("div.content-time-published.margin .time-modified.margin::text").extract_first()
        title = response.css("span#id-blasting-tv-masthead-video-title::text").extract_first()
        subtitle = response.css("h2.title-h2::text").extract_first()
        
        try:
            article =  remove_tags_with_content(response.css("div.article-body.p402_premium.template-a").extract_first(),which_ones=('div','script'))
        except:
            article =  remove_tags_with_content(response.css("div#article-body-p1").extract_first(),which_ones=('div','a','script'))

        article = remove_tags(article)
        article = replace_escape_chars(article, which_ones = ('\n'))
        article = re.sub(r'http\S+','', article).strip()
        yield {
            'article': article,
            'subtitle': subtitle,
            'title': title,
            'date': date,
            'link': response.url,
            'website': 'blasting'
        }
