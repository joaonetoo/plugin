# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
from scrapy.utils.markup import remove_tags,remove_tags_with_content
from lxml import etree
import requests,re
from datetime import date,datetime

class UolSitemMapSpider(SitemapSpider):

    name = "uol_site_map"
    
    def get_urls():

        def date_calculate(dateSitemap, format="%Y-%m-%d"):    
            dateNow = date.today()
            dateSitemap = datetime.strptime(dateSitemap, format).date()
            return abs((dateNow - dateSitemap).days)

        days_for_scrapy = 60
        sitemapXml = []
        request = requests.get("https://noticias.uol.com.br/sitemap/index.xml")
        all_sitemaps = etree.fromstring(request.content)
        
        for xml in all_sitemaps:
            children = xml.getchildren()
            sitemapXml.append([children[0].text,children[1].text])

        urls = []
        
        for sitemap in sitemapXml:
            if date_calculate(sitemap[1]) <= days_for_scrapy:
                urls.append(sitemap[0])
        return urls

    sitemap_urls = get_urls()

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

