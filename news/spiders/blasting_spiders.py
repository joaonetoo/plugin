# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.markup import remove_tags,remove_tags_with_content,replace_escape_chars

class BlastingSpider(scrapy.Spider):

    name = "blasting"
    start_urls = ['https://br.blastingnews.com/brasil/p/2/']

    def parse(self,response):
        for post in response.css('div.content-news'):
            link_notice = post.css("a::attr(href)").extract_first()
            yield response.follow(link_notice, self.parse_news)

        next_page = response.css(".infinite-more-link::attr(href)").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    
    def parse_news(self,response):
        dateTime = response.css("div.content-time-published.margin .time-modified.margin::text").extract_first()
        title = response.css("span#id-blasting-tv-masthead-video-title::text").extract_first()
        subtitle = response.css("h2.title-h2::text").extract_first()
        article =  remove_tags_with_content(response.css("div.article-body.p402_premium.template-a").extract_first(),which_ones=('div','script'))
        article = remove_tags(article)
        article = replace_escape_chars(article, which_ones = ('\n')).strip()
        yield {
            'article': article,
            'subtitle': subtitle,
            'title': title,
            'dateTime': dateTime,
            'link': response.url
        }
