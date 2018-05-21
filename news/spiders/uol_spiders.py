# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
from scrapy.utils.markup import remove_tags,remove_tags_with_content

class UolSpider(SitemapSpider):

    name = "uol"
    sitemap_urls = ['https://noticias.uol.com.br/robots.txt']

    def parse(self,response):

        have_image = response.css("div.imagem-representativa").extract_first()

        if have_image :
            text = remove_tags_with_content(response.css("div#texto").extract_first(),which_ones=("div",))
            body_article = remove_tags(text)
        else:
            body_article = remove_tags(response.css("div#texto").extract_first())

        yield {
            'title': response.css("div.header > h1::text").extract_first(),
            'article': body_article,
            'dateTime': response.css("span.color1::text").extract_first(),
            'link': response.url

        }
