# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import csv
import logging
from watches import settings
from datetime import datetime

class CsvWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open(settings.csv_file_path % (spider.name, datetime.utcnow()), 'wb')
        self.items = []
        self.colnames = []

    def close_spider(self, spider):
        csvWriter = csv.DictWriter(self.file, fieldnames = self.colnames)#, delimiter=',')
        logging.info("HEADER: " + str(self.colnames))
        csvWriter.writeheader()
        for item in self.items:
            csvWriter.writerow(item)
        self.file.close()

    def process_item(self, item, spider):
        # add the new fields
        for f in item.keys():
            if f not in self.colnames:
                self.colnames.append(f)

        # add the item itself to the list
        self.items.append(item)
        return item