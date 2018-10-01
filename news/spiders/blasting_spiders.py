# -*- coding: utf-8 -*-
import scrapy, re
from scrapy.utils.markup import remove_tags,remove_tags_with_content,replace_escape_chars
from news.items import NewsItem
class BlastingSpider(scrapy.Spider):

    name = "blasting"
    start_urls = ['https://br.blastingnews.com/brasil/p/2/',
    'https://br.blastingnews.com/economia/p/2/',
    'https://br.blastingnews.com/cultura/p/2/',
    'https://br.blastingnews.com/mundo/p/2/',
    'https://br.blastingnews.com/politica/p/2/',
    'https://br.blastingnews.com/tecnologia/p/2/']

    def parse(self,response):
        for post in response.css('div.content-news'):
            link_notice = post.css("a::attr(href)").extract_first()
            yield response.follow(link_notice, self.parse_news)

        next_page = response.css(".infinite-more-link::attr(href)").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    
    def parse_news(self,response):
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
        
        article = article
        # subtitle = subtitle
        title = title
        date = date
        link = response.url
        website = 'blasting'
        yield NewsItem(title = title, article = article, date = date, link = link, website = website)

