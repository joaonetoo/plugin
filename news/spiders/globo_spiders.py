# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.markup import remove_tags

class GloboSpider(scrapy.Spider):
    name = "globo"
    start_urls =['http://g1.globo.com/']

    def parse(self,response):
        for post in response.css('div.post-item'):
            link_notice = post.css("a.feed-post-link::attr(href)").extract_first()
            yield response.follow(link_notice, self.parse_news)

        next_page = response.css('div.load-more a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_news(self,response):
        
        def extract_notice(query):
            return response.css(query).extract_first()

        article_body = []
        
        for column in response.css("div.mc-column.content-text"):
            text_with_tags = column.css("div.mc-column.content-text").extract_first()
            text_without_tags = remove_tags(text_with_tags)
            article_body.append(text_without_tags)
        
        yield {
            'article': article_body,
            'subtitle': extract_notice("h2.content-head__subtitle::text"),
            'title': extract_notice("h1.content-head__title::text"),
            'dateTime': extract_notice("p.content-publication-data__updated time::text"),
            'link': response.url
        }

