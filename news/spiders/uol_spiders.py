# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.utils.markup import remove_tags,remove_tags_with_content
from datetime import date,datetime
from news.items import NewsItem

class UolSpider(scrapy.Spider):
    name = "uol"
    custom_settings = {
        'ITEM_PIPELINES': {
            'news.pipelines.NewsPipeline': 300,
        }
    }
    start_urls =['https://noticias.uol.com.br/noticias']

    def parse(self,response):
        
        domain = "https://noticias.uol.com.br/"

        for post in response.css('ul.viewport > li' ):
            link_notice = post.css("a::attr(href)").extract_first()
            if re.search(domain, link_notice):
                yield response.follow(link_notice, self.parse_news)

        next_page = response.css('div.filtro-paginacao > a.nav.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


    def parse_news(self,response):

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

        title = response.css("div.header > h1::text").extract_first()
        article = body_article
        date = date
        link = response.url
        website = 'uol'
        yield NewsItem(title = title, article = article, date = date, link = link, website = website)

