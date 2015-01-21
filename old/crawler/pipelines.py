# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class CrawlerPipeline(object):
	def __init__(self):
		self.db = pymongo.Connection('ip',123)['name']
		self.db.authenticate('user_name',"password")
		self.profile = self.db['crawledData_copy']
		
	def process_item(self, item, spider):
		entry = self.profile.find_one({"ID":item['_id']})
		if entry is not None:
			entry['pubs'].extend(item['pubs'])
			self.profile.save(entry)
		else:
			post = {'ID':item['_id'], 'url':item['url'], 'name':item['name'], 'info':item['info'],
					'pubs':item['pubs']}
			self.profile.insert(post)

		return item
