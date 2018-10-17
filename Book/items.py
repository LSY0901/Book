# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    href = scrapy.Field()
    mhref = scrapy.Field()
    ltitle = scrapy.Field()
    lauthor = scrapy.Field()
    lscore = scrapy.Field()
    lnumber = scrapy.Field()
    lbs = scrapy.Field()
    lcontent = scrapy.Field()
    PL = scrapy.Field()
