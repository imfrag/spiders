# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    comic_id = scrapy.Field()
    vol_id = scrapy.Field()
    page = scrapy.Field()
    url = scrapy.Field()


class VolItem(scrapy.Item):
    comic_id = scrapy.Field()
    vol_id = scrapy.Field()
    images = scrapy.Field()


class ManhuaItem(scrapy.Item):
    comic_id = scrapy.Field()
    url = scrapy.Field()
    thumbnail = scrapy.Field()
    title = scrapy.Field()
    original_title = scrapy.Field()
    author = scrapy.Field()
    summary = scrapy.Field()
    state = scrapy.Field()
    duration = scrapy.Field()
    vols = scrapy.Field()
