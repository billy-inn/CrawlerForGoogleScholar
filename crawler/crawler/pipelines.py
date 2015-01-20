# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from bson import ObjectId

class CrawlerPipeline(object):
	def __init__(self):
		self.db = pymongo.Connection('166.111.7.105',30017)['bigsci']
		self.db.authenticate('user_name',"password")
		database = open("conf").readlines()[1].strip()
		self.profile = self.db[database]
		
	def process_item(self, item, spider):
		if spider.name == "1":
			post = {'ID':item['_id'], 'url':item['url'], 'name':item['name'], 'info':item['info'],
					'pubs':item['pubs']}
			self.profile.insert(post)
		elif spider.name == "2":
			#entry = self.profile.find_one({"_id":ObjectId(item['_id'])})
			#if entry is not None:
			#	entry['pubs'].extend(item['pubs'])
			#	self.profile.save(entry)
			pass
		elif spider.name == "3":
			pass

		return item