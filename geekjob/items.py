# -*- coding: utf-8 -*-
import scrapy


class GeekjobItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
