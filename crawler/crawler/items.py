# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlerItem(Item):
	_id = Field()
	ID = Field()
	url = Field()
	name = Field()
	info = Field()
	pubs = Field()
	token = Field()

