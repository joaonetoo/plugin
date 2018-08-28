# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.utils.markup import remove_tags

class GloboSpider(scrapy.Spider):
    name = "globo"
    start_urls =['https://g1.globo.com']

    def parse(self,response):
        for post in response.css('div.bastian-feed-item'):
            link_notice = post.css("a.feed-post-link::attr(href)").extract_first()
            yield response.follow(link_notice, self.parse_news)

        next_page = response.css('div.load-more a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


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

        yield {
            'article': article_body,
            'subtitle': response.css("h2.content-head__subtitle::text").extract_first(),
            'title': response.css("h1.content-head__title::text").extract_first(),
            'date': date,
            'link': response.url,
            'website': 'globo'
        }

