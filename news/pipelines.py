# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import os
from scripts.utils import DataUtility

class NewsPipeline(object):
    
    def open_spider(self, spider):
        hostname = os.environ.get("HOST_DB")
        username = os.environ.get("USER_POSTGRES")
        password = os.environ.get("PASS_POSTGRES")
        database = os.environ.get("DB_NAME")
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            processed_data = DataUtility.pre_processing(item['article'])
            self.cur.execute("insert into news(title,article,date,link,website,processed) values(%s,%s,%s,%s,%s,%s)",(item['title'],item['article'],item['date'],item['link'],item['website'],processed_data))
            self.connection.commit()
        except:
            self.connection.rollback()
        return item