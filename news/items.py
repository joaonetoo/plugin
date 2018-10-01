# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsItem(scrapy.Item):
    article = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    website = scrapy.Field()
